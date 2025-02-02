#10

def unique(l:list):
    q = []
    for e in l:
        if e not in l:
            q.append(e)
    return q

