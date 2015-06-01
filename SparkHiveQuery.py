from pyspark import SparkContext
from pyspark.sql import HiveContext
sc = SparkContext()
cxt = HiveContext(sc)

result = cxt.sql("SELECT date, avg(value) as average \
          FROM prcp \
          WHERE date like '%-12-22' \
          GROUP BY date \
          ORDER BY date;")

with open("precep.csv", "wb") as prep:
    for row in result:
        prep.write(row.date.split("-")[0] + "," + str(row.average) + "\n")
        print(row.date.split("-")[0], row.average)
