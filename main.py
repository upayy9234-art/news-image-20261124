#!/usr/bin/env python3
"""The World in One Image: Tuesday 24 November 2026.

Draws a one-page front page summing up the world's news of
24 November 2026 and writes it to entry.png (1024x1024, under 1 MiB).

Pure Python standard library only (math, os, struct, sys, zlib).
No network, no clock, no randomness: two runs produce byte-identical
output. The program re-reads its own output and verifies every PNG
chunk CRC, the 1024x1024 dimensions and the 1 MiB size limit before
exiting 0.

Output path, in order: argv[1], $MAKEFUN_OUTPUT_DIR/entry.png,
./entry.png, then entry.png beside this file.
"""

import math
import os
import struct
import sys
import zlib

W = 1024
H = 1024
MAX_BYTES = 1048576

# ---------------------------------------------------------------- palette
PAPER = (247, 243, 232)
INK = (24, 24, 28)
NAVY = (13, 32, 61)
NAVY2 = (18, 44, 84)
GOLD = (198, 155, 51)
GOLD_LT = (226, 190, 96)
RED = (178, 34, 34)
GREEN = (22, 122, 62)
GREEN_LT = (46, 160, 90)
SKY_TOP = (7, 22, 44)
SKY_LOW = (52, 74, 110)
SEA_TOP = (13, 58, 86)
SEA_BOT = (6, 30, 50)
WAVE = (36, 96, 128)
SHIP = (8, 12, 18)
CRANE = (16, 24, 36)
FIRE_Y = (255, 220, 120)
FIRE_O = (255, 176, 32)
FIRE_R = (242, 94, 24)
FIRE_D = (214, 48, 16)
SMOKE = (96, 96, 104)
MOON = (232, 228, 210)
MUTED = (90, 86, 76)
WHITE = (255, 255, 255)
CREAM = (250, 246, 236)

