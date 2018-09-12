#Dylan Shekter (lead programmer) and Ari Sporkin (lead codebreaker, lead brainstormer)
import copy
from copy import *
from random import *
#from pympler.asizeof import asizeof
##################################
def deepcopy1(x):
    if hasattr(x,'__deepcopy__'):
        try:
            return x.__deepcopy__()
        except TypeError:
            return x.__deepcopy__(x)
    else:
        return copy.deepcopy(x)
################################

#questions from assignment
#How many games can a human player 1 win on a 3 by 3 board before the computer is unbeatable?
# around 14 or so
#How many possible games are there on a 3 by 3 board? A 4 by 3 board? A 4 by 4 board?
#252,6003, a single 4x4 board tree creation crashed computer after 30 minutes of chugging
#On a 4 by 4 board, does player 1 or player 2 resign first? On average, how many games does it take before one player becomes unbeatable?
#N/A
#What is the largest square board that you can make before your computer runs out of memory? What does this mean about a more complicated game like chess?
#even at 30000x25000 it only used python only used total 4,766,544k bringing ram use up to 96% with bacground processes,
#so if everything was closed probably like 37000x37000 ish

class Board:
    def __init__(self,width, height):
        self.currMove = 'White' 
        self.lW = [[x,height-1] for x in xrange(0,width)]
        self.lB = [[x,0] for x in xrange(0,width)]
        self.piece_map = [] #If I created this board on one line it did bad things
        [self.piece_map.append([None]*width) for i in xrange(height)]
        self.piece_map[0] = ["B"]*width
        self.piece_map[-1] = ["W"]*width
    def __str__(self): #replaces everything with everything else
        return str(self.piece_map).replace('[[','|').replace(']]','|').replace('], ','|\n').replace("'",'').replace('[','|').replace(',','|').replace('None',' ').replace(' B','B').replace(' W','W').replace('  ',' ')
    #checks the 3 different win conditions
def bReset(self):
        self.__init__(len(self.piece_map[0]),len(self.piece_map))
def winCheck(self,debug = False):
    #if one side has been completely eliminated
    if len(self.lW) == 0:
        return "Black Wins, count 0"
    if len(self.lB) == 0:
        return "White Wins, count 0"
        
    #if there is a black piece in a white starting spot
    if 'B' in self.piece_map[-1]:
        return "Black Wins, other side"
    #if there is a white piece in a black starting spot
    if "W" in self.piece_map[0]:
        return "White Wins, other side"
        
    # if every white piece has a black piece above it
    if self.currMove == 'White':
        for coord in self.lW:
            if self.piece_map[coord[1]-1][coord[0]] != 'B':
                break
        else: # all blocked
            for coord in self.lB:
                if coord[0] > 0:
                    if (self.piece_map[coord[1]+1][coord[0]-1] == "W"):
                        break
                if coord[0] < (len(self.piece_map[0])-1): 
                    if (self.piece_map[coord[1]+1][coord[0]+1] == "W"):
                        break
            else:
                return "Black Wins, all blocked"
            
    #if every black piece has a white piece below it
    elif self.currMove == 'Black':
        for coord in self.lB:
            if self.piece_map[coord[1]+1][coord[0]] != 'W':
                if debug:
                    print 'found an empty space at: ',self.piece_map[coord[1]+1][coord[0]]
                break
        else: # all blocked
            for coord in self.lW:
                if coord[0] > 0:
                    if (self.piece_map[coord[1]-1][coord[0]-1] == "B"):
                        break
                if coord[0] < (len(self.piece_map[0])-1): 
                    if (self.piece_map[coord[1]-1][coord[0]+1] == "B"):
                        break
            else:
                return "White Wins, all blocked"


