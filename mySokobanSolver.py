
'''

    2019 CAB320 Sokoban assignment

The functions and classes defined in this module will be called by a marker script. 
You should complete the functions and classes according to their specified interfaces.

You are not allowed to change the defined interfaces.
That is, changing the formal parameters of a function will break the 
interface and triggers to a fail for the test of your code.
 
# by default does not allow push of boxes on taboo cells
SokobanPuzzle.allow_taboo_push = False 

# use elementary actions if self.macro == False
SokobanPuzzle.macro = False 

'''

# you have to use the 'search.py' file provided
# as your code will be tested with this specific file
import search
import sokoban
import math
from sokoban import * 
from search import *
import time
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def my_team():
    '''
    Return the list of the team members of this assignment submission as a list
    of triplet of the form (student_number, first_name, last_name)
    
    '''
    return [ (9972676, 'Wesley', 'Kok'), (9930141, 'Daryl', 'Tan')]

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def taboo_cells(warehouse):
    '''  
    Identify the taboo cells of a warehouse. A cell inside a warehouse is 
    called 'taboo' if whenever a box get pushed on such a cell then the puzzle 
    becomes unsolvable.  
    When determining the taboo cells, you must ignore all the existing boxes, 
    simply consider the walls and the target cells.  
    Use only the following two rules to determine the taboo cells;
     Rule 1: if a cell is a corner inside the warehouse and not a target, 
             then it is a taboo cell.
     Rule 2: all the cells between two corners inside the warehouse along a 
             wall are taboo if none of these cells is a target.
    
    @param warehouse: a Warehouse object

    @return
       A string representing the puzzle with only the wall cells marked with 
       an '#' and the taboo cells marked with an 'X'.  
       The returned string should NOT have marks for the worker, the targets,
       and the boxes.  
    '''
    ##         "INSERT YOUR CODE HERE"    
    signsNotNeeded = ['@', '$'] # character and box symbol
    targetSquares = ['!', '.', '*'] # Player on goal, empty goal, and box on goal symbol
    wall = '#'
    taboo = 'X'

    def check_corner_square(warehouse, x, y, alongWall=0):
        walls_above_below = 0
        walls_left_right = 0
        # check for walls above and below
        for (dx, dy) in [(0, -1), (0, 1)]:
            if warehouse[y + dy][x + dx] == wall:
                walls_above_below += 1
        # check for walls left and right
        for (dx, dy) in [(-1, 0), (1, 0)]:
            if warehouse[y + dy][x + dx] == wall:
                walls_left_right += 1
        if alongWall:
            return (walls_above_below >= 1) or (walls_left_right >= 1)
        else:
            return (walls_above_below >= 1) and (walls_left_right >= 1)
    
    #Turn warehouse into 2d array y(row),x(col)
    #   0 1 2 3 
    #   1
    #   2
    #   3
    warehouseStr = str(warehouse)
    #Remove boxes and player
    for char in signsNotNeeded:
        warehouseStr = warehouseStr.replace(char, ' ')
        
    warehouse_2d = [list(row) for row in warehouseStr.split('\n')]
    """ 2d array is jagged, """
    
    ''' rule 1 function '''
    def rule1(warehouse_2d):
        for y in range(len(warehouse_2d) - 1):
            inside = False
            for x in range(len(warehouse_2d[0]) - 1):
                # inside when loop hits the first wall
                
                if not inside:
                    if warehouse_2d[y][x] == wall:
                        inside = True
                        #print("Inside") #working correctly
                else:
                    # check if cell from x:end is empty
                    if all([cell == ' ' for cell in warehouse_2d[y][x:]]):
                        break
                    # only changes if its an empty square, then check if corner
                    if warehouse_2d[y][x] not in targetSquares:
                        if warehouse_2d[y][x] != wall:
                            if check_corner_square(warehouse_2d, x, y):
                                warehouse_2d[y][x] = taboo
        return warehouse_2d
        
        
    def rule2(warehouse_2d):
        for y in range(1, len(warehouse_2d)-1):
            for x in range(1, len(warehouse_2d[0]) - 1):
                if warehouse_2d[y][x] == taboo and check_corner_square(warehouse_2d, x, y):
                    currentRow = warehouse_2d[y][x+1:]
                    currentColumn = [eachRow[x] for eachRow in warehouse_2d[y + 1:]]
                
                    
                    # to check across left to right
                    for nextSquare in range(len(currentRow)):
                        #if any of the do not touch symbols
                        if currentRow[nextSquare] in targetSquares or currentRow[nextSquare] == wall:
                            break 
                        
                        if currentRow[nextSquare] == taboo and check_corner_square(warehouse_2d, x + nextSquare + 1, y):
                            if all([check_corner_square(warehouse_2d, nextNextSquare, y, 1)
                                    for nextNextSquare in range(x+1, nextSquare + x + 1)]):
                                for edgeSquares in range(x+1, nextSquare + x + 1):
                                    warehouse_2d[y][edgeSquares] = taboo
                    # to check up and down
                    for nextSquareY in range(len(currentColumn)):
                        if currentColumn[nextSquareY] in targetSquares or currentColumn[nextSquareY] == wall:
                            break
                        
                        if currentColumn[nextSquareY] == taboo and check_corner_square(warehouse_2d, x, nextSquareY + y + 1):
                            if all([check_corner_square(warehouse_2d, x, nextNextSquareY, 1)
                                    for nextNextSquareY in range(y + 1, nextSquareY + y + 1)]):
                                for edgeSquaresY in range(y + 1, nextSquareY + y + 1):
                                    warehouse_2d[edgeSquaresY][x] = taboo
        return warehouse_2d
                    
    warehouse_2d = rule2(rule1(warehouse_2d)) #Tested working
    
    #Convert 2D array back into string
    warehouse_taboo = '\n'.join([''.join(line) for line in warehouse_2d])
    #Remove target square symbols
    for char in targetSquares:
        warehouse_taboo = warehouse_taboo.replace(char, ' ')
        
    
    return warehouse_taboo

            
    
    


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


