A, B ,V = map(int, input().split())

res = (V - B) / (A - B)

if res == int(res):
    print(int(res))
else:
    print(int(res) + 1)