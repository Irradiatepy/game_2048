# -*- coding:utf-8 -*-
"""
在上一版本的基础上美化了游戏的界面，游戏时删除了游标，支持vim键和箭头以及修改了部分代码
还可以添加的东西：
    使用文件比如pickle文件来保存游戏分数
    添加游戏失败功能，当所有方向都无法移动（在所有格都被填满的情况下）时告诉玩家失败了
"""
from __future__ import print_function
import atexit
from colorama import init, Fore, Style
import keypress
import random
import copy
import os
import sys

init(autoreset=True)  # 设置autoreset后变色效果只对当前输出有作用，输出后，颜色恢复成默认值

_SIZE = 4
score = 0

# 二维数组表示游戏方格
cells = [[0]*_SIZE for _ in xrange(_SIZE)]

# color dict
COLORS = {
    2:    Fore.GREEN,
    4:    Fore.LIGHTBLUE_EX,
    # 8:    Fore.CYAN + Style.BRIGHT,
    8:    Fore.BLUE + Style.BRIGHT,
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
    margins = {'left': 4, 'top': 4, 'bottom': 2}
    rg = xrange(_SIZE)
    left = ' ' * margins.get('left', 0)
    c = '\n'.join([left + ' '.join([getCellStr(y, x) for x in rg]) for y in rg])
    top = '\n' * margins.get('top', 0)
    bottom = '\n' * margins.get('bottom', 0)
    scores = ' \tScore: %5d\n' % (score)
    print(top + c.replace('\n', scores, 1) + bottom)


def clearScreen():
    """
    Clear the console
    """
    os.system('clear')


def hideCursor():
    """
    Hide the cursor. Don't forget to call ``showCursor`` to restore
    the normal shell behavior. This is a no-op if ``clear_screen`` is
    falsy.
    """
    sys.stdout.write('\033[?25l')


def showCursor():
    """
    Show the cursor.
    """
    sys.stdout.write('\033[?25h')


def initGame():
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
    if not cell:
        return '  .'
    else:
        str_cell = '%3d' % cell
        return str(COLORS.get(cell, Fore.GREEN) + str_cell + Style.RESET_ALL)


def cellZip(direction):
    if direction == 'down':
        for line in xrange(_SIZE):
            for row in xrange(_SIZE - 1, 0, -1):
                if not cells[row][line]:
                    cells[row][line], cells[row - 1][line] = cells[row - 1][line], 0
    elif direction == 'left':
        for line in xrange(_SIZE):
            for row in xrange(0, _SIZE - 1, 1):
                if not cells[line][row]:
                    cells[line][row], cells[line][row + 1] = cells[line][row + 1], 0
    elif direction == 'right':
        for line in xrange(_SIZE):
            for row in xrange(_SIZE - 1, 0, -1):
                if not cells[line][row]:
                    cells[line][row], cells[line][row - 1] = cells[line][row - 1], 0
    elif direction == 'up':
        for line in xrange(_SIZE):
            for row in xrange(0, _SIZE - 1, 1):
                if not cells[row][line]:
                    cells[row][line], cells[row + 1][line] = cells[row + 1][line], 0


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
    # 访问并修改全局变量需要使用global
    global score
    cellsZip(direction)
    if direction == 'down':
        for line in xrange(_SIZE):
            for row in xrange(_SIZE - 1, 0, -1):
                if cells[row - 1][line] == cells[row][line] != 0:
                    cells[row][line], cells[row - 1][line] = 2*cells[row][line], 0
                    score += cells[row][line]
    elif direction == 'left':
        for line in xrange(_SIZE):
            for row in xrange(0, _SIZE - 1, 1):
                if cells[line][row] == cells[line][row + 1] != 0:
                    cells[line][row], cells[line][row + 1] = 2*cells[line][row], 0
                    score += cells[line][row]
    elif direction == 'up':
        for line in xrange(_SIZE):
            for row in xrange(0, _SIZE - 1, 1):
                if cells[row][line] == cells[row + 1][line] != 0:
                    cells[row][line], cells[row + 1][line] = 2*cells[row][line], 0
                    score += cells[row][line]
    elif direction == 'right':
        for line in xrange(_SIZE):
            for row in xrange(_SIZE - 1, 0, -1):
                if cells[line][row] == cells[line][row - 1] != 0:
                    cells[line][row], cells[line][row - 1] = 2*cells[line][row], 0
                    score += cells[line][row]
    elif direction == 'quit':
        print('quit')
        sys.exit()
    cellsZip(direction)


def operation():
    op = keypress.getArrowKey()
    directions = {65:'up', 66:'down', 67:'right', 68:'left', 81:'quit', 113:'quit'}
    moveCells(direction=directions.get(op, 'wrong direction'))


def run():
    atexit.register(showCursor)  # This will run showCursor function to show the crusor when exit
    hideCursor()
    while True:
        clearScreen()
        display()
        old_cells = copy.deepcopy(cells)  # 必须使用深复制，否则两者变化会一致
        operation()
        if old_cells != cells:  # 如果方格有移动，则选择一个方格添加一个值
            addCell()


initGame()
print('Input：h(Left) j(Down) k(Up) l(Right) q(Quit) or HJKL or the arrow.')
run()










