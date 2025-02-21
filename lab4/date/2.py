import datetime as d
now = d.datetime.now()
yesterday = now - d.timedelta(days = 1)
tommorow = now + d.timedelta(days = 1)

print(
    f"Today ={now.strftime('%Y-%m-%d')}",
    f"Yesterday = {yesterday.strftime('%Y-%m-%d')}",
    f"Tommorow = {tommorow.strftime('%Y-%m-%d')}",
    sep = "\n"
)