"""Images for the Compass Strip and Button of Holding entries: icons, the card picture and the Nordic frame as PNG.
Run: python tools/make_compass_img.py   (from the Site folder)"""
import math
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
IMG = os.path.join(HERE, '..', 'img')
MEDIA = os.path.join(HERE, '..', '..', 'CompassStrip', 'CompassStrip', 'Media')


def font(size, bold=False):
    for name in (('arialbd.ttf' if bold else 'arial.ttf'), 'DejaVuSans.ttf'):
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            pass
    return ImageFont.load_default()


def rounded(img, r):
    m = Image.new('L', img.size, 0)
    ImageDraw.Draw(m).rounded_rectangle((0, 0, img.size[0] - 1, img.size[1] - 1), r, fill=255)
    img.putalpha(m)
    return img


def gradient(w, h, top, bot):
    g = Image.new('RGB', (w, h))
    d = ImageDraw.Draw(g)
    for y in range(h):
        t = y / max(1, h - 1)
        d.line((0, y, w, y), fill=tuple(int(top[i] + (bot[i] - top[i]) * t) for i in range(3)))
    return g


# Nordic frame as PNG for the browser demo
cap = Image.open(os.path.join(MEDIA, 'NordicCap.tga')).convert('RGBA')
bar = Image.open(os.path.join(MEDIA, 'NordicBar.tga')).convert('RGBA')
cap.save(os.path.join(IMG, 'nordic-cap.png'))
bar.save(os.path.join(IMG, 'nordic-bar.png'))


