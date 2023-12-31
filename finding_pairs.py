"""
Все случаи взаимного расположения отрезков [n, N] и [m, M] представляют собой: 1) Отсутствие пересечения,
2)Пересечение без полного включения и совпадения, 3) Пересечение с полным включением и совпадение.
1)В первом случае нужно посчитать количество элементов декартового прозведения: произведение длин
отрезков, увеличенных на единицу.
2)Во втором случае нужно посчитать количество элементов декартового произведения (так же, как и в первом пункте),
а затем отнять сумму арифметической прогрессии от 1 до длины общего отрезка + 1 (шаг арифметической прогрессии
равен 1). Тот факт, что количество элементов, которые не нужно учитывать, равно именно сумме такой арифметической
прогрессии легко увидеть, если изобразить все уникальные пары для совпадающих отрезков в виде матрицы.
3) В третьем случае нужно по аналогии с первым пунктом посчитать количество элементов декартового произведения, а затем
отнять сумму арифметической прогрессии от 1 до длины минимального из начальных отрезков + 1 (т.к. такой отрезок и будет
полностью включен в другой, либо же совпадать с другим).
"""


def find_pairs(n, N, m, M):
    if (n < m and N < m) or (m < n and M < n):
        return (N - n + 1) * (M - m + 1)
    if (N >= m >= n) or (M >= n >= m):
        return (N - n + 1) * (M - m + 1) - sum(range(min((N - m + 1), (M - n + 1))))
    if (n <= m <= M <= N) or (m <= n <= N <= M):
        return (N - n + 1) * (M - m + 1) - sum(range(min((M - m + 1), (N - n + 1))))


answer = find_pairs(500, 500000, 999, 999999)
print(answer)