# ------------------------------------------------------------------- font
# 5x7 bitmap font. Each glyph is 7 rows of 5 bits ("1" = ink).
FONT = {
    "A": ["01110", "10001", "10001", "11111", "10001", "10001", "10001"],
    "B": ["11110", "10001", "10001", "11110", "10001", "10001", "11110"],
    "C": ["01110", "10001", "10000", "10000", "10000", "10001", "01110"],
    "D": ["11110", "10001", "10001", "10001", "10001", "10001", "11110"],
    "E": ["11111", "10000", "10000", "11110", "10000", "10000", "11111"],
    "F": ["11111", "10000", "10000", "11110", "10000", "10000", "10000"],
    "G": ["01110", "10001", "10000", "10111", "10001", "10001", "01111"],
    "H": ["10001", "10001", "10001", "11111", "10001", "10001", "10001"],
    "I": ["01110", "00100", "00100", "00100", "00100", "00100", "01110"],
    "J": ["00111", "00010", "00010", "00010", "00010", "10010", "01100"],
    "K": ["10001", "10010", "10100", "11000", "10100", "10010", "10001"],
    "L": ["10000", "10000", "10000", "10000", "10000", "10000", "11111"],
    "M": ["10001", "11011", "10101", "10101", "10001", "10001", "10001"],
    "N": ["10001", "11001", "10101", "10011", "10001", "10001", "10001"],
    "O": ["01110", "10001", "10001", "10001", "10001", "10001", "01110"],
    "P": ["11110", "10001", "10001", "11110", "10000", "10000", "10000"],
    "Q": ["01110", "10001", "10001", "10001", "10101", "10010", "01101"],
    "R": ["11110", "10001", "10001", "11110", "10100", "10010", "10001"],
    "S": ["01111", "10000", "10000", "01110", "00001", "00001", "11110"],
    "T": ["11111", "00100", "00100", "00100", "00100", "00100", "00100"],
    "U": ["10001", "10001", "10001", "10001", "10001", "10001", "01110"],
    "V": ["10001", "10001", "10001", "10001", "10001", "01010", "00100"],
    "W": ["10001", "10001", "10001", "10101", "10101", "10101", "01010"],
    "X": ["10001", "10001", "01010", "00100", "01010", "10001", "10001"],
    "Y": ["10001", "10001", "01010", "00100", "00100", "00100", "00100"],
    "Z": ["11111", "00001", "00010", "00100", "01000", "10000", "11111"],
    "0": ["01110", "10001", "10011", "10101", "11001", "10001", "01110"],
    "1": ["00100", "01100", "00100", "00100", "00100", "00100", "01110"],
    "2": ["01110", "10001", "00001", "00110", "01000", "10000", "11111"],
    "3": ["11111", "00010", "00100", "00010", "00001", "10001", "01110"],
    "4": ["00010", "00110", "01010", "10010", "11111", "00010", "00010"],
    "5": ["11111", "10000", "11110", "00001", "00001", "10001", "01110"],
    "6": ["00110", "01000", "10000", "11110", "10001", "10001", "01110"],
    "7": ["11111", "00001", "00010", "00100", "01000", "01000", "01000"],
    "8": ["01110", "10001", "10001", "01110", "10001", "10001", "01110"],
    "9": ["01110", "10001", "10001", "01111", "00001", "00010", "01100"],
    " ": ["00000", "00000", "00000", "00000", "00000", "00000", "00000"],
    ".": ["00000", "00000", "00000", "00000", "00000", "01100", "01100"],
    ",": ["00000", "00000", "00000", "00000", "01100", "00100", "01000"],
    ":": ["00000", "01100", "01100", "00000", "01100", "01100", "00000"],
    ";": ["00000", "01100", "01100", "00000", "01100", "00100", "01000"],
    "'": ["00100", "00100", "01000", "00000", "00000", "00000", "00000"],
    "-": ["00000", "00000", "00000", "01110", "00000", "00000", "00000"],
    "\u2014": ["00000", "00000", "00000", "11111", "00000", "00000", "00000"],
    "/": ["00001", "00010", "00010", "00100", "01000", "01000", "10000"],
    "(": ["00010", "00100", "01000", "01000", "01000", "00100", "00010"],
    ")": ["01000", "00100", "00010", "00010", "00010", "00100", "01000"],
    "%": ["11001", "11010", "00010", "00100", "01000", "01011", "10011"],
    "+": ["00000", "00100", "00100", "11111", "00100", "00100", "00000"],
    "$": ["00100", "01111", "10100", "01110", "00101", "11110", "00100"],
    "!": ["00100", "00100", "00100", "00100", "00100", "00000", "00100"],
    "?": ["01110", "10001", "00001", "00110", "00100", "00000", "00100"],
    "=": ["00000", "00000", "11111", "00000", "11111", "00000", "00000"],
    "&": ["01100", "10010", "10100", "01000", "10101", "10010", "01101"],
    '"': ["01010", "01010", "00000", "00000", "00000", "00000", "00000"],
    "\u2022": ["00000", "00100", "01110", "01110", "01110", "00100", "00000"],
    "*": ["00000", "10101", "01110", "11111", "01110", "10101", "00000"],
}
BLANK = ["00000"] * 7


def text_width(text, scale):
    """Pixel width of text at the given scale (6*scale per character)."""
    return len(text) * 6 * scale


