document.addEventListener('DOMContentLoaded', () => {
    let randomNumber;
    let maxNumber;
    let attemptsLeft = 3;

    const guessInput = document.getElementById('guessInput');
    const submitBtn = document.getElementById('submitBtn');
    const message = document.getElementById('message');
    const attemptsLeftDisplay = document.getElementById('attemptsLeft');
    const restartBtn = document.getElementById('restartBtn');
    const levelSelect = document.getElementById('levelSelect');

    levelSelect.addEventListener('change', startGame);
    submitBtn.addEventListener('click', makeGuess);
    restartBtn.addEventListener('click', startGame);

    function startGame() {
        attemptsLeft = 3;
        attemptsLeftDisplay.textContent = attemptsLeft;
        message.textContent = '';
        guessInput.value = '';
        guessInput.disabled = false;
        submitBtn.disabled = false;
        restartBtn.style.display = 'none';

        switch (levelSelect.value) {
            case 'easy':
                maxNumber = 10;
                break;
            case 'medium':
                maxNumber = 20;
                break;
            case 'hard':
                maxNumber = 100;
                break;
        }

        randomNumber = Math.floor(Math.random() * maxNumber) + 1;
        guessInput.placeholder = `Digite um número entre 1 e ${maxNumber}`;
    }

    function makeGuess() {
        const userGuess = parseInt(guessInput.value);
        if (isNaN(userGuess) || userGuess < 1 || userGuess > maxNumber) {
            message.textContent = `Por favor, insira um número válido entre 1 e ${maxNumber}.`;
            return;
        }

        attemptsLeft--;
        attemptsLeftDisplay.textContent = attemptsLeft;

        if (userGuess === randomNumber) {
            message.textContent = 'Parabéns! Você acertou o número!';
            message.className = 'success';
            endGame();
        } else if (userGuess > randomNumber) {
            message.textContent = 'Muito alto! Tente novamente.';
            message.className = 'danger';
        } else {
            message.textContent = 'Muito baixo! Tente novamente.';
            message.className = 'danger';
        }

        if (attemptsLeft === 0) {
            message.innerHTML = `<span class="lose">Você perdeu!</span><br>O número correto era ${randomNumber}.`;
            endGame();
        }
    }

    function endGame() {
        guessInput.disabled = true;
        submitBtn.disabled = true;
        restartBtn.style.display = 'inline';
    }

    startGame(); // Inicia o jogo pela primeira vez
});
