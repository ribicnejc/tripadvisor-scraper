import unicodedata
import hashlib
from datetime import datetime, timedelta

dates = {"Jan": "01",
         "Feb": "02",
         "Mar": "03",
         "Apr": "04",
         "May": "05",
         "Jun": "06",
         "Jul": "07",
         "Aug": "08",
         "Sep": "09",
         "Oct": "10",
         "Nov": "11",
         "Dec": "12"}

datesV2 = {"January": "01",
           "February": "02",
           "March": "03",
           "April": "04",
           "May": "05",
           "June": "06",
           "July": "07",
           "August": "08",
           "September": "09",
           "October": "10",
           "November": "11",
           "December": "12"}


def byte_to_string(b_string):
    if isinstance(b_string, str):
        return b_string
    return b_string.decode('utf-8')


def unicode_to_string(value):
    if isinstance(value, str):
        return value
    if value is not None:
        return unicodedata.normalize('NFKD', value).encode('utf8', 'ignore')
    return None


def unicode_string_to_md5(value):
    return hashlib.md5(value.encode()).hexdigest()


def unicode_list_to_string(arr):
    value = ""
    for el in arr:
        value += unicode_to_string(el) + " & "
    return value[:-3]


def unicode_int_list_to_string(arr):
    value = ""
    for el in arr:
        value += str(el) + " & "
    return value[:-3]


def unicode_date_v2_to_string_number(date):
    date = unicode_to_string(date)
    date = date.replace(" wrote a review ", "").split(" ")
    day = '01'
    month = '01'
    year = '1000'
    if len(date) == 1:  # wrote a review Yesterday
        # print("case 3")
        yesterday = datetime.now() - timedelta(1)
        day = yesterday.now().day
        month = yesterday.now().month
        year = yesterday.now().year

    elif len(date) == 2 and len(date[1]) == 4:  # wrote a review Nov 2020
        # print("case 2")
        month = dates[date[0]]
        year = date[1]

    elif len(date) == 2 and len(date[1]) < 4:  # wrote a review Dec 1 // date[0] = Dec
        # print("case 1")
        day = date[1]
        month = dates[date[0]]
        if len(day) == 1:
            day = '0' + day
        year = datetime.now().year

    return str(year) + month + day
    # current_month = datetime.now().strftime('%m')
    # current_month_text = datetime.now().strftime('%h')
    # current_month_text = datetime.now().strftime('%B')
    # current_day = datetime.now().strftime('%d')
    # current_day_text = datetime.now().strftime('%a')
    # current_day_full_text = datetime.now().strftime('%A')
    #
    # current_weekday_day_of_today = datetime.now().strftime('%w')
    # current_year_full = datetime.now().strftime('%Y')
    # current_year_short = datetime.now().strftime('%y')
    # current_second = datetime.now().strftime('%S')
    # current_minute = datetime.now().strftime('%M')
    # current_hour = datetime.now().strftime('%H')
    # current_hour = datetime.now().strftime('%I')
    # current_hour_am_pm = datetime.now().strftime('%p')
    # current_microseconds = datetime.now().strftime('%f')


def unicode_date_v3_to_string_number(date):
    date = unicode_to_string(date)
    date = date.replace(",", "").split(" ")
    year = date[2]
    month = datesV2[date[1]]
    day = '01'
    return year + month + day


def unicode_date_to_string_number(date):
    date = unicode_to_string(date)
    date = date.replace(",", "").split(" ")
    dates = {"Jan": "01",
             "Feb": "02",
             "Mar": "03",
             "Apr": "04",
             "May": "05",
             "Jun": "06",
             "Jul": "07",
             "Aug": "08",
             "Sep": "09",
             "Oct": "10",
             "Nov": "11",
             "Dec": "12"}
    if int(date[1]) < 10:
        date[1] = "0" + date[1]
    return date[2] + dates[date[0]] + date[1]


def unicode_rating_to_string(rating):
    return str(int(unicode_to_string(rating).split(" ")[1].replace("bubble_", "")) / 10)


def unicode_user_uid_to_string(uid):
    if unicode_to_string(uid) is not None:
        return unicode_to_string(uid).split("-")[0].split("_")[1]
    return "tripadvisor-member"
