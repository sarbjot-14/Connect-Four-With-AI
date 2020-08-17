console.log("this is app client side")




var gameState = ['□','□','□','□','□', '□','□','□','□','□','□','□', '□','□','□','□','□','□','□', '□','□','□','□','□','□','□', '□','□','□','□','□','□','□', '□','□','□','□','□','□','□', '□','□']
var turn = '○'
var gameOver = false
var difficulty = "impossible"
updateStatistics("start")

function updateStatistics(result){
    var entry = {
        outcome: result
    };

    fetch(`${window.origin}/start/stats`,{
        method:"POST",
        credentials:"include",
        body: JSON.stringify(entry),
        cache:"no-cache",
        headers: new Headers({
            "content-type":"application/json"
        })

    })
    .then(resp=>{
        if( resp.status !== 200){
            console.log("Did not succesfully retrieve json in browser")
        }
        else{
            resp.json().then(data=>{
               
                document.getElementById("wins").innerHTML = "Wins: "+data.wins;
                document.getElementById("losses").innerHTML = "Losses: "+data.losses;
                document.getElementById("draws").innerHTML = "Draws: "+data.draws;

            })
        }
    })
}

function setMove(column, elmnt){
    document.getElementById("feedback").innerHTML = "Black's move";
    var entry = {
        move: parseInt(column),
        board: gameState,
        difficulty:difficulty
    };

    fetch(`${window.origin}/start/move`,{
        method:"POST",
        credentials:"include",
        body: JSON.stringify(entry),
        cache:"no-cache",
        headers: new Headers({
            "content-type":"application/json"
        })

    })
    .then(resp=>{
        if( resp.status !== 200){
            console.log("Did not succesfully retrieve json in browser")
        }
        else{
            resp.json().then(data=>{
                console.log("AI move is "+data.move)
                numPlayouts = data.playouts

                //if legal move notify user
                //reset 
                document.getElementById("errors").innerHTML = "";
                if(data.move == "illegal"){
                    console.log("illegal move")
                    document.getElementById("errors").innerHTML = "Invalid move try again";
                    return

                }

                // update UI
                
                //console.log(data.gameState)
                gameState = data.gameState
                for (var i = 0 ;i < gameState.length;i++){
                   
                    if (gameState[i] =='e'){
                        gameState[i] = '□'
                    }
                    else if( gameState[i] =='w'){
                        gameState[i] = '○'
                    }
                    else {
                        gameState[i] = '●'
                    }

                    document.getElementById(i).innerHTML = gameState[i];
                    if(gameState[i] != '□'){
                        document.getElementById(i).classList.add("black");
                    }
                    

                    
                }
                document.getElementById("feedback").innerHTML = "White's move";
                

                
                if(data.winner == "Draw"){
                    gameOver = true
                    document.getElementById("feedback").innerHTML = data.winner;
                    //update statistics
                    updateStatistics("Draw")
                    return
                }

                // check if anyone won
                if(data.winner != "none"){
                    //console.log("Winner is "+data.winner)
                    gameOver = true
                    document.getElementById("feedback").innerHTML = "The Winner is "+data.winner;
                    //update statistics
                    if(data.winner == "Black"){
                        updateStatistics("Lost")
                    }
                    else{
                        updateStatistics("Won")
                    }
                    return

                }
               
                
            })
        }
        
    })

}
function myFunction(elmnt) {
    // entry point: finds which element was clicked 
    // makes a move accordingly
    if (gameOver){
        document.getElementById("errors").innerHTML = "Game over. Start new Game!";
        return
    }
    console.log("Human chose column number: "+elmnt.id)
    

    setMove(elmnt.id,elmnt)

}


function newGame(){
    // resets state and reloads the page
    location.reload()

    gameOver = false
    gameState = ['□','□','□','□','□', '□','□','□','□','□','□','□', '□','□','□','□','□','□','□', '□','□','□','□','□','□','□', '□','□','□','□','□','□','□', '□','□','□','□','□','□','□', '□','□']

    document.getElementById("feedback").innerHTML = "White's move";


}

function clearHistory(){
    // clears the recoreded wins/losses/draws and updates UI
    fetch(`${window.origin}/start/clear-history`,{
        method:"POST",
        credentials:"include",
        body: JSON.stringify({}),
        cache:"no-cache",
        headers: new Headers({
            "content-type":"application/json"
        })

    })
    .then(resp=>{
        if( resp.status !== 200){
            console.log("Did not succesfully retrieve json in browser")
        }
        else{
            document.getElementById("wins").innerHTML = "Wins: 0";
                document.getElementById("losses").innerHTML = "Losses: 0";
                document.getElementById("draws").innerHTML = "Draws: 0";
        }
    })

}


// set the difficulty to auto
function auto(){
    difficulty = "auto"
    document.getElementById("difficulty").innerHTML = "Difficulty: Auto";                
}

//set the difficulty to impossible
function impossible(){
    difficulty = "impossible"
    document.getElementById("difficulty").innerHTML = "Difficulty: Impossible";                
}