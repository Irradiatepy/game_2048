# -*- coding: UTF-8 -*-
"""
这是一段键盘输入的代码，可以得到输入的字符的Ascii码值
绑定了VIM中的hjkl键，和键盘中的上下左右箭头。(支持大小写字母)
即键入h或左箭头，返回68；
键入l或右箭头，返回67；
键入k或上箭头，返回65；
键入j或下箭头，返回66
"""
# Common values

# Space Bar key to pause the game
SPACE = 32

# Vim keys
K, J, L, H = 74, 75, 76, 72
k, j, l, h = 107, 106, 108, 104

try:
    # termios只在Unix下运行
    import termios
except ImportError:
    # Windows

    import msvcrt

    UP, DOWN, RIGHT, LEFT = 72, 80, 77, 75

    __key_aliases = {
        K: UP,
        J: DOWN,
        L: RIGHT,
        H: LEFT,
        h: LEFT,
        k: UP,
        j: DOWN,
        l: RIGHT,
    }

    def getKey():
        while True:
            if msvcrt.kbhit():
                a = ord(msvcrt.getch())
                return __key_aliases.get(a, a)

else:
    # Linux/OSX

    # refs:
    # http://bytes.com/topic/python/answers/630206-check-keypress-linux-xterm
    # http://stackoverflow.com/a/2521032/735926
    import sys
    import tty

    __fd = sys.stdin.fileno()
    __old = termios.tcgetattr(__fd)

    # Arrow keys
    # they are preceded by 27 and 91, hence the double 'if' in getKey.
    UP, DOWN, RIGHT, LEFT = 65, 66, 67, 68

    __key_aliases = {
        K: UP,
        J: DOWN,
        L: RIGHT,
        H: LEFT,
        h: LEFT,
        k: UP,
        j: DOWN,
        l: RIGHT,
    }

    def __getKey():
        """Return a key pressed by the user"""
        try:
            tty.setcbreak(sys.stdin.fileno())
            termios.tcflush(sys.stdin, termios.TCIOFLUSH)
            ch = sys.stdin.read(1)
            return ord(ch) if ch else None
        finally:
            termios.tcsetattr(__fd, termios.TCSADRAIN, __old)

    def getKey():
        """
        same as __getKey, but handle arrow keys
        """
        k = __getKey()
        if k == 27:
            k = __getKey()
            if k == 91:
                k = __getKey()

        return __key_aliases.get(k, k)

# legacy support
getArrowKey = getKey
print getArrowKey()
