#!/usr/bin/python
import csv
PRCP = open("PRCP.csv", "wb")
SNOW = open("SNOW.csv", "wb")
SNWD = open("SNWD.csv", "wb")
TMAX = open("TMAX.csv", "wb")
TMIN = open("TMIN.csv", "wb")

PRCPWriter = csv.writer(PRCP)
SNOWWriter = csv.writer(SNOW)
SNWDWriter = csv.writer(SNWD)
TMAXWriter = csv.writer(TMAX)
TMINWriter = csv.writer(TMIN)

f = open("state25_NE.txt")
for line in f:
    code = line[0:6]
    year = line[6:10]
    month = line[10:12]
    t = line[12:16]

    writer = PRCPWriter if t == 'PRCP' else \
            SNOWWriter if t == 'SNOW' else \
            SNWDWriter if t == 'SNWD' else \
            TMAXWriter if t == 'TMAX' else TMINWriter

    data = [line[i:i + 8] for i in range(16, len(line)-1, 8)]
    for date, day in enumerate(data):
        if day[:5].strip() == '-9999':
            continue  # If no data exists, don't write the line

        d = list()
        d.append(int(day[:5].strip()))
        d.append("{0}-{1}-{2}".format(year, month, date+1))
        d.append(day[5:6] if day[5:6] != ' ' else '')
        d.append(day[6:7] if day[6:7] != ' ' else '')
        d.append(day[7:8] if day[7:8] != ' ' else '')
        writer.writerow(d)

f.close()
PRCP.close()
SNOW.close()
SNWD.close()
TMAX.close()
TMIN.close()
