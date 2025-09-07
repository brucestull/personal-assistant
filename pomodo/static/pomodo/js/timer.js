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

  // NEW: time/apply & stop controls
  const applyBtn      = document.getElementById('apply-time-button');
  const stopBtn       = document.getElementById('stop-button');

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

  // NEW: small UI state helpers
  function enterRunningState() {
    startBtn.disabled         = true;
    startBtn.textContent      = 'Sturt';
    pauseBtn.disabled         = false;
    pauseBtn.style.display    = 'inline-block';
    continueBtn.style.display = 'none';
    cancelBtn.style.display   = 'none';
    stopBtn.disabled          = false;
  }
  function enterIdleState() {
    startBtn.disabled         = false;
    startBtn.textContent      = 'Sturt';
    pauseBtn.disabled         = true;
    pauseBtn.style.display    = 'inline-block';
    continueBtn.style.display = 'none';
    cancelBtn.style.display   = 'none';
    stopBtn.disabled          = true;
  }

  function lockInDurationFromInput() {
    const mins = parseInt(durationInput.value, 10);
    originalDuration = (isNaN(mins) || mins < 1 ? 1 : mins) * 60;
    duration  = originalDuration;
    warningAt = originalDuration > 5*60 ? originalDuration - 5*60 : -1;
  }

  function stopInterval() {
    if (intervalId) {
      clearInterval(intervalId);
      intervalId = null;
    }
  }

  function tick() {
    elapsed++;
    updateDisplay();
    if (warningAt > 0 && elapsed === warningAt) {
      try {
        warningSound.currentTime = 0;
        warningSound.play();
      } catch (e) {
        console.warn('Warning sound failed:', e);
      }
    }

    if (elapsed >= duration) {
      stopInterval();
      try {
        alarmSound.currentTime = 0;
        alarmSound.play();
      } catch (e) {
        console.warn('Alarm sound failed:', e);
      }

      cancelBtn.style.display   = 'inline-block';
      pauseBtn.disabled         = true;
      continueBtn.style.display = 'none';

      startBtn.disabled   = false;
      startBtn.textContent = 'ReSturt';
      stopBtn.disabled     = true;
    }
  }

  startBtn.addEventListener('click', () => {
    const isRestart = startBtn.textContent === 'ReSturt';

    if (!isRestart) {
      // fresh start → stamp in originalDuration from the input
      lockInDurationFromInput();
    } else {
      // restart uses last applied `originalDuration`
      duration  = originalDuration;
      warningAt = originalDuration > 5*60 ? originalDuration - 5*60 : -1;
    }

    elapsed = 0;
    updateDisplay();

    alarmSound.pause();
    alarmSound.currentTime = 0;

    enterRunningState();
    stopInterval();
    intervalId = setInterval(tick, 1000);
  });

  pauseBtn.addEventListener('click', () => {
    if (!intervalId) return;
    stopInterval();

    // hide pause, show continue, and activate restart
    pauseBtn.style.display    = 'none';
    continueBtn.style.display = 'inline-block';
    startBtn.disabled         = false;
    startBtn.textContent      = 'ReSturt';
    stopBtn.disabled          = false; // still allow hard stop while paused
  });

  continueBtn.addEventListener('click', () => {
    if (intervalId) return;
    intervalId = setInterval(tick, 1000);

    continueBtn.style.display = 'none';
    pauseBtn.style.display    = 'inline-block';
    startBtn.disabled         = true;
    startBtn.textContent      = 'Sturt';
    stopBtn.disabled          = false;
  });

  cancelBtn.addEventListener('click', () => {
    stopInterval();
    alarmSound.pause();
    alarmSound.currentTime = 0;

    elapsed = 0;
    duration = originalDuration;
    updateDisplay();
    enterIdleState();
  });

  // —— NEW: Apply time (Enter key also applies) —— //
  if (applyBtn) {
    applyBtn.addEventListener('click', () => {
      const wasRunning = !!intervalId;

      // stop current countdown/alarm
      stopInterval();
      alarmSound.pause();
      alarmSound.currentTime = 0;

      // lock in new time and reset to 00:00 of that time
      lockInDurationFromInput();
      elapsed = 0;
      updateDisplay();

      if (wasRunning) {
        // auto-restart with the new length
        enterRunningState();
        intervalId = setInterval(tick, 1000);
      } else {
        // leave idle; user can press Start
        enterIdleState();
      }
    });
  }

  if (durationInput) {
    durationInput.addEventListener('keydown', (e) => {
      if (e.key === 'Enter') {
        e.preventDefault();
        applyBtn?.click();
      }
    });
  }

  // —— NEW: Stop Now —— //
  if (stopBtn) {
    stopBtn.addEventListener('click', () => {
      // stop everything and reset to last applied duration
      stopInterval();
      alarmSound.pause();
      alarmSound.currentTime = 0;

      elapsed  = 0;
      duration = originalDuration;
      updateDisplay();
      enterIdleState();
    });
  }

  // —— Audio Test Helpers (unchanged logic) —— //
  function setTestStatus(msg) {
    if (testStatus) testStatus.textContent = msg || '';
  }

  async function playElementFor(el, ms = 1500, volume = 0.75) {
    const originalVolume = el.volume;
    const originalLoop   = el.loop;
    try {
      el.loop = false;
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
    gain.gain.exponentialRampToValueAtTime(0.5, now + 0.02);

    osc.start(now);

    const endTime = now + durationMs / 1000;
    gain.gain.exponentialRampToValueAtTime(0.0001, endTime);
    osc.stop(endTime + 0.05);

    return new Promise((resolve) => {
      osc.onended = resolve;
    });
  }

  if (testBtn && testSelect) {
    testBtn.addEventListener('click', async () => {
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
  enterIdleState();
});
