from boggle import Boggle
from flask import Flask, request, render_template, session, jsonify

app = Flask(__name__)
app.config['SECRET_KEY'] = "oh-so-secret"
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0


boggle_game = Boggle()

@app.route("/")
def show_board():
    "Initiate game and display board"

    board = boggle_game.make_board()
    session['board'] = board

    return render_template("home.html", board = board)

@app.route("/check-word")
def check_word():
    """Check if guess is in dictionary."""

    guess = request.args["guess"]
    board = session["board"]
    response = boggle_game.check_valid_word(board, guess)

    return jsonify({'result': response})

@app.route("/track-score", methods=["POST"])
def track_score():
    score = request.json["score"]

    # Increment the number of times played and update the highest score if needed
    session["times_played"] = session.get("times_played", 0) + 1
    session["highest_score"] = max(session.get("highest_score", 0), score)

    return jsonify({
        "message": "Score tracked successfully!",
        "highest_score": session["highest_score"],
        "times_played": session["times_played"]
    })

@app.route("/reset-game", methods=["GET", "POST"])
def reset_game():
    board = boggle_game.make_board()
    session['board'] = board
    return jsonify({"message": "Game reset successfully!"})


