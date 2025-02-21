import datetime as d
now = d.datetime.now()
x = now - d.timedelta(days = 5)
print(now.strftime("%Y-%m-%d"), "- 5days =", x.strftime("%Y-%m-%d"))