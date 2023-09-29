# hp_4.py
#
from datetime import datetime, timedelta
from csv import DictReader, DictWriter
from collections import defaultdict


def reformat_dates(old_dates):
    """Accepts a list of date strings in format yyyy-mm-dd, re-formats each
    element to a format dd mmm yyyy--01 Jan 2001."""
    format_dates = "%d %b %Y"
    format_str_p_time = "%Y-%m-%d"
    listed_dates = []
    for date in old_dates:
        date_time_object = datetime.strptime(date, format_str_p_time)
        listed_dates.append(date_time_object.strftime(format_dates))
    return listed_dates


def date_range(start, n):
    """For input date string `start`, with format 'yyyy-mm-dd', returns
    a list of of `n` datetime objects starting at `start` where each
    element in the list is one day after the previous."""
    range_list = []
    date_string = start
    format_string = "%Y-%m-%d %H:%M:%S"
    start_date_time = datetime.strptime(start, format_string)
    range_list.append(start_date_time)
    if not isinstance(date_string, str) or not isinstance(n, int):
        raise TypeError
    else:
        for days_to_add in range(1, n + 1):
            day = timedelta(days=days_to_add)
            current_date = start_date_time + day
            range_list.append(current_date)

    return range_list







def add_date_range(values, start_date):
    """Adds a daily date range to the list `values` beginning with
    `start_date`.  The date, value pairs are returned as tuples
    in the returned list."""
    pass


def fees_report(infile, outfile):
    """Calculates late fees per patron id and writes a summary report to
    outfile."""
    pass


# The following main selection block will only run when you choose
# "Run -> Module" in IDLE.  Use this section to run test code.  The
# template code below tests the fees_report function.
#
# Use the get_data_file_path function to get the full path of any file
# under the data directory.

if __name__ == '__main__':
    
    try:
        from src.util import get_data_file_path
    except ImportError:
        from util import get_data_file_path

    # BOOK_RETURNS_PATH = get_data_file_path('book_returns.csv')
    BOOK_RETURNS_PATH = get_data_file_path('book_returns_short.csv')

    OUTFILE = 'book_fees.csv'

    fees_report(BOOK_RETURNS_PATH, OUTFILE)

    # Print the data written to the outfile
    with open(OUTFILE) as f:
        print(f.read())
