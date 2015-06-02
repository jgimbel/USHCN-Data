#!/usr/bin/python
f = open("state25_NE.txt")
months = []
for line in f:
    m = dict()
    m['code'] = line[0:6]
    m['year'] = line[6:10]
    m['month'] = line[10:12]
    m['type'] = line[12:16]
    m['days'] = list()

    data = [line[i:i + 8] for i in range(16, len(line)-1, 8)]
    for date, day in enumerate(data):
        if day[:5].strip() == '-9999':
            continue  # If no data exists, don't write the line

        d = dict()
        d['value'] = int(day[:5].strip())

        d['date'] = "{}-{}-{}".format(m['year'], m['month'], date+1)
        if day[5:6] != ' ':
            d['measure'] = day[5:6]
        if day[6:7] != ' ':
            d['quality'] = day[6:7]
        if day[7:8] != ' ':
            d['source'] = day[7:8]

        m['days'].append(d)
    months.append(m)

import json
with open("output.json", "wb") as out:
    json.dump(months, out)
f.close()
