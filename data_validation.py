from tkinter import messagebox
from datetime import datetime


def validate_float_input(user_input):
    if not user_input:
        return False
    try:
        float(user_input)
        return True
    except ValueError:
        return False


def on_invalid_input():
    return messagebox.showinfo(title="Wrong Input", message="Enter only numbers")


def parse_date_to_sql(date):
    date = datetime.strptime(date,"%d/%m/%Y")
    return datetime.strftime(date, "%Y-%m-%d")


def parse_sql_date(date):
    date = datetime.strptime(date, "%Y-%m-%d")
    return datetime.strftime(date, "%d/%m/%Y")