#lets pieces move across the board and capture other pieces and then WinChecks
def move(*args):
    self = args[0]
    """x1,y1,x2,y2"""
    if len(args) == 0:
        s1 = str(raw_input("Enter X,Y coordinate to move from: "))
        s2 = str(raw_input("Enter X,Y coordinate to move to: "))
        x1,y1 = s1[:s1.find(',')],s1[s1.find(',')+1:]
        x2,y2 = s2[:s2.find(',')],s2[s2.find(',')+1:]
    elif len(args) == 2:
        x1,y1,x2,y2 = args[1][0],args[1][1],args[1][2],args[1][3]
    else:
        x1,y1,x2,y2 = args[0:4]
    try:
        x1,x2,y1,y2 = int(x1),int(x2),int(y1),int(y2)
    except ValueError:
        return ('please enter numeric coordinates')
    if ((y2 > y1) and self.currMove == "White"):
        return ("can't move backwards, white")
    if((y2 < y1) and self.currMove == "Black"):
        print("can't move backwards, black")
        print x1,',',y1,'->',x2,',',y2
        print self
        return 
    if (y2 == y1):
        return ("can't move sideways")
    if (x1 < 0 or x1 > len(self.piece_map[0])) or (x2 < 0 or x2 > len(self.piece_map[0])) or (y1 < 0 or y1 > len(self.piece_map)) or (y2 < 0 or y2 > len(self.piece_map)):
        return ('invalid move, out of bounds')
    if (x1 == x2 and y1 == y2):
        return ('invalid move, try again 1')
    if self.currMove == "White":
        if (y2 < y1-1):
            return ('invalid move, try again 2')
        if self.piece_map[y1][x1] != "W":
            return ('not your piece, try again')
        if (self.piece_map[y2][x2] == 'B'):#valid capture move
            if (x2 == x1+1 or x2==x1-1):
                counter = 0
                while counter < len(self.lB):
                    coord = self.lB[counter]
                    if coord[0]==x2 and coord[1]==y2:
                        self.lB[counter] == None
                        self.lB.pop(counter)
                        break
                    else:
                        counter += 1
                else:
                    raise BaseException('piece not found! tried '+str(counter)+' time(s)')
                self.piece_map[y2][x2] = "W"
                self.piece_map[y1][x1] = None
                for index in xrange(len(self.lW)):
                    coord = self.lW[index]
                    if coord[0]==x1 and coord[1]==y1:
                        self.lW[index] = [x2,y2]
                        break
            else:
                return ('invalid move, try again 3'+str(x2 == x1+1)+str(x2==x1-1))
        elif (self.piece_map[y2][x2] == 'W'):
            return ("can't move onto your own piece.")
            return 
        else: #valid moving move
            if (self.piece_map[y2][x2] == None) and x2 == x1:
                    self.piece_map[y2][x2] = "W"
                    self.piece_map[y1][x1] = None
                    for index in xrange(len(self.lW)):
                        coord = self.lW[index]
                        if coord[0]==x1 and coord[1]==y1:
                            self.lW[index] = [x2,y2]
                            break
                    else:
                        print 'piece not found!'
            else:
                return ("invalid move, try again 4")
                    
    elif self.currMove == "Black":
        if (y2 > y1+1):
            print('invalid move, try again 5')
            print self
        if self.piece_map[y1][x1] != "B":
            print('not your piece, try again')
            print self
            
        if (self.piece_map[y2][x2] == "W"):#valid capture move
            if (x2 == x1-1 or x2==x1+1):
                self.piece_map[y2][x2] = "B"
                self.piece_map[y1][x1] = None
                counter = 0
                while counter <= len(self.lW):
                    coord = self.lW[counter]
                    if coord[0]==x2 and coord[1]==y2:
                        self.lW[counter] == None
                        self.lW.pop(counter)
                        break
                    counter += 1
                else:
                    print('piece not found! tried'+str(counter)+'time(s)')
                    print args
                for index in xrange(len(self.lB)):
                    coord = self.lB[index]
                    if coord[0]==x1 and coord[1]==y1:
                        self.lB[index] = [x2,y2]
                        break
                else:
                    print('piece not found to move!')
            else:
                print self
                return ("invalid move, try again 6")
                
        elif (self.piece_map[y2][x2] == 'B'):
            print self
            return ("Can't move onto your own piece.")
        else: #valid moving move
            if (self.piece_map[y2][x2] == None):
                if x2 == x1:
                    self.piece_map[y2][x2] = "B"
                    self.piece_map[y1][x1] = None
                    for index in xrange(len(self.lB)):
                        coord = self.lB[index]
                        if coord[0]==x1 and coord[1]==y1:
                            self.lB[index] = [x2,y2]
                            break
                else:
                    print self
                    return ("invalid move, try again 7")
    else:
        print 'invalid currMove'
                    
    self.currMove = "White" if self.currMove=="Black" else "Black"
    return (True,[x1,y1,x2,y2])
class Tree:
    def __init__(self,parent=None,board=None,mMove=None,player='White'):
        if player != 'White' and player != 'Black':
            print 'PLAYER INVALID'
        self.parent = parent
        self.children = []
        self.board = deepcopy(board)
        self.player = player
        self.move = mMove
        if mMove != None:
            self.board.currMove = player
            move(self.board,mMove)
        if parent == None:
            populate(self)
def bStr(match_box):
    return str(match_box.board)
def bLen(match_box):
    counter = len(match_box.children)
    for i in match_box.children:
        counter += bLen(i)
    return counter if match_box.parent != None else counter + 1
def leftSide(match_box):
    print match_box.board,match_box.move,match_box.player
    if len(match_box.children) > 0:
        leftSide(match_box.children[0])
def rightSide(match_box):
    print match_box.board,match_box.move,match_box.player
    if len(match_box.children) > 0:
        rightSide(match_box.children[-1])
def populate(match_box,side = 'White'):
    if type(winCheck(match_box.board)) == str: 
        return match_box
    elif (winCheck(match_box.board)) == False or (winCheck(match_box.board)) == None:
        #iPoss = match_box.genMoves('White')
        if side == 'White':
            for move in genMoves(match_box.board,'White'):
                newBox = Tree(match_box,deepcopy(match_box.board),move,'White')
                match_box.children.append(newBox)
                populate(newBox,'Black')
        elif side == 'Black':
            for move in genMoves(match_box.board,'Black'):
                newBox = Tree(match_box,deepcopy(match_box.board),move,'Black')
                match_box.children.append(newBox)
                populate(newBox,'White')
        try:
            del match_box.board
            return newBox
        except UnboundLocalError:
            raise BaseException('Contact Dylan, he was already waiting for that line to mess things up')
