n = int(input("Enter the number of inputs: "))
print("Enter inputs in format x1 x2 ... t:")
table = list()
for i in range(2**n):
    x = input().split(sep=" ")
    if len(x) != n + 1:
        print("Invalid input!")
        exit()
    table.append([int(j) for j in x])

epoch = int(input("Enter no. of epochs: "))
alpha = float(input("Learning rate= "))
bias = float(input("Bias= "))
weights = []
for i in range(n):
    weights.append(float(input(f"w{i+1}= ")))
theta = float(input("Theta= "))

def activate(yin):
    if yin > theta:
        return 1
    elif yin < theta:
        return -1
    else:
        return 0

for epoch_num in range(epoch):
    print(f"\nRound {epoch_num + 1}:")
    for i in range(n):
        print(f"x{i+1}", end="\t")
    print("t\tyin\ty=f(yin)", end="\t")
    for i in range(n):
        print(f"w{i+1}", end="\t")
    print("bias")

    for i in range(2**n):
        yin = bias
        for j in range(n):
            yin += weights[j] * table[i][j]
            print(table[i][j], end="\t")
        print(table[i][n], end="\t")
        print(f"{yin:.2f}", end="\t")

        y = activate(yin)
        print(y, end="\t")

        if y != table[i][n]:
            for k in range(n):
                weights[k] = weights[k] + alpha * table[i][k] * table[i][n]
            bias = bias + alpha * table[i][n]

        for k in range(n):
            print(f"{weights[k]:.2f}", end="\t")
        print(f"{bias:.2f}")
