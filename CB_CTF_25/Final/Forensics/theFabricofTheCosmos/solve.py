#!/usr/bin/env python3
"""
morse_from_audio.py
Read a Morse-code audio file and output Morse symbols (and optionally decode to text).

Assumptions:
- Audio contains a fairly pure tone (CW) keyed on/off (no speech).
- WAV is recommended. Other formats work if soundfile is installed.
- Timing is reasonably consistent (standard Morse ratios ~1:3:7).

Usage:
  python morse_from_audio.py input.wav
  python morse_from_audio.py input.wav --decode
  python morse_from_audio.py input.wav --tone 700          # if you know the CW tone (Hz)
"""

import argparse
import math
import sys
from typing import List, Tuple, Optional

import numpy as np

# Prefer scipy for WAV I/O and filtering; fall back to soundfile if needed
try:
    from scipy.io import wavfile
    from scipy.signal import butter, filtfilt, welch
except ImportError:
    wavfile = None
    butter = filtfilt = welch = None

try:
    import soundfile as sf  # for non-wav formats
except ImportError:
    sf = None

# -------------------- Morse tables --------------------
TEXT_TO_MORSE = {
    'A': '.-',    'B': '-...',  'C': '-.-.', 'D': '-..',   'E': '.',
    'F': '..-.',  'G': '--.',   'H': '....', 'I': '..',    'J': '.---',
    'K': '-.-',   'L': '.-..',  'M': '--',   'N': '-.',    'O': '---',
    'P': '.--.',  'Q': '--.-',  'R': '.-.',  'S': '...',   'T': '-',
    'U': '..-',   'V': '...-',  'W': '.--',  'X': '-..-',  'Y': '-.--',
    'Z': '--..',
    '0': '-----', '1': '.----', '2': '..---','3': '...--', '4': '....-',
    '5': '.....', '6': '-....', '7': '--...', '8': '---..','9': '----.',
    '&': '.-...',  "'": '.----.','@': '.--.-.','(': '-.--.',' )': '-.--.-',
    ':': '---...', ',': '--..--','=': '-...-','!': '-.-.--','.': '.-.-.-',
    '-': '-....-','+': '.-.-.','"': '.-..-.','?': '..--..','/': '-..-.'
}
MORSE_TO_TEXT = {v: k for k, v in TEXT_TO_MORSE.items()}

# -------------------- Audio helpers --------------------
def load_audio(path: str) -> Tuple[int, np.ndarray]:
    """Load audio, return (sample_rate, mono_float32)."""
    if wavfile is not None:
        try:
            sr, data = wavfile.read(path)
            # convert to float32 mono
            if data.dtype.kind in "iu":
                # scale int to [-1, 1]
                maxv = np.iinfo(data.dtype).max
                data = data.astype(np.float32) / maxv
            else:
                data = data.astype(np.float32)
        except Exception:
            sr = None
            data = None
    else:
        sr = None
        data = None

    if data is None and sf is not None:
        data, sr = sf.read(path, dtype='float32', always_2d=True)
        data = data.mean(axis=1)

    if data is None:
        raise RuntimeError(
            "Could not read audio. Install scipy (preferred) or soundfile.\n"
            "pip install scipy soundfile"
        )

    if data.ndim > 1:
        data = data.mean(axis=1)
    return sr, data.astype(np.float32, copy=False)

def butter_bandpass(low, high, fs, order=4):
    nyq = 0.5 * fs
    lowc = max(1.0, low) / nyq
    highc = min(high, nyq * 0.99) / nyq
    b, a = butter(order, [lowc, highc], btype='band')
    return b, a

def dominant_tone_hz(x: np.ndarray, sr: int, fmin=300.0, fmax=2000.0) -> float:
    """Estimate dominant CW tone using Welch periodogram."""
    nperseg = min(8192, max(1024, 2 ** int(np.floor(np.log2(sr * 0.1)))))  # ~0.1s window
    freqs, psd = welch(x, sr, nperseg=nperseg)
    mask = (freqs >= fmin) & (freqs <= fmax)
    if not np.any(mask):
        return 700.0
    peak_idx = np.argmax(psd[mask])
    dom = float(freqs[mask][peak_idx])
    return dom

