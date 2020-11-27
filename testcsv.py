import datetime
d = datetime.date(2012, 12, 14)

import csv
row = []
row.append(d)
row.append('hi')
row.append('ho')
print(row)
with open('run2file.csv', 'w', newline='', encoding='utf-8') as csv_file:
    writer = csv.writer(csv_file, delimiter=';')
    writer.writerow(row)