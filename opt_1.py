from math import pow, sqrt

# T - число беспилотных такси
# P - кол-во болельщиков
# Z - координаты фан-зон

T = int(input())
# T_coord = [[int(j) for j in input().split(' ')] for i in range(T)]
T_coord = {i: [int(j) for j in input().split(' ')] for i in range(T)}

P = int(input())
# P_coord = [[int(j) for j in input().split(' ')] for i in range(P)]
P_coord = {i: [int(j) for j in input().split(' ')] for i in range(P)}

Z = int(input())
# Z_coord = [[int(j) for j in input().split(' ')] for i in range(Z)]
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


def update_taxi_coord(T_P_dist, index):
    pass

################################################## Расчёт ###########################################################
# расстояния от пассажиров до ближаших стадионов
P_Z_dist = A_B_dist(P_coord, Z_coord)

# расстояния от такси до ближаших пассажиров
T_P_dist = A_B_dist(T_coord, P_coord)

# список строк с перемещениями
MovesList = []
movescount = 0

for i in range(P):
    # Определю, какое такси полетит к болельщику
    t_index, t_par = next_taxi(T_P_dist)
    MovesList.append('MOVE ' + str(t_par[2])
                     + ' '
                     + str(t_par[3])
                     + ' '
                     + str(1)
                     + ' '
                     + str(t_index + 1))
    T_coord[t_index] = [T_coord[t_index][0] + t_par[2], T_coord[t_index][1] + t_par[3]]
    movescount += 1

    # перемещение от болельщика до точки, t_par[-2] - идентификатор болельщика
    p_par = P_Z_dist[t_par[-2]]
    MovesList.append('MOVE ' + str(p_par[2])
                     + ' '
                     + str(p_par[3])
                     + ' '
                     + str(1)
                     + ' '
                     + str(t_index + 1))
    T_coord[t_index] = [T_coord[t_index][0] + p_par[2], T_coord[t_index][1] + p_par[3]]
    movescount += 1

    # # сдвину такси на 1 со стадиона
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

        T_coord[t_index] = [T_coord[t_index][0] + shift, T_coord[t_index][1]]
        MovesList.append('MOVE ' + str(shift)
                         + ' '
                         + str(0)
                         + ' '
                         + str(1)
                         + ' '
                         + str(t_index + 1))
        movescount += 1

    # удалю болельщика из списка
    P_coord.pop(t_par[-2])
    P_Z_dist.pop(t_par[-2])
    # Обновлю данные от такси до болельщиков
    # print(t_index, P_coord)
    # обновление расстояний до точек
    # print(t_par[-2], t_index, T_P_dist)

    # print(T_P_dist)

    for key, value in T_P_dist.items():
        if value[-2] == t_par[-2]:
            # print(key, Z_coord)
            # print(A_B_dist({key: Z_coord[key]}, P_coord))
            T_P_dist[key] = A_B_dist({key: T_coord[key]}, P_coord)[key]

print(movescount)
for i in MovesList:
    print(i)
