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
    
    # Fixed signs that are used for clarity
    signsNotNeeded = ['@', '$']
    targetSquares = ['!', '.', '*']
    wall = '#'
    taboo = 'X'

    global actionDict
    actionDict = {'Up':(0,-1), 'Down':(0,1), 'Left':(-1,0), 'Right':(1,0)}
    
    def check_corner_square(warehouse, x, y, alongWall= False):
        walls_above_below = 0
        walls_left_right = 0
        # check for walls above and below
        for (dx, dy) in [actionDict['Up'], actionDict['Down']]:
            if warehouse[y + dy][x + dx] == wall:
                walls_above_below += 1
        # check for walls left and right
        for (dx, dy) in [actionDict['Left'], actionDict['Right']]:
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
    
    
    # Function to fulfil rule 1
    def rule1(warehouse_2d):
        for y in range(len(warehouse_2d) - 1):
            inside = False
            for x in range(len(warehouse_2d[0]) - 1):
                # inside when loop hits the first wall
                
                if not inside:
                    if warehouse_2d[y][x] == wall:
                        inside = True
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
        
    # function to fulfil rule 2
    def rule2(warehouse_2d):
        for y in range(1, len(warehouse_2d)-1):
            for x in range(1, len(warehouse_2d[0]) - 1):
                if warehouse_2d[y][x] == taboo and check_corner_square(warehouse_2d, x, y):
                    currentRow = warehouse_2d[y][x+1:]
                    currentColumn = [eachRow[x] for eachRow in warehouse_2d[y + 1:]]
                
                    
                    # to check cells across left to right 
                    for nextSquare in range(len(currentRow)):
                        #if any of the do not touch symbols
                        if currentRow[nextSquare] in targetSquares or currentRow[nextSquare] == wall:
                            break 
                        
                        if currentRow[nextSquare] == taboo and check_corner_square(warehouse_2d, x + nextSquare + 1, y):
                            if all([check_corner_square(warehouse_2d, nextNextSquare, y, True)
                                    for nextNextSquare in range(x+1, nextSquare + x + 1)]):
                                for edgeSquares in range(x+1, nextSquare + x + 1):
                                    warehouse_2d[y][edgeSquares] = taboo
                   
                    # to check cells up and down
                    for nextSquareY in range(len(currentColumn)):
                        if currentColumn[nextSquareY] in targetSquares or currentColumn[nextSquareY] == wall:
                            break
                        
                        if currentColumn[nextSquareY] == taboo and check_corner_square(warehouse_2d, x, nextSquareY + y + 1):
                            if all([check_corner_square(warehouse_2d, x, nextNextSquareY, True)
                                    for nextNextSquareY in range(y + 1, nextSquareY + y + 1)]):
                                for edgeSquaresY in range(y + 1, nextSquareY + y + 1):
                                    warehouse_2d[edgeSquaresY][x] = taboo
        return warehouse_2d
                    
    warehouse_2d = rule2(rule1(warehouse_2d))
    
    
    ### Converts back to string for sanity_check to pass
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

    global actionDict
    actionDict = {'Up':(0,-1), 'Down':(0,1), 'Left':(-1,0), 'Right':(1,0)}
    
    
    def __init__(self, warehouse, initial = None, goal = None, macro = False, allow_taboo_push = False):
        if initial == None:
            self.initial = str(warehouse)
        else:
            self.initial = initial
        
        # Goal string is initial string replaced with boxes removed and 
        # targets(.) replaced with boxes on target(*) 
        if goal == None:
            self.goal = str(warehouse).replace("$", " ").replace(".", "*").replace("!", "*")
        else:
            self.goal = goal
        self.macro = macro
        self.allow_taboo_push = allow_taboo_push
        self.taboo = [list(row) for row in taboo_cells(warehouse).split('\n')]

    def actions(self, state):
        """
        Return the list of actions that can be executed in the given state.
        
        As specified in the header comment of this class, the attributes
        'self.allow_taboo_push' and 'self.macro' should be tested to determine
        what type of list of actions is to be returned.
        """
        
        warehouseObject = Warehouse()
        warehouseObject.extract_locations(state.split(sep='\n'))
        
        validActions = []
        macroActions = []
        
        # Elementary actions
        if not self.macro:
            for names, coords in actionDict.items():
                # resulted coords from 1 single action
                resultX = warehouseObject.worker[0] + coords[0]
                resultY = warehouseObject.worker[1] + coords[1]
                
                #optimised
                # If next block is not a wall or a box, its a space
                if (resultX, resultY) not in warehouseObject.walls and (resultX, resultY) not in warehouseObject.boxes:
                    validActions.append(names)                   
                    
                # result of action is a box square
                elif((resultX, resultY) in warehouseObject.boxes):
                    boxX = resultX + coords[0]
                    boxY = resultY + coords[1]
                    
                    # can push box
                    if ((boxX, boxY) not in warehouseObject.boxes and (boxX, boxY) not in warehouseObject.walls):
                        # check taboo
                        if (self.allow_taboo_push): 
                            validActions.append(names)                
                        else:
                            if ((boxX, boxY) not in self.taboo):
                                validActions.append(names)

            return validActions
        
        # Macro actions
        if self.macro:
            for box in warehouseObject.boxes:
                for names, coords in actionDict.items():
                    workerX = box[0]-coords[0]
                    workerY = box[1]-coords[1]
                    
                    # optimised
                    # If new position is not a wall or a box
                    if (workerX, workerY) not in warehouseObject.walls and (workerX, workerY) not in warehouseObject.boxes:
                        # can push box
                        boxX = box[0] + coords[0]
                        boxY = box[1] + coords[1]
                        
                        # If box's new position is not another box or wall
                        if ((boxX, boxY) not in warehouseObject.boxes and (boxX, boxY) not in warehouseObject.walls):
                            #check can go there
                            if (can_go_there(warehouseObject, (workerY, workerX))):
                                # check taboo
                                if (self.allow_taboo_push): 
                                    macroActions.append(((box[1], box[0]), names))             
                                else:
                                    if (self.taboo[boxY][boxX] != 'X'):
                                        macroActions.append(((box[1], box[0]), names))

            return macroActions

    def result(self, state, action):
        """Return the state that results from executing the given
            action in the given state. The action must be one of
            self.actions(state).
            We have two different types of action depending on self.macro = True/False    
        """
        warehouseObject = Warehouse()
        warehouseObject.extract_locations(state.split(sep='\n'))
        if self.macro:
            action = ((action[0][1], action[0][0]), action[1])
            if (action[0] in warehouseObject.boxes):
                playerPosX = action[0][0] + actionDict[action[1]][0]
                playerPosY = action[0][1] + actionDict[action[1]][1]
                
                warehouseObject.boxes.remove((action[0][0], action[0][1]))
                warehouseObject.boxes.append((playerPosX, playerPosY))
                
                warehouseObject.worker = (action[0][0], action[0][1])
        
        else:
            
            playerPosX = warehouseObject.worker[0] + actionDict[action][0]
            playerPosY = warehouseObject.worker[1] + actionDict[action][1]
            
            # push box
            if (playerPosX, playerPosY) in warehouseObject.boxes:
                warehouseObject.boxes.remove((playerPosX, playerPosY))
                warehouseObject.boxes.append((playerPosX + actionDict[action][0], playerPosY + actionDict[action][1]))
                
            warehouseObject.worker = (playerPosX, playerPosY)
        return str(warehouseObject)


          
    def goal_test(self, state):
        """Return True if the state is a goal by removing the player from warehouse string
        """
        return self.goal == state.replace("@", " ")
    
    def path_cost(self, c, state1, action, state2):
        """Return the cost of a solution path that arrives at state2 from
        state1 via action, assuming cost c to get up to state1. If the problem
        is such that the path doesn't matter, this function will only look at
        state2.  If the path does matter, it will consider c and maybe state1
        and action. The default method costs 1 for every step in the path."""
        return c + 1
    
## - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

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
    actionDict = {'Up':(0,-1), 'Down':(0,1), 'Left':(-1,0), 'Right':(1,0)}
    
    # Get each action
    for actions in action_seq:
        currentPos = warehouse.worker
        if actions in actionDict.keys():
            # coords of worker after actions
            resultX = currentPos[0] + actionDict.get(actions)[0]
            resultY = currentPos[1] + actionDict.get(actions)[1]
             
            if (resultX, resultY) in warehouse.walls: 
                 # cannot move there since it's a wall
                return failedSeq
            
            # Checks if its box
            elif (resultX, resultY) in warehouse.boxes:
                # coords of box after actions
                boxResultX = resultX + actionDict.get(actions)[0] 
                boxResultY = resultY + actionDict.get(actions)[1]
                 
                # if moved box is wall/ another box it's a wrong sequence
                if (boxResultX, boxResultY) in warehouse.walls or (boxResultX,boxResultY) in warehouse.boxes:                    
                    return failedSeq
                 
                # successful, commit changes to coords
                else:
                    warehouse.boxes.remove(resultX, resultY)
                    warehouse.boxes.append(boxResultX, boxResultY)
                    warehouse.worker = (resultX, resultY)
                     
            else:
                warehouse.worker = (resultX, resultY)
                
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
    
    global actionDict
    actionDict = {'Up':(0,-1), 'Down':(0,1), 'Left':(-1,0), 'Right':(1,0)}
    
    initialStr = str(warehouse)
    goalStr = str(warehouse).replace("$", " ").replace(".", "*").replace("@", " ")
    # Initialise a puzzle with elementary actions
    puzzle = SokobanPuzzle(warehouse, initialStr, goalStr, macro = False)
    
    if puzzle.goal_test == True:
        return []    
    
    def manhattanDistance(square1, square2):
        return (abs(square1[0]- square2[0]) + abs(square1[1] - square2[1]))

    def heuristic(n):
        state = n.state
        warehouseCurrent = Warehouse()
        warehouseCurrent.extract_locations(state.split(sep='\n'))
        hVal = 0
        for box in warehouseCurrent.boxes:
            distance = 0
            for target in warehouseCurrent.targets:
                # Sums distance from box to all targets
                distance += manhattanDistance(box, target)
                
            # We define h as the average distance of a box to all targets and manhattan distance of worker to all boxes
            hVal += 0.2*distance/len(warehouseCurrent.targets) + 0.75*manhattanDistance(warehouseCurrent.worker, box)
                
        return hVal
        