def qmark(d, x, y, s, col=(255, 210, 40)):
    f = font(int(s * 1.25), True)
    d.text((x, y), '?', font=f, fill=col, anchor='mm', stroke_width=max(2, s // 9), stroke_fill=(40, 25, 0))


def bang(d, x, y, s, col=(255, 210, 40)):
    f = font(int(s * 1.25), True)
    d.text((x, y), '!', font=f, fill=col, anchor='mm', stroke_width=max(2, s // 9), stroke_fill=(40, 25, 0))


# Compass Strip icon: a strip with N over a dusk sky, and a gold marker
S = 512
ic = gradient(S, S, (40, 52, 84), (14, 16, 30)).convert('RGBA')
d = ImageDraw.Draw(ic)
d.rectangle((0, 150, S, 270), fill=(10, 12, 20, 230))
d.line((0, 270, S, 270), fill=(255, 210, 80), width=6)
for i, x in enumerate(range(16, S, 48)):
    d.line((x, 250, x, 268), fill=(230, 230, 230), width=4)
d.text((S // 2, 205), 'N', font=font(96, True), fill=(255, 210, 40), anchor='mm', stroke_width=5, stroke_fill=(0, 0, 0))
qmark(d, 395, 205, 90)
bang(d, 110, 205, 80)
d.polygon([(S // 2, 300), (S // 2 - 70, 470), (S // 2, 425), (S // 2 + 70, 470)], fill=(105, 233, 172))
d.polygon([(S // 2, 300), (S // 2, 425), (S // 2 + 70, 470)], fill=(60, 170, 120))
rounded(ic, 96).resize((256, 256), Image.LANCZOS).save(os.path.join(IMG, 'compass-icon.png'))

# Button of Holding icon: a purple bag spilling small round buttons
bg = gradient(S, S, (52, 30, 88), (16, 10, 30)).convert('RGBA')
d = ImageDraw.Draw(bg)
d.ellipse((96, 150, 416, 470), fill=(120, 72, 190), outline=(200, 160, 255), width=10)
d.polygon([(196, 170), (316, 170), (350, 90), (162, 90)], fill=(120, 72, 190), outline=(200, 160, 255))
d.line((180, 165, 332, 165), fill=(255, 210, 80), width=14)
for cx, cy, col in ((210, 300, (105, 233, 172)), (300, 300, (255, 120, 90)), (255, 380, (90, 156, 255)),
                    (340, 390, (255, 210, 60)), (170, 385, (230, 230, 230))):
    d.ellipse((cx - 34, cy - 34, cx + 34, cy + 34), fill=(20, 16, 30), outline=(210, 200, 170), width=7)
    d.ellipse((cx - 20, cy - 20, cx + 20, cy + 20), fill=col)
rounded(bg, 96).resize((256, 256), Image.LANCZOS).save(os.path.join(IMG, 'boh-icon.png'))

# Card picture: an evening landscape with the strip on top and the Nordic bar below it
W, H = 800, 450
pic = gradient(W, H, (96, 120, 160), (40, 46, 60)).convert('RGBA')
d = ImageDraw.Draw(pic)
hills = [(0, 300), (100, 250), (210, 285), (330, 225), (440, 270), (560, 215), (690, 265), (800, 240), (800, 450), (0, 450)]
d.polygon(hills, fill=(44, 58, 52))
d.polygon([(0, 350), (190, 315), (400, 340), (610, 305), (800, 340), (800, 450), (0, 450)], fill=(30, 40, 34))
pic = pic.filter(ImageFilter.GaussianBlur(1))
# full-width strip, see-through
ov = Image.new('RGBA', (W, H), (0, 0, 0, 0))
ImageDraw.Draw(ov).rectangle((0, 0, W, 64), fill=(0, 0, 0, 115))
pic = Image.alpha_composite(pic, ov)
d = ImageDraw.Draw(pic)
d.line((0, 64, W, 64), fill=(255, 210, 80), width=2)
half, th = W / 2, math.tan(math.radians(45))
heading = 20


def sx(bearing):
    dd = (bearing - heading + 180) % 360 - 180
    if abs(dd) >= 89:
        return None
    return half + math.tan(math.radians(dd)) / th * half


for b in range(0, 360, 15):
    x = sx(b)
    if x is None or not 0 <= x <= W:
        continue
    lab = {0: 'N', 45: 'NE', 90: 'E', 135: 'SE', 180: 'S', 225: 'SW', 270: 'W', 315: 'NW'}.get(b)
    if lab:
        d.text((x, 32), lab, font=font(26 if len(lab) == 1 else 20, True), anchor='mm',
               fill=(255, 210, 40) if len(lab) == 1 else (215, 215, 215), stroke_width=2, stroke_fill=(0, 0, 0))
    else:
        d.line((x, 52, x, 63), fill=(255, 255, 255, 150), width=2)
for b, kind in ((9, '?'), (48, '!'), (-25, 'f'), (31, 'p')):
    x = sx(b)
    if kind == '?':
        qmark(d, x, 32, 44)
    elif kind == '!':
        bang(d, x, 32, 36)
    elif kind == 'f':
        d.ellipse((x - 13, 19, x + 13, 45), fill=(105, 233, 172), outline=(10, 40, 30), width=3)
    else:
        d.ellipse((x - 9, 23, x + 9, 41), fill=(255, 125, 10), outline=(0, 0, 0), width=2)
x = sx(9)
d.text((x, 92), 'Marshal Dughan', font=font(22, True), fill=(255, 210, 40), anchor='mm', stroke_width=2, stroke_fill=(0, 0, 0))
d.text((x, 118), '86 yd', font=font(20), fill=(255, 255, 255), anchor='mm', stroke_width=2, stroke_fill=(0, 0, 0))
# Nordic bar lower down
bh = 40
bw = 440
by = 300
bx = (W - bw) // 2
pic.alpha_composite(bar.resize((bw, bh), Image.LANCZOS), (bx, by))
cs = cap.resize((bh * 2, bh), Image.LANCZOS)
pic.alpha_composite(cs, (bx - bh * 2, by))
pic.alpha_composite(cs.transpose(Image.FLIP_LEFT_RIGHT), (bx + bw, by))
d = ImageDraw.Draw(pic)
d.text((W // 2 - 120, by + bh // 2), 'W', font=font(26), fill=(235, 235, 232), anchor='mm')
qmark(d, W // 2 + 60, by + bh // 2, 34, (232, 232, 228))
d.text((W // 2, by + bh + 24), 'Marshal Dughan', font=font(22), fill=(235, 235, 232), anchor='mm')
pic.convert('RGB').save(os.path.join(IMG, 'compass-card.jpg'), quality=88)
print('ok')
