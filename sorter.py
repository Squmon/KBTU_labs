with open("main.py", 'r') as j:
    content = map(lambda x: '#' + x, j.read().split("#"))
for n, c in enumerate(content):
    with open(f"functions1/task{n}.py", 'w') as j:
        j.write(c)