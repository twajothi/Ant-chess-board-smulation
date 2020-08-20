# This is a sample Python script.
import random

import numpy as np
from scipy import stats

"""
*Two ants start in opposite corners of a regular chessboard.
  Every 10 seconds, they move from the center of the square they're on to the
  center of an adjacent square. How long until they both land on the same
  square? How long until their paths cross (Ant A moving from square K to L and
  Ant B moving from square L to K)? What happens if we allow the ants to move
  diagonally? What happens if we restrict ants from moving to their immediately
 previous square?
"""

""""
Note : 
* the ants are randomly moving
Chess board can be considered an 8x8 matrix which is defined by  {row,col} coordinates,
* Ant must always move to the new square. 
 
* corner point : 
{0,0} is the top left corner 
{0,7} is the top right corner 
{7,0} is the bottom left corner
{7,7} is the bottom right corner 

"""

"""
Approach run a simulation for all possible moves and find the averages and STD
"""


class Point:
    def __init__(self, row: int, col: int):
        self.row = row
        self.col = col

    def set(self, point):
        self.row = point.row
        self.col = point.col

    def set(self, newrow, newcol):
        self.row = newrow
        self.col = newcol

    def incr(self, offset):
        Point.row = self.row + offset.row
        Point.col = self.col + offset.col

    def __eq__(self, other):
        return isinstance(other, Point) and \
               other.col == self.col and other.row == self.row

    def __str__(self):
        return '{' + str(self.row) + "," + str(self.col) + "}"

    def equals(self, other):
        if self == other:
            return True
        if other is None:
            return False


"""  
Ant has a current position and a last position. the last position exits so 
that we can determine if the ant path cross and to avoid moving to the previous
position if that is what is being simulate. 

"""


class Ant:

    def __init__(self, startRow, startCol):
        self.current = Point(startRow, startCol)
        self.last = Point(None, None)

    def __eq__(self, other):
        return self.current.row == other.current.row and self.current.col == other.current.col

    def newPos(self, newrow, newcol):
        if self.last.col is None and self.last.row is None:
            self.last = Point(0, 0)
        self.last.set(self.current.row, self.current.col)
        self.current.set(newrow, newcol)
        return self

    def collide(self, other):
        return self.current == other.current

    def equalLast(self, newRow, newCol):
        eqLast = False
        if self.last.col is not None and self.last.row is not None:
            eqLast = (self.last.row == newRow and self.last.col == newCol)
        return eqLast

    def pathsCross(self, AntB):
        crossed = False
        if self.last is not None and AntB.last is not None:
            crossed = (self.current == AntB.last and AntB.current == self.last)
        return crossed


global middle, Col_MAX, Row_MAX
middle = [Point(0, -1), Point(-1, 0),
          Point(0, 1), Point(1, 0), Point(-1, -1),
          Point(-1, 1), Point(1, 1), Point(1, -1)]
Col_MAX = 7
Row_MAX = 7


def getMoveOffset(p, diag=True):
    Point.offset = Point(None, None)
    while Point.offset.col is None and Point.offset.row is None:

        if diag:
            ix = random.randint(0, 7)
        else:
            ix = random.randint(0, 3)
        global middle
        Point.t = middle[ix]
        newRow = p.row + Point.t.row
        newCol = p.col + Point.t.col
        if 0 <= newRow <= Row_MAX and 0 <= newCol <= Col_MAX:
            Point.offset = Point.t
    return Point.offset


def makeMove(ant):
    Ant.ant = ant
    Point.point = Ant.ant.current
    newRow = 0
    newCol = 0
    Point.offset = getMoveOffset(Point.point)
    newRow = Point.point.row + Point.offset.row
    newCol = Point.point.row + Point.offset.col
    Ant.result = Ant.ant.newPos(newRow, newCol)

    return Ant.result


def antcollision():
    global Row_MAX
    global Col_MAX
    moves = 0
    Ant.antA = Ant(0, 0)
    Ant.antB = Ant(Row_MAX, Col_MAX)

    while not Ant.antA.collide(Ant.antB):
        Ant.antA = makeMove(Ant.antA)
        Ant.antB = makeMove(Ant.antB)
        moves += 1
    return moves


def calculate(maxIter, flag):

    collisionTimes = [0] * maxIter
    for i in range(0, maxIter):
        move = antcollision()
        collisionTimes[i] = move * 10  # multiply by 10 to get time
    mean = np.mean(collisionTimes)
    std = np.std(collisionTimes)
    stdError = stats.sem(collisionTimes)

    print(" iterations used : " + str(maxIter) + " iter")
    print(" ")
    print("values in seconds for every 10 seconds move ")
    if flag:
        print(" Collision with non diagnal : ")
    else:
        print(" Collision with diagnal : ")

    print('mean of simulation is ' + str(mean))
    print('std of simulation is ' + str(std))
    print('std Error of simmulation is ' + str(stdError))


if __name__ == '__main__':
    maxIter = 1000000
    random.seed(350)
    collisionTimes = [0] * maxIter
    calculate(maxIter, True)
    calculate(maxIter, False)