# -------------------- Morse extraction --------------------
def envelope_from_bandpassed(x: np.ndarray, sr: int, tone_hz: float) -> np.ndarray:
    """Bandpass around tone, rectify, and smooth to get envelope."""
    bw = max(80.0, tone_hz * 0.15)  # generous bandwidth
    low = max(50.0, tone_hz - bw)
    high = tone_hz + bw
    b, a = butter_bandpass(low, high, sr, order=4)
    y = filtfilt(b, a, x)

    # Rectify and smooth (moving average ~10 ms)
    env = np.abs(y)
    win_ms = 10.0
    win = max(1, int(sr * win_ms / 1000.0))
    kernel = np.ones(win) / win
    env = np.convolve(env, kernel, mode='same')
    return env

def binary_keying(env: np.ndarray, sr: int) -> np.ndarray:
    """Convert envelope to binary on/off based on adaptive threshold."""
    # Robust threshold: between median and 90th percentile
    med = np.median(env)
    p90 = np.percentile(env, 90)
    thr = med + 0.35 * (p90 - med)
    # Safety fallback if extremely clean
    if thr <= 1e-8:
        thr = np.mean(env) * 0.5
    on = (env >= thr).astype(np.uint8)

    # Debounce with a small morphological open/close (~10 ms)
    k = max(1, int(sr * 0.01))  # 10 ms
    # Opening: erode then dilate
    on = _morph_open(on, k)
    # Closing: dilate then erode
    on = _morph_close(on, k)
    return on

def _morph_open(x: np.ndarray, k: int) -> np.ndarray:
    if k <= 1:
        return x
    # Erode
    er = np.convolve(x, np.ones(k, dtype=int), 'same') == k
    # Dilate
    di = np.convolve(er.astype(int), np.ones(k, dtype=int), 'same') > 0
    return di.astype(np.uint8)

def _morph_close(x: np.ndarray, k: int) -> np.ndarray:
    if k <= 1:
        return x
    # Dilate
    di = np.convolve(x, np.ones(k, dtype=int), 'same') > 0
    # Erode
    er = np.convolve(di.astype(int), np.ones(k, dtype=int), 'same') == k
    return er.astype(np.uint8)

def segments_from_binary(on: np.ndarray, sr: int) -> Tuple[List[float], List[float]]:
    """Return lists of on-durations and off-durations in milliseconds."""
    # Find edges
    diff = np.diff(on.astype(int), prepend=on[0])
    # positions where rising edge (0->1) and falling edge (1->0)
    rises = np.where(diff == 1)[0]
    falls = np.where(diff == -1)[0]

    # Fix if we start in 'on' state
    if on[0] == 1:
        rises = np.insert(rises, 0, 0)
    if on[-1] == 1:
        falls = np.append(falls, len(on) - 1)

    on_durs = []
    off_durs = []
    last_edge = 0
    for r, f in zip(rises, falls):
        # off duration before this pulse
        if r > last_edge:
            off_dur_ms = (r - last_edge) * 1000.0 / sr
            off_durs.append(off_dur_ms)
        # on duration
        on_dur_ms = (f - r) * 1000.0 / sr
        on_durs.append(on_dur_ms)
        last_edge = f

    # Trailing off duration (not usually needed)
    if last_edge < len(on) - 1:
        off_dur_ms = (len(on) - 1 - last_edge) * 1000.0 / sr
        off_durs.append(off_dur_ms)

    # Remove possible leading/trailing zeros
    on_durs = [d for d in on_durs if d > 0.1]
    off_durs = [d for d in off_durs if d > 0.1]
    return on_durs, off_durs

def estimate_unit_ms(on_durs: List[float], off_durs: List[float]) -> float:
    """Estimate the Morse 'unit' (dot length) in ms from duration distributions."""
    if not on_durs and not off_durs:
        raise RuntimeError("No signal segments detected; check audio or thresholding.")
    durs = np.array(on_durs + off_durs, dtype=np.float64)
    # Use robust lower-quantiles: the unit tends to be the small cluster center
    base = np.median(durs[durs <= np.percentile(durs, 35)])  # lower third median
    # Clamp to sensible bounds (20–300 ms typical)
    base = float(np.clip(base, 20.0, 300.0))
    return base

