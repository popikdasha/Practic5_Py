import random
import multiprocessing as mp
from typing import List


def matrix_multiply_chunk(A: List[List[int]], B: List[List[int]], result: List, rows_A: int, cols_B: int,
                          row_start: int, row_end: int, col_start: int, col_end: int):
    for i in range(row_start, row_end):
        for j in range(col_start, col_end):
            result[i * cols_B + j] = sum(A[i][k] * B[k][j] for k in range(len(A[0])))


def multiply_matrices(A: List[List[int]], B: List[List[int]]) -> List[List[int]]:
    rows_A, cols_A = len(A), len(A[0])
    rows_B, cols_B = len(B), len(B[0])

    if cols_A != rows_B:
        raise ValueError("Количество столбцов первой матрицы должно быть равно количеству строк второй матрицы")

    # Создаем разделяемый массив для хранения результата
    result = mp.Array('i', rows_A * cols_B, lock=False)
    processes = []
    chunk_size = max(1, rows_A // mp.cpu_count())

    for i in range(0, rows_A, chunk_size):
        end_i = min(i + chunk_size, rows_A)
        p = mp.Process(target=matrix_multiply_chunk, args=(A, B, result, rows_A, cols_B, i, end_i, 0, cols_B))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()

    # Преобразуем разделяемый массив в двумерный список
    result_matrix = [[result[i * cols_B + j] for j in range(cols_B)] for i in range(rows_A)]
    return result_matrix


def generate_matrix(rows: int, cols: int) -> List[List[int]]:
    return [[random.randint(1, 9) for _ in range(cols)] for _ in range(rows)]


if __name__ == '__main__':
    # Ввод размеров матриц
    rows_A = int(input("Введите количество строк для матрицы A: "))
    cols_A = int(input("Введите количество столбцов для матрицы A: "))
    rows_B = int(input("Введите количество строк для матрицы B: "))
    cols_B = int(input("Введите количество столбцов для матрицы B: "))

    if cols_A != rows_B:
        print("Ошибка: Количество столбцов в A должно быть равно количеству строк в B для умножения")
    else:
        # Генерация случайных матриц
        A = generate_matrix(rows_A, cols_A)
        B = generate_matrix(rows_B, cols_B)

        # Выполнение умножения
        result = multiply_matrices(A, B)

        # Вывод результатов
        print("Матрица A:")
        for row in A:
            print(row)

        print("\nМатрица B:")
        for row in B:
            print(row)

        print("\nРезультирующая матрица (A * B):")
        for row in result:
            print(row)