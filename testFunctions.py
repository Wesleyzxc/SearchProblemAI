# -*- coding: utf-8 -*-
"""
Created on Sat Mar 30 21:16:36 2019

@author: n9972676
"""
from sokoban import * 
from search import *
import search
import math 

wh = Warehouse()

wh.load_warehouse("warehouses/warehouse_01.txt")
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

def rule1(warehouse_2d):
        for y in range(len(warehouse_2d) - 1):
            inside = False
            for x in range(len(warehouse_2d[0]) - 1):
                # move through row in warehouse until we hit first wall
                # means we are now inside the warehouse
                if not inside:
                    if warehouse_2d[y][x] == wall_square:
                        inside = True
                else:
                    # check if all the cells to the right of current cell are empty
                    # means we are now outside the warehouse
                    if all([cell == ' ' for cell in warehouse_2d[y][x:]]):
                        break
                    if warehouse_2d[y][x] not in target_squares:
                        if warehouse_2d[y][x] != wall_square:
                            if is_corner_cell(warehouse_2d, x, y):
                                warehouse_2d[y][x] = taboo_square
        return warehouse_2d
                            
def rule2(warehouse_2d):
        for y in range(1, len(warehouse_2d) - 1):
            for x in range(1, len(warehouse_2d[0]) - 1):
                if warehouse_2d[y][x] == taboo_square \
                        and is_corner_cell(warehouse_2d, x, y):
                    row = warehouse_2d[y][x + 1:]
                    col = [row[x] for row in warehouse_2d[y + 1:][:]]
                    # fill in taboo_cells in row to the right of corner taboo cell
                    for x2 in range(len(row)):
                        if row[x2] in target_squares or row[x2] == wall_square:
                            break
                        if row[x2] == taboo_square \
                                and is_corner_cell(warehouse_2d, x2 + x + 1, y):
                            if all([is_corner_cell(warehouse_2d, x3, y, 1)
                                    for x3 in range(x + 1, x2 + x + 1)]):
                                for x4 in range(x + 1, x2 + x + 1):
                                    warehouse_2d[y][x4] = 'X'
                    # fill in taboo_cells in column moving down from corner taboo
                    # cell
                    for y2 in range(len(col)):
                        if col[y2] in target_squares or col[y2] == wall_square:
                            break
                        if col[y2] == taboo_square \
                                and is_corner_cell(warehouse_2d, x, y2 + y + 1):
                            if all([is_corner_cell(warehouse_2d, x, y3, 1)
                                    for y3 in range(y + 1, y2 + y + 1)]):
                                for y4 in range(y + 1, y2 + y + 1):
                                    warehouse_2d[y4][x] = 'X'
        return warehouse_2d

class CanGoThereProblem(search.Problem):
    
    def __init__(self, initial, warehouse, goal=None):
        self.initial = initial
        self.goal = goal
        self.warehouse = warehouse
        
    '''cost = 1 for all'''
    def value(self, state):
        return 1 
    
    ''' all possible actions'''
    def actions(self, state):
        uprightleftdown = [(1,0), (0,1), (-1,0), (0,-1)]
        for validMove in uprightleftdown:
            newPos = (state[0] + validMove[0], state[1] + validMove[1])
            
            if newPos not in self.warehouse.walls:
                yield validMove
                
    '''resulting state after action'''
    def result(self, state, action):
        return (state[0] + action[0], state[1] + action[1])
    
def can_go_there(warehouse, dst):
    '''    
    Determine whether the worker can walk to the cell dst=(row,column) 
    without pushing any box.
    
    @param warehouse: a valid Warehouse object

    @return
      True if the worker can walk to cell dst=(row,column) without pushing any box
      False otherwise
    '''
    
    def heuristic(GoThereProblem):
        state = GoThereProblem.state
        # distance = sqrt(xdiff^2 + ydiff^2). Basic distance formula heuristic.
        return math.sqrt((math.pow(state[1] - dst[1], 2))
                         + (math.pow(state[0] - dst[0], 2)))

    dst = (dst[1], dst[0]) # flip it

    # Use an A* graph search on the FindPathProblem search
    node = astar_graph_search(CanGoThereProblem(warehouse.worker, warehouse, dst),
                       heuristic)
    return node is not None
    
def check_action_seq(warehouse, action_seq):
    '''
    
    Determine if the sequence of actions listed in 'action_seq' is legal or not.
    
    Important notes:
      - a legal sequence of actions does not necessarily solve the puzzle.
      - an action is legal even if it pushes a box onto a taboo cell.
        
    @param warehouse: a valid Warehouse object

    @param action_seq: a sequence of legal actions.
           For example, ['Left', 'Down', Down','Right', 'Up', 'Down']
           
    @return
        The string 'Failure', if one of the action was not successul.
           For example, if the agent tries to push two boxes at the same time,
                        or push one box into a wall.
        Otherwise, if all actions were successful, return                 
               A string representing the state of the puzzle after applying
               the sequence of actions.  This must be the same string as the
               string returned by the method  Warehouse.__str__()
    '''
    
    ##         "INSERT YOUR CODE HERE"
    actionDict = {'Down':(0,-1), 'Up':(0,1), 'Left':(-1,0), 'Right':(1,0)}
    print(actionDict)



taboo_Check = rule2((rule1(warehouse_2d)))
warehouse_str = '\n'.join([''.join(line) for line in taboo_Check])

# remove the remaining target_squares
for char in target_squares:
    warehouse_str = warehouse_str.replace(char, ' ')