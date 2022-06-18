from tkinter import *
from tkinter.filedialog import *
from tkinter.ttk import *
import os
import csv
from tkintertable import TableCanvas, TableModel


class Birthtimes(Tk):
    dbName = "people.csv"

    def __init__(self):
        super().__init__()

        self.nameLabel = Label(self, text="Name")
        self.nameLabel.pack()
        self.nameEntry = Entry(self)
        self.nameEntry.pack()

        self.bdayLabel = Label(self, text="Birthday")
        self.bdayLabel.pack()
        self.bdayEntry = Entry(self)
        self.bdayEntry.pack()

        self.refrButton = Button(self, text="Refresh", command=lambda: self.refr())
        self.refrButton.pack()

        self.tframe = Frame(self)
        self.tframe.pack()

        self.table = TableCanvas(self.tframe, data=self.dataFromFile())
        self.table.show()

    def refr(self):
        name = self.nameEntry.get()
        bday = self.bdayEntry.get()
        if len(name) > 0 and len(bday) > 0:
            self.nameEntry.delete(0, END)
            self.bdayEntry.delete(0, END)
            with open(self.dbName, "a") as f:
                f.write(f"\n{name},{bday}")
            self.table.model.importDict(self.dataFromFile())
            self.table.redraw()

    def dataFromFile(self):
        ans = dict()
        with open(self.dbName, newline="") as csvfile:
            peopleReader = csv.reader(csvfile, delimiter=",")
            n = 0
            for person in peopleReader:
                if len(person) == 2:
                    ans[n] = {"Name": person[0], "Birthday": person[1]}
                    n += 1

        return ans


if __name__ == "__main__":
    birthtimes = Birthtimes()
    birthtimes.mainloop()
