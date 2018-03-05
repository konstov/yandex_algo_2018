from math import pow

# T - число беспилотных такси
# P - кол-во болельщиков
# Z - координаты фан-зон

T = int(input())
T_coord = [[int(j) for j in input().split(' ')] for i in range(T)]

P = int(input())
P_coord = [[int(j) for j in input().split(' ')] for i in range(P)]

Z = int(input())
Z_coord = [[int(j) for j in input().split(' ')] for i in range(Z)]

# вычисление расстояния от каждого такси до каждого объекта
T_dist = [[[k[0] - k[1] for k in zip(j, i)] for i in P_coord] for j in T_coord]


# бейзлайн на одной такси
t_0 = T_coord[0]

def min_d_to_P(t_0, P):
    # print(t_0, P)
    distances = [pow(sum([pow(i[0] - i[1], 2) for i in zip(p, t_0)]), 0.5) for p in P]
    m = min(distances)
    m_index = distances.index(m)
    return m, m_index

# Число перемещений при бейзлайне
MovesCount = P * 2

# выбранная такси
t = T_coord[0]

# список строк с перемещениями
MovesList = []


for i in range(P):
    m, m_index = min_d_to_P(t, P_coord)
    MovesList.append('MOVE ' + str(P_coord[m_index][0] - t[0])
                     + ' '
                     + str(P_coord[m_index][1] - t[1])
                     + ' '
                     + str(1)
                     + ' '
                     + str(1))
    t = P_coord[m_index]
    P_coord.pop(m_index)

    # до площадки
    m, m_index = min_d_to_P(t, Z_coord)
    MovesList.append('MOVE ' + str(Z_coord[m_index][0] - t[0])
                     + ' '
                     + str(Z_coord[m_index][1] - t[1])
                     + ' '
                     + str(1)
                     + ' '
                     + str(1))
    t = Z_coord[m_index]

print(MovesCount)
for i in MovesList:
    print(i)


