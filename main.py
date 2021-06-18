import csv
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt


def nums_gen():  # генератор номеров систем сосудов
    for i in (100+i for i in range(1, 100)):
        yield i


def search_anv(lst):
    ans, f1, avg = [], False, sum(lst)/len(lst)
    for i, el in enumerate(lst):
        if el > avg:
            if not f1:
                begin, f1 = i, True
        elif f1 and el < avg:
            end, f1 = i-1, False
            ans += [[begin, end]]
    return ans


def search_vessels(m, x, y, z, code, borders, chcode):
    '''
    :param m: матрица в которой выполняется поиск
    :param x: координата по оси х
    :param y: координата по оси у
    :param z: координата по оси z
    :param code: код на который меняеются коды ячеек
    :param borders: границы обхода
    :param chcode: код который заменяется на заданный
    обходит систему сосудов, размечает принадлежащие ему ячейки соответствующиим кодом
    '''
    queue = [(z, y, x)]
    while queue:
        z1, y1, x1 = queue[0]
        del queue[0]
        if m[z1][y1][x1] == chcode:
            m[z1][y1][x1] = code
            if code != -1:
                vessels_systems[code]['l'][z1] += 1
                vessels_systems[code]['point'][z1] = [x1, y1, z1]
            for c in range(-1, 2):
                for b in range(-1, 2):
                    for a in range(-1, 2):
                        if borders['x_min'] <= x1 + a <= borders['x_max'] and borders['y_min'] <= y1 + b <= borders[
                            'y_max'] and \
                                borders['z_min'] <= z1 + c <= borders['z_max'] and m[z1 + c][y1 + b][x1 + a] == chcode:
                            queue += [(z1 + c, y1 + b, x1 + a)]


def analysis(m, gen):
    for z in range(len(m)):
        for y in range(len(m[z])):
            for x in range(len(m[z][y])):
                if m[z][y][x] == 2:
                    code = next(gen, None)
                    vessels_systems[code] = {'l': [0 for _ in range(len(m))],
                                             'point': [0 for _ in range(len(m))]}
                    borders = {'x_min': 0, 'y_min': 0, 'z_min': 0, 'x_max': len(m[0][0])-1, 'y_max': len(m[0])-1,
                               'z_max': len(m)-1}
                    search_vessels(m, x, y, z, code, borders, 2)


def border(m):
    for z in range(len(m)):
        for y in range(len(m[z])):
            for x in range(len(m[z][y])):
                if m[z][y][x] == 1:
                    near = []
                    for a in range(-1, 2):
                        for b in range(-1, 2):
                            for c in range(-1, 2):
                                if 0 <= x+a < len(m[z][y]) and 0 <= y+b < len(m[z]) and 0 <= z+c < len(m):
                                    near += [m[z+c][y+b][x+a]]
                    if 0 in near:
                        m[z][y][x] = 2


matrix = []
with open('res.csv', newline='') as f:
    reader = csv.reader(f)
    k = 0
    s = []
    for row in reader:
        line = [int(i) for i in row[0] if i.isdigit()]
        s += [line]
        k += 1
        if k == 850:
            matrix += [s]
            k = 0
            s = []
number_generator = nums_gen()
vessels_systems = {}
border(matrix)
analysis(matrix, number_generator)
for id in vessels_systems:
    anv = search_anv(vessels_systems[id]['l'])
    for elem in anv:
        border = {'x_min': 0, 'y_min': 0, 'z_min': elem[0], 'x_max': len(matrix[0][0])-1, 'y_max': len(matrix[0])-1,
                  'z_max': elem[1]}
        x, y, z = vessels_systems[id]['point'][elem[0]]
        search_vessels(matrix, x, y, z, -1, border, id)
fig = plt.figure(figsize=(11, 11))
ax = Axes3D(fig)
colors = {1: 'red', 2: 'black', -1: 'black', 101: 'red', 102: 'red', 103: 'red', 104: 'red', 105: 'red'}
for k in range(len(matrix)):
    for j in range(380, 460):
        for i in range(420, 500):
            if matrix[k][j][i] in colors:
                ax.scatter(i, j, k, s=0.5, c=colors[matrix[k][j][i]])
ax.set_xlabel('X Label')
ax.set_ylabel('Y Label')
ax.set_zlabel('Z Label')
plt.xlim([300, 500])
plt.ylim([300, 500])
plt.show()
