from datetime import datetime
from tkinter import *
import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import Calendar
from sql_functions import fetch_all_data, delete_row, insert_row, initiate_sql
from data_visualization import plot_entries, get_summary
from data_validation_parsing import (validate_float_input,
                                     parse_date_to_sql, parse_sql_date)


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
        self.transient(main_window)

        self._amount_label = tk.Label(self, text="Set amount")
        self._amount_label.pack()
        self._validate_float = self.register(validate_float_input)
        self._invalid_input = self.register(NewEntryWindow.invalid_input_msg)
        self._amount_entry = tk.Entry(self, validate="key",
                                      validatecommand=(self._validate_float, "%P"),
                                      invalidcommand=self._invalid_input)
        self._amount_entry.pack()

        self._entry_category = ttk.Combobox(self)
        self._entry_category["values"] = ("Income", "Expense")
        self._entry_category.current(0)
        self._entry_category.pack()

        self._description_label = tk.Label(self, text="Description")
        self._description_label.pack()
        self._description_entry = tk.Entry(self)
        self._description_entry.pack()

        self._today = datetime.today().timetuple()[:3]
        self._calendar = Calendar(self, selectmode="day",
                                  year=self._today[0], month=self._today[1], day=self._today[2],
                                  date_pattern="dd/mm/yyyy")
        self._calendar.pack()

        self._date_label = tk.Label(self, text=f"Selected date: {self._calendar.get_date()}")
        self._date_label.pack()
        self._calendar.bind("<<CalendarSelected>>", self.update_date_label)

        self._add_entry_button = tk.Button(self, text="Add Entry", command=self.add_entry)
        self._add_entry_button.pack()


    @staticmethod
    def invalid_input_msg():
        return messagebox.showinfo(title="Wrong Input", message="Enter only numbers")

    def update_date_label(self, event):
        self._date_label.config(text=f"Selected date: {self._calendar.get_date()}")

    def add_entry(self):
        if not self._amount_entry.get():
            messagebox.showinfo(message="Insert amount!", title="No amount")
            return
        selected_date = self._calendar.get_date()
        try:
            parsed_date = parse_date_to_sql(selected_date)
        except ValueError:
            print(f"Parsing failed {selected_date}")
            return
        insert_row(parsed_date, self._amount_entry.get(),
                   self._entry_category.get(), self._description_entry.get())
        self.main_window.update_main_win_data()
        self.destroy()


class App(Tk):
    def __init__(self):
        super().__init__()
        initiate_sql()

        self.title("Finance Manager")
        self.geometry("800x600")
        self.config(background="#fff6f2")

        self._delete_entry_button = Button(self, text="Delete Entry", command=self.delete_entry)
        self._delete_entry_button.pack()
        self._new_entry_button = Button(self, text="New Entry", command=self.new_entry_window)
        self._new_entry_button.pack()
        self._plot_entries_button = Button(self, text="Plot Entries",
                                           command=App.try_plotting_entries)
        self._plot_entries_button.pack()

        self._table = ttk.Treeview(self, columns=("id", "date", "amount", "category", "description"), show="headings")
        self._table.column("id", width=0, stretch=tk.NO)
        self._table.heading("id", text="")
        self._table.heading("date", text="Date")
        self._table.heading("amount", text="Amount")
        self._table.heading("category", text="Category")
        self._table.heading("description", text="Description")
        self._table.pack()
        self._income_label = tk.Label(self, text="All Income: ")
        self._expense_label = tk.Label(self, text="All Expenses: ")
        self._net_savings_label = tk.Label(self, text="Net Savings: ")
        for n in (self._income_label, self._expense_label, self._net_savings_label):
            n.pack()
        self.update_main_win_data()

    def update_main_win_data(self):
        self.update_summary_labels()
        self.load_table()

    def update_summary_labels(self):
        data_summary = get_summary()
        self._income_label.config(text=f"All Income: {data_summary[0]}")
        self._expense_label.config(text=f"All Expenses: {data_summary[1]}")
        self._net_savings_label.config(text=f" Net Savings: {data_summary[2]}")

    @staticmethod
    def try_plotting_entries():
        if not plot_entries():
            messagebox.showinfo(title="No data", message="Nothing to show")
        return

    def load_table(self):
        for item in self._table.get_children():
            self._table.delete(item)
        for row in fetch_all_data():
            modified_row = list(row)
            try:
                modified_row[1] = parse_sql_date(row[1])
            except ValueError:
                print(f"Parsing failed {modified_row[1]}")
                return
            self._table.insert('', tk.END, values=modified_row)

    def delete_entry(self):
        selected_entry = self._table.selection()
        if not selected_entry:
            messagebox.showinfo("Info", "Please select an entry for deletion")
            return
        confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete the selected entry?")
        if confirm:
            row_id = self._table.item(selected_entry[0], "values")
            delete_row(row_id[0])
            self.update_main_win_data()


    def new_entry_window(self):
        return NewEntryWindow(self)


if __name__ == "__main__":
    app = App()
    app.mainloop()
