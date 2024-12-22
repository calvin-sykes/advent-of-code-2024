from common import *
from functools import cache

def mix(a, b):
    return a ^ b

def prune(a):
    return a % 16777216

def next_secret(secret):
    secret = prune(mix(secret, secret * 64))
    secret = prune(mix(secret, secret // 32))
    return prune(mix(secret, secret * 2048))

@cache
def generate_secrets(secret, n_generate):
    secrets = [secret]
    for _ in range(n_generate):
        secret = next_secret(secret)
        secrets.append(secret)
    return secrets

def day22_part1(filename):
    lines = parse_lines(filename)
    starting_secrets = list(map(int, lines))

    sum_secrets = 0
    n_generate = 2000
    for secret in starting_secrets:
        sum_secrets += generate_secrets(secret, n_generate)[-1]
    return sum_secrets

def day22_part2(filename):
    lines = parse_lines(filename)
    starting_secrets = list(map(int, lines))

    n_generate = 2000
    sequences = defaultdict(lambda: 0)
    for secret in starting_secrets:
        price_differences = []
        secrets_this_buyer = generate_secrets(secret, n_generate)
        sequences_this_buyer = dict()

        for i in range(n_generate):
            price = secret % 10
            if i != 0:
                price_differences.append(price - last_price)
            last_price = price

            if i > 4:
                previous_changes = tuple(price_differences[i-4:i])
                if previous_changes not in sequences_this_buyer:
                    sequences_this_buyer[previous_changes] = price
            secret = secrets_this_buyer[i+1]

        for seq, price in sequences_this_buyer.items():
            sequences[seq] += price
    
    best_sequence = max(sequences, key=sequences.__getitem__)
    return sequences[best_sequence]

if __name__ == "__main__":
    print("Part 1 example", day22_part1("input/day22_example.txt"))
    print("Part 1", day22_part1("input/day22.txt"))
    print("Part 2 example", day22_part2("input/day22_example2.txt"))
    print("Part 2", day22_part2("input/day22.txt"))
