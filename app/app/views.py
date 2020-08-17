from app import app
from flask import render_template, request, redirect, jsonify, make_response
import random
import time
import copy
import example

#tutorial followed to learn flask
#https://www.youtube.com/watch?v=QKcVjdLEX_s

"""
write the report
"""
count = 0


def checkWinner(turn, board):
    
    # check horizontal
    for i in range(0,6):
        row = board[i*7:((i*7)+7)]
        for j in range(0,4):
            count = 0
            for k in range(0,4):
                if row[j+k] == turn:
                    count= count +1
                    if count == 4:
                       
                        return "Won"


    
    # check vertical
    for i in range(0,7):
        for j in range(0,3):
            start = i + j*7
            count = 0
            for k in range(0,4):
                if board[start + k*7] == turn:
                    count = count +1
                    if count == 4:
                        
                        return "Won"
     

    # check diagonal negative slope
    for i in range(0,3): # first three rows
        for j in range(0,4): #first 4 positions in each row
     
            count = 0
            start = (i*7)+j
            for k in range(0,4):
                if board[start+(8*k)] == turn:
                    count = count +1
                    if count == 4:
                      
                        return "Won"


    #check diagonal positive slope
    for i in range(0,3): # first three rows
        for j in range(0,4):
            start = ((i*7)+3)+j
            count = 0
            for k in range(0,4):
                if board[start+(6*k)] == turn:
                
                    count = count + 1
                    if count == 4:
                    
                        return "Won"
         
    #Check draw

    for i in range(0,7):
        if board[i] == 'e':
            return "None" #continue playing
    return "Draw"




def makeMove(turn,col, tempBoard):

    bottom = (7 * 5  ) + col
    for i in range(0,6):  
        

        if tempBoard[bottom] == 'e':
            tempBoard[bottom] = turn
           
            break;
        
        bottom = bottom -7
    
    return tempBoard

def printState(gameState):
    for i in range(0,42):
        if i%7 == 0:
            print("")
        print(gameState[i],end=" ")
    print("")
    return

def legalMoves(board):
    # return all available moves
    topRow = board[0:7]
    legMovArr= []
    for cell in range(0,7):
        if topRow[cell] == 'e':
            legMovArr.append(cell)
    return  legMovArr



def playout(tempBoard, move):
    # perfomr one playout where AI simulates random moves for each player
    #AI always goes first 
    playoutTurn = 'b'
    # make the move that we are testing
    tempBoard = makeMove(playoutTurn,move,tempBoard)
    result = checkWinner('b',tempBoard)
    if result == "Won":
        return 'W'
    elif result == "Draw":
        return 'D'

    
    playoutGameOver = False
  
    #keep going until game is over
    while not playoutGameOver:
        playoutTurn = 'w'
        moves = legalMoves(tempBoard)
        tempBoard = makeMove(playoutTurn,random.choice(moves),tempBoard)
        result = checkWinner(playoutTurn,tempBoard)
        if result == "Won":
            
            return 'L'
        elif result == "Draw":
            return 'D'
        
        playoutTurn = 'b'
        moves = legalMoves(tempBoard)
        tempBoard = makeMove(playoutTurn,random.choice(moves),tempBoard)
        result = checkWinner(playoutTurn,tempBoard)
        if result == "Won":
            
            return 'W'
        elif result == "Draw":
            return 'D'




def multiplePlayOuts(gameState, move,playouts):
    #simulate multiple games to see 
    wins = 0
    draws = 0
    loses = 0
    
    # keep track of how many wins losses draws this one playout resulted in
    for i in range(0, playouts): #numPlayouts):
        newBoard =  copy.deepcopy(gameState)
        result = playout(newBoard,move)
        if result == 'W':
            wins+=1
        elif result == 'L':
            loses+=1
        elif result == 'D':
            draws+=1

    return (move,wins,loses,draws)

def AImove(gameState,playouts):
    moves = legalMoves(gameState)
    stats  =[]
    #for every possible move, record the wins/losses/draw statistics 
    for i in range(len(moves)):
        stats.append(multiplePlayOuts(gameState,moves[i],playouts))
   
    # pick the move that resulted in them most wins
    bestMove  = stats[0]
    for stat in stats:
        if stat[1]>bestMove[1]:
            bestMove = stat
    print("AI picked",bestMove)
    return bestMove[0]

# server homepage
@app.route('/')
def index():

    return render_template("/public/index.html")

#clear the win/loss/draw tallies in scores.txt file
@app.route("/start/clear-history",methods=["POST"])
def clearHistory():
    example.clear_history()
    res = make_response(jsonify({}),200)

    return res

#return the statitics to the client
@app.route("/start/stats",methods=["POST"])
def newGame():
   

    req = request.get_json()
    # log new score
    # 0 won, 1 lost, 2 draw
    if req['outcome'] !="start":
        if req['outcome'] == "Won":
            example.logging_score(0)

        elif req['outcome'] == "Lost":
            example.logging_score(1)
        elif req['outcome'] == "Draw":
            example.logging_score(2)

    #Send back new statistics
    wins = example.stats(0)
    losses= example.stats(1)
    draws = example.stats(2)
    statistics = {"wins":wins, "losses":losses, "draws":draws}
    res = make_response(jsonify(statistics),200)

    return res






@app.route("/start/move",methods=["POST"])
def move():
    
    #AI is always black

    req = request.get_json()
    
    # find playouts based on difficulty
    max = 80
    if req['difficulty'] == "auto":
        playouts = example.calculate_difficulty(max)
    else:
        playouts = max

    actualBoard = req['board']
    for i in range(0,len(actualBoard)):
        if actualBoard[i] == '□':
            actualBoard[i] = 'e'
        elif actualBoard[i] == '●':
            actualBoard[i] = 'b'
        else:
            actualBoard[i] = 'w'

    # check if valid move
    legMoves = legalMoves(actualBoard)
  

    if req['move'] not in legMoves:
        res = make_response(jsonify({"winner":"Black", "move":"illegal", "gameState":[]}),200)
        return res
      
    # record move made
    # move will be  -1 if AI has first move
    gameState = makeMove('w',req['move'],actualBoard)

    # check if it was winning move
    result = checkWinner('w', gameState)
    if result == "Won":
       
        res = make_response(jsonify({"winner":"White", "move":"none", "gameState":gameState}),200)
        return res
    elif result == "Draw":
        res = make_response(jsonify({"winner":"Draw", "move":"none", "gameState":gameState}),200)
        return res

    # calculate AI move
    move = AImove(gameState,playouts)
    #record AI move
    
    gameState = makeMove('b',move,gameState)
    result = checkWinner('b',gameState)

    if result == "Won" :
        res = make_response(jsonify({"winner":"Black", "move":"none", "gameState":gameState}),200)
        return res

    elif result == "Draw" :
        res = make_response(jsonify({"winner":"Draw", "move":"none", "gameState":gameState}),200)
        return res

 

    # send move to server
 
    res = make_response(jsonify({"winner":"none", "move":move, "gameState":gameState}),200)

    return res

