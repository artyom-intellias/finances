
def main():
    total = 500_000
    sum_ = 0
    for year_index in range(1, 11):
        if year_index != 1:
            total = total*1.05
        monthly_deposited = total / (10*12)
        sum_ += monthly_deposited*12
        print(f'montly: {monthly_deposited:.0f}')
        print(f'money deposited {year_index:.0f}: {sum_:.0f}')
        print(f'total {total:.0f}')
        print()
    print(f'{sum_=:.0f}')


if __name__ == '__main__':
    main()
