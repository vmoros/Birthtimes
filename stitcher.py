from tkinter import *
from tkinter.filedialog import *
from tkinter.ttk import *
import os

class Stitcher(Tk):
    def __init__(self):
        super().__init__()

        # directory/file labels
        self.input_label = Label(self, text = 'Folder that has queries: ')
        self.input_label.grid(row = 0, column = 0, sticky = E)
        self.output_label = Label(self, text = 'Folder where stitched queries will go: ')
        self.output_label.grid(row = 1, column = 0, sticky = E)
        self.filename_label = Label(self, text = 'Name of output file (with .sql): ')
        self.filename_label.grid(row = 2, column = 0, sticky = E)
        

        # directory/file names
        self.input_dir = Entry(self)
        self.input_dir.grid(row = 0, column = 1, sticky = E+W, pady = 3)
        self.output_dir = Entry(self)
        self.output_dir.grid(row = 1, column = 1, sticky = E+W, pady = 3)
        self.output_file = Entry(self)
        self.output_file.grid(row = 2, column = 1, sticky = E+W, pady = 3)

        # directory choosing buttons
        self.select_input_dir = Button(self, text='Choose folder', command = lambda: self.choose_directory('in'))
        self.select_input_dir.grid(row = 0, column = 2, sticky = W)
        self.select_output_dir = Button(self, text='Choose folder', command = lambda: self.choose_directory('out'))
        self.select_output_dir.grid(row = 1, column = 2, sticky = W)

        # test plan type options
        self.types_label = Label(self, text='Choose your test plan type(s) below')
        self.types_label.grid(row = 3, column = 0, pady = (10, 0))
        self.normal_box = Checkbutton(self, text = 'Normal')
        self.normal_box.grid(row = 4, column = 0, sticky = W, padx = 5)
        self.DTE_box = Checkbutton(self, text = 'DTE')
        self.DTE_box.grid(row = 5, column = 0, sticky = W, padx = 5)
        self.ASM_box = Checkbutton(self, text = 'ASM')
        self.ASM_box.grid(row = 6, column = 0, sticky = W, padx = 5)
        self.TI_box = Checkbutton(self, text = 'TI')
        self.TI_box.grid(row = 7, column = 0, sticky = W, padx = 5)

        # list of files and stitch button
        self.file_list_label = Label(self, text = 'All queries in given folder: ')
        self.file_list_label.grid(row = 3, column = 1)
        self.file_list = Listbox(self, selectmode=MULTIPLE, activestyle='none')
        self.file_list.grid(row = 4, column = 1, rowspan=100)
        self.stitch_button = Button(self, text = "Stitch 'em up", command = self.stitch)
        self.stitch_button.grid(column = 1)

        # PBR can
        self.pbr_pic = PhotoImage(file = 'PBR.png')
        self.pbr_label = Label(self, image = self.pbr_pic)
        self.pbr_label.grid(row = 0, column = 3, rowspan=100)

    def choose_directory(self, inorout):
        directory = askdirectory()
        if inorout == 'in':
            self.input_dir.delete(0, END); self.input_dir.insert(0, directory)
            sql_files = [x for x in sorted(os.listdir(directory)) if x.endswith('.sql') and os.path.isfile(os.path.join(directory, x))]
            for file in sql_files:
                full_path = os.path.join(directory, file)
                if os.path.isfile(full_path):
                    self.file_list.insert(END, file)
            return
        elif inorout == 'out':
            self.output_dir.delete(0, END); self.output_dir.insert(0, directory)
            return
        else:
            return 'Invalid type of directory'

    def stitch(self):
        selected_file_indexes = self.file_list.curselection()
        query_dir = self.input_dir.get()
        output_dir = self.output_dir.get()
        output_file = self.output_file.get()
        sql_files = [x for x in sorted(os.listdir(query_dir)) if x.endswith('.sql') and os.path.isfile(os.path.join(query_dir, x))]
        selected_files = [sql_files[i] for i in selected_file_indexes]

        output = ''
        for file in selected_files:
            full_path = os.path.join(query_dir, file)
            with open(full_path, 'r') as f:
                output += f.read() + 2*'\n'

        output_full_path = os.path.join(output_dir, output_file)
        with open(output_full_path, 'w') as f:
            f.write(output)

        return
            
    def select_files(self):
        return

if __name__ == '__main__':
    stitcher = Stitcher()
    stitcher.mainloop()
