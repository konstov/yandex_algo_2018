from math import pow, sqrt
# from time import time

# T - число беспилотных такси
# P - кол-во болельщиков
# Z - координаты фан-зон
# start = time()
T = int(input())
T_coord = {i: [int(j) for j in input().split(' ')] for i in range(T)}

P = int(input())
P_coord = {i: [int(j) for j in input().split(' ')] for i in range(P)}

Z = int(input())
Z_coord = {i: [int(j) for j in input().split(' ')] for i in range(Z)}

# вычисление расстояния от каждого такси до каждого пассажира
# T_dist = [[[k[0] - k[1] for k in zip(j, i)] for i in P_coord] for j in T_coord]


# Функция, которая находит минимальное расстония для каждой точки из первого словаря
# до точки из второго словаря
# в словаре координаты точки и смещения, чтобы до них добраться и расстояние
def A_B_dist(A_coord, B_coord):
    A_B_distances = {}
    for p_index, p in A_coord.items():
        min_dist, min_coord, z_index = 1000000, [], 0
        for index, z in B_coord.items():
            dist = sqrt((p[0] - z[0]) ** 2 + (p[1] - z[1]) ** 2)
            # print(p_index, index, dist, min_dist)
            if dist < min_dist:
                min_dist = dist
                min_coord = z
                z_index = index
        A_B_distances[p_index] = min_coord + [i[0] - i[1] for i in zip(min_coord, p)] + [z_index] + [min_dist]
    return A_B_distances


# Функция для поиска такси, которое сейчас полетит (у которого самый короткий путь болельщика)
def next_taxi(T_P_dist):
    min_d = 100000
    index_d = 0
    for key, value in T_P_dist.items():
        # print(value, min_d)
        if value[-1] < min_d:
            min_d, index_d = value[-1], key
    return index_d, T_P_dist[index_d]


def taxi_to_move(t_index, par, T_P_dist):
    taxi_cnt = 1
    taxi_numbers = [t_index]
    for key, value in T_P_dist.items():
        if t_index != key and is_similar_vector(par[2:4], value[2:4], value[0:2]):
            taxi_cnt += 1
            taxi_numbers.append(key)
    return taxi_cnt, taxi_numbers


def update_dist_A_B(A_B_dist_old, A_coord, B_coord, taxi_numbers):
    for key, value in T_P_dist.items():
        if value[-2] == t_par[-2] or key in taxi_numbers:
            A_B_dist_old[key] = A_B_dist({key: A_coord[key]}, B_coord)[key]
    return A_B_dist_old

# вектора смещения похожи если направлены в одну четверть
# и если их длины примерно равны
def is_similar_vector(a, b, pos_b):
    summ = 0
    summ_1 = 0
    for i in zip(a, b, pos_b):
        delta = abs(i[1] - i[0])
        if i[0] * i[1] >= 0 and delta < 5:
            summ_1 += delta
            summ += 1
    if summ == len(a) and summ_1 < sqrt(b[0] ** 2 + b[1] ** 2) and pos_b[0] + a[0] < 10000 and pos_b[1] + a[1] < 10000:
        return True
    return False


def is_similar_vector_new(a, b, pos_b):
    alpha_2 = sqrt((pow(a[0], 2) + pow(a[1], 2)) * (pow(b[0], 2) + pow(b[1], 2)))
    if alpha_2 != 0:
        alpha = (a[0] * b[0] + a[1] * b[1])
        cos_alpha = alpha / alpha_2
    else:
        cos_alpha = 1
    if cos_alpha > 0.7 and pos_b[0] + a[0] < 10000 and pos_b[1] + a[1] < 10000:
        return True
    return False


def is_similar_vector_new_(a, b, pos_b):
    if 2 * (a[0] * b[0] + a[1] * b[1]) > a[0] ** 2 + a[1] ** 2\
                and pos_b[0] + a[0] < 10000 and pos_b[1] + a[1] < 10000:
        return True
    return False

# Генерирование текста для перемещения
def generate_move(par, taxi_cnt, taxi_numbers):
    if isinstance(taxi_numbers, list):
        return 'MOVE {0} {1} {2} {3}'.format(str(par[2]),
                                             str(par[3]),
                                             str(taxi_cnt),
                                             str(' '.join([str(i+1) for i in sorted(taxi_numbers)]))
                                             )
    return 'MOVE {0} {1} {2} {3}'.format(str(par[2]),
                                         str(par[3]),
                                         str(taxi_cnt),
                                         str(taxi_numbers+1)
                                         )

