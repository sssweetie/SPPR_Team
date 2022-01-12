import csv
import math
import pathlib
import re
dir_path = pathlib.Path.cwd()
arraySquare = []
arrayId = []
arrayHumans = []
print("Введите страну")
country = input()
with open(str(dir_path) + '\\SPPR_Population\\' + str(country), newline='', encoding="utf-8") as cities:
     datacity = csv.reader(cities)
     next(datacity)
     sum_citizens = 0
     for row in datacity:
         sum_houses = 0
         row = str(row).split(";")
         population = row[1]
         population = float(re.sub("[\"\[',\]" "]",
                             "",
                             population))
         sum_citizens += population

with open(str(dir_path) + '\\SPPR_Houses\\' + str(country), newline='') as f:
    datahouse = csv.reader(f)
    next(datahouse, None)
    for string in datahouse:
        arrayId.append(string[0])
        arraySquare.append(string[1])
        square = string[1]
        square = float(square)
        sum_houses += square
avg_human = sum_citizens / sum_houses

with open(str(dir_path) + '\\final\\' + str(country), 'w', newline='') as f:
    bahamas = csv.writer(f, delimiter=',')
    for object in arraySquare:
        arrayHumans.append(math.ceil(avg_human * float(object)))
    for row in zip(arrayId,arraySquare,arrayHumans):
        bahamas.writerow(row)

print("finish")




