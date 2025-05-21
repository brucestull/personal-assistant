document.addEventListener('DOMContentLoaded', () => {
    const startBtn = document.getElementById('start-button');
    const pauseBtn = document.getElementById('pause-button');
    const cancelBtn = document.getElementById('cancel-button');
    const display = document.getElementById('timer-display');
    const durationInput = document.getElementById('duration-input');
    const warningSound = document.getElementById('warning-sound');
    const alarmSound = document.getElementById('alarm-sound');

    let elapsed = 0;
    let intervalId = null;
    let duration = 25 * 60;
    let warningAt = duration - 5 * 60;

    function updateDisplay() {
        const m = String(Math.floor(elapsed / 60)).padStart(2, '0');
        const s = String(elapsed % 60).padStart(2, '0');
        display.textContent = `${m}:${s}`;
    }

    function tick() {
        elapsed++;
        updateDisplay();

        // play warning if configured
        if (warningAt > 0 && elapsed === warningAt) {
            warningSound.play();
        }
        // end of timer
        if (elapsed >= duration) {
            clearInterval(intervalId);
            intervalId = null;
            alarmSound.play();
            cancelBtn.style.display = 'inline-block';
            startBtn.disabled = true;
            pauseBtn.disabled = true;
        }
    }

    startBtn.addEventListener('click', () => {
        // read user input (minutes) and recalc durations
        const mins = parseInt(durationInput.value, 10);
        duration = (isNaN(mins) || mins < 1 ? 1 : mins) * 60;
        warningAt = (mins > 5) ? duration - 5 * 60 : -1;

        if (!intervalId) {
            elapsed = 0;
            updateDisplay();
            startBtn.disabled = true;
            pauseBtn.disabled = false;
            cancelBtn.style.display = 'none';
            alarmSound.pause();
            alarmSound.currentTime = 0;
            intervalId = setInterval(tick, 1000);
        }
    });

    pauseBtn.addEventListener('click', () => {
        if (intervalId) {
            clearInterval(intervalId);
            intervalId = null;
            startBtn.disabled = false;
            pauseBtn.disabled = true;
        }
    });

    cancelBtn.addEventListener('click', () => {
        alarmSound.pause();
        alarmSound.currentTime = 0;
        cancelBtn.style.display = 'none';
        elapsed = 0;
        updateDisplay();
        startBtn.disabled = false;
    });

    updateDisplay();
});
