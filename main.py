N = int(input())

init = ['***','* *','***']
def star(n = 3, arr = init):
    if n == N:
        return arr

    Li = []
    for i in range(n):
        Li.append(arr[i] * 3)

    for i in range(n):
        Li.append(arr[i] + ' ' * n + arr[i])

    for i in range(n):
        Li.append(arr[i] * 3)

    return star(n * 3, Li)

res = star(3, init)

for j in res:
    print(j)