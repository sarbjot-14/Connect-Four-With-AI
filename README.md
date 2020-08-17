# Connect-Four-With-AI

## Exactly what steps should be taken to get the project working, after getting your code? 

### Two options
#### Docker
I used docker to run the project. Please use : "docker-compose up" in the the same directory as the docker compose file.

Then visit http://0.0.0.0:5001/ 
and not http://0.0.0.0:80/

port 80 is being forwarded to 5001

#### Without Docker

1. Move to /app directory (same directoroy as run.py). 
2. Download python
  * `sudo apt-get install python3.6`
3. Download pip3
  * `sudo apt install python3-pip`
4. Download flask
  * `pip install Flask`
5. Run app
  * `python run.py`
6. Visit web app at http://127.0.0.1:5000/



## What is the overall goal of the project (i.e. what does it do, or what problem is it solving)?

The goal is to create Connect Four (https://en.wikipedia.org/wiki/Connect_Four) game where you can play against the computer. You can choose between a "impossible" mode, which is still beatable or you can choose to play against "automatic" mode. The automatic mode changes difficulty to suit your playing style. It will play harder if you win, and play easier if you are losing too much. This is so that the player can stay engaged and become a better player.


## Which languages did you use, and what parts of the system are implemented in each?

I used a client server model with a REST API. The server is written uses flask framework which is written in Python and the client side uses Javascript. I also do file I/O and some calculations with C on the server side.


## What methods did you use to communicate between languages?

The client and server communicate using a REST API. Usually the client makes a post request to the server and the server takes the request does calculations and sends data back. The data is in JSON format. 

Communications between example.c and views.py uses SWIG. The C file (example.c) is precompiled into a python library called example.py which is imported into view.py and used accordingly.




##  Key features?

The code is mainly split between three files:
app/app/static/js/app.js
This javascipt file is run on the client side.
This code:
	- Takes user input
	- Handles errors
	- Makes updates to UI
	- Stores current game state data
	- Makes post requests to the server

app/app/views.py
This is the server side code that mainly does the calculations so that the AI can choose the next move.
This code:
	- recieves/processes requests from the client (new game, a move, difficulty change)
	- Check if either human or AI won the game
	- Uses Monte Carlos Search Tree AI method to calculate the next move
		- This strategy essentially simulates n number of games for each move legal in order to decide the next move
		- More information here: https://en.wikipedia.org/wiki/Monte_Carlo_tree_search
	- Dynamically change the strength of the AI if "auto" mode is on based on the results of the last 5 games played
	- Call methods in example.c to
		- log and read the history of wins/losses/draws
		- calculate the difficulty the AI should use 
			
app/example.c
	- Log whether the human won lost or game resulted in draw using file I/O
	- Read the history of wins/losses/draws
	- Calculate the difficulty the AI 
		- Max difficulty, "impossible" mode is when AI uses 60 playouts, and very easy is 0 playouts
		- When "auto" mode is on the playouts will be between 0-60, and decided based on the past 5 games
	- Difficulty mode can be changed at any point and the server will use this file to recalculate difficulty accordingly
