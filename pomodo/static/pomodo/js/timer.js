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

  // NEW: Audio test controls
  const testBtn       = document.getElementById('test-audio-button');
  const testSelect    = document.getElementById('test-sound-select');
  const testStatus    = document.getElementById('audio-test-status');

  let elapsed          = 0;
  let intervalId       = null;
  let duration         = 25 * 60;
  let warningAt        = duration - 5 * 60;
  let originalDuration = duration;  // store the “locked-in” run length

  // NEW: web audio context (lazy)
  let audioCtx = null;

  function pad(n) { return String(n).padStart(2, '0'); }

  function updateDisplay() {
    const remaining = Math.max(duration - elapsed, 0);
    remainingDisp.textContent = `${pad(Math.floor(remaining/60))}:${pad(remaining%60)}`;
    elapsedDisp.textContent   = `${pad(Math.floor(elapsed/60))}:${pad(elapsed%60)}`;
  }

  function tick() {
    elapsed++;
    updateDisplay();
    if (warningAt > 0 && elapsed === warningAt) {
      // reset position and play warning once
      try {
        warningSound.currentTime = 0;
        warningSound.play();
      } catch (e) {
        console.warn('Warning sound failed:', e);
      }
    }

    if (elapsed >= duration) {
      clearInterval(intervalId);
      intervalId = null;
      try {
        alarmSound.currentTime = 0;
        alarmSound.play();
      } catch (e) {
        console.warn('Alarm sound failed:', e);
      }

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
    startBtn.disabled         = true;
    startBtn.textContent      = 'Sturt';  // revert label
    pauseBtn.disabled         = false;
    pauseBtn.style.display    = 'inline-block';
    continueBtn.style.display = 'none';
    cancelBtn.style.display   = 'none';
    alarmSound.pause();
    alarmSound.currentTime    = 0;

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

  // —— NEW: Audio Test Helpers ——
  function setTestStatus(msg) {
    if (testStatus) testStatus.textContent = msg || '';
  }

  async function playElementFor(el, ms = 1500, volume = 0.75) {
    const originalVolume = el.volume;
    const originalLoop   = el.loop;
    try {
      el.loop = false;          // ensure we don't keep looping during the short test
      el.currentTime = 0;
      el.volume = volume;
      await el.play();
      await new Promise((r) => setTimeout(r, ms));
    } finally {
      el.pause();
      el.currentTime = 0;
      el.volume = originalVolume;
      el.loop   = originalLoop;
    }
  }

  async function playBeep(freq = 880, durationMs = 450, type = 'sine') {
    // Create (or reuse) a single AudioContext—button click counts as a user gesture
    if (!audioCtx) {
      const Ctx = window.AudioContext || window.webkitAudioContext;
      audioCtx = new Ctx();
    }
    if (audioCtx.state === 'suspended') {
      await audioCtx.resume();
    }

    const osc  = audioCtx.createOscillator();
    const gain = audioCtx.createGain();

    osc.type = type;
    osc.frequency.value = freq;

    osc.connect(gain);
    gain.connect(audioCtx.destination);

    const now = audioCtx.currentTime;
    gain.gain.setValueAtTime(0.0001, now);
    gain.gain.exponentialRampToValueAtTime(0.5, now + 0.02); // quick fade-in

    osc.start(now);

    const endTime = now + durationMs / 1000;
    gain.gain.exponentialRampToValueAtTime(0.0001, endTime); // fade-out
    osc.stop(endTime + 0.05);

    return new Promise((resolve) => {
      osc.onended = resolve;
    });
  }

  // —— NEW: Test button wiring ——
  if (testBtn && testSelect) {
    testBtn.addEventListener('click', async () => {
      // If timer alarm is blaring, pause it so test is audible
      try { alarmSound.pause(); } catch (_) {}

      const choice = testSelect.value;
      try {
        if (choice === 'beep') {
          setTestStatus('Playing simple beep…');
          await playBeep(880, 450, 'sine');
          setTestStatus('Beep done.');
        } else {
          const el = choice === 'warning' ? warningSound : alarmSound;
          setTestStatus(`Playing ${choice} sound…`);
          await playElementFor(el, 2000, 0.75);
          setTestStatus('Test complete.');
        }
      } catch (err) {
        // Fallback to generated beep if file playback fails
        try {
          setTestStatus('Sound file failed—playing simple beep fallback…');
          await playBeep(880, 450, 'sine');
          setTestStatus('Beep done.');
        } catch (e2) {
          setTestStatus('Unable to play audio. Check system/browser sound settings.');
          console.error('Audio test failed:', err, e2);
        }
      }
    });
  }

  // initialize
  updateDisplay();
});