################################################## Расчёт ###########################################################
# расстояния от пассажиров до ближаших стадионов
P_Z_dist = A_B_dist(P_coord, Z_coord)
# расстояния от такси до ближаших пассажиров
T_P_dist = A_B_dist(T_coord, P_coord)
# список строк с перемещениями
MovesList = []
movescount = 0
Z_coord_list = [value for key, value in Z_coord.items()]

for i in range(P):
    # Определю, какое такси полетит к болельщику
    t_index, t_par = next_taxi(T_P_dist)

    # попробую сдвинуть похожие такси
    if movescount / 3 < P - 1:
        taxi_cnt, taxi_numbers = taxi_to_move(t_index, t_par, T_P_dist)

        # Изменю координаты такси, если сдвиг приведёт к совпадению, то не буду сдвигать
        T_coords_list = [value for key, value in T_coord.items()]
        taxi_numbers_c = taxi_numbers.copy()
        for num in taxi_numbers_c:
            new_coord = [T_coord[num][0] + t_par[2], T_coord[num][1] + t_par[3]]
            if new_coord not in T_coords_list and new_coord not in Z_coord_list:
                T_coord[num] = new_coord
                T_coords_list = [value for key, value in T_coord.items()]
            else:
                taxi_cnt -= 1
                taxi_numbers.remove(num)

        # пересчитаю расстояния после сдвига такси
        T_P_dist = update_dist_A_B(T_P_dist, T_coord, P_coord, taxi_numbers)
        MovesList.append(generate_move(t_par, taxi_cnt, taxi_numbers))
    else:
        t_index, t_par = next_taxi(T_P_dist)
        MovesList.append(generate_move(t_par, 1, t_index))

        T_coord[t_index] = [T_coord[t_index][0] + t_par[2], T_coord[t_index][1] + t_par[3]]
        T_P_dist = update_dist_A_B(T_P_dist, T_coord, P_coord, [t_index])

    movescount += 1

    # перемещение от болельщика до точки, t_par[-2] - идентификатор болельщика
    p_par = P_Z_dist[t_par[-2]]

    # попробую сдвинуть похожие такси
    if movescount / 3 < P - 1:
        taxi_cnt, taxi_numbers = taxi_to_move(t_index, p_par, T_P_dist)

        # Изменю координаты такси, если сдвиг приведёт к совпадению, то не буду сдвигать
        T_coords_list = [value for key, value in T_coord.items()]
        taxi_numbers_c = taxi_numbers.copy()
        for num in taxi_numbers_c:
            new_coord = [T_coord[num][0] + p_par[2], T_coord[num][1] + p_par[3]]
            if num == t_index or (new_coord not in T_coords_list and new_coord not in Z_coord_list):
                T_coord[num] = new_coord
                T_coords_list = [value for key, value in T_coord.items()]
            #new_coord = [T_coord[num][0] + p_par[2], T_coord[num][1] + p_par[3]]
            #if (new_coord not in T_coords_list and new_coord not in Z_coord_list):
            #    T_coord[num] = new_coord
            else:
                taxi_cnt -= 1
                taxi_numbers.remove(num)

        # пересчитаю расстояния после сдвига такси
        T_P_dist = update_dist_A_B(T_P_dist, T_coord, P_coord, taxi_numbers)
        MovesList.append(generate_move(p_par, taxi_cnt, taxi_numbers))
    else:
        p_par = P_Z_dist[t_par[-2]]
        MovesList.append(generate_move(p_par, 1, t_index))

        T_coord[t_index] = [T_coord[t_index][0] + p_par[2], T_coord[t_index][1] + p_par[3]]
        T_P_dist = update_dist_A_B(T_P_dist, T_coord, P_coord, [t_index])
    movescount += 1

    # сдвину такси на немного со стадиона
    if (movescount - 2) // 3 < P - 1:
        isPlaceBusy = True
        shift = 1
        while isPlaceBusy:
            isPlaceBusy = False
            for key in T_coord:
                if T_coord[key] == [T_coord[t_index][0] + shift, T_coord[t_index][1]] and key != t_index:
                    isPlaceBusy = True
                    shift += 1
                    break

        MovesList.append(generate_move([0, 0, shift, 0], 1, t_index))
        T_coord[t_index] = [T_coord[t_index][0] + shift, T_coord[t_index][1]]
        movescount += 1

    # удалю болельщика из списка
    P_coord.pop(t_par[-2])
    P_Z_dist.pop(t_par[-2])

    # пеерсчёт расстояний до болельщиков
    for key, value in T_P_dist.items():
        if value[-2] == t_par[-2] or key in taxi_numbers:
            T_P_dist[key] = A_B_dist({key: T_coord[key]}, P_coord)[key]

print(movescount)
for i in MovesList:
    print(i)

# print(time() - start)