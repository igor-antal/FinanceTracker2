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
        self.geometry("500x250")
        self.transient(main_window)

        right_frame = tk.Frame(self)

        amount_frame = tk.Frame(right_frame)
        tk.Label(amount_frame, text="Set amount").pack()
        self._validate_float = self.register(validate_float_input)
        self._invalid_input = self.register(NewEntryWindow.invalid_input_msg)
        self._amount_entry = tk.Entry(amount_frame, validate="key",
                                      validatecommand=(self._validate_float, "%P"),
                                      invalidcommand=self._invalid_input)
        self._amount_entry.pack(fill="x", pady=(0, 20))
        amount_frame.pack(fill="x")

        self._entry_category = ttk.Combobox(right_frame)
        self._entry_category["values"] = ("Income", "Expense")
        self._entry_category.current(0)
        self._entry_category.pack(fill="x", pady=(0, 10))

        description_frame = tk.Frame(right_frame)
        tk.Label(description_frame, text="Description").pack()
        self._description_entry = tk.Entry(description_frame)
        self._description_entry.pack(fill="x", pady=(0, 10))
        description_frame.pack(fill="x")

        (tk.Button(right_frame, text="Add Entry", command=self.add_entry)
         .pack(side="bottom", pady=(0, 20)))

        right_frame.pack(side="right", fill="y", pady=(15, 0), padx=(0, 20))

        left_frame = tk.Frame(self)
        self._today = datetime.today().timetuple()[:3]
        self._calendar = Calendar(left_frame, selectmode="day",
                                  year=self._today[0], month=self._today[1], day=self._today[2],
                                  date_pattern="dd/mm/yyyy")
        self._calendar.pack()

        self._date_label = tk.Label(left_frame, text=f"Selected date: {self._calendar.get_date()}")
        self._date_label.pack(pady=(15, 0))
        self._calendar.bind("<<CalendarSelected>>", self.update_date_label)

        left_frame.pack(side="left", fill="y", pady=(15, 0), padx=(15, 0))

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
        insert_row(parsed_date, float(self._amount_entry.get()),
                   self._entry_category.get(), self._description_entry.get())
        self.main_window.update_main_win_data()
        self.destroy()


class App(Tk):
    def __init__(self):
        super().__init__()
        initiate_sql()

        self.title("Finance Manager")
        self.geometry("800x400")
        self.resizable(width=False, height=False)

        self._table = ttk.Treeview(self, columns=("id", "date", "amount", "category", "description"), show="headings")
        self._table.column("id", width=0, stretch=tk.NO)
        self._table.heading("id", text="")
        self._table.heading("date", text="Date")
        self._table.heading("amount", text="Amount")
        self._table.heading("category", text="Category")
        self._table.heading("description", text="Description")
        self._table.pack()

        buttons_frame = tk.Frame(self)
        Button(buttons_frame, text="Delete Entry", command=self.delete_entry).grid(column=1, row=0, padx=(20, 0))
        Button(buttons_frame, text="New Entry", command=self.new_entry_window).grid(column=0, row=0)
        Button(buttons_frame, text="Plot Entries", command=App.try_plotting_entries).grid(column=2, row=0, padx=(20, 0))
        buttons_frame.pack(side="left", fill="y", pady=15, padx=(15, 0))

        summary_frame = tk.Frame(self)
        self._income_label = tk.Label(summary_frame, text="All Income: ")
        self._income_label.pack()
        self._expense_label = tk.Label(summary_frame, text="All Expenses: ")
        self._expense_label.pack()
        self._net_savings_label = tk.Label(summary_frame, text="Net Savings: ")
        self._net_savings_label.pack()
        summary_frame.pack(side="right", fill="y", pady=15, padx=(0, 15))

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
        for row in fetch_all_data()[::-1]:
            modified_row = list(row)
            modified_row[1] = parse_sql_date(row[1])
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
