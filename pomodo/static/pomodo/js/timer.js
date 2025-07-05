document.addEventListener('DOMContentLoaded', () => {
  const startBtn      = document.getElementById('start-button');
  const pauseBtn      = document.getElementById('pause-button');
  const continueBtn   = document.getElementById('continue-button');
  const cancelBtn     = document.getElementById('cancel-button');
  const remainingDisp = document.getElementById('remaining-display');
  const elapsedDisp   = document.getElementById('elapsed-display');
  const durationInput = document.getElementById('duration-input');
  const warningSound  = document.getElementById('warning-sound');
  const alarmSound    = document.getElementById('alarm-sound');

  let elapsed          = 0;
  let intervalId       = null;
  let duration         = 25 * 60;
  let warningAt        = duration - 5 * 60;
  let originalDuration = duration;  // store the “locked-in” run length

  function pad(n) { return String(n).padStart(2, '0'); }

  function updateDisplay() {
    const remaining = Math.max(duration - elapsed, 0);
    remainingDisp.textContent = `${pad(Math.floor(remaining/60))}:${pad(remaining%60)}`;
    elapsedDisp.textContent   = `${pad(Math.floor(elapsed/60))}:${pad(elapsed%60)}`;
  }

  function tick() {
    elapsed++;
    updateDisplay();
    if (warningAt > 0 && elapsed === warningAt) warningSound.play();

    if (elapsed >= duration) {
      clearInterval(intervalId);
      intervalId = null;
      alarmSound.play();

      // show reset opportunity
      cancelBtn.style.display   = 'inline-block';
      pauseBtn.disabled         = true;
      continueBtn.style.display = 'none';

      startBtn.disabled   = false;
      startBtn.textContent = 'ReSturt';
    }
  }

  startBtn.addEventListener('click', () => {
    const isRestart = startBtn.textContent === 'ReSturt';

    if (!isRestart) {
      // fresh start → stamp in originalDuration from the input
      const mins = parseInt(durationInput.value, 10);
      originalDuration = (isNaN(mins) || mins < 1 ? 1 : mins) * 60;
    }

    // set runtime & warning
    duration  = originalDuration;
    warningAt = originalDuration > 5*60 ? originalDuration - 5*60 : -1;

    // reset and kick off
    elapsed = 0;
    updateDisplay();
    startBtn.disabled        = true;
    startBtn.textContent     = 'Sturt';  // revert label
    pauseBtn.disabled        = false;
    pauseBtn.style.display   = 'inline-block';
    continueBtn.style.display= 'none';
    cancelBtn.style.display  = 'none';
    alarmSound.pause();
    alarmSound.currentTime   = 0;

    intervalId = setInterval(tick, 1000);
  });

  pauseBtn.addEventListener('click', () => {
    if (!intervalId) return;
    clearInterval(intervalId);
    intervalId = null;

    // hide pause, show continue, and activate restart
    pauseBtn.style.display    = 'none';
    continueBtn.style.display = 'inline-block';
    startBtn.disabled         = false;
    startBtn.textContent      = 'ReSturt';
  });

  continueBtn.addEventListener('click', () => {
    if (intervalId) return;
    intervalId = setInterval(tick, 1000);

    // swap back to running state
    continueBtn.style.display = 'none';
    pauseBtn.style.display    = 'inline-block';
    startBtn.disabled         = true;
    startBtn.textContent      = 'Sturt';
  });

  cancelBtn.addEventListener('click', () => {
    clearInterval(intervalId);
    intervalId = null;
    alarmSound.pause();
    alarmSound.currentTime    = 0;

    // full reset
    elapsed = 0;
    updateDisplay();
    startBtn.disabled         = false;
    startBtn.textContent      = 'Sturt';
    pauseBtn.disabled         = true;
    pauseBtn.style.display    = 'inline-block';
    continueBtn.style.display = 'none';
    cancelBtn.style.display   = 'none';
  });

  // initialize
  updateDisplay();
});
