from datetime import datetime
from tkinter import *
import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import Calendar
from sql_functions import fetch_all_data, delete_row, insert_row
from data_validation import validate_float_input, on_invalid_input


def plot_entries(self):
    pass


class Singleton(type):
    _instances = {}

    def __call__(cls, main_window):
        if cls not in cls._instances or not tk.Toplevel.winfo_exists(cls._instances[cls]):
            cls._instances[cls] = super().__call__(main_window)


class NewEntryWindow(tk.Toplevel, metaclass=Singleton):

    def __init__(self, main_window):
        super().__init__()

        self.main_window = main_window
        self.geometry("600x600")

        self.amount_label = tk.Label(self, text="Set amount")
        self.amount_label.pack()
        self.validate_float = self.register(validate_float_input)
        self.invalid_input = self.register(on_invalid_input)
        self.amount_entry = tk.Entry(self, validate="key",
                                     validatecommand=(self.validate_float, "%P"),
                                     invalidcommand=self.invalid_input)
        self.amount_entry.pack()

        self.entry_type = ttk.Combobox(self)
        self.entry_type["values"] = ("Income", "Expense")
        self.entry_type.current(0)
        self.entry_type.pack()

        self.description_label = tk.Label(self, text="Descripiton")
        self.description_label.pack()
        self.description_entry = tk.Entry(self)
        self.description_entry.pack()

        self.today = datetime.today().timetuple()[:3]
        self.calendar = Calendar(self, selectmode="day",
                                 year=self.today[0], month=self.today[1], day=self.today[2])
        self.calendar.pack()
        self.date_label = tk.Label(self, text=f"Selected date: {self.calendar.get_date()}")
        self.date_label.pack()
        self.calendar.bind("<<CalendarSelected>>", self.update_date_label)

        self.add_entry_button = tk.Button(self, text="Add Entry", command=self.add_entry)
        self.add_entry_button.pack()

    def update_date_label(self, event):
        self.date_label.config(text=f"Selected date: {self.calendar.get_date()}")

    def add_entry(self):
        insert_row(self.calendar.get_date(), self.amount_entry.get(),
                   self.entry_type.get(), self.description_entry.get())
        self.main_window.load_table()
        self.destroy()
        return







class App(Tk):
    def __init__(self):
        super().__init__()

        self.title("Finance Manager")
        self.geometry("800x600")
        self.config(background="#fff6f2")

        Button(self, text="Delete Entry", command=self.delete_entry).grid(row=0, column=1)
        Button(self, text="New Entry", command=self.new_entry_window).grid(row=0, column=2)
        Button(self, text="Plot Entries", command=plot_entries).grid(row=0, column=3)

        self.table = ttk.Treeview(self, columns=("id", "date", "amount", "type", "description"), show="headings")
        self.table.column("id", width=0, stretch=tk.NO)
        self.table.heading("id", text="")
        self.table.heading("date", text="Date")
        self.table.heading("amount", text="Amount")
        self.table.heading("type", text="Type")
        self.table.heading("description", text="Description")
        self.table.grid(row=1, column=1, columnspan=3)

    def load_table(self):
        for item in self.table.get_children():
            self.table.delete(item)
        for row in fetch_all_data():
            self.table.insert('', tk.END, values=row)

    def delete_entry(self):
        selected_entry = self.table.selection()
        if not selected_entry:
            messagebox.showinfo("Info", "Please select an entry for deletion")
            return
        confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete the selected entry?")
        if confirm:
            row_id = self.table.item(selected_entry[0], "values")
            delete_row(row_id[0])
            self.load_table()
            return

    def new_entry_window(self):
        return NewEntryWindow(self)




if __name__ == "__main__":
    app = App()
    app.load_table()
    app.mainloop()


