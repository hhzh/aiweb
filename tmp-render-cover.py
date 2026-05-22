from PIL import Image, ImageDraw, ImageFont, ImageFilter
from pathlib import Path
import math


ROOT = Path("/Users/yideng/Documents/workspace/aiweb")
OUT = ROOT / "src/img/02-claude-overview-and-usage-guide.png"
W, H = 1600, 900


def font(path, size):
    return ImageFont.truetype(path, size=size)


FONT_CN = "/System/Library/Fonts/Hiragino Sans GB.ttc"
FONT_CN_BOLD = "/System/Library/Fonts/STHeiti Medium.ttc"
FONT_MONO = "/System/Library/Fonts/Menlo.ttc"

f_top = font(FONT_CN_BOLD, 30)
f_title = font(FONT_CN_BOLD, 104)
f_subtitle = font(FONT_CN, 35)
f_step = font(FONT_CN_BOLD, 25)
f_panel_title = font(FONT_CN_BOLD, 28)
f_chip = font(FONT_CN_BOLD, 21)
f_mono = font(FONT_MONO, 24)
f_mono_big = font(FONT_MONO, 30)


def lerp(a, b, t):
    return int(a + (b - a) * t)


def vertical_gradient():
    img = Image.new("RGB", (W, H))
    px = img.load()
    for y in range(H):
        t = y / (H - 1)
        for x in range(W):
            u = x / (W - 1)
            c1 = (7, 17, 31)
            c2 = (16, 36, 63)
            c3 = (18, 43, 46)
            m = (t * 0.68 + u * 0.32)
            if m < 0.55:
                k = m / 0.55
                c = tuple(lerp(c1[i], c2[i], k) for i in range(3))
            else:
                k = (m - 0.55) / 0.45
                c = tuple(lerp(c2[i], c3[i], k) for i in range(3))
            px[x, y] = c
    return img.convert("RGBA")


def radial_glow(size, color):
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(glow)
    cx, cy, radius = size
    for r in range(radius, 0, -8):
        alpha = int(color[3] * (1 - r / radius) ** 1.8)
        draw.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(*color[:3], alpha))
    return glow.filter(ImageFilter.GaussianBlur(12))


def shadowed_round(draw_img, xy, radius, fill, outline=None, shadow=(0, 0, 0, 90), blur=24, offset=(0, 18), width=1):
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sdraw = ImageDraw.Draw(layer)
    sx1, sy1, sx2, sy2 = xy
    ox, oy = offset
    sdraw.rounded_rectangle((sx1 + ox, sy1 + oy, sx2 + ox, sy2 + oy), radius=radius, fill=shadow)
    draw_img.alpha_composite(layer.filter(ImageFilter.GaussianBlur(blur)))
    d = ImageDraw.Draw(draw_img)
    d.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=width)
    return d


img = vertical_gradient()
img.alpha_composite(radial_glow((190, 120, 420), (59, 130, 246, 86)))
img.alpha_composite(radial_glow((1390, 145, 360), (16, 185, 129, 70)))
draw = ImageDraw.Draw(img)

# Background grid
for x in range(0, W, 48):
    draw.line((x, 0, x, H), fill=(255, 255, 255, 20), width=1)
for y in range(0, H, 48):
    draw.line((0, y, W, y), fill=(255, 255, 255, 20), width=1)

# Technical rings
for r, col, wid in [
    (260, (103, 232, 249, 46), 2),
    (188, (52, 211, 153, 38), 2),
    (106, (251, 191, 36, 48), 2),
]:
    draw.ellipse((1520 - r, -80 - r, 1520 + r, -80 + r), outline=col, width=wid)
for a in range(0, 360, 16):
    rad = math.radians(a)
    x1 = 1520 + math.cos(rad) * 188
    y1 = -80 + math.sin(rad) * 188
    x2 = 1520 + math.cos(rad) * 198
    y2 = -80 + math.sin(rad) * 198
    draw.line((x1, y1, x2, y2), fill=(52, 211, 153, 42), width=2)

# Top mark
shadowed_round(img, (88, 76, 146, 134), 16, (8, 20, 39, 188), (125, 211, 252, 108), shadow=(45, 212, 191, 30), blur=22, offset=(0, 0))
draw = ImageDraw.Draw(img)
draw.text((105, 87), ">", font=f_mono_big, fill=(103, 232, 249, 255))
draw.text((162, 88), "终端 AI 代理 · 官方工作原理", font=f_top, fill=(185, 228, 255, 255))

# Main title
draw.text((88, 208), "Claude Code", font=f_title, fill=(139, 233, 253, 255))
draw.text((88, 326), "工作原理", font=f_title, fill=(248, 251, 255, 255))
draw.text((88, 444), "使用指南", font=f_title, fill=(248, 251, 255, 255))
draw.text((92, 596), "理解需求、调用工具、自主执行，", font=f_subtitle, fill=(214, 232, 246, 255))
draw.text((92, 647), "再用测试与反馈完成验证闭环。", font=f_subtitle, fill=(214, 232, 246, 255))