def classify_morse(on_durs: List[float], off_durs: List[float], unit: float) -> str:
    """
    Convert on/off durations to a Morse string:
    - dot '.' if on < 2*unit, else '-' (dash)
    - gap rules:
        intra-character gap: < 2*unit -> no separator
        inter-character gap: < 5*unit -> ' ' (space)
        word gap: >= 5*unit  -> ' / ' (slash)
    """
    symbols = []
    # Iterate pairs: off (before), on, off, on, ...
    # We built them as off-before-first, on1, off1, on2, ...
    # Start with an initial gap (ignore leading gap)
    # Create iterators with the same length by padding off_durs
    off_iter = list(off_durs)
    if off_iter:
        off_iter = off_iter[1:]  # drop the leading gap before first tone

    # Classify each on-duration
    tones = [('.' if d < 2.0 * unit else '-') for d in on_durs]

    # Build Morse string with gaps
    for i, tone in enumerate(tones):
        symbols.append(tone)
        # Append gap classification if there's a following gap
        if i < len(off_iter):
            g = off_iter[i]
            if g < 2.0 * unit:
                # intra-character: no separator
                pass
            elif g < 5.0 * unit:
                symbols.append(' ')
            else:
                symbols.append(' / ')
    return ''.join(symbols).strip()

def decode_morse(morse: str) -> str:
    """Decode morse ('.' and '-') with spaces between letters and ' / ' between words."""
    words = []
    for word in morse.split(' / '):
        letters = []
        for sym in word.strip().split(' '):
            if not sym:
                continue
            letters.append(MORSE_TO_TEXT.get(sym, '?'))
        words.append(''.join(letters))
    return ' '.join(words)

# -------------------- Main pipeline --------------------
def morse_from_audio(
    path: str,
    known_tone_hz: Optional[float] = None
) -> Tuple[str, float, float]:
    """
    Return (morse_string, tone_hz, unit_ms)
    """
    sr, x = load_audio(path)
    # Normalize
    x = x / (np.max(np.abs(x)) + 1e-9)

    # Light high-pass to kill hum
    if butter is not None:
        from scipy.signal import butter as _butter, filtfilt as _filtfilt
        b, a = _butter(2, 100.0 / (0.5 * sr), btype='high')
        x = _filtfilt(b, a, x)

    # Detect or use provided tone
    if known_tone_hz is None:
        if welch is None:
            tone_hz = 700.0
        else:
            tone_hz = dominant_tone_hz(x, sr)
    else:
        tone_hz = float(known_tone_hz)

    # Envelope
    env = envelope_from_bandpassed(x, sr, tone_hz)

    # Binary keying
    on = binary_keying(env, sr)

    # Segment durations
    on_durs, off_durs = segments_from_binary(on, sr)

    # Estimate unit
    unit = estimate_unit_ms(on_durs, off_durs)

    # Classify to Morse
    morse = classify_morse(on_durs, off_durs, unit)
    return morse, tone_hz, unit

def main():
    ap = argparse.ArgumentParser(description="Extract Morse code from audio.")
    ap.add_argument("input", help="Input audio file (WAV recommended).")
    ap.add_argument("--decode", action="store_true", help="Also decode Morse to text.")
    ap.add_argument("--tone", type=float, default=None, help="Known CW tone in Hz (skip autodetect).")
    args = ap.parse_args()

    try:
        morse, tone_hz, unit = morse_from_audio(args.input, args.tone)
    except Exception as e:
        print(f"[!] Error: {e}", file=sys.stderr)
        sys.exit(1)

    print(f"# Detected tone: {tone_hz:.1f} Hz")
    print(f"# Estimated unit: {unit:.1f} ms (dot length)")
    print("MORSE:")
    print(morse)
    if args.decode:
        print("\nDECODED:")
        print(decode_morse(morse))

if __name__ == "__main__":
    main()
