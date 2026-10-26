import timeit
import os
 
# ---------- Boyer-Moore ----------
def build_shift_table(pattern):
    table = {}
    length = len(pattern)
    for index, char in enumerate(pattern[:-1]):
        table[char] = length - index - 1
    table.setdefault(pattern[-1], length)
    return table
 
 
def boyer_moore_search(text, pattern):
    shift_table = build_shift_table(pattern)
    i = 0
    while i <= len(text) - len(pattern):
        j = len(pattern) - 1
        while j >= 0 and text[i + j] == pattern[j]:
            j -= 1
        if j < 0:
            return i  # Match foundh
        i += shift_table.get(text[i + len(pattern) - 1], len(pattern))
    return -1
 
 
# ---------- Knuth-Morris-Pratt ----------
def compute_lps(pattern):
    lps = [0] * len(pattern)
    length = 0
    i = 1
    while i < len(pattern):
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1
    return lps
 
 
def kmp_search(text, pattern):
    lps = compute_lps(pattern)
    i = j = 0
    while i < len(text):
        if pattern[j] == text[i]:
            i += 1
            j += 1
            if j == len(pattern):
                return i - j 
        elif j != 0:
            j = lps[j - 1]
        else:
            i += 1
    return -1
 
 
# ---------- Rabin-Karp ----------
def polynomial_hash(s, base=256, modulus=101):
    h = 0
    for char in s:
        h = (h * base + ord(char)) % modulus
    return h
 
 
def rabin_karp_search(text, pattern):
    base = 256
    modulus = 101
    m = len(pattern)
    n = len(text)
 
    pattern_hash = polynomial_hash(pattern, base, modulus)
    window_hash = polynomial_hash(text[:m], base, modulus)
 
    h_multiplier = pow(base, m - 1, modulus)
 
    for i in range(n - m + 1):
        if pattern_hash == window_hash:
            if text[i:i + m] == pattern:
                return i
        if i < n - m:
            window_hash = (window_hash - ord(text[i]) * h_multiplier) % modulus
            window_hash = (window_hash * base + ord(text[i + m])) % modulus
    return -1


def read_file(filename):
    filename = os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return f.read()
    except UnicodeDecodeError:
        with open(filename, "r", encoding="cp1251") as f:
            return f.read()

def measure(func, text, pattern, number=100):
    total = timeit.timeit(lambda: func(text, pattern), number=number)
    return total / number

def main():
    text1 = read_file("стаття 1.txt")
    text2 = read_file("стаття 2.txt")

    real1 = "основне завдання програміста"
    real2 = "Структура розгорнутого списку дуже проста"
    fake = "квантовий комп'ютер на бананах"

    algorithms = [
        ("Боєр-Мур", boyer_moore_search),
        ("КМП", kmp_search),
        ("Рабін-Карп", rabin_karp_search),
    ]

    tests = [
        ("Стаття 1", text1, real1, fake),
        ("Стаття 2", text2, real2, fake),
    ]

    # total time of each algorithm for all tests
    total = {"Боєр-Мур": 0, "КМП": 0, "Рабін-Карп": 0}

    for name, text, real, fake_pattern in tests:
        print()
        print(name)
        print("Існуючий підрядок:", real)
        print("Вигаданий підрядок:", fake_pattern)
        times = {}

        for algo_name, func in algorithms:
            t_real = measure(func, text, real)
            t_fake = measure(func, text, fake_pattern)
            times[algo_name] = t_real + t_fake
            total[algo_name] += t_real + t_fake
            pos_real = func(text, real)
            pos_fake = func(text, fake_pattern)

            print(algo_name)
            print("  існуючий підрядок: позиція", pos_real, "час", round(t_real * 1000, 4), "мс")
            print("  вигаданий підрядок: позиція", pos_fake, "час", round(t_fake * 1000, 4), "мс")

        best = min(times, key=times.get)
        print("Найшвидший для", name, "->", best)
        print()
        print("Загальний час:")
    for algo_name in total:
        print(" ", algo_name, round(total[algo_name] * 1000, 4), "мс")

    best_total = min(total, key=total.get)
    print("Найшвидший в цілому ->", best_total)


if __name__ == "__main__":
    main()