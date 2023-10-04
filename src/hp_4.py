# hp_4.py
#
from datetime import datetime, timedelta
from csv import DictReader, DictWriter
from collections import defaultdict
from pathlib import Path
import os


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
    format_string = "%Y-%m-%d"
    start_date_time = datetime.strptime(start, format_string)
    range_list.append(start_date_time)
    if not isinstance(start, str) or not isinstance(n, int):
        raise TypeError
    else:
        for days_to_add in range(1, n):
            day = timedelta(days=days_to_add)
            current_date = start_date_time + day
            range_list.append(current_date)
    return range_list


def add_date_range(values, start_date):
    """Adds a daily date range to the list `values` beginning with
    `start_date`.  The date, value pairs are returned as tuples
    in the returned list."""
    date_ranges = date_range(start_date, len(values))
    return list(zip(date_ranges, values))


def fees_report(infile, outfile):
    """Calculates late fees per patron id and writes a summary report to
    outfile."""
    #fee .25/day
    #book_uid, isbn_13, patron_id, date_checkout, date_due, date_returned
    #patron_id: A unique ID string associated with a library patron account. Note that there may be duplicates for this field as many patrons check out multiple books.
    #date_due: A date string representing the date that the book was due. The date format is mm/dd/yyyy.
    #date_returned: The date that the book was returned. The date format is mm/dd/yy.
    #outputs:
    #late_fees: the total USD amount fee for the patron_id formatted as a floating point value with 2 decimal places of precision. Note: No "$" should be included in the values. Example: 1.25.
    #Constants

    fee = 0.25
    format_sting = "%m/%d/%Y"
    output_fields = ["patron_id", "late_fees"]
    result = defaultdict(float)
    output_data = ""
    #raise TypeError(outfile)
    #C:\Users\chake\AppData\Local\Temp\tmpuek1io45\fees_report_out_short.txt
    with open(os.path.join(os.pardir, infile), 'r') as csv_file:
        reader = DictReader(csv_file)
        for row in reader:
            patron_id = row['patron_id']
            date_due = datetime.strptime(row['date_due'], format_sting)
            date_returned = datetime.strptime(row['date_returned'], format_sting)
            if date_due < date_returned:
                days_late = date_returned - date_due
                result[patron_id] += days_late.days * fee
            else:
                result[patron_id] += 0
        output_data = [{"patron_id":k, "late_fees": '{:.2f}'.format(v)} for k, v in result.items()]
    with open(outfile, 'w') as csv_file:
        writer = DictWriter(csv_file, fieldnames=output_fields)
        writer.writeheader()
        writer.writerows(output_data)


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