# Loop chips
loop_y = 768
items = [("收集上下文", 90), ("采取行动", 326), ("验证结果", 540)]
for label, x in items:
    shadowed_round(img, (x, loop_y, x + 184, loop_y + 60), 8, (6, 20, 34, 190), (167, 243, 208, 84), shadow=(0, 0, 0, 45), blur=18, offset=(0, 8))
    draw = ImageDraw.Draw(img)
    draw.ellipse((x + 20, loop_y + 23, x + 34, loop_y + 37), fill=(52, 211, 153, 255))
    draw.text((x + 46, loop_y + 15), label, font=f_step, fill=(220, 252, 231, 255))
for x in (288, 502):
    draw.line((x, loop_y + 30, x + 24, loop_y + 30), fill=(125, 211, 252, 230), width=5)
    draw.polygon([(x + 24, loop_y + 30), (x + 12, loop_y + 20), (x + 12, loop_y + 40)], fill=(125, 211, 252, 230))

# Terminal
shadowed_round(img, (948, 122, 1508, 628), 8, (4, 11, 22, 220), (148, 214, 255, 62), shadow=(0, 0, 0, 95), blur=30, offset=(0, 22))
draw = ImageDraw.Draw(img)
draw.rounded_rectangle((948, 122, 1508, 170), radius=8, fill=(255, 255, 255, 14))
draw.rectangle((948, 154, 1508, 170), fill=(255, 255, 255, 14))
for i, c in enumerate([(251, 113, 133), (250, 204, 21), (52, 211, 153)]):
    draw.ellipse((966 + i * 24, 140, 979 + i * 24, 153), fill=c)

tx, ty = 980, 204
terminal_lines = [
    (">", (103, 232, 249), ' claude "fix auth bug"', (248, 250, 252)),
    ("", (0, 0, 0), "scan src/auth/", (147, 169, 186)),
    ("", (0, 0, 0), "read tests and git state", (147, 169, 186)),
    ("OK", (134, 239, 172), " context mapped", (215, 243, 255)),
    ("", (0, 0, 0), "", (0, 0, 0)),
    ("agent", (103, 232, 249), " choose tools", (215, 243, 255)),
    ("", (0, 0, 0), "edit · shell · search · test", (147, 169, 186)),
    ("OK", (134, 239, 172), " patch applied", (215, 243, 255)),
    ("", (0, 0, 0), "", (0, 0, 0)),
    (">", (103, 232, 249), " npm test", (248, 250, 252)),
    ("OK", (134, 239, 172), " all checks passed", (215, 243, 255)),
]
for prefix, pc, text, tc in terminal_lines:
    if text == "":
        ty += 27
        continue
    draw.text((tx, ty), prefix, font=f_mono, fill=(*pc, 255))
    px = tx + (draw.textlength(prefix, font=f_mono) if prefix else 0)
    draw.text((px, ty), text, font=f_mono, fill=(*tc, 255))
    ty += 39

# Feature panel
shadowed_round(img, (1018, 686, 1488, 832), 8, (9, 23, 39, 188), (255, 255, 255, 42), shadow=(0, 0, 0, 70), blur=26, offset=(0, 18))
draw = ImageDraw.Draw(img)
draw.text((1048, 714), "模型 + 工具双驱动", font=f_panel_title, fill=(224, 242, 254, 255))
chips = [("Agentic Loop", 1048, 764), ("Shell 执行", 1268, 764), ("上下文管理", 1048, 812), ("安全权限", 1268, 812)]
for label, x, y in chips:
    draw.rounded_rectangle((x, y, x + 186, y + 38), radius=8, fill=(14, 165, 233, 25), outline=(125, 211, 252, 66), width=1)
    tw = draw.textlength(label, font=f_chip)
    draw.text((x + (186 - tw) / 2, y + 6), label, font=f_chip, fill=(207, 250, 254, 255))

# Subtle vignette
vignette = Image.new("L", (W, H), 0)
vd = ImageDraw.Draw(vignette)
vd.rectangle((0, 0, W, H), fill=210)
vignette = vignette.filter(ImageFilter.GaussianBlur(80))
edge = Image.new("RGBA", (W, H), (0, 0, 0, 0))
ed = ImageDraw.Draw(edge)
ed.rectangle((0, 0, W, H), outline=(0, 0, 0, 58), width=36)
edge = edge.filter(ImageFilter.GaussianBlur(36))
img.alpha_composite(edge)

OUT.parent.mkdir(parents=True, exist_ok=True)
img.convert("RGB").save(OUT, "PNG", optimize=True)
print(OUT)
