from tkinter import messagebox


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
