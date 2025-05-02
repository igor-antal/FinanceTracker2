import pandas as pd
from sql_functions import fetch_all_data
import matplotlib.pyplot as plt


def plot_entries():
    df = pd.DataFrame(fetch_all_data(), columns=("id", "date", "amount", "category", "description"))
    if df.empty:
        return False
    df["date"] = pd.to_datetime(df["date"], format="%Y-%m-%d")
    df.set_index("date", inplace=True)

    income_df = df[df["category"] == "Income"].resample("D").sum().reindex(df.index, fill_value=0)
    expense_df = df[df["category"] == "Expense"].resample("D").sum().reindex(df.index, fill_value=0)
    income_df.index = income_df.index.strftime("%d/%m/%Y")
    expense_df.index = expense_df.index.strftime("%d/%m/%Y")

    plt.figure(figsize=(10, 5))
    plt.plot(income_df.index, income_df["amount"], label="Income", color="g")
    plt.plot(expense_df.index, expense_df["amount"], label="Income", color="r")
    plt.xlabel("Date")
    plt.ylabel("Amount")
    plt.title("Income and Expense Over Time")
    plt.legend()
    plt.grid(True)
    plt.show()
    get_summary()


def get_summary():
    df = pd.DataFrame(fetch_all_data(), columns=("id", "date", "amount", "category", "description"))
    total_income = df[df["category" == "Income"]]["amount"].sum()
    total_expense = df[df["category" == "Expense"]]["amount"].sum()
    net_saving = total_income - total_expense
    return total_income, total_expense, net_saving