#    def heuristic(n):
#        state = n.state
#        warehouseCurrent = Warehouse()
#        warehouseCurrent.extract_locations(state.split(sep='\n'))
#        hVal = 0
#        for box in warehouseCurrent.boxes:
#            hVal += math.sqrt((box[0]- warehouseCurrent.worker[0])**2 + (box[1] - warehouseCurrent.worker[1])**2)
#        return hVal/len(warehouseCurrent.boxes)
    

    x = best_first_graph_search(puzzle, heuristic)
#    x = breadth_first_graph_search(puzzle)
    
    # Returns a list with string Impossible if no solution can be found
    if x is None:
        return ['Impossible']
        
        
    # Assigns path of solution and create a generator for each node.
    nodes = x.path()
    nodes = [eachNode.action for eachNode in nodes]
    return(nodes[1:])
    
    
    
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class CanGoThereProblem(search.Problem):
    '''
    An instance of the class 'CanGoThereProblem' represents a problem between worker and destination.
    An instance contains information about the walls, targets, boxes and worker.
    
    Each instance contains the initial string of the warehouse, the warehouse object
    and the destination of the worker (goal state)
    '''
    def __init__(self, initial, warehouse, goal=None):
        self.initial = initial
        self.goal = goal
        self.warehouse = warehouse
        
    global actionDict
    actionDict = {'Up':(0,-1), 'Down':(0,1), 'Left':(-1,0), 'Right':(1,0)}
    
    
    def actions(self, state):
        """Return the actions that can be executed in the given
        state.
        """
        for names, coords in actionDict.items():
            newPos = (state[0] + coords[0], state[1] + coords[1])
            
            if newPos not in self.warehouse.walls:
                if newPos not in self.warehouse.boxes:
                    yield coords
                
                
    def result(self, state, action):
        """Return the state that results from executing the given
        action in the given state. The action must be one of
        self.actions(state).
        """
        return ((state[0] + action[0], state[1] + action[1]))
    
    
    
