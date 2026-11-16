"""Images for the Profession Flowchart entry: the icon and the card picture (a small crafting chart).
Run: python tools/make_pflow_img.py   (from the Site folder)"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
IMG = os.path.join(HERE, '..', 'img')

BG = (26, 22, 17)
PANEL = (34, 29, 22)
LINE = (140, 122, 96)
GOLD = (232, 181, 74)
COL = {'orange': (255, 128, 64), 'yellow': (255, 255, 0), 'green': (64, 192, 64), 'raw': (158, 133, 97)}


def font(size, bold=False):
    for name in (('arialbd.ttf' if bold else 'arial.ttf'), 'DejaVuSans.ttf'):
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            pass
    return ImageFont.load_default()


# Icon: three boxes joined into one, gold on dark leather
S = 512
ic = Image.new('RGBA', (S, S), BG + (255,))
d = ImageDraw.Draw(ic)
d.rounded_rectangle((16, 16, S - 16, S - 16), 70, fill=(48, 38, 26), outline=(110, 86, 52), width=10)
boxes = [(70, 330, 190, 430), (196, 330, 316, 430), (322, 330, 442, 430), (166, 90, 346, 210)]
for x0, y0, x1, y1 in boxes[:3]:
    cx = (x0 + x1) // 2
    d.line((cx, y0, cx, 270), fill=GOLD, width=12)
d.line((130, 270, 382, 270), fill=GOLD, width=12)
d.line((256, 270, 256, 210), fill=GOLD, width=12)
for i, b in enumerate(boxes):
    d.rounded_rectangle(b, 14, fill=(30, 24, 17), outline=GOLD if i == 3 else (205, 170, 110), width=10)
ic.resize((256, 256), Image.LANCZOS).save(os.path.join(IMG, 'pflow-icon.png'))

# Card: the gloves chain, top-down like the addon
W, H = 800, 450
pic = Image.new('RGB', (W, H), BG)
d = ImageDraw.Draw(pic)
d.rectangle((0, 0, W, 44), fill=PANEL)
d.text((18, 22), 'Toughened Leather Gloves x1', font=font(20, True), fill=(239, 230, 210), anchor='lm')
d.text((W - 18, 22), 'skill-ups ~3.4   profit +11s', font=font(17), fill=(127, 208, 127), anchor='rm')
BW, BH = 200, 64


def box(x, y, name, tally, act, kind, glow=False):
    if glow:
        d.rectangle((x - 5, y - 5, x + BW + 5, y + BH + 5), fill=(90, 70, 30))
    d.rectangle((x, y, x + BW, y + BH), fill=(30, 26, 21), outline=COL[kind], width=3)
    d.rectangle((x + 8, y + 8, x + 40, y + 40), fill=(80, 62, 40))
    d.text((x + 50, y + 12), name, font=font(16, True), fill=(255, 210, 90))
    d.text((x + 50, y + 32), tally, font=font(14), fill=(220, 220, 220))
    d.text((x + 10, y + 48), act, font=font(13, True), fill=(255, 208, 96) if act.startswith('Make') else (200, 200, 200))
    return (x + BW // 2, y, y + BH)


def link(a, b):
    d.line((b[0], b[1], b[0], b[1] - 16), fill=LINE, width=3)
    d.line((a[0], a[2], a[0], a[2] + 16), fill=LINE, width=3)
    d.line((a[0], a[2] + 16, b[0], b[1] - 16), fill=LINE, width=3)


top = box(300, 66, 'Toughened Gloves', 'make 1', '1 to make, parts first', 'yellow')
med = box(40, 176, 'Medium Leather', 'have 0 / need 4', 'Make 4', 'yellow', glow=True)
cur = box(300, 176, 'Cured Medium Hide', 'have 0 / need 2', 'Make 2', 'green')
thr = box(560, 176, 'Fine Thread', 'have 0 / need 2', 'buy 2   2s vendor', 'raw')
lig = box(40, 286, 'Light Leather', 'have 16 / need 16', 'ready', 'raw')
hid = box(300, 286, 'Medium Hide', 'have 2 / need 2', 'ready', 'raw')
salt = box(300, 370, 'Salt', 'have 2 / need 2', 'ready', 'raw')
for c in (med, cur, thr):
    link(top, c)
link(med, lig)
# stacked materials: down the left side of the column, then into each block
for seg in ((400, 240, 400, 258), (400, 258, 290, 258), (290, 258, 290, 402), (290, 318, 300, 318), (290, 402, 300, 402)):
    d.line(seg, fill=LINE, width=3)
pic.save(os.path.join(IMG, 'pflow-card.jpg'), quality=88)
print('ok')
