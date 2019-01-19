import unicodedata


def unicode_to_string(value):
    return unicodedata.normalize('NFKD', value).encode('utf8', 'ignore')


def unicode_list_to_string(list):
    value = ""
    for el in list:
        value += unicode_to_string(el) + " & "
    return value[:-3]


def unicode_date_to_string_number(date):
    date = unicode_to_string(date)
    date = date.replace(",", "").split(" ")
    dates = {"January": "01",
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
    return date[2] + dates[date[0]] + date[1]


def unicode_rating_to_string(rating):
    return str(int(unicode_to_string(rating).split(" ")[1].replace("bubble_", "")) / 10)


def unicode_user_uid_to_string(uid):
    return unicode_to_string(uid).split("-")[0].split("_")[1]
