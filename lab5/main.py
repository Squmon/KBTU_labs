import re

txt = "The best cat in the world! Baba is you BaBa is you a0 a00 abbb abb abbbb ab a0b a00b a0bbb The end! hello_world world_hello theWorld"


tasks = [
    re.findall(r'a(0|b+)', txt),
    re.findall(r'ab{2,3}', txt),
    re.findall(r'[A-Z][a-z]', txt),
    re.findall(r'a.+b', txt),
    re.sub('[ ,.]', ':', txt),
    re.sub(r'_([a-zA-Z])', lambda match: match.group(1).upper(), txt),
    re.split(r"[A-Z]", txt),
    re.sub(r'([a-z])([A-Z])', lambda match: match.group(1) + " " + match.group(2), txt),
    re.sub(r'([a-z])([A-Z])', lambda match: match.group(1) + "_" + match.group(2).lower(), txt)
]
print("original string", txt, sep = '\n')
for n, t in enumerate(tasks):
    print(f"---{n}----", t, '', sep = '\n')