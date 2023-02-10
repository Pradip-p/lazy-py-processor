import datetime


def get_current_date(format="%Y-%m-%d"):
    """
    Returns the current date
    :param format: desired Date format
            examples:
                    %Y-%m-%d
                    %d-%m-%Y
                    %Y/%m/%d

    :return: date string in the format specified.
            Default format is  YYYY-MM-DD
    """
    return datetime.datetime.now().strftime(format)


def get_day():
    """
    returns current day
    :return: int
    """
    return datetime.datetime.now().day


def get_month():
    """
    returns current month
    :return:  int
    """
    return datetime.datetime.now().month


def get_year():
    """
    Returns current year
    :return: int
    """
    return datetime.datetime.now().year
