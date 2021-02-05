f = open("to_scrap.log", "r")
duplicates = []
for x in f:
    if x not in duplicates:
        duplicates.append(x)

filename = 'to_scrap.log'
with open(filename, 'a+') as f:
    f.write("\n--------------\n")
    for e in duplicates:
        f.write(e)
    f.close()
