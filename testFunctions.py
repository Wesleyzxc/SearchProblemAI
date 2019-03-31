# -*- coding: utf-8 -*-
"""
Created on Sat Mar 30 21:16:36 2019

@author: n9972676
"""
from sokoban import * 

wh = Warehouse()

wh.load_warehouse("warehouses/warehouse_203.txt")
warehouse_2d = [list(row) for row in str(wh).split('\n')]

squares_to_remove = ['$', '@']
target_squares = ['.', '!', '*']
wall_square = '#'
taboo_square = 'X'


def is_corner_cell(warehouse, x, y, wall=0):
    """
    cell is in a corner if there is at least 1 wall above/below
    and at least one wall left/right...
    """
    num_ud_walls = 0
    num_lr_walls = 0
    # check for walls above and below
    for (dx, dy) in [(0, 1), (0, -1)]:
        if warehouse[y + dy][x + dx] == wall_square:
            num_ud_walls += 1
    # check for walls left and right
    for (dx, dy) in [(1, 0), (-1, 0)]:
        if warehouse[y + dy][x + dx] == wall_square:
            num_lr_walls += 1
    if wall:
        return (num_ud_walls >= 1) or (num_lr_walls >= 1)
    else:
        return (num_ud_walls >= 1) and (num_lr_walls >= 1)
    
    
    ''' function to find length of the wall so we can alternate inside outside'''
def wallLength(row, startX = 0):
    testnum = 0
    for x in row[startX:]:
        #print(x)
        print(row[row.index(x)+1])
        if (x == '#' and row[row.index(x)+1] == '#'):
            testnum = testnum + 1
        elif x == " " and row.index(x) != startX:
            return testnum
    return testnum
            
''' ray tracing function '''
def checkInside(warehouse):
    newArray = []
    for i in range(len(warehouse)):
        newArray.append([])
        
    for y in range(len(warehouse)):
        inside = False
        for x in range(len(warehouse[0])):
            newVal = warehouse[y][x]
            """ ignoring first and last row 
            of warehouse to be considered
            then becomes inside once it reaches wall"""
            if all([cell == ' ' for cell in warehouse[y][x:]]): # whole row empty, means outside warehouse
                    break
                
            if x != len(warehouse[0])-1:
                if warehouse[y][x] == '#' and warehouse[y][x+1] == ' ':
                    inside = not inside
#            if x != len(warehouse[0])-1: 
#                if (not inside and (y != 0)  and  y != len(warehouse)-1) and x != len(warehouse[0])-1:
#                    if warehouse[y][x] == '#' and warehouse[y][x+1] == ' ':
#                        inside = not inside
                if warehouse[y][x] == " " and inside == True:
                    newVal = "I"
            else:
                if all([cell == ' ' for cell in warehouse[y][x:]]): # whole row empty, means outside warehouse
                    break
#            if x == "#" and oldX != x:
#                inside = not inside
            newArray[y].insert(x, newVal)
    return newArray


asd = checkInside(warehouse_2d)
testrow = ['#', '#', '#', ' ', ' ', '#', '#']
wallLength(testrow, 3)