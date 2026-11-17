#!/usr/bin/env python3
"""The Whistle: sound stems written in code (numpy). Every layer is a pure function of the seed.
Writes audio/stems/*.wav (48 kHz stereo float WAV) and audio/mix.json for tools/mix.py.
Identity: pressure. Muffled, close beds; one clear whistle breaks through; silence when the reply is missing."""
import json, os, wave
import numpy as np

SR, DUR = 48000, 60.0
N = int(SR * DUR)
T = np.arange(N) / SR
RNG = np.random.default_rng(7)
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'stems')
os.makedirs(OUT, exist_ok=True)


def sstep(a, b, x):
    t = np.clip((np.asarray(x) - a) / (b - a), 0, 1)
    return t * t * (3 - 2 * t)


def fft_filter(x, lo=None, hi=None, edge=0.15):
    """Zero-phase band filter with soft edges (fraction of the corner frequency)."""
    n = len(x)
    X = np.fft.rfft(x)
    f = np.fft.rfftfreq(n, 1 / SR)
    g = np.ones_like(f)
    if hi is not None:
        g *= 1 - sstep(hi * (1 - edge), hi * (1 + edge), f)
    if lo is not None:
        g *= sstep(lo * (1 - edge), lo * (1 + edge), f)
    return np.fft.irfft(X * g, n)


def noise(n=N, lo=None, hi=None):
    return fft_filter(RNG.standard_normal(n), lo, hi)


def stereo_noise(lo=None, hi=None):
    return np.stack([noise(N, lo, hi), noise(N, lo, hi)], axis=1)


def norm(x, peak=0.9):
    m = np.max(np.abs(x))
    return x * (peak / m) if m > 0 else x


def write_wav(name, y):
    y = np.clip(y, -1, 1)
    pcm = (y * 32767).astype('<i2')
    with wave.open(os.path.join(OUT, name), 'wb') as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())


def reverb_ir(seconds=2.6, decay=0.75, seed=3):
    r = np.random.default_rng(seed)
    n = int(SR * seconds)
    t = np.arange(n) / SR
    ir = r.standard_normal((n, 2)) * np.exp(-t / decay)[:, None]
    for c in range(2):
        ir[:, c] = fft_filter(ir[:, c], hi=3800)
    for d, a in ((0.031, 0.5), (0.057, 0.35), (0.089, 0.25)):          # early reflections from the rock face
        k = int(d * SR)
        ir[k, 0] += a; ir[k + 37, 1] += a * 0.8
    return ir / np.sqrt(np.sum(ir ** 2, axis=0))


IR = reverb_ir()


def convolve(y, ir=IR):
    n = len(y) + len(ir) - 1
    size = 1 << (n - 1).bit_length()
    out = np.zeros((len(y), 2))
    for c in range(2):
        src = y[:, c] if y.ndim == 2 else y
        out[:, c] = np.fft.irfft(np.fft.rfft(src, size) * np.fft.rfft(ir[:, c], size), size)[:len(y)]
    return out


# ------------------------------------------------------------------ whistle voice
# a note: (start s, dur s, f0 Hz, f1 Hz, amp); phrases are what the neighbours say, in whistled speech
PHRASES = {
    'call_light':  [(0.00, .22, 2300, 2700, 1), (.30, .14, 2700, 2700, .9), (.50, .30, 2100, 2500, 1), (.90, .12, 2500, 2500, .8), (1.08, .50, 2900, 2000, 1)],
    'reply_morn':  [(0.00, .28, 1900, 2300, 1), (.38, .20, 2300, 2300, .85), (.65, .25, 2300, 1750, 1), (1.00, .14, 1750, 1750, .8), (1.20, .40, 1750, 2100, 1), (1.70, .30, 2100, 1800, .8)],
    'call_wind':   [(0.00, .18, 2400, 2800, 1), (.25, .18, 2800, 2400, .9), (.50, .30, 2400, 3000, 1), (.90, .12, 3000, 3000, .8), (1.10, .50, 3000, 2300, 1)],
    'reply_wash':  [(0.00, .30, 1800, 2100, 1), (.40, .15, 2100, 2100, .85), (.62, .15, 2300, 2300, .85), (.85, .40, 2300, 1700, 1), (1.40, .40, 1700, 1900, .8)],
    'call_ask':    [(0.00, .20, 2000, 2000, .9), (.30, .40, 2000, 2900, 1), (.78, .16, 2900, 2900, .9)],
    'call_loud':   [(0.00, .25, 2600, 3100, 1), (.35, .25, 3100, 2500, 1), (.70, .20, 2500, 3100, 1), (1.00, .55, 3100, 2700, 1)],
}


def whistle(phrase, breath=0.05, vib=0.012, seed=0):
    """Dry mono whistle for one phrase: a pure tone with a small second harmonic, vibrato and breath noise."""
    r = np.random.default_rng(100 + seed)
    notes = PHRASES[phrase]
    length = max(s + d for s, d, *_ in notes) + 0.4
    n = int(length * SR)
    y = np.zeros(n)
    t = np.arange(n) / SR
    for s, d, f0, f1, a in notes:
        i0, i1 = int(s * SR), int((s + d) * SR)
        m = i1 - i0
        u = np.linspace(0, 1, m, endpoint=False)
        gl = f0 + (f1 - f0) * (u * u * (3 - 2 * u))
        gl = gl * (1 + vib * np.sin(2 * np.pi * 5.4 * t[:m] + seed) * sstep(0.08, 0.22, t[:m]))
        ph = 2 * np.pi * np.cumsum(gl) / SR
        tone = np.sin(ph) + 0.1 * np.sin(2 * ph) + 0.03 * np.sin(3 * ph)
        att, rel = int(0.025 * SR), int(0.07 * SR)
        env = np.ones(m)
        env[:att] = np.linspace(0, 1, att)
        env[-rel:] *= np.linspace(1, 0, rel)
        hiss = fft_filter(r.standard_normal(m), lo=max(f0, f1) * 0.7, hi=max(f0, f1) * 1.3) * 7 * breath
        y[i0:i1] += (tone + hiss) * env * a * 0.5
    return y


def place(buf, mono, at, gain_db=0.0, pan=0.0, lp=None):
    """Mix a mono source into a stereo buffer at time `at` s with gain, equal-power pan and an optional low-pass."""
    x = mono.copy()
    if lp:
        x = fft_filter(x, hi=lp)
    g = 10 ** (gain_db / 20)
    th = (pan + 1) * np.pi / 4
    i0 = int(at * SR)
    i1 = min(N, i0 + len(x))
    buf[i0:i1, 0] += x[:i1 - i0] * g * np.cos(th)
    buf[i0:i1, 1] += x[:i1 - i0] * g * np.sin(th)


# ------------------------------------------------------------------ the timeline (matches engine/whistle.html)
# near: the keeper's own whistles, dry and close; far: replies from the other rock, low-passed and in the air
CLOSE = [  # (phrase, at, gain_db, pan, seed, lowpass)
    ('call_light', 0.00, -4, 0.0, 1, None),     # S01 hook: whistle on frame 1
    ('call_light', 7.20, -15, 0.25, 2, 7000),    # S02 seen from 125 m
    ('call_wind', 15.20, -4, 0.1, 3, None),     # S03 beside him
    ('call_light', 31.20, -15, 0.25, 4, 7000),   # S05 same far view, no answer follows
    ('call_ask', 40.00, -3, 0.0, 5, None),      # S06
    ('call_loud', 43.20, -1, 0.0, 6, None),     # S06 louder, the wind takes it
    ('reply_morn', 47.00, -3, 0.0, 7, None),    # S07 he whistles the neighbour's reply himself
]
FAR = [    # replies from the far rock: (phrase, at, gain_db, pan, seed)
    ('reply_morn', 10.20, -8, -0.55, 11),       # S02
    ('reply_wash', 18.20, -9, -0.5, 12),        # S03
    ('reply_morn', 55.40, -12, -0.5, 13),       # S08, faint: friend or echo
]

dry = np.zeros((N, 2))
far = np.zeros((N, 2))
for ph, at, g, pan, sd, lp in CLOSE:
    place(dry, whistle(ph, seed=sd), at, g, pan, lp)
sends = np.zeros((N, 2))                                     # what goes to the shared open-air reverb
for ph, at, g, pan, sd, lp in CLOSE:
    place(sends, whistle(ph, seed=sd), at, g - 6, pan, lp or 7000)
for ph, at, g, pan, sd in FAR:
    w = whistle(ph, breath=0.12, vib=0.02, seed=sd)
    place(far, w, at, g, pan, lp=4200)
    place(sends, w, at, g + 2, pan, lp=4200)
# S08's reply comes back a second time off the cliff: the same phrase, later and fainter, so it could be an echo
echo = whistle('reply_morn', breath=0.14, vib=0.022, seed=14)
place(far, echo, 55.40 + 2.35, -20, -0.45, lp=3200)
place(sends, echo, 55.40 + 2.35, -17, -0.45, lp=3200)
wet = convolve(sends)
write_wav('whistles-close.wav', dry * 0.8)
write_wav('whistles-far.wav', (far * 0.8 + wet * 0.55))

# ------------------------------------------------------------------ beds
# surf: low swell breaths every ~9 s plus a hiss that rises with each wave; muffled, never bright
swell = (0.5 + 0.5 * np.sin(2 * np.pi * T / 9.3 + 0.7)) ** 1.8
surf = stereo_noise(60, 520) * (0.35 + 0.65 * swell)[:, None] * 1.3
surf += stereo_noise(500, 2400) * (0.06 + 0.22 * swell ** 2)[:, None]
quiet = 1 - 0.55 * sstep(33.4, 34.2, T) * (1 - sstep(38.2, 38.8, T))   # the missing reply: surf only, nothing else
write_wav('sea.wav', norm(surf) * 0.8)

# wind: band-passed rush, rising through S06 (38 to 46), easing in S07, thinner outside the gallery shots
wl = 0.18 + 0.35 * sstep(14, 16, T) * (1 - sstep(22, 23, T)) + 0.22 * sstep(30, 31, T)
wl = wl + 0.75 * sstep(38, 43.5, T) * (1 - sstep(45.6, 47.0, T)) + 0.2 * sstep(54, 57, T)
wl = wl * (0.85 + 0.15 * np.sin(2 * np.pi * T / 4.1)) * (1 - 0.4 * (T > 22) * (T < 30))
wind = np.stack([noise(N, 160, 900), noise(N, 160, 900)], axis=1) * wl[:, None]
wind += np.stack([noise(N, 900, 2600), noise(N, 900, 2600)], axis=1) * (0.12 * wl ** 2)[:, None]
write_wav('wind.wav', norm(wind) * 0.8)

# room and mechanism: lamp motor hum while the lamp turns, a low interior tone for the tally room (S04)
hum = np.sin(2 * np.pi * 96 * T) + 0.4 * np.sin(2 * np.pi * 192 * T + 1) + 0.15 * np.sin(2 * np.pi * 288 * T)
hum_env = (T < 2.4) * (1 - sstep(1.2, 2.4, T) * 0.9) + ((T >= 30) & (T < 56.2)) * 0.45 + (T >= 56.2) * 0.45 * (1 - sstep(56.2, 57.6, T))
hum_env = hum_env * sstep(0, 0.05, T) * (1 - 0.85 * sstep(33.4, 34.0, T) * (1 - sstep(38, 38.6, T)))
room = hum * hum_env * 0.09
room_tone = (noise(N, 40, 260) * 0.8 + np.sin(2 * np.pi * 55 * T) * 0.25) * (sstep(21.6, 22.6, T) * (1 - sstep(29.4, 30.2, T)))
room_tone *= 0.25
write_wav('room.wav', np.stack([room + room_tone, room * 0.95 + room_tone * 1.05], axis=1))

# ------------------------------------------------------------------ foley and one-off sounds
foley = np.zeros((N, 2))


def click(at, gain_db=-8, pan=-0.2):            # brass lever: a short knock and a ring
    n = int(0.25 * SR); t = np.arange(n) / SR
    x = np.sin(2 * np.pi * 1200 * t) * np.exp(-t / 0.012) + 0.6 * np.sin(2 * np.pi * 410 * t) * np.exp(-t / 0.045) + noise(n, 2000, 6000) * np.exp(-t / 0.006) * 0.6
    place(foley, x, at, gain_db, pan)


click(2.25)
click(2.42, -14)                               # the lever settles
# fingertip over plaster (S04): a dry scrape while the finger travels along the marks
for i in range(14):
    a0 = 23.5 + i * 0.4 + (i % 3) * 0.03
    n = int(0.22 * SR); t = np.arange(n) / SR
    x = noise(n, 2500, 7000) * np.sin(np.pi * t / 0.22) ** 2 * 0.35
    place(foley, x, a0, -17 + (i % 2) * 2, 0.1)
# tally scratches: a single harder scratch each time the finger passes a mark
for a0 in (24.1, 25.3, 26.5, 27.7):
    n = int(0.12 * SR); t = np.arange(n) / SR
    place(foley, noise(n, 1500, 6500) * np.exp(-t / 0.05) * 0.8, a0, -14, 0.15)
# oil lamp ticks
for i in range(16):
    a0 = 22.2 + RNG.random() * 7.5
    n = int(0.01 * SR)
    place(foley, noise(n, 3000, 9000) * np.hanning(n), a0, -26, 0.4)
# rail creak (S06) and gallery boots
for a0, g in ((40.6, -16), (44.0, -14)):
    n = int(0.55 * SR); t = np.arange(n) / SR
    f = 260 + 90 * np.sin(2 * np.pi * 3.0 * t) + 40 * t * 8
    place(foley, np.sin(2 * np.pi * np.cumsum(f) / SR) * np.sin(np.pi * t / 0.55) * 0.5 + noise(n, 400, 2200) * 0.12, a0, g, -0.3, lp=2400)
write_wav('foley.wav', foley)

gulls = np.zeros((N, 2))


def gull(at, gain_db, pan, f=1700):
    n = int(0.9 * SR); t = np.arange(n) / SR
    out = np.zeros(n)
    for k, (s, d) in enumerate(((0.0, 0.38), (0.45, 0.3))):
        i0 = int(s * SR); m = int(d * SR); u = np.linspace(0, 1, m)
        fr = f * (1.35 - 0.7 * u + 0.12 * np.sin(2 * np.pi * 14 * u))
        ph = 2 * np.pi * np.cumsum(fr) / SR
        x = (np.sin(ph) + 0.5 * np.sin(2 * ph) + 0.3 * np.sin(3 * ph)) * np.sin(np.pi * u) ** 0.6 * 0.4
        out[i0:i0 + m] += x
    place(gulls, out, at, gain_db, pan, lp=5200)


for a0, g, p in ((12.4, -22, -0.3), (17.6, -20, 0.5), (21.3, -23, -0.4), (36.2, -24, 0.3), (51.6, -24, -0.2)):
    gull(a0, g, p)
write_wav('gulls.wav', convolve(gulls, IR[:int(SR * 1.1)]) * 0.6 + gulls * 0.5)

# ------------------------------------------------------------------ music: a drone and a four-note figure taken from the whistle phrase
mus = np.zeros((N, 2))
d_env = 0.4 * sstep(0.5, 4, T) * (1 - sstep(29.6, 31.0, T) * (1 - sstep(41.0, 43.0, T)) * 1.0)
d_env = np.where((T > 31.0) & (T < 41.0), 0, d_env)
d_env = d_env + 0.0
d_env = np.where(T >= 41.0, 0.5 * sstep(41.0, 45.0, T) * (1 - sstep(46.5, 47.4, T) * 0.8) + 0.5 * sstep(50.5, 53.0, T) * 0.0, d_env)
drone = (np.sin(2 * np.pi * 73.42 * T) + 0.5 * np.sin(2 * np.pi * 110.0 * T + 1) + 0.25 * np.sin(2 * np.pi * 146.84 * T + 2)) * (0.8 + 0.2 * np.sin(2 * np.pi * T / 11))
drone = fft_filter(drone, hi=420)
mus += np.stack([drone, drone * 0.98], axis=1) * d_env[:, None] * 0.28


def figure(at, notes, gain_db, lp=900):
    """Four slow, soft notes (sine plus a quiet octave): the contour of the whistle call, played low."""
    for k, (f, d) in enumerate(notes):
        n = int(d * SR); t = np.arange(n) / SR
        x = (np.sin(2 * np.pi * f * t) + 0.3 * np.sin(4 * np.pi * f * t)) * np.exp(-t / (d * 0.55)) * np.minimum(1, t / 0.02)
        place(mus, x, at + sum(dd for _, dd in notes[:k]), gain_db, 0.0, lp=lp)


F4 = [(293.66, 1.0), (349.23, 1.0), (329.63, 1.0), (220.0, 2.2)]          # D F E A: up, back, down
figure(22.4, F4, -22)                                                       # S04, over the tally
figure(54.2, [(293.66, 1.1), (349.23, 1.1), (440.0, 1.3), (587.33, 3.0)], -20, lp=1500)   # S08: the same shape, opened upward
wetm = convolve(mus * 0.7, IR[:int(SR * 2.0)])
write_wav('music.wav', mus * 0.8 + wetm * 0.35)

# ------------------------------------------------------------------ mix plan for tools/mix.py
plan = {
    'duration': DUR, 'out': 'audio/mix-v1.wav',
    'layers': [
        {'file': 'audio/stems/sea.wav', 'at': 0.0, 'gain_db': -17, 'bus': 'ambience'},
        {'file': 'audio/stems/wind.wav', 'at': 0.0, 'gain_db': -18, 'bus': 'ambience'},
        {'file': 'audio/stems/room.wav', 'at': 0.0, 'gain_db': -14, 'bus': 'ambience'},
        {'file': 'audio/stems/gulls.wav', 'at': 0.0, 'gain_db': -4, 'bus': 'sfx'},
        {'file': 'audio/stems/foley.wav', 'at': 0.0, 'gain_db': -2, 'bus': 'foley'},
        {'file': 'audio/stems/music.wav', 'at': 0.0, 'gain_db': -6, 'bus': 'music'},
        {'file': 'audio/stems/whistles-close.wav', 'at': 0.0, 'gain_db': -4, 'bus': 'dialogue'},
        {'file': 'audio/stems/whistles-far.wav', 'at': 0.0, 'gain_db': -4, 'bus': 'dialogue'},
    ],
}
with open(os.path.join(HERE, 'mix.json'), 'w') as f:
    json.dump(plan, f, indent=2)
print('stems written:', ', '.join(sorted(os.listdir(OUT))))