class SokobanPuzzle(search.Problem):
    '''
    An instance of the class 'SokobanPuzzle' represents a Sokoban puzzle.
    An instance contains information about the walls, the targets, the boxes
    and the worker.

    Your implementation should be fully compatible with the search functions of 
    the provided module 'search.py'. 
    
    Each instance should have at least the following attributes
    - self.allow_taboo_push
    - self.macro
    
    When self.allow_taboo_push is set to True, the 'actions' function should 
    return all possible legal moves including those that move a box on a taboo 
    cell. If self.allow_taboo_push is set to False, those moves should not be
    included in the returned list of actions.
    
    If self.macro is set True, the 'actions' function should return 
    macro actions. If self.macro is set False, the 'actions' function should 
    return elementary actions.
        
    '''
    #
    #         "INSERT YOUR CODE HERE"
    #
    #     Revisit the sliding puzzle and the pancake puzzle for inspiration!
    #
    #     Note that you will need to add several functions to 
    #     complete this class. For example, a 'result' function is needed
    #     to satisfy the interface of 'search.Problem'.
    
    
    
    def __init__(self, warehouse, allow_taboo_push, macro):
        if allow_taboo_push is None:
            self.allow_taboo_push = True
        if macro is None:
            self.macro = True
        if (not self.allow_taboo_push):
            taboo_str = taboo_cells(warehouse)
            self.taboo = [list(row) for row in taboo_str.split('\n')]
    
    def is_box(resultX,resultY):
        return ((resultX, resultY) in warehouse.boxes)
    
    def is_box_taboo(self,resultX,resultY,coordX,coordY):
        boxResultX = resultX + coordX
        boxResultY = resultY + coordY
        return (self.taboo[boxResultY][boxResultX] == "X")
        
    def actions(self, state):
        validActions = []
        actionDict = {'Up':(0,-1), 'Down':(0,1), 'Left':(-1,0), 'Right':(1,0)}
        
        if (self.allow_taboo_push):
            for names, coords in actionDict.items():
                resultX = state.worker[0] + coords[0]
                resultY = state.worker[1] + coords[1]
                if (can_go_there(state, (resultY,resultX))): #going to empty space is valid action
                    validActions.append(names)
                elif (is_box(resultX,resultY)): #pushing box is valid action
                    validActions.append(names)
        else:
            for names, coords in actionDict.items():
                resultX = state.worker[0] + coords[0]
                resultY = state.worker[1] + coords[1]
                ##is_taboo = (taboo_str[y][])
                if (is_box(resultX,resultY)):
                    if (not is_box_taboo(resultX,resultY,coords[0],coords[1])):
                        validActions.append(names)
                elif (can_go_there(state, (resultY,resultX))):
                    validActions.append(names)
                    
        return validActions
    
    #def result(self, state, action):
            
        """
        Return the list of actions that can be executed in the given state.
        
        As specified in the header comment of this class, the attributes
        'self.allow_taboo_push' and 'self.macro' should be tested to determine
        what type of list of actions is to be returned.
        """
        
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

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
    failedSeq = 'Failure'
    ##         "INSERT YOUR CODE HERE"
    actionDict = {'Up':(0,-1), 'Down':(0,1), 'Left':(-1,0), 'Right':(1,0)}
    
    for actions in action_seq:
        currentPos = warehouse.worker
        if actions in actionDict.keys():
            # coords of worker after actions
            resultX = currentPos[0] + actionDict.get(actions)[0]
            resultY = currentPos[1] + actionDict.get(actions)[1]
             
            if (resultX, resultY) in warehouse.walls: 
                 #NOT OPTIMISED - loops through walls everytime.
                 #Alternative - load warehouse_2d once,  if (warehouse_2d(resultX,resultY) == "#")
                 
                 
                 # cannot move there since it's a wall
                return failedSeq
            
            elif (resultX, resultY) in warehouse.boxes:
                # coords of box after actions
                boxResultX = resultX + actionDict.get(actions)[0] 
                boxResultY = resultY + actionDict.get(actions)[1]
                 
                # if moved box is wall/ another box
                if (boxResultX, boxResultY) in warehouse.walls or (boxResultX,boxResultY) in warehouse.boxes:
                    #NOT OPTIMISED - loops through walls everytime.
                    #Alternative - load warehouse_2d once,  if (warehouse_2d(resultX,resultY) == "#")
                    
                    return failedSeq
                 
                # successful, commit changes to coords
                else:
                    warehouse.boxes.remove(resultX, resultY)
                    warehouse.boxes.append(boxResultX, boxResultY)
                    warehouse.worker = (resultX, resultY)
                    print(warehouse.worker) # CAN DELETE REMEMBER TO DELETE
                     
            else:
                warehouse.worker = (resultX, resultY)
                print(warehouse.worker) # CAN DELETE REMEMBER TO DELETE
                
    return str(warehouse)
        

            

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def solve_sokoban_elem(warehouse):
    '''    
    This function should solve using elementary actions 
    the puzzle defined in a file.
    
    @param warehouse: a valid Warehouse object

    @return
        If puzzle cannot be solved return the string 'Impossible'
        If a solution was found, return a list of elementary actions that solves
            the given puzzle coded with 'Left', 'Right', 'Up', 'Down'
            For example, ['Left', 'Down', Down','Right', 'Up', 'Down']
            If the puzzle is already in a goal state, simply return []
    '''
    
    ##         "INSERT YOUR CODE HERE"
    
    raise NotImplementedError()

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class CanGoThereProblem(search.Problem):
    
    def __init__(self, initial, warehouse, goal=None):
        self.initial = initial
        self.goal = goal
        self.warehouse = warehouse
        
    '''cost = 1 for all Daryl - pancake used astar but no value?'''
    def value(self, state):
        return 1 
    
    ''' all possible actions'''
    def actions(self, state):
        uprightleftdown = [(1,0), (0,1), (-1,0), (0,-1)]
        for validMove in uprightleftdown:
            newPos = (state[0] + validMove[0], state[1] + validMove[1])
            
            if newPos not in self.warehouse.walls:
                if newPos not in self.warehouse.boxes:
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
        # distance = sqrt(xdist^2 + ydist^2). Basic distance formula heuristic.
        return math.sqrt((math.pow(state[1] - dst[1], 2)) + (math.pow(state[0] - dst[0], 2)))

    dst = (dst[1], dst[0]) # flip it

    # Use an A* graph search on the CanGoThereProblem search
    node = astar_graph_search(CanGoThereProblem(warehouse.worker, warehouse, dst),
                       heuristic)
    return node is not None
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def solve_sokoban_macro(warehouse):
    '''    
    Solve using macro actions the puzzle defined in the warehouse passed as
    a parameter. A sequence of macro actions should be 
    represented by a list M of the form
            [ ((r1,c1), a1), ((r2,c2), a2), ..., ((rn,cn), an) ]
    For example M = [ ((3,4),'Left') , ((5,2),'Up'), ((12,4),'Down') ] 
    means that the worker first goes the box at row 3 and column 4 and pushes it left,
    then goes to the box at row 5 and column 2 and pushes it up, and finally
    goes the box at row 12 and column 4 and pushes it down.
    
    @param warehouse: a valid Warehouse object

    @return
        If puzzle cannot be solved return the string 'Impossible'
        Otherwise return M a sequence of macro actions that solves the puzzle.
        If the puzzle is already in a goal state, simply return []
    '''
    
    ##         "INSERT YOUR CODE HERE"
    
    raise NotImplementedError()

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


# TESTING OF FUNCTION DIRECTLY ON THIS FILE CAN DELETE AFTER
wh = Warehouse()
wh.load_warehouse("warehouses/warehouse_01.txt")
#puzzle = SokobanPuzzle(wh, None, None)
#


taboo_cells(wh)
#t0 = time.time()
#test_checkaction = check_action_seq(wh, ['Up', 'Left', 'Up'])
#
#t1 = time.time()
#
#print ("Solver took ",t1-t0, ' seconds')