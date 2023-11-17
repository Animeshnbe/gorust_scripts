# program to generate prime numbers till 1000
def prime_numbers(n):
    prime_list = []
    for i in range(2, n):
        # optimise the inner loop
        for j in range(2, i):
            if i % j == 0:
                break
        else:
            prime_list.append(i)
    print(prime_list)

if __name__ == '__main__':
    prime_numbers(1000)