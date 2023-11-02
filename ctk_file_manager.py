import os
import tkinter as tk
import customtkinter as ctk
from tkinter import filedialog,ttk


# Basic parameters and initializations
# Supported modes : Light, Dark, System
ctk.set_appearance_mode("System")
 
# Supported themes : green, dark-blue, blue
ctk.set_theme("green")   
 
appWidth, appHeight = 600, 700



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



class FileManagementApp():
    def __init__(self,root):
        # super().__init__()
        self.root = root

        self.root.title("File Management System")

        # self.current_directory = os.getcwd()
        self.current_directory = "C:"

        self.root.label = ctk.CTkLabel(self.root, text="Current Directory: " + self.current_directory,pady=0)
        self.root.label.grid(padx=8,pady=0)

        self.tool_bar=ttk.Label(self.root,background='#5a32a8')
        self.tool_bar.pack(side=tk.TOP,fill=tk.X)

        self.listbox = tk.Listbox(self.root)
        self.listbox.pack(padx=10,pady=10,fill=tk.BOTH, expand=True)

        self.load_files()

        self.button_open = tk.Button(self.tool_bar, text="Open", command=self.open_file,activebackground='#b4cfba',background='#5e8267')
        self.button_open.grid(row=0,column=0,padx=5,pady=5)

        self.button_delete = tk.Button(self.tool_bar, text="Delete", command=self.delete_file,activebackground='#b4cfba',background='Red')
        self.button_delete.grid(row=0,column=1,padx=5,pady=5)

        self.button_back = tk.Button(self.tool_bar, text="Back", command=self.navigate_back,activebackground='#b4cfba',background='Blue')
        self.button_back.grid(row=0,column=2,padx=5,pady=5)

        self.button_refresh = tk.Button(self.tool_bar, text="Refresh", command=self.refresh_files,activebackground='#b4cfba',background='#dae014')
        self.button_refresh.grid(row=0,column=3,padx=5,pady=5)
        
        self.button_newfolder = tk.Button(self.tool_bar, text="New Folder", command=self.new_folder,activebackground='#b4cfba',background='#09a3eb')
        self.button_newfolder.grid(row=0,column=4,padx=5,pady=5)

        self.button_select_drive = tk.Button(self.tool_bar, text="Select Drive", command=self.open_drive_selection,activebackground='#b4cfba',background='Green')
        self.button_select_drive.grid(row=0,column=5,padx=5,pady=5)


        self.bind_listbox_double_click()

    
    
    def get_available_drives(self):
        drives = []
        for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
            drive_path = f"{letter}:\\"
            if os.path.exists(drive_path):
                drives.append(drive_path)
        return drives


    def load_files(self):
        self.listbox.delete(0, tk.END)
        for item in os.listdir(self.current_directory):
            self.listbox.insert(tk.END, item)

    def open_file(self):
        selected_item = self.listbox.get(self.listbox.curselection())
        file_path = os.path.join(self.current_directory, selected_item)
        try:
            if os.name == 'nt':  # Windows
                if os.path.isdir(file_path):
                    self.current_directory=file_path
                    self.label.config(text="Current Directory: " + file_path)
                    self.load_files()
                elif os.path.isfile(file_path):
                    os.startfile(file_path)
            else:  # Linux and macOS
                subprocess.run(['xdg-open', file_path])
        except Exception as e:
            tk.messagebox.showerror("Error", f"Failed to open: {e}")


    def delete_file(self):
        selected_item = self.listbox.get(self.listbox.curselection())
        file_path = os.path.join(self.current_directory, selected_item)
        try:
            os.remove(file_path)
            self.load_files()
        except Exception as e:
            tk.messagebox.showerror("Error", f"Failed to delete: {e}")

    def navigate_back(self):
        self.current_directory = os.path.dirname(self.current_directory)
        self.label.config(text="Current Directory: " + self.current_directory)
        self.load_files()

    def refresh_files(self):
        self.load_files()

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

    
    def on_listbox_double_click(self, event):
        selected_item = self.listbox.get(self.listbox.curselection())
        item_path = os.path.join(self.current_directory, selected_item)
        
        if os.path.isdir(item_path):
            self.current_directory = item_path
            self.label.config(text="Current Directory: " + self.current_directory)
            self.load_files()
        else:
            self.open_file()

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
    # root.vm_iconbitmap('icon.ico')

    root.resizable(width=True,height=True)
    app = FileManagementApp(root)
    root.mainloop()

