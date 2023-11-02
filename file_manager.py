from cgitb import text
from re import T
from sys import flags
import tkinter as tk
from tkinter import RAISED, Button, Canvas, Image, Label, PhotoImage, Tk, Toplevel, YView, ttk
from tkinter import font,colorchooser,filedialog,messagebox
import os,shutil
from turtle import back, delay, title, width
# from PIL import ImageTk,Image
from pip import main



class DriveSelectionPopup:
    def __init__(self, root,app_instance):
        self.root = root
        self.root.title("Select Drive")
        self.root.resizable(width=False,height=False)
        self.root.geometry("300x450")

        self.app_instance=app_instance

        self.label = tk.Label(self.root, text="Select a Drive:")
        self.label.pack()

        self.drive_var = tk.StringVar()
        self.drive_var.set("")  # Initialize the selected drive

        self.drive_listbox = tk.Listbox(self.root)
        # , selectmode=tk.SINGLE
        self.drive_listbox.pack(padx=10,pady=10,fill=tk.BOTH, expand=True)

        self.ok_button = tk.Button(self.root, text="OK", command=self.select_drive)
        self.ok_button.pack()

        self.load_drives()


    def load_drives(self):
        drives = self.get_available_drives()
        for drive in drives:
            self.drive_listbox.insert(tk.END, drive)
    
    def get_available_drives(self):
        drives = []
        for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
            drive_path = f"{letter}:\\"
            if os.path.exists(drive_path):
                drives.append(drive_path)
        return drives

    def select_drive(self):
        selected_drive = self.drive_listbox.get(tk.ACTIVE)
        if selected_drive:
            self.app_instance.set_current_drive(selected_drive)
            self.root.destroy()



