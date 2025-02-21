import json
with open("lab4/json/sample-data.json", 'r') as j:
    content = j.read()
q = json.loads(content)

heads = (
    ['dn', "DN"],
    ["descr", "Description"],
    ["speed", "Speed"],
    ['mtu', "MTU"],
    ["id", "ID"])

table = {
    "heads": [h[1] for h in heads],
    "content": [[d["l1PhysIf"]["attributes"][h[0]] for h in heads] for d in q['imdata']]
}


def print_table(table, sep=' | '):
    heads = table["heads"]
    content = table["content"]
    head_lenghts = [max(map(len, (c[i] for c in content))) + len(h) for i, h in enumerate(heads)]
    print("Interface Status", "="*sum(head_lenghts), sep = '\n')
    print(*(h + " "*(head_lenghts[i] - len(h)) for i, h in enumerate(heads)), sep=sep)
    print(*(l*"-" for l in head_lenghts), sep=sep)
    for c in content:
        print(*((q := str(f)) + abs(len(q) -
              head_lenghts[i])*' ' for i, f in enumerate(c)), sep=sep)


print_table(table)