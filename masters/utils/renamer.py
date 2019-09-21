import os
import re

# <>:"/\|?*
folder = "../scraped_data/data_reviews_hungary"
for file in os.listdir(folder):
    file_old = file
    if file.__contains__("<"):
        file = file.replace("<", "_")
    if file.__contains__(">"):
        file = file.replace(">", "_")
    if file.__contains__(":"):
        file = file.replace(":", "_")
    if file.__contains__("\""):
        file = file.replace("\"", "_")
    if file.__contains__("/"):
        file = file.replace("/", "_")
    if file.__contains__("\\"):
        file = file.replace("\\", "_")
    if file.__contains__("|"):
        file = file.replace("|", "_")
    if file.__contains__("?"):
        file = file.replace("?", "_")
    if file.__contains__("*"):
        file = file.replace("*", "_")

    if file_old != file:
        os.rename(folder + "/" + file_old, folder + "/" + file)
        print(file_old)
