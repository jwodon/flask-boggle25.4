//
$.noConflict();
jQuery(document).ready(function ($) {
    class BoggleGame {
        constructor() {
            this.score = 0;
            this.usedWords = [];
            this.board = $("#game");
            this.$guessInput = $("#guess-input", this.board);
            this.$guessButton = $("#guess-button", this.board);
            this.$resetButton = $("#reset", this.board);
            this.$timeLeft = $("#time-left");
            this.$guessedWords = $("#guessed-words");

            this.$guessButton.on("click", this.getGuess.bind(this));
            this.$resetButton.on("click", this.resetGame.bind(this));

            // Set a 60-second timer
            this.timeLeft = 60;
            this.timer = setInterval(() => {
                this.updateTimeLeft();
            }, 1000);

            // Disable the game after 60 seconds
            setTimeout(() => {
                this.disableGame();
            }, 60000);
        }

        updateTimeLeft() {
            this.$timeLeft.text(`Time left: ${this.timeLeft} seconds`);
            this.timeLeft -= 1;

            if (this.timeLeft < 0) {
                clearInterval(this.timer);
                this.disableGame();
            }
        }

        async disableGame() {
            this.$guessInput.prop("disabled", true);
            this.$guessButton.prop("disabled", true);
            this.showMessage("Game over. Time limit reached.");

            const response = await axios.post("/track-score", { score: this.score });

            this.updateStats(response.data.highest_score, response.data.times_played);
        }

        updateStats(highScore, timesPlayed) {
            $("#high-score").text(`High Score: ${highScore}`);
            $("#times-played").text(`Times Played: ${timesPlayed}`);
        }

        showMessage(msg) {
            $(".msg", this.board).text(msg).addClass("visible");
        }

        async resetGame(evt) {
            evt.preventDefault();
            
            const response = await axios.post("/reset-game");
            if (response.data.message === "Game reset successfully!") {
                this.resetGameData();
            }
        }

        resetGameData() {
            this.score = 0;
            this.usedWords = [];
            this.$guessedWords.empty();
            $("#score").text(`Score: ${this.score}`);
            $(".msg", this.board).removeClass("visible");
            this.$guessInput.prop("disabled", false);
            this.$guessButton.prop("disabled", false);
            this.timeLeft = 60;
            this.updateTimeLeft();
            clearInterval(this.timer);
            this.timer = setInterval(() => {
                this.updateTimeLeft();
            }, 1000);
        }

        async getGuess(evt) {
            evt.preventDefault();

            let guess = this.$guessInput.val();

            if (!guess) return;
            if (this.usedWords.includes(guess)) {
                this.showMessage(`${guess} has already been guessed`)
                return;
            }

            const response = await axios.get("/check-word", {
                params: { guess: guess },
            });

            if (response.data.result === "not-word") {
                this.showMessage(`${guess} is not a valid English word`);
            } else if (response.data.result === "not-on-board") {
                this.showMessage(`${guess} is not a valid word on this board`);
            } else {
                this.showMessage(`Added: ${guess}`);
                let score_value = guess.length;
                this.score += score_value;
                this.usedWords.push(guess);
                $("#score").text(`Score: ${this.score}`);
                this.updateGuessedWords();
            }
            this.$guessInput.val(""); // Reset the input field
        }

        updateGuessedWords() {
            this.$guessedWords.empty();
            this.usedWords.forEach((word) => {
              this.$guessedWords.append(`<li>${word}</li>`);
            });
        }
    }
    const game = new BoggleGame();
});

