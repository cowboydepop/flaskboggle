from flask import Flask,render_template, request, session, jsonify
from boggle import Boggle

app = Flask(__name__)
app.config['SECRET_KEY'] = 'catzthemovie'

boggle_game = Boggle()

@app.route("/")
def home_page():
   
    return render_template("index.html")

@app.route("/start", methods=["POST"])
def start_game():
 
 
    board = boggle_game.make_board()

    session['board'] = board
   
    if "games" in session:
        session["games"] += 1
    else:
        session["games"] = 1
    return render_template("start.html", board=board)

@app.route("/validate_guess", methods=["POST"])
def validate_guess():
    
   
    guess = request.json.get("guess")
 
    board = session["board"]

    result = boggle_game.check_valid_word(board, guess)
   
    return jsonify({'result': result, "word":guess})

@app.route("/game_over", methods=["POST"])
def update_game_stats():
  
    
    
    gameScore = request.json.get("gameScore")
    

    gamesPlayed = session.get("games", 0)
    
 
    gamesPlayed += 1
    session["games"] = gamesPlayed


    if "high_score" in session:
        if gameScore > session["high_score"]:
            session["high_score"] = gameScore 
    else:
        session["high_score"] = gameScore
        
    current_high_score = session["high_score"]
    
   
    return jsonify({"games": gamesPlayed, "high_score": current_high_score})

        
    