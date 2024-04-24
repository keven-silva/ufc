function randomBall() {
    const ballElement = document.getElementById("ball");
    const ball = Math.floor(Math.random() * 3) + 1;
    if (ball == 1) {
        ballElement.style.backgroundColor = "pink";
    } else if (ball == 2) {
        ballElement.style.backgroundColor = "blue";
    } else if (ball == 3) {
        ballElement.style.backgroundColor = "green";
    }
    return ball;
}

function point() {
    const pointValue = document.getElementById("point-value");
    let points = pointValue.innerHTML;
    points++;
    pointValue.innerHTML = points;
}

function resetPoints() {
    const pointValue = document.getElementById("point-value");
    pointValue.innerHTML = 0;
}

function eventBall(event) {
    if (ball == 1 && event.type == "mouseleave") {
        point();
        ball = randomBall();
    } else if (ball == 2 && event.type == "click") {
        point();
        ball = randomBall();
    } else if (ball == 3 && event.code == "KeyD") {
        point();
        ball = randomBall();
    }
}

function gameTime() {
    const timerValue = document.getElementById("timer-value");
    let seconds = timerValue.innerHTML;

    ball = randomBall();

    stopwatch = setInterval(() => {
        if (seconds > 0) {
            seconds--;
            timerValue.innerHTML = seconds;
        } else if (seconds == 0) {
            clearInterval(stopwatch);
            resetGameTime();
        }
    }, "1000");
}

function resetGameTime() {
    const timerValue = document.getElementById("timer-value");
    timerValue.innerHTML = 30;

    const ballElement = document.getElementById("ball");
    ballElement.style.backgroundColor = "rgba(206, 203, 203, 0.719)";

    const btn = document.getElementById("start-button");
    btn.innerHTML = "Iniciar";

    ballElement.removeEventListener("click", eventBall);
    ballElement.removeEventListener("mouseleave", eventBall);
    document.removeEventListener("keypress", eventBall);
}

function resetGame() {
    clearInterval(stopwatch);
    resetPoints();
    resetGameTime();
}

function startGame() {
    const ballElement = document.getElementById("ball");

    const btn = document.getElementById("start-button");
    btn.addEventListener("click", startGame);

    if (btn.innerHTML == "Reiniciar") {
        // Remove os eventos do jogo
        ballElement.removeEventListener("click", eventBall);
        ballElement.removeEventListener("mouseleave", eventBall);
        document.removeEventListener("keypress", eventBall);
        // Reseta o jogo
        resetGame();
    } else if (btn.innerHTML == "Iniciar") {
        // Adiciona os eventos do jogo
        ballElement.addEventListener("click", eventBall);
        ballElement.addEventListener("mouseleave", eventBall);
        document.addEventListener("keypress", eventBall);

        // Reinicia o pontos
        resetPoints();
        startButton.innerHTML = "Reiniciar";
        // Inicia o jogo
        gameTime();
    }
}

const startButton = document.getElementById("start-button");
startButton.addEventListener("click", startGame);

let stopwatch = null;
let ball = null;