def can_go_there(warehouse, dst):
    '''    
    Determine whether the worker can walk to the cell dst=(row,column) 
    without pushing any box.
    
    @param warehouse: a valid Warehouse object
    @return
      True if the worker can walk to cell dst=(row,column) without pushing any box
      False otherwise
    '''
    
    # The heuristic is defined as the shortest distance from worker to destination
    def heuristic(GoThereProblem):
        state = GoThereProblem.state
        return math.sqrt((math.pow(state[1] - dst[1], 2)) + (math.pow(state[0] - dst[0], 2)))

    dst = (dst[1], dst[0])
    
    # Use best first graph search on the CanGoThereProblem search
    node = best_first_graph_search(CanGoThereProblem(warehouse.worker, warehouse, dst),
                       heuristic)
    
    return node is not None

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

## COORDINATE IS IN (y,x)
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
    initialStr = str(warehouse)
    
    # Goal string is initial string where all boxes are on targets, represented by *
    # and player is removed so the final position of the player does not matter
    goalStr = str(warehouse).replace("$", " ").replace(".", "*").replace("@", " ")
    
    # A puzzle is initialised with the following variables and allow_taboo_push is set to false
    # to increase speed for testing
    puzzle = SokobanPuzzle(warehouse, initialStr, goalStr, macro = True, allow_taboo_push = False)
    
    
    # Basic formula for Manhattan distance predefined
    def manhattanDistance(square1, square2):
        return (abs(square1[0]- square2[0]) + abs(square1[1] - square2[1]))

    # Heuristic formula is based on sum of the average distance of each box to all targets
    def heuristic(n):
        state = n.state
        warehouseCurrent = Warehouse()
        warehouseCurrent.extract_locations(state.split(sep='\n'))
        hVal = 0
        for box in warehouseCurrent.boxes:
            targetDistance = 0
            for target in warehouseCurrent.targets:
                targetDistance += manhattanDistance(box, target)
                
            hVal = manhattanDistance(warehouseCurrent.worker, box)/len(warehouseCurrent.boxes) + targetDistance/len(warehouseCurrent.targets) #no cost from worker to box for macro
                
        return hVal
        
    # Tests for goal test before running search to prevent pointless search
    if puzzle.goal_test == True:
        return []

    # Greedy first search is used to fasten process
    x = best_first_graph_search(puzzle, heuristic)
#    x = astar_graph_search(puzzle, heuristic)    
    # Returns a list with string Impossible if no solution can be found
    if x is None:
        return ['Impossible']
        
        
    # Assigns path of solution and create a generator for each node.
    nodes = x.path()
    nodes = [eachNode.action for eachNode in nodes]
    return(nodes[1:])
    

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


# TESTING OF FUNCTION DIRECTLY ON THIS FILE CAN DELETE AFTER
wh = Warehouse()
wh.load_warehouse("warehouses/warehouse_57.txt")
t0 = time.time()
x = solve_sokoban_macro(wh)
print(x)
t1 = time.time()
print ("Solver took ",t1-t0, ' seconds')