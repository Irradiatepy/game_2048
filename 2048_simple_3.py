# -*- coding:utf-8 -*-
"""
在上一版本的基础上，利用了colorama模块，实现了在命令行显示时不同的数字能显示成不同的颜色
"""
from __future__ import print_function
# from atexit
from colorama import init, Fore, Style
import random
import copy
import sys

init(autoreset=True)

_SIZE = 4
score = 0

# 二维数组表示游戏方格
cells = [[0]*_SIZE for _ in xrange(_SIZE)]
COLORS = {
    2:    Fore.GREEN,
    4:    Fore.BLUE + Style.BRIGHT,
    8:    Fore.CYAN,
    16:   Fore.RED,
    32:   Fore.MAGENTA,
    64:   Fore.CYAN,
    128:  Fore.BLUE + Style.BRIGHT,
    256:  Fore.MAGENTA,
    512:  Fore.GREEN,
    1024: Fore.RED,
    2048: Fore.YELLOW,
    # just in case people set an higher goal they still have colors
    4096: Fore.RED,
    8192: Fore.CYAN,
}


def display():
    margins = {'left': 4, 'top': 4, 'bottom': 4}
    rg = xrange(_SIZE)
    left = ' ' * margins.get('left', 0)
    c = '\n'.join([left + ' '.join([getCellStr(y, x) for x in rg]) for y in rg])
    print(c)
    print ('Total score: %s' % score)


def init():
    """
    Initiate the game.
    初始化游戏，初始方格中有两个值
    """
    addCell()
    addCell()


def getEmptyCells():
    """
    Get the empty cells list.
    得到非空方格数组
    """
    return [(x,y) for x in xrange(_SIZE) for y in xrange(_SIZE) if getCell(x, y) == 0]


def addCell():
    """
    Choice a empty cell and place one value.
    随机选择一个空格并放入一个随机值（从[2, 2, 2, 2, 2, 2, 2, 2, 2, 4]选取）
    """
    v = random.choice([2]*9 + [4])
    empty = getEmptyCells()
    if empty:
        x, y = random.choice(empty)
        setCell(x, y, v)


def setCell(x, y, value):
    cells[x][y] = value


def getCell(x, y):
    return cells[x][y]


def getCellStr(x, y):
    cell = getCell(x, y)
    if cell == 0:
        return '  .'
    else:
        str_cell = '%3d' % cell
        return str(COLORS.get(cell, Fore.GREEN) + str_cell + Style.RESET_ALL)


def cellZip(direction):
    if direction == 'down':
        for line in xrange(_SIZE):
            for row in xrange(3, 0, -1):
                if cells[row][line] == 0:
                    cells[row][line] = cells[row - 1][line]
                    cells[row - 1][line] = 0
    elif direction == 'left':
        for line in xrange(_SIZE):
            for row in xrange(0, 3, 1):
                if cells[line][row] == 0:
                    cells[line][row] = cells[line][row + 1]
                    cells[line][row + 1] = 0
    elif direction == 'right':
        for line in xrange(_SIZE):
            for row in xrange(3, 0, -1):
                if cells[line][row] == 0:
                    cells[line][row] = cells[line][row - 1]
                    cells[line][row - 1] = 0
    elif direction == 'up':
        for line in xrange(_SIZE):
            for row in xrange(0, 3, 1):
                if cells[row][line] == 0:
                    cells[row][line] = cells[row + 1][line]
                    cells[row + 1][line] = 0


def cellsZip(direction):
    """
    Compress the cells according to the direction.
    依据给定的方向进行方格的压缩，如某行为[2, 0, 0, 2]，向左压缩，结果为[2, 2, 0, 0]
    """
    cellZip(direction)
    cellZip(direction)


def moveCells(direction):
    """
    Merge the cell according to the direction.
    依据给定的方向进行方格的移动。
    """
    global score
    cellsZip(direction)
    if direction == 'down':
        for line in xrange(_SIZE):
            for row in xrange(3, 0, -1):
                if cells[row - 1][line] == cells[row][line] != 0:
                    cells[row][line] *= 2
                    score += cells[row][line]
                    cells[row - 1][line] = 0
    elif direction == 'left':
        for line in xrange(_SIZE):
            for row in xrange(0, 3, 1):
                if cells[line][row] == cells[line][row + 1] != 0:
                    cells[line][row] *= 2
                    score += cells[line][row]
                    cells[line][row + 1] = 0
    elif direction == 'up':
        for line in xrange(_SIZE):
            for row in xrange(0, 3, 1):
                if cells[row][line] == cells[row + 1][line] != 0:
                    cells[row][line] *= 2
                    score += cells[row][line]
                    cells[row + 1][line] = 0
    elif direction == 'right':
        for line in xrange(_SIZE):
            for row in xrange(3, 0, -1):
                if cells[line][row] == cells[line][row - 1] != 0:
                    cells[line][row] *= 2
                    score += cells[line][row]
                    cells[line][row - 1] = 0
    cellsZip(direction)


def operation():
    op = raw_input('Operator:')
    if op in ['a', 'A']:
        moveCells(direction='left')
    elif op in ['direction', 'D']:
        moveCells(direction='right')
    elif op in ['w', 'W']:
        moveCells(direction='up')
    elif op in ['s', 'S']:
        moveCells(direction='down')
    elif op in ['q', 'Q']:
        print ('quit')
        sys.exit()


def run():
    while True:
        display()
        old_cells = copy.deepcopy(cells)  # 必须使用深复制，否则两者变化会一致
        operation()
        if old_cells != cells:  # 如果方格有移动，则选择一个方格添加一个值
            addCell()


init()
print('Input：W(Up) S(Down) A(Left) D(Right) Q(Quit)')
run()










