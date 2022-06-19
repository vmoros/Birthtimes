import csv
import tkinter as tk
from ctypes import windll
from datetime import datetime
from pathlib import Path
from tkinter import messagebox, filedialog
from tkintertable import TableCanvas


# how many seconds, minutes, hours, etc. have elapsed since the given datetime
def allTimesSinceDatetime(bday: datetime):
    sec = (datetime.today() - bday).total_seconds()
    mins = sec / 60
    hrs = mins / 60
    days = hrs / 24
    wks = days / 7
    months = days / 30.42
    yrs = days / 365.25

    return {
        "Years": f"{round(yrs, 2):,}",
        "Months": f"{round(months, 2):,}",
        "Weeks": f"{round(wks, 2):,}",
        "Days": f"{round(days):,}",
        "Hours": f"{round(hrs):,}",
        "Minutes": f"{round(mins):,}",
        "Seconds": f"{round(sec):,}",
    }


class Birthtimes(tk.Tk):
    bdayFormat = "%Y-%m-%d"

    def __init__(self):
        windll.shcore.SetProcessDpiAwareness(2)

        super().__init__()
        windowWidth = 2 * self.winfo_screenwidth() // 3
        self.geometry(f"{windowWidth}x{self.winfo_screenheight() // 2}")
        self.title("Birthtimes ⏲️")

        #####################################################################
        # Section with buttons and entries: Enter name, birthday, "add person" button, "refresh" button, select CSV
        entriesFrame = tk.Frame(self)
        entriesFrame.pack(side="left", anchor="nw")
        nameLabel = tk.Label(entriesFrame, text="Name")
        nameLabel.pack()
        self.nameEntry = tk.Entry(entriesFrame)
        self.nameEntry.pack()

        bdayLabel = tk.Label(entriesFrame, text="Birthday (YYYY-MM-DD)")
        bdayLabel.pack()
        self.bdayEntry = tk.Entry(entriesFrame)
        self.bdayEntry.pack()

        addPersonButton = tk.Button(
            entriesFrame, text="Add person", command=lambda: self.refr(True)
        )
        addPersonButton.pack()

        refrButton = tk.Button(
            entriesFrame, text="Refresh", command=lambda: self.refr(False)
        )
        refrButton.pack()

        csvFileLabel = tk.Label(entriesFrame, text="Selected CSV file(s):")
        csvFileLabel.pack()
        self.selectedCsv = tk.Entry(entriesFrame)
        self.selectedCsv.pack()
        pickCsvButton = tk.Button(
            entriesFrame, text="Select CSV(s)", command=lambda: self.selectCsv()
        )
        pickCsvButton.pack()

        createCsvLabel = tk.Label(entriesFrame, text="Name of CSV to create:")
        createCsvLabel.pack()
        self.createCsvName = tk.Entry(entriesFrame)
        self.createCsvName.pack()
        createCsvButton = tk.Button(
            entriesFrame, text="Create CSV", command=lambda: self.createCsv()
        )
        createCsvButton.pack()
        #####################################################################

        self.tableFrame = tk.Frame(self)
        self.tableFrame.pack(side="right", anchor="e", expand=True, fill=tk.BOTH)

        # data = self.dataFromFile()
        self.table = TableCanvas(
            self.tableFrame,
            data=dict(),
            read_only=True,
        )
        self.table.rowheaderwidth = 0
        self.table.show()

    def refr(self, addingPerson: bool):
        csvNamesRaw = self.selectedCsv.get()
        if len(csvNamesRaw) == 0:
            messagebox.showerror("Error", "Select at least one CSV file")
            return
        csvTuple = csvNamesRaw.split(",")

        if addingPerson:
            if len(csvTuple) > 1:
                messagebox.showerror(
                    "Error", "To add a person, select only one CSV to write to"
                )
                return

            name = self.nameEntry.get()
            bday = self.bdayEntry.get()
            if len(name) == 0 or len(bday) == 0:
                messagebox.showerror(
                    "Error", "You must provide both a name and a birthday"
                )
                return

            try:
                datetime.strptime(bday, self.bdayFormat)
            except:
                messagebox.showerror("Error", "Birthday must be in YYYY-MM-DD format")
                return
            self.nameEntry.delete(0, tk.END)
            self.bdayEntry.delete(0, tk.END)

            with open(csvNamesRaw, "a+") as f:
                f.write(f"{name},{bday}\n")

        self.table.model.createEmptyModel()
        self.table.model.importDict(self.dataFromFile(csvTuple))

        newColWidth = (self.tableFrame.winfo_width() // 9) - 1
        self.table.cellwidth = newColWidth
        for c in self.table.model.columnwidths:
            # setting the table's cellwidth won't update manually-resized columns, but this way will
            self.table.model.columnwidths[c] = newColWidth
        self.table.redraw()

    def dataFromFile(self, csvTuple):
        ans = dict()

        n = 0
        for csvName in csvTuple:
            with open(csvName, newline="", mode="r+") as csvfile:
                peopleReader = csv.reader(csvfile, delimiter=",")
                for person in peopleReader:
                    if len(person) == 2:
                        bdayStr = person[1].strip()
                        try:
                            bday = datetime.strptime(bdayStr, self.bdayFormat)
                        except:
                            continue

                        ans[n] = {"Name": person[0], "Birthday": bdayStr}
                        ans[n].update(allTimesSinceDatetime(bday))
                        n += 1  # TkinterTable takes data in a weird format - a dict of dicts in which the outermost keys are meaningless

        return ans

    def selectCsv(self):
        selectedCsvPath = filedialog.askopenfilenames(
            filetypes=[("CSV", "*.csv")], initialdir="."
        )
        self.selectedCsv.delete(0, tk.END)
        self.selectedCsv.insert(0, ",".join(selectedCsvPath))
        self.refr(False)

    def createCsv(self):
        csvName = self.createCsvName.get()
        if len(csvName) == 0:
            messagebox.showerror("Error", "Please enter a name for your CSV")
            return

        self.createCsvName.delete(0, tk.END)
        Path(csvName + ".csv").touch(exist_ok=True)


if __name__ == "__main__":
    birthtimes = Birthtimes()
    birthtimes.mainloop()