def genMoves(board,side=None):
        oPoss = list()
        if side == 'Black':
            for x,y in board.lB:
                oPoss.append([x,y,x,y+1])#center
                oPoss.append([x,y,x-1,y+1])#left
                oPoss.append([x,y,x+1,y+1])#right
        elif side == 'White':
            for x,y in board.lW:
                oPoss.append([x,y,x,y-1])#center
                oPoss.append([x,y,x-1,y-1])#left
                oPoss.append([x,y,x+1,y-1])#right
        poss = list()
        for move in oPoss:
            if legal_move(board,move,side):
                poss.append(move)
        return poss
def legal_move(board,tInput,side):
    x1,y1,x2,y2=tInput[0],tInput[1],tInput[2],tInput[3]
    if (x1 < 0 or x1 > len(board.piece_map[0])-1) or (x2 < 0 or x2 > len(board.piece_map[0])-1) or (y1 < 0 or y1 > len(board.piece_map)-1) or (y2 < 0 or y2 > len(board.piece_map)-1):
        return False
    if side == 'Black':
        if (board.piece_map[y2][x2] == 'B') or (board.piece_map[y1][x1] != "B") or ((board.piece_map[y2][x2] == None) and x2 != x1) or (board.piece_map[y2][x2] == 'W' and x1==x2) or (board.piece_map[y1][x1] == 'W'):
            return False
        return True
    elif side == 'White':
        if (board.piece_map[y2][x2] == 'W') or (board.piece_map[y1][x1] != "W") or ((board.piece_map[y2][x2] == None) and x2 != x1) or (board.piece_map[y2][x2] == 'B' and x1==x2):
            return False
        return True
    raise BaseException("WHAT")
class Controller:
    def __init__(self,tree,side):
        self.tree = tree
        self.currNode = self.tree
        self.side = side
    def find_box(self,node,mMove):
        for box in node.children:
            if box.move == mMove:
                return box
        else:
            raise BaseException('box not found '+self.side)
    def made_move(self,mMove):
        if len(self.currNode.children) == 0:
            raise BaseException("The children are 0 in number")
        try:
            self.currNode = self.find_box(self.currNode,mMove)
        except ValueError:
            print 'looking for: ',mMove
            for mMMove in self.currNode.children:
                print mMove.mMMove
            raise BaseException
    def make_move(self):
        if len(self.tree.children) == 0:
            return 'concede'
        node = choice(self.currNode.children)
        counter = 0
        while len(node.children) == 0 and winCheck(node.board) == False:
            counter += 1
            node = choice(self.currNode.children)
            if counter >= len(self.currNode.children)*5:
                raise BaseException("Infinite Loop "+str(counter)+str(self.currNode.children))
        self.currNode = node
        return node.move
    def lost(self):
        walker = self.currNode
        walkerPrev = None
        while len(walker.parent.children) <= 1 or walker.player != self.side:
            walker = walker.parent if walker.player != self.side else walker.parent.parent
            if walker == None or walker.parent == None:
                walkerPrev,walker = None,None
                return 'Concede'
            walkerPrev = walker
        try:
            walker.parent.children.remove(walker)
        except ValueError:
            raise BaseException('Contact Dylan, he was already waiting for that line to mess things up as well')
        if len(walker.parent.children) == 0:
            raise BaseException('I DONE MESSED THIS HERE THANG UP')
    def reset(self):
        self.currNode = self.tree
        self.movesList = []
if __name__ == '__main__':
    board = Board(4,4)
    print 'beggining!'
    black = Controller(Tree(board=board),'Black')
    print 'made black'
    white = Controller(Tree(board=board),'White')
    print 'made white'
    print 'length of black: '+str(bLen(black.tree))
    cW,cB = 0,0
    while True:
        while winCheck(board) == None:
            WMove = white.make_move()
            res = move(board,WMove)
            if res[0] != True:
                print res
                raise BaseException
            if winCheck(board) != None:
                break
            black.made_move(WMove)
            BMove = black.make_move()
            if winCheck(board) != None:
                break
            res = move(board,BMove)
            if res[0] != True:
                print res
                raise BaseException
            white.made_move(BMove)
        if winCheck(board)[:5] == "White":
            cW += 1
            res = black.lost()
            if res == "Concede":
                print "White Wins, Black Conceded"
                break
        elif winCheck(board)[:5] == "Black":
            cB += 1
            res = white.lost()
            if res == "Concede":
                print "Black Wins, White Conceded"
                break
        else:
            raise BaseException("Invalid Loss")
        bReset(board)
        white.reset()
        black.reset()
        print '(White Wins, Black Wins) '+str(cW)+' '+str(cB)
