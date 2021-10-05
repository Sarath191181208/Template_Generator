i = 0
while i < 10:
    for _ in range(20):
        if i == 5:
            break
    i += 1
    print(i)
