import pandas as pd
from sql_functions import fetch_all_data
import matplotlib.pyplot as plt


def plot_entries() -> bool:
    """
      Plots the daily income and expense amounts over time if there are any entries.

      Fetches all financial entries, preprocesses the data into pandas DataFrames
      for income and expenses, resamples the data to daily sums, and then
      generates and displays a line plot.

      :return:
          bool: True if there was data to plot and the plot was displayed successfully.
                False if there are no financial entries, and thus nothing to plot.
    """
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
    plt.title("Income and Expenses Over Time")
    plt.legend()
    plt.grid(True)
    plt.show()
    return True


def get_summary() -> tuple:
    """
    Fetches all financial entries and calculates amount sum of Income and Expenses and Net Savings
    :return:
        tuple: [0] = Total Income, [1] = Total Expense, [2] = Net Savings
    """
    df = pd.DataFrame(fetch_all_data(), columns=("id", "date", "amount", "category", "description"))
    total_income = df[df["category"] == "Income"]["amount"].sum()
    total_expense = df[df["category"] == "Expense"]["amount"].sum()
    net_savings = total_income - total_expense
    return total_income, total_expense, net_savings
