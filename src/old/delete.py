from decimal import *

acc = 1
base_inf = Decimal(0.1)


for i in range(5):
    acc *= 1 - base_inf
    # acc = acc * (1 - base_inf)
    print(f'{acc:.2f}')
