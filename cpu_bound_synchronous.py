import time
from tracemalloc import start

def cpu_bound(number):
    return sum(i * i for i in range(number))

def find_sums(numbers):
    res = []
    for n in numbers:
        res.append(cpu_bound(n))
    return res

def main():
    numbers = [3_000_000 + x for x in range(30)]

    start_time = time.time()

    total = find_sums(numbers)

    print(f'total list : {total}')
    print(f'sum : {sum(total)}')

    duration = time.time() - start_time

    print(f'duration : {duration}')

if __name__ == '__main__':
    main()
