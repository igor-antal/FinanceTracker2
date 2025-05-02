from datetime import datetime


def parse_date_to_sql(date: str) -> str:
    """
        Parses date string into sqlite support date string format.
        :param date: Date string in day/month/year format.
        :return:
            str: Date string in year/month/day format.
    """
    date = datetime.strptime(date, "%d/%m/%Y")
    return datetime.strftime(date, "%Y-%m-%d")


def validate_float_input(user_input: str) -> bool:
    """
    Validating function for tkinter Entry field. Checks if users input is float or not.
    :param user_input: Users input
    :return:
        bool: True if users input is float.
              False if users input is empty or not float.
    :raises ValueError: When user enters anything that's not float.
    """
    if not user_input:
        return False
    try:
        float(user_input)
        return True
    except ValueError:
        return False


def parse_sql_date(date: str) -> str:
    """
        Parses sqlite supported date string into more readable format.
        :param date: Date string in year/month/day format.
        :return:
            str: Date string in day/month/year format.
    """
    date = datetime.strptime(date, "%Y-%m-%d")
    return datetime.strftime(date, "%d/%m/%Y")
