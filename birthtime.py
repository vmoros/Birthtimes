import tkinter as tk
import csv
from tkinter import messagebox
from datetime import datetime
from tkintertable import TableCanvas
from pathlib import Path
from ctypes import windll


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
    dbName = "people.csv"
    bdayFormat = "%Y-%m-%d"

    def __init__(self):
        windll.shcore.SetProcessDpiAwareness(2)
        Path("people.csv").touch()

        super().__init__()
        windowWidth = 2 * self.winfo_screenwidth() // 3
        self.geometry(f"{windowWidth}x{self.winfo_screenheight() // 2}")
        self.title("Birthtimes ⏲️")

        nameLabel = tk.Label(self, text="Name")
        nameLabel.pack()
        self.nameEntry = tk.Entry(self)
        self.nameEntry.pack()

        bdayLabel = tk.Label(self, text="Birthday (YYYY-MM-DD)")
        bdayLabel.pack()
        self.bdayEntry = tk.Entry(self)
        self.bdayEntry.pack()

        addPersonButton = tk.Button(
            self, text="Add person", command=lambda: self.refr(True)
        )
        addPersonButton.pack()

        refrButton = tk.Button(self, text="Refresh", command=lambda: self.refr(False))
        refrButton.pack()

        tframe = tk.Frame(self)
        tframe.pack(expand=True, fill=tk.BOTH)

        data = self.dataFromFile()
        self.table = TableCanvas(
            tframe, data=data, cellwidth=(windowWidth // 9) - 1, read_only=True
        )
        self.table.rowheaderwidth = 0
        self.table.show()

    def refr(self, addingPerson):
        if addingPerson:
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
            with open(self.dbName, "a+") as f:
                f.write(f"{name},{bday}\n")

        self.table.model.importDict(self.dataFromFile())

        newColWidth = (self.winfo_width() // 9) - 1
        self.table.cellwidth = newColWidth
        for (
            c
        ) in (
            self.table.model.columnwidths
        ):  # setting the table's cellwidth won't update manually-resized columns, but this way will
            self.table.model.columnwidths[c] = newColWidth
        self.table.redraw()

    def dataFromFile(self):
        ans = dict()
        with open(self.dbName, newline="", mode="r+") as csvfile:
            peopleReader = csv.reader(csvfile, delimiter=",")
            n = 0
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


if __name__ == "__main__":
    birthtimes = Birthtimes()
    birthtimes.mainloop()