def wrap_text(text, max_width, scale):
    """Greedy word wrap; returns a list of lines fitting max_width."""
    limit = max(1, max_width // (6 * scale))
    words = text.split(" ")
    lines = []
    cur = ""
    for word in words:
        if not cur:
            cur = word
        elif len(cur) + 1 + len(word) <= limit:
            cur += " " + word
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


# ------------------------------------------------------------------ canvas
class Canvas:
    def __init__(self, w, h, bg):
        self.w = w
        self.h = h
        self.px = bytearray(bg * (w * h))

    def set(self, x, y, color):
        if 0 <= x < self.w and 0 <= y < self.h:
            i = (y * self.w + x) * 3
            self.px[i] = color[0]
            self.px[i + 1] = color[1]
            self.px[i + 2] = color[2]

    def rect(self, x, y, w, h, color):
        x0 = max(0, x)
        y0 = max(0, y)
        x1 = min(self.w, x + w)
        y1 = min(self.h, y + h)
        for yy in range(y0, y1):
            base = (yy * self.w + x0) * 3
            row = bytes(color) * (x1 - x0)
            self.px[base:base + (x1 - x0) * 3] = row

    def hline(self, x0, x1, y, color, thick=1):
        for t in range(thick):
            self.rect(x0, y + t, x1 - x0, 1, color)

    def vline(self, x, y0, y1, color, thick=1):
        for t in range(thick):
            self.rect(x + t, y0, 1, y1 - y0, color)

    def line(self, x0, y0, x1, y1, color, thick=1):
        """Bresenham line, stamped with a square brush of size thick."""
        dx = abs(x1 - x0)
        dy = -abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx + dy
        x, y = x0, y0
        half = thick // 2
        while True:
            self.rect(x - half, y - half, thick, thick, color)
            if x == x1 and y == y1:
                break
            e2 = 2 * err
            if e2 >= dy:
                err += dy
                x += sx
            if e2 <= dx:
                err += dx
                y += sy

    def circle(self, cx, cy, r, color):
        """Filled circle by scanlines (integer math only)."""
        for dy in range(-r, r + 1):
            dx = math.isqrt(max(0, r * r - dy * dy))
            self.rect(cx - dx, cy + dy, 2 * dx + 1, 1, color)

    def ring(self, cx, cy, r, color, thick=2):
        for k in range(thick):
            rr = r - k
            if rr <= 0:
                break
            for dy in range(-rr, rr + 1):
                dx = math.isqrt(max(0, rr * rr - dy * dy))
                self.set(cx - dx, cy + dy, color)
                self.set(cx + dx, cy + dy, color)

    def vgrad(self, x, y, w, h, top, bot):
        for yy in range(h):
            t = yy / max(1, h - 1)
            c = (round(top[0] + (bot[0] - top[0]) * t),
                 round(top[1] + (bot[1] - top[1]) * t),
                 round(top[2] + (bot[2] - top[2]) * t))
            self.rect(x, y + yy, w, 1, c)

    def text(self, x, y, s, scale, color, align="left"):
        s = s.upper()
        if align == "center":
            x = x - text_width(s, scale) // 2
        elif align == "right":
            x = x - text_width(s, scale)
        for ch in s:
            glyph = FONT.get(ch, BLANK)
            for row_i, row in enumerate(glyph):
                for col_i, bit in enumerate(row):
                    if bit == "1":
                        self.rect(x + col_i * scale, y + row_i * scale,
                                  scale, scale, color)
            x += 6 * scale

    def para(self, x, y, width, items, scale, color, line_h=None, gap=8):
        """Draw wrapped paragraphs; items is a list of strings. Returns y."""
        if line_h is None:
            line_h = 7 * scale + 4
        for item in items:
            for line in wrap_text(item, width, scale):
                self.text(x, y, line, scale, color)
                y += line_h
            y += gap
        return y


def lcg(seed):
    """Tiny deterministic generator (no random module, no clock)."""
    state = seed & 0x7FFFFFFF
    while True:
        state = (1103515245 * state + 12345) & 0x7FFFFFFF
        yield state


# -------------------------------------------------------------------- hero
def draw_hero(cv, x0, y0, w, h):
    """Night sea at Benghazi: the corvette Merkury burning, sea drones
    closing in, port cranes on the left, moon and stars above."""
    horizon = y0 + 168
    # Sky and sea.
    cv.vgrad(x0, y0, w, horizon - y0, SKY_TOP, SKY_LOW)
    cv.vgrad(x0, horizon, w, y0 + h - horizon, SEA_TOP, SEA_BOT)
    # Stars (fixed pseudo-random positions, deterministic).
    rnd = lcg(2411)
    for _ in range(46):
        sx = x0 + 8 + next(rnd) % (w - 16)
        sy = y0 + 8 + next(rnd) % 120
        cv.set(sx, sy, (200, 205, 220))
        if next(rnd) % 3 == 0:
            cv.set(sx + 1, sy, (200, 205, 220))
    # Moon, top right.
    cv.circle(x0 + w - 92, y0 + 52, 20, MOON)
    cv.circle(x0 + w - 100, y0 + 46, 5, (206, 202, 186))
    cv.circle(x0 + w - 84, y0 + 60, 4, (206, 202, 186))
    # Horizon glow from the burning ship.
    for i in range(3):
        cv.rect(x0, horizon - 6 - i * 3, w, 3,
                (150 + i * 20, 70 + i * 8, 24))
    # Waves: short strokes across the sea.
    rnd = lcg(1124)
    for yy in range(horizon + 14, y0 + h - 8, 15):
        for _ in range(9):
            wx = x0 + 10 + next(rnd) % (w - 80)
            wl = 18 + next(rnd) % 44
            cv.hline(wx, wx + wl, yy, WAVE, 2)
    # Port cranes and containers, left side.
    for cx in (x0 + 74, x0 + 176):
        cv.rect(cx, horizon - 96, 10, 96, CRANE)
        cv.line(cx + 5, horizon - 96, cx + 92, horizon - 40, CRANE, 5)
        cv.line(cx + 5, horizon - 96, cx - 44, horizon - 58, CRANE, 5)
        cv.rect(cx - 2, horizon - 100, 14, 6, CRANE)
    cv.rect(x0 + 30, horizon - 30, 46, 30, (64, 40, 34))
    cv.rect(x0 + 80, horizon - 30, 46, 30, (38, 74, 66))
    cv.rect(x0 + 130, horizon - 30, 46, 30, (90, 60, 30))
    cv.rect(x0 + 30, horizon - 62, 46, 30, (38, 74, 66))
    cv.rect(x0 + 80, horizon - 62, 46, 30, (64, 40, 34))
    cv.rect(x0, horizon - 2, 250, 4, (10, 14, 20))
    # The corvette: hull, superstructure, funnel, mast.
    hull_y = horizon + 34
    bx0, bx1 = x0 + 520, x0 + 880
    cv.rect(bx0 + 20, hull_y, bx1 - bx0 - 20, 26, SHIP)
    for i in range(26):
        cv.rect(bx0 + 20 - i, hull_y + i, 1, 26 - i, SHIP)
    cv.rect(bx0 + 150, hull_y - 34, 120, 34, SHIP)
    cv.rect(bx0 + 210, hull_y - 58, 26, 24, SHIP)
    cv.rect(bx0 + 250, hull_y - 72, 10, 72, SHIP)
    cv.line(bx0 + 255, hull_y - 72, bx0 + 300, hull_y - 58, SHIP, 3)
    cv.rect(bx0 + 60, hull_y - 20, 70, 20, (30, 34, 40))
    cv.rect(bx0 + 300, hull_y - 20, 40, 20, (30, 34, 40))
    # Fire reflection on the water below the blast.
    rnd = lcg(777)
    for _ in range(22):
        rx = x0 + 668 + next(rnd) % 96
        rl = 8 + next(rnd) % 26
        col = (FIRE_O, FIRE_R, FIRE_D)[next(rnd) % 3]
        cv.vline(rx, hull_y + 28, hull_y + 28 + rl, col, 3)
    # Explosion above mid-ship: layered fireball, flame spikes, smoke.
    ex, ey = x0 + 690, hull_y - 66
    cv.circle(ex, ey, 54, FIRE_D)
    cv.circle(ex, ey, 42, FIRE_R)
    cv.circle(ex, ey, 30, FIRE_O)
    cv.circle(ex, ey, 17, FIRE_Y)
    for ang, ln in ((18, 46), (62, 58), (104, 40), (150, 52), (196, 44),
                    (238, 56), (284, 42), (326, 50)):
        rad = math.radians(ang)
        tx = ex + round(ln * math.cos(rad))
        ty = ey + round(ln * math.sin(rad)) - 8
        cv.line(ex, ey, tx, ty, FIRE_O, 4)
    cv.circle(ex - 40, ey + 26, 12, FIRE_R)
    cv.circle(ex + 44, ey + 20, 10, FIRE_O)
    cv.circle(ex + 8, ey - 48, 11, FIRE_R)
    cv.circle(ex - 58, ey - 52, 22, SMOKE)
    cv.circle(ex - 16, ey - 66, 26, SMOKE)
    cv.circle(ex + 34, ey - 56, 20, SMOKE)
    cv.circle(ex + 66, ey - 34, 14, SMOKE)
    # Seven sea drones closing in, low in the water.
    drones = [(584, 452), (636, 436), (684, 452), (732, 434),
              (780, 450), (828, 436), (872, 452)]
    for px, py in drones:
        cv.circle(px, py, 4, (235, 240, 245))
        cv.line(px - 4, py + 3, px - 26, py + 12, (150, 185, 205), 2)
        cv.line(px + 4, py + 3, px + 26, py + 12, (150, 185, 205), 2)
    # Panel frame.
    cv.rect(x0, y0, w, 3, INK)
    cv.rect(x0, y0 + h - 3, w, 3, INK)
    cv.rect(x0, y0, 3, h, INK)
    cv.rect(x0 + w - 3, y0, 3, h, INK)
    # Location tag, top left inside the panel.
    cv.rect(x0 + 12, y0 + 12, 196, 28, NAVY)
    cv.rect(x0 + 12, y0 + 12, 196, 3, GOLD)
    cv.text(x0 + 22, y0 + 19, "BENGHAZI, LIBYA", 2, WHITE)


# -------------------------------------------------------------------- page
def draw_page():
    cv = Canvas(W, H, PAPER)
    # Top gold rule.
    cv.rect(0, 0, W, 10, GOLD)
    # Masthead.
    cv.rect(0, 10, W, 108, NAVY)
    cv.text(W // 2, 30, "THE WORLD IN ONE IMAGE", 6, CREAM, align="center")
    cv.text(W // 2, 84, "TUESDAY, 24 NOVEMBER 2026", 3, GOLD_LT,
            align="center")
    cv.rect(0, 118, W, 4, GOLD)
    # Hero picture.
    draw_hero(cv, 24, 134, 976, 352)
    # Headline.
    cv.text(W // 2, 500, "UKRAINE SINKS RUSSIAN", 6, INK, align="center")
    cv.text(W // 2, 548, "WARSHIP IN LIBYA", 6, RED, align="center")
    # Sub-headline, centred and wrapped.
    sub = ("SEVEN SEA DRONES SINK THE CORVETTE MERKURY AT BENGHAZI; "
           "A KA-27 HELICOPTER IS DESTROYED AND THE CARGO SHIP MV "
           "ANGARA IS HIT. KYIV SAYS THE WAR HAS SPILLED 2,000 KM "
           "FROM THE FRONT.")
    y = 606
    for line in wrap_text(sub, 976, 2):
        cv.text(W // 2, y, line, 2, INK, align="center")
        y += 18
    cv.rect(24, 668, 976, 3, INK)
    # Middle row: two boxes.
    box_y, box_h = 682, 176
    # --- Markets box.
    cv.rect(24, box_y, 476, box_h, CREAM)
    cv.rect(24, box_y, 476, 3, INK)
    cv.rect(24, box_y + box_h - 3, 476, 3, INK)
    cv.rect(24, box_y, 3, box_h, INK)
    cv.rect(497, box_y, 3, box_h, INK)
    cv.rect(24, box_y, 476, 34, GREEN)
    cv.text(40, box_y + 7, "MARKETS ROAR BACK", 3, WHITE)
    # Rising chart.
    pts = [(48, 806), (110, 798), (172, 802), (234, 782), (296, 786),
           (358, 762), (420, 748), (472, 730)]
    for a, b in zip(pts, pts[1:]):
        cv.line(a[0], a[1], b[0], b[1], GREEN, 4)
    cv.line(472, 730, 458, 734, GREEN, 4)
    cv.line(472, 730, 466, 744, GREEN, 4)
    cv.hline(44, 480, 812, MUTED, 1)
    cv.text(44, 820, "NVIDIA +31% AS HUANG RETURNS", 2, INK)
    cv.text(44, 838, "NASDAQ +6% - S&P 500 +5%", 2, INK)
    # --- Washington box.
    cv.rect(524, box_y, 476, box_h, CREAM)
    cv.rect(524, box_y, 476, 3, INK)
    cv.rect(524, box_y + box_h - 3, 476, 3, INK)
    cv.rect(524, box_y, 3, box_h, INK)
    cv.rect(997, box_y, 3, box_h, INK)
    cv.rect(524, box_y, 476, 34, NAVY2)
    cv.text(540, box_y + 7, "WASHINGTON", 3, WHITE)
    cv.para(540, box_y + 44, 444, [
        "FBI DEPUTY DIRECTOR TO RETIRE IN DECEMBER",
        "TRUMP BLOCKS ARMY PLAN TO DETONATE IOWA CHEMICALS WITHOUT COURT OK",
        "DEMOCRATS PLAN 12 DEBATES FOR 2028 PRIMARY",
    ], 2, INK, gap=6)
    # Briefs band.
    cv.rect(24, 872, 976, 3, INK)
    cv.text(24, 884, "ALSO TODAY", 3, RED)
    briefs = [
        "EU UNVEILS SWEEPING NEW RUSSIA SANCTIONS ON BANKS, CRYPTO AND SPORT",
        "FIFA PICKS US TO CO-HOST 2031 WOMEN'S WORLD CUP; UK GETS 2035",
        "US LOSES MEASLES-FREE STATUS AS CASES HIT DECADES HIGH",
        "CONGO TO HALT COBALT EXPORTS FROM 30 NOVEMBER TO LIFT PRICES",
    ]
    y = 916
    for item in briefs:
        cv.text(24, y, "\u2022", 2, RED)
        cv.text(44, y, item, 2, INK)
        y += 20
    # Footer.
    cv.rect(24, 1000, 976, 3, GOLD)
    cv.text(W // 2, 1006, "24 NOVEMBER 2026 - ONE DAY, ONE IMAGE", 2,
            MUTED, align="center")
    return cv


# ---------------------------------------------------------------------- png
def chunk(kind, data):
    out = struct.pack(">I", len(data)) + kind + data
    out += struct.pack(">I", zlib.crc32(kind + data) & 0xFFFFFFFF)
    return out


def encode_png(w, h, px):
    raw = bytearray()
    stride = w * 3
    for y in range(h):
        raw.append(0)
        raw += px[y * stride:(y + 1) * stride]
    ihdr = struct.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0)
    png = b"\x89PNG\r\n\x1a\n"
    png += chunk(b"IHDR", ihdr)
    png += chunk(b"IDAT", zlib.compress(bytes(raw), 9))
    png += chunk(b"IEND", b"")
    return png


def validate_png(path):
    """Re-read the file: signature, chunk CRCs, IHDR size, 1 MiB cap."""
    with open(path, "rb") as fh:
        data = fh.read()
    if len(data) > MAX_BYTES:
        return "file is %d bytes, over the 1 MiB limit" % len(data)
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        return "bad PNG signature"
    pos = 8
    dims = None
    idat = bytearray()
    while pos < len(data):
        if pos + 8 > len(data):
            return "truncated chunk header"
        size = struct.unpack(">I", data[pos:pos + 4])[0]
        kind = data[pos + 4:pos + 8]
        body = data[pos + 8:pos + 8 + size]
        if len(body) != size or pos + 12 + size > len(data):
            return "truncated %s chunk" % kind.decode("latin1")
        crc = struct.unpack(">I", data[pos + 8 + size:pos + 12 + size])[0]
        if zlib.crc32(kind + body) & 0xFFFFFFFF != crc:
            return "bad CRC in %s chunk" % kind.decode("latin1")
        if kind == b"IHDR":
            dims = struct.unpack(">II", body[:8])
        if kind == b"IDAT":
            idat += body
        pos += 12 + size
        if kind == b"IEND":
            break
    if dims != (W, H):
        return "dimensions are %s, expected (1024, 1024)" % (dims,)
    try:
        raw = zlib.decompress(bytes(idat))
    except zlib.error:
        return "IDAT does not decompress"
    if len(raw) != H * (1 + W * 3):
        return "decoded image data has the wrong length"
    return None


# --------------------------------------------------------------------- main
def resolve_output(argv):
    if len(argv) > 1 and argv[1]:
        path = argv[1]
        if os.path.isdir(path):
            path = os.path.join(path, "entry.png")
        return path
    outdir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if outdir:
        return os.path.join(outdir, "entry.png")
    try:
        cwd = os.getcwd()
    except Exception:
        cwd = ""
    if cwd:
        return os.path.join(cwd, "entry.png")
    here = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(here, "entry.png")


def run(argv):
    out = resolve_output(argv)
    cv = draw_page()
    png = encode_png(W, H, bytes(cv.px))
    parent = os.path.dirname(os.path.abspath(out))
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(out, "wb") as fh:
        fh.write(png)
    problem = validate_png(out)
    if problem:
        sys.stderr.write("validation failed: %s\n" % problem)
        return 1
    sys.stdout.write("wrote %s (%d bytes)\n" % (out, len(png)))
    return 0


def main(argv):
    try:
        return run(argv)
    except Exception as exc:  # never raise a traceback
        sys.stderr.write("error: %s\n" % exc)
        return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
