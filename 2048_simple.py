# -*- coding:utf-8 -*-
"""
初步实现2048，支持asdw键
缺陷：
    在不能移动时仍然可以出现新的数字。
    在某些情况会出现移动错误，如［ 4    4    0    4］向左移动，会出现［4    8    0    0］的结果
"""
from __future__ import print_function
import random
import sys


_SIZE = 4
# print([[0]*4 for _ in xrange(4)])
cells = [[0]*_SIZE for _ in xrange(_SIZE)]


def display():
    """
    Display the game
    """
    for i in xrange(_SIZE):
        print('{0:4} {1:4} {2:4} {3:4}'.format(cells[i][0], cells[i][1], cells[i][2], cells[i][3]))


def init():
    """
    Initiate the game
    """
    addCell()
    addCell()


def getEmptyCells():
    return [(x,y) for x in xrange(_SIZE) for y in xrange(_SIZE) if getCell(x, y) == 0]


def addCell(value=None, choice=([2]*9 + [4])):
    if value:
        choice = [value]

    v = random.choice(choice)
    empty = getEmptyCells()
    if empty:
        x, y = random.choice(empty)
        setCell(x, y, v)


def setCell(x, y, value):
    cells[x][y] = value


def getCell(x, y):
    return cells[x][y]


def merge(d):
    if d == 'down':
        for line in xrange(_SIZE):
            for row in xrange(0, 3, 1):
                if cells[row][line] == cells[row + 1][line] != 0:
                    cells[row + 1][line] *= 2
                    cells[row][line] = 0
                elif cells[row + 1][line] == 0:
                    cells[row + 1][line] = cells[row][line]
                    cells[row][line] = 0
    elif d == 'left':
        for line in xrange(_SIZE):
            for row in xrange(3, 0, -1):
                if cells[line][row] == cells[line][row - 1] != 0:
                    cells[line][row - 1] *= 2
                    cells[line][row] = 0
                elif cells[line][row - 1] == 0:
                    cells[line][row - 1] = cells[line][row]
                    cells[line][row] = 0
    elif d == 'up':
        for line in xrange(_SIZE):
            for row in xrange(3, 0, -1):
                if cells[row][line] == cells[row - 1][line] != 0:
                    cells[row - 1][line] *= 2
                    cells[row][line] = 0
                elif cells[row - 1][line] == 0:
                    cells[row - 1][line] = cells[row][line]
                    cells[row][line] = 0
    elif d == 'right':
        for line in xrange(_SIZE):
            for row in xrange(0, 3, 1):
                if cells[line][row] == cells[line][row + 1] != 0:
                    cells[line][row + 1] *= 2
                    cells[line][row] = 0
                elif cells[line][row + 1] == 0:
                    cells[line][row + 1] = cells[line][row]
                    cells[line][row] = 0


def operation():
    op = raw_input('Operator:')
    if op in ['a', 'A']:
        merge(d='left')
    elif op in ['d', 'D']:
        merge(d='right')
    elif op in ['w', 'W']:
        merge(d='up')
    elif op in ['s', 'S']:
        merge(d='down')
    elif op in ['q', 'Q']:
        print ('quit')
        sys.exit()


def run():
    while True:
        display()
        operation()
        addCell()


init()
print('Input：W(Up) S(Down) A(Left) D(Right), Q(Quit)')
run()