class FileManagementApp:
    
    def __init__(self, root):
        self.root = root
        self.root.title("File Management System")

        # self.current_directory = os.getcwd()
        self.current_directory = "C:"

        self.click_count= 0

        self.label = tk.Label(self.root, text="Current Directory: " + self.current_directory,pady=0)
        self.label.pack(padx=8,pady=0)

        self.tool_bar=ttk.Label(self.root,background='#5a32a8')
        self.tool_bar.pack(side=tk.TOP,fill=tk.X)

        self.listbox = tk.Listbox(self.root,background="black",
                                  activestyle='dotbox',
                                  font=('times',14),
                                  foreground='white',
                                  selectmode=tk.SINGLE,
                                #   selectmode='multiple',
                                  selectbackground="grey",
                                  selectforeground='black',
                                  selectborderwidth=2
                                  )
        self.listbox.pack(pady=10,fill=tk.BOTH, expand=True,side=tk.LEFT)

        self.scrollbar = ttk.Scrollbar(root,orient=tk.VERTICAL,command=self.listbox.yview)
        self.listbox['yscrollcommand'] = self.scrollbar.set
        self.scrollbar.pack(side=tk.LEFT, fill=tk.Y)

        self.load_files()

        self.drop_select_drive = ttk.Combobox(self.tool_bar,state="readonly",values=drives,width=8)
        self.drop_select_drive.grid(row=0,column=0,padx=5,pady=5)
        self.drop_select_drive.current(0)
        # self.drop_select_drive.configure(background='Green',foreground='blue')
        self.drop_select_drive.bind("<<ComboboxSelected>>",self.selected_combobox)

        self.button_open = tk.Button(self.tool_bar, text="Open", command=self.open_file,activebackground='#b4cfba',background='#5e8267',justify='center')
        self.button_open.grid(row=0,column=1,padx=5,pady=5)

        self.button_delete = tk.Button(self.tool_bar, text="Delete", command=self.delete_selected,activebackground='#b4cfba',background='Red',justify='center')
        self.button_delete.grid(row=0,column=2,padx=5,pady=5)

        self.button_back = tk.Button(self.tool_bar, text="Back", command=self.navigate_back,activebackground='#b4cfba',background='Blue',justify='center')
        self.button_back.grid(row=0,column=3,padx=5,pady=5)

        self.button_refresh = tk.Button(self.tool_bar, text="Refresh", command=self.refresh_files,activebackground='#b4cfba',background='#dae014')
        self.button_refresh.grid(row=0,column=4,padx=5,pady=5)
        
        self.button_newfolder = tk.Button(self.tool_bar, text="New Folder", command=self.new_folder,activebackground='#b4cfba',background='#09a3eb')
        self.button_newfolder.grid(row=0,column=6,padx=5,pady=5)

        self.button_organise = tk.Button(self.tool_bar, text="Organise", command=self.organise_folder,activebackground='Green',background='#98e9ed')
        self.button_organise.grid(row=0,column=7,padx=5,pady=5)
        
        self.button_select = tk.Button(self.tool_bar, text="Select", command=self.toggle_function,activebackground='blue',background='Green',state='normal')
        self.button_select.grid(row=0,column=8,padx=5,pady=5)
        
        self.button_select_drive = tk.Button(self.tool_bar, text="Select Drive", command=self.open_drive_selection,activebackground='blue',background='Green')
        # self.button_select_drive.grid(row=0,column=9,padx=5,pady=5)

        self.bind_listbox_double_click()


    def load_files(self):
        self.listbox.delete(0, tk.END)
        folders = []
        files = []
        for item in os.listdir(self.current_directory):
            item_path = os.path.join(self.current_directory, item)
            if os.path.isdir(item_path):
                folders.append(item)
            else:
                files.append(item)
        folders.sort()
        files.sort()
        # Insert folders with folder icon
        for folder in folders:
            self.listbox.insert(tk.END, ('*',folder))
        # Insert files with file icon
        for file in files:
            self.listbox.insert(tk.END, ('/',file))
        self.listbox.bind("<Double-1>", self.on_listbox_double_click)


    def get_available_drives(self):
        drives = []
        for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
            drive_path = f"{letter}:\\"
            if os.path.exists(drive_path):
                drives.append(drive_path)
        return drives

    def selected_combobox(self,event):
        selection=self.drop_select_drive.get()
        self.current_directory=selection
        self.load_files()

    def open_file(self):
        # selected_items = self.listbox.get(self.listbox.curselection())
        selected_items = [self.listbox.get(index) for index in self.listbox.curselection()]
        for item_type,selected_item in selected_items:
            file_path = os.path.join(self.current_directory, selected_item)
        try:
            if os.name == 'nt':  # Windows
                if item_type == "*":
                    self.current_drive = file_path
                    self.label.config(text="Current Drive: " + self.current_drive)
                    self.load_files()
                else:
                    os.startfile(file_path)
            else:  # Linux and macOS
                subprocess.run(['xdg-open', file_path])
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open: {e}")
        self.load_files()


    def delete_selected(self):
        selected_item = self.listbox.curselection()
        if not selected_item:
            messagebox.showinfo("No Selection", "No files selected for deletion.")
            return
        for item in selected_item:
            selected_item=self.listbox.get(item)
            file_path = os.path.join(self.current_directory, selected_item)
            print(file_path)
            try:
                if os.path.isdir(file_path):
                    shutil.rmtree(file_path)
                else:
                    os.remove(file_path)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete: {e}")    
        self.load_files()

    def navigate_back(self):
        self.current_directory = os.path.dirname(self.current_directory)
        self.label.config(text="Current Directory: " + self.current_directory)
        self.load_files()

    def refresh_files(self):
        self.load_files()
        messagebox.askokcancel(title='WARNING!',message='Please Make Sure, You already opened or You are on that folder Which you want to organize!')


    def insert_val(e):
        e.insert(0, "Enter a new folder name: ")

    def new_folder(self):
        new_folder_name = tk.simpledialog.askstring("New Folder", "Enter a name for the new folder:")
        if new_folder_name:
            new_folder_path = os.path.join(self.current_directory, new_folder_name)
            try:
                os.mkdir(new_folder_path)
                self.load_files()
            except Exception as e:
                tk.messagebox.showerror("Error", f"Failed to create folder: {e}")

    
    # def on_listbox_double_click(self, event):
    #     selected_item = self.listbox.get(self.listbox.curselection())
    #     print(selected_item)
    #     item_path = os.path.join(self.current_directory, selected_item)
        
    #     if os.path.isdir(item_path):
    #         self.current_directory = item_path
    #         self.label.config(text="Current Directory: " + self.current_directory)
    #         self.load_files()
    #     else:
    #         self.open_file()

    def on_listbox_double_click(self, event):
        selected_item = self.listbox.get(self.listbox.curselection())
        print(selected_item)
        item_type, item_name = selected_item
        item_path = os.path.join(self.current_directory, item_name)
        if item_type == "*":
            self.current_directory = item_path
            self.label.config(text="Current Drive: " + self.current_directory)
            self.load_files()
        else:
            os.startfile(item_path)

    
    def toggle_function(self):
        if self.click_count % 2 == 0:
            self.button_select.config(text="Unselect")
            self.listbox.config(selectmode=tk.MULTIPLE)
        else:
           self.button_select.config(text="Select")
           self.listbox.config(selectmode=tk.SINGLE)

        self.load_files()
        self.click_count+=1

    
    def organise_folder(self):
        mbox=messagebox.askokcancel(title='WARNING!',message='Please Make Sure,\nYou already opened\nor\nYou are on that folder\nWhich you want to organize!')
        if mbox is True:
            dict_extension={
                'Audio_extension':('.mp3','.m4a','.wav','.flac','.aac','.wav','.wma'),
                'Video_extension':('.mp4','.mov','.wmv','.avi','.avchd','.flv','.f4v','.swf','.mkv','.webm','mpeg-2'),
                'Document_extension':('.doc','.docx','.pdf','.txt','.pptx','.htm','.odt','.xls','.xlsx','.ods','.ppt','.webp'),
                'Coding_extension':('.py','.js','.css','.html','.cpp','.c','.java','.ipynb','.ino'),
                'Image_extension':('.jpg','.png','.jpeg','.RAW','.gif','.tiff','.psd','.eps','.ai','.ind','NEF','.svg'),
                'Compressed_extension':('.zip','.rar'),
                'WindowsApp_extension':('.exe','.msi')
            }

            def file_finder(folder_path,file_extension):
                files=[]
                for file in os.listdir(folder_path):
                    for extension in file_extension:
                        if file.endswith(extension):
                            files.append(file)
                return files

            for extension_type,extension_tuple in dict_extension.items():
                folder_name=extension_type.split('_')[0]+' '+'Files'
                folder_path=os.path.join(self.current_directory,folder_name)
                os.mkdir(folder_path)
                for items in file_finder(self.current_directory,extension_tuple):
                    item_path=os.path.join(self.current_directory,items)
                    item_new_path=os.path.join(folder_path,items)
                    shutil.move(item_path,item_new_path)
                self.load_files()
        elif mbox is False:
            return

    def open_drive_selection(self):
        drive_popup = tk.Toplevel(self.root)
        DriveSelectionPopup(drive_popup,self)

    def set_current_drive(self, drive):
        self.current_directory = drive
        self.label.config(text="Current Drive: " + self.current_directory)
        self.load_files()

    def bind_listbox_double_click(self):
        self.listbox.bind("<Double-1>", self.on_listbox_double_click)

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry('1200x800')
    drives = []
    for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        drive_path = f"{letter}:\\"
        if os.path.exists(drive_path):
            drives.append(drive_path)
    # root.vm_iconbitmap('icon.ico')

    root.resizable(width=True,height=True)
    app = FileManagementApp(root)
    root.mainloop()

