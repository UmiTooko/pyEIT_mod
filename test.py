a = [[[0], [1]], [[0], [1]], [[0], [1]]]
b = []
for i in a:
    t = []
    print(i)
    for j in i:
        t.append(j[0])
    b.append(t)
print(b)