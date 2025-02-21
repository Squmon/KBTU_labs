import datetime as d
date1 = d.datetime(2025, 11, 2, 10, 3, 5)
date2 = d.datetime(2025, 10, 1, 11, 2, 1)

print(date1.timestamp() - date2.timestamp() )