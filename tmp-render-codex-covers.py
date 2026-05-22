from pathlib import Path
import math
from PIL import Image, ImageDraw, ImageFont, ImageFilter


ROOT = Path("/Users/yideng/Documents/workspace/aiweb")
OUT_DIR = ROOT / "src/img"
W, H = 1600, 900

FONT_CN = "/System/Library/Fonts/Hiragino Sans GB.ttc"
FONT_CN_BOLD = "/System/Library/Fonts/STHeiti Medium.ttc"
FONT_MONO = "/System/Library/Fonts/Menlo.ttc"


def font(path, size):
    return ImageFont.truetype(path, size=size)


F_TOP = font(FONT_CN_BOLD, 29)
F_TITLE = font(FONT_CN_BOLD, 102)
F_TITLE_SM = font(FONT_CN_BOLD, 84)
F_SUB = font(FONT_CN, 34)
F_CHIP = font(FONT_CN_BOLD, 23)
F_PANEL = font(FONT_CN_BOLD, 28)
F_MONO = font(FONT_MONO, 24)
F_NO = font(FONT_MONO, 40)


ARTICLES = {
    "01-codex-basic-configuration": {
        "title": "基础配置教程",
        "eyebrow": "Codex · Basic Configuration",
        "subtitle": "从 config.toml、模型、权限与沙箱开始，快速跑通第一套配置。",
        "theme": "config",
        "chips": ["config.toml", "模型选择", "沙箱模式", "项目信任"],
        "lines": ["model = gpt-5.5", "sandbox = workspace", "approval = on-request", "trust project"],
        "palette": ((7, 18, 32), (9, 105, 218), (34, 211, 238), (52, 211, 153)),
    },
    "02-codex-advanced-configuration": {
        "title": "高级配置教程",
        "eyebrow": "Codex · Advanced Configuration",
        "subtitle": "用 Profiles、模型提供商、沙箱策略与监控配置支撑复杂团队场景。",
        "theme": "advanced",
        "chips": ["Profiles", "Provider", "Telemetry", "TUI 优化"],
        "lines": ["profile = work", "provider = openai", "otel enabled", "policy layered"],
        "palette": ((9, 19, 36), (79, 70, 229), (14, 165, 233), (250, 204, 21)),
    },
    "03-codex-prompt-tutorial": {
        "title": "提示词使用教程",
        "eyebrow": "Codex · Prompting",
        "subtitle": "用目标、上下文、约束与验收标准，把需求交代得像工程任务。",
        "theme": "prompt",
        "chips": ["目标明确", "上下文完整", "约束清晰", "可验证"],
        "lines": ["goal: fix bug", "context: @files", "constraints: style", "verify: tests"],
        "palette": ((13, 24, 40), (147, 51, 234), (45, 212, 191), (251, 146, 60)),
    },
    "04-codex-hooks-tutorial": {
        "title": "Hooks 使用教程",
        "eyebrow": "Codex · Hooks",
        "subtitle": "在会话与工具调用关键节点注入脚本，实现拦截、增强与自动化。",
        "theme": "hooks",
        "chips": ["PreToolUse", "PostToolUse", "SessionStart", "Stop"],
        "lines": ["event captured", "check command", "inject context", "write summary"],
        "palette": ((18, 22, 38), (190, 24, 93), (249, 115, 22), (34, 211, 238)),
    },
    "05-codex-mcp-tutorial": {
        "title": "MCP 全流程教程",
        "eyebrow": "Codex · MCP",
        "subtitle": "通过标准协议连接本地工具、HTTP 服务、文档、设计与外部系统。",
        "theme": "mcp",
        "chips": ["STDIO", "HTTP", "OAuth", "环境变量"],
        "lines": ["start server", "list tools", "call resource", "stream result"],
        "palette": ((6, 24, 43), (37, 99, 235), (16, 185, 129), (168, 85, 247)),
    },
    "06-codex-skills-tutorial": {
        "title": "Skills 使用教程",
        "eyebrow": "Codex · Skills",
        "subtitle": "把专项任务、脚本、参考资料与团队规范封装为可复用工作流。",
        "theme": "skills",
        "chips": ["SKILL.md", "脚本资源", "按需加载", "团队复用"],
        "lines": ["load skill", "read references", "run workflow", "save result"],
        "palette": ((8, 27, 34), (5, 150, 105), (14, 165, 233), (250, 204, 21)),
    },
    "07-codex-plugins-tutorial": {
        "title": "Plugins 使用教程",
        "eyebrow": "Codex · Plugins",
        "subtitle": "把 Skills、Apps 与 MCP 服务打包，安装后扩展完整工作流。",
        "theme": "plugins",
        "chips": ["Skills", "Apps", "MCP", "Marketplace"],
        "lines": ["install plugin", "enable package", "load tools", "share workflow"],
        "palette": ((18, 22, 39), (217, 70, 239), (14, 165, 233), (245, 158, 11)),
    },
    "08-codex-rules-tutorial": {
        "title": "Rules 使用教程",
        "eyebrow": "Codex · Rules",
        "subtitle": "用命令级 allow、prompt、forbidden 规则构建沙箱外安全防线。",
        "theme": "rules",
        "chips": ["allow", "prompt", "forbidden", "Starlark"],
        "lines": ["match command", "score risk", "block danger", "ask approval"],
        "palette": ((19, 23, 35), (220, 38, 38), (245, 158, 11), (45, 212, 191)),
    },
    "09-codex-subagent-tutorial": {
        "title": "Subagent 实用教程",
        "eyebrow": "Codex · Subagents",
        "subtitle": "让主代理创建专业子代理，并行审查、调试、审计与汇总结果。",
        "theme": "subagents",
        "chips": ["主代理", "并行任务", "独立上下文", "结果汇总"],
        "lines": ["spawn reviewer", "spawn debugger", "wait all", "merge answer"],
        "palette": ((12, 22, 42), (79, 70, 229), (34, 211, 238), (132, 204, 22)),
    },
    "10-codex-memory-tutorial": {
        "title": "记忆功能教程",
        "eyebrow": "Codex · Memories",
        "subtitle": "把稳定偏好、项目规范和工作流经验留存在本地上下文缓存层。",
        "theme": "memory",
        "chips": ["Memories", "Chronicle", "AGENTS.md", "本地缓存"],
        "lines": ["learn pattern", "store preference", "load context", "avoid repeat"],
        "palette": ((18, 25, 43), (147, 51, 234), (20, 184, 166), (251, 191, 36)),
    },
    "11-codex-agents-guide": {
        "title": "AGENTS 加载指令",
        "eyebrow": "Codex · AGENTS.md",
        "subtitle": "用全局与项目分层指令，把编码规范、测试要求和目录规则注入会话。",
        "theme": "agents",
        "chips": ["全局指令", "项目指令", "目录覆盖", "合并规则"],
        "lines": ["read global", "read project", "merge layers", "apply nearest"],
        "palette": ((8, 24, 42), (2, 132, 199), (52, 211, 153), (250, 204, 21)),
    },
    "12-codex-workflow-guide": {
        "title": "官方工作流指南",
        "eyebrow": "Codex · Workflows",
        "subtitle": "覆盖 CLI、IDE 与云端场景，用标准化流程完成端到端开发任务。",
        "theme": "workflow",
        "chips": ["代码解读", "Bug 修复", "测试编写", "代码审查"],
        "lines": ["describe goal", "attach context", "define done", "verify checks"],
        "palette": ((9, 25, 43), (14, 116, 144), (99, 102, 241), (34, 197, 94)),
    },
    "13-codex-project-customization": {
        "title": "项目定制化教程",
        "eyebrow": "Codex · Project Customization",
        "subtitle": "用五层能力协同，把通用助手定制成项目专属开发成员。",
        "theme": "custom",
        "chips": ["AGENTS", "Memories", "Skills", "MCP"],
        "lines": ["set rules", "remember context", "reuse skills", "connect tools"],
        "palette": ((10, 24, 42), (8, 145, 178), (168, 85, 247), (34, 197, 94)),
    },
    "14-codex-example-configurations": {
        "title": "示例配置教程",
        "eyebrow": "Codex · Example Configurations",
        "subtitle": "从基础入门到企业模板，整理可直接复制套用的配置方案。",
        "theme": "examples",
        "chips": ["基础模板", "进阶优化", "专项场景", "完整配置"],
        "lines": ["copy template", "edit model", "set sandbox", "restart codex"],
        "palette": ((11, 24, 38), (59, 130, 246), (14, 165, 233), (251, 146, 60)),
    },
    "15-codex-best-practices": {
        "title": "最佳实践",
        "eyebrow": "Codex · Best Practices",
        "subtitle": "围绕提示词、规划、规范、安全、工具和自动化建立可靠工作习惯。",
        "theme": "best",
        "chips": ["精准提示", "先计划", "小步验证", "权限可控"],
        "lines": ["write context", "make plan", "test changes", "review result"],
        "palette": ((13, 25, 37), (22, 163, 74), (59, 130, 246), (250, 204, 21)),
    },
}


def lerp(a, b, t):
    return int(a + (b - a) * t)


def size(draw, text, fnt):
    box = draw.textbbox((0, 0), text, font=fnt)
    return box[2] - box[0], box[3] - box[1]


def background(palette):
    c1, c2, c3, c4 = palette
    img = Image.new("RGB", (W, H))
    px = img.load()
    for y in range(H):
        ty = y / (H - 1)
        for x in range(W):
            tx = x / (W - 1)
            t = ty * 0.6 + tx * 0.4
            if t < 0.58:
                k = t / 0.58
                col = tuple(lerp(c1[i], c2[i], k) for i in range(3))
            else:
                k = (t - 0.58) / 0.42
                col = tuple(lerp(c2[i], c1[i], k * 0.5) for i in range(3))
            px[x, y] = col
    img = img.convert("RGBA")
    for cx, cy, r, color in [(190, 115, 430, c2), (1390, 160, 360, c3), (1140, 820, 340, c4)]:
        glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        gd = ImageDraw.Draw(glow)
        for rr in range(r, 0, -10):
            a = int(64 * (1 - rr / r) ** 1.8)
            gd.ellipse((cx - rr, cy - rr, cx + rr, cy + rr), fill=(*color, a))
        img.alpha_composite(glow.filter(ImageFilter.GaussianBlur(16)))
    d = ImageDraw.Draw(img)
    for x in range(0, W, 50):
        d.line((x, 0, x, H), fill=(255, 255, 255, 18), width=1)
    for y in range(0, H, 50):
        d.line((0, y, W, y), fill=(255, 255, 255, 18), width=1)
    return img


def card(img, xy, radius, fill, outline=None):
    shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    x1, y1, x2, y2 = xy
    sd.rounded_rectangle((x1, y1 + 20, x2, y2 + 20), radius=radius, fill=(0, 0, 0, 84))
    img.alpha_composite(shadow.filter(ImageFilter.GaussianBlur(24)))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=1)
    return d


def split_title(text):
    if len(text) <= 8:
        return [text]
    for token in ["加载", "使用", "配置", "全流程", "实用", "项目", "示例"]:
        idx = text.find(token)
        if idx > 1:
            return [text[:idx], text[idx:]]
    mid = len(text) // 2
    return [text[:mid], text[mid:]]


def draw_header(d, no, meta, palette):
    d.rounded_rectangle((88, 76, 146, 134), radius=16, fill=(8, 20, 39, 190), outline=(*palette[2], 120), width=1)
    d.text((104, 86), ">", font=F_NO, fill=(*palette[2], 255))
    d.text((164, 90), meta["eyebrow"], font=F_TOP, fill=(210, 235, 255, 255))
    d.text((1394, 88), f"#{no}", font=F_NO, fill=(255, 255, 255, 150))


def draw_title(d, meta):
    d.text((88, 208), "Codex", font=F_TITLE, fill=(139, 233, 253, 255))
    lines = split_title(meta["title"])
    f = F_TITLE if max(len(x) for x in lines) <= 8 else F_TITLE_SM
    y = 326
    for line in lines:
        d.text((88, y), line, font=f, fill=(248, 251, 255, 255))
        y += 112 if f is F_TITLE else 98
    d.text((92, 592), meta["subtitle"][:21], font=F_SUB, fill=(217, 233, 246, 255))
    d.text((92, 642), meta["subtitle"][21:], font=F_SUB, fill=(217, 233, 246, 255))


def draw_terminal(img, meta, palette):
    d = card(img, (948, 122, 1508, 620), 8, (4, 11, 22, 224), (148, 214, 255, 65))
    d.rounded_rectangle((948, 122, 1508, 170), radius=8, fill=(255, 255, 255, 20))
    d.rectangle((948, 154, 1508, 170), fill=(255, 255, 255, 20))
    for i, c in enumerate([(251, 113, 133), (250, 204, 21), (52, 211, 153)]):
        d.ellipse((966 + i * 24, 140, 979 + i * 24, 153), fill=c)
    y = 210
    d.text((980, y), "$", font=F_MONO, fill=(*palette[2], 255))
    d.text((1008, y), "codex", font=F_MONO, fill=(248, 250, 252, 255))
    y += 52
    for line in meta["lines"]:
        d.text((980, y), "OK", font=F_MONO, fill=(134, 239, 172, 255))
        d.text((1022, y), line, font=F_MONO, fill=(210, 231, 244, 255))
        y += 45
    y += 18
    d.text((980, y), "ready", font=F_MONO, fill=(*palette[2], 255))
    d.text((1060, y), "for project work", font=F_MONO, fill=(147, 169, 186, 255))


def draw_chips(img, meta, palette):
    d = card(img, (1018, 686, 1488, 832), 8, (9, 23, 39, 188), (255, 255, 255, 42))
    d.text((1048, 714), "核心能力地图", font=F_PANEL, fill=(224, 242, 254, 255))
    for idx, chip in enumerate(meta["chips"]):
        x = 1048 + (idx % 2) * 220
        y = 764 + (idx // 2) * 48
        d.rounded_rectangle((x, y, x + 186, y + 38), radius=8, fill=(*palette[1], 45), outline=(*palette[2], 80), width=1)
        tw, _ = size(d, chip, F_CHIP)
        d.text((x + (186 - tw) / 2, y + 6), chip, font=F_CHIP, fill=(231, 255, 255, 255))


def draw_icon(img, meta, palette):
    d = ImageDraw.Draw(img)
    cx, cy = 730, 770
    c = (*palette[2], 230)
    faint = (*palette[2], 70)
    theme = meta["theme"]
    if theme in {"config", "advanced", "examples"}:
        d.rounded_rectangle((cx - 150, cy - 96, cx + 150, cy + 92), radius=12, outline=c, fill=(*palette[1], 38), width=3)
        for i, text in enumerate(["[profile]", "model =", "sandbox ="]):
            y = cy - 62 + i * 52
            d.text((cx - 114, y), text, font=F_MONO, fill=(248, 250, 252, 230))
            d.line((cx + 18, y + 18, cx + 116, y + 18), fill=faint, width=4)
    elif theme in {"prompt", "best", "workflow"}:
        labels = ["Goal", "Context", "Verify"] if theme != "workflow" else ["Plan", "Build", "Check"]
        for i, label in enumerate(labels):
            x = cx - 190 + i * 160
            d.rounded_rectangle((x, cy - 34, x + 120, cy + 34), radius=8, outline=c, fill=(*palette[1], 45), width=2)
            tw, _ = size(d, label, F_CHIP)
            d.text((x + (120 - tw) / 2, cy - 15), label, font=F_CHIP, fill=(232, 255, 255, 255))
            if i < 2:
                d.line((x + 124, cy, x + 154, cy), fill=c, width=5)
                d.polygon([(x + 154, cy), (x + 140, cy - 10), (x + 140, cy + 10)], fill=c)
    elif theme == "hooks":
        for a in range(0, 360, 60):
            r = math.radians(a)
            x = cx + math.cos(r) * 92
            y = cy + math.sin(r) * 74
            d.line((cx, cy, x, y), fill=faint, width=3)
            d.ellipse((x - 14, y - 14, x + 14, y + 14), fill=c)
        d.ellipse((cx - 30, cy - 30, cx + 30, cy + 30), outline=c, width=5)
    elif theme == "mcp":
        for i in range(4):
            a = math.radians(45 + i * 90)
            x = cx + math.cos(a) * 112
            y = cy + math.sin(a) * 84
            d.line((cx, cy, x, y), fill=faint, width=4)
            d.rounded_rectangle((x - 44, y - 28, x + 44, y + 28), radius=8, outline=c, fill=(*palette[1], 45), width=2)
        d.ellipse((cx - 44, cy - 44, cx + 44, cy + 44), outline=c, width=5)
    elif theme == "skills":
        for i in range(3):
            d.rounded_rectangle((cx - 116 + i * 60, cy - 66 + i * 28, cx + 78 + i * 60, cy + 12 + i * 28), radius=8, outline=c, fill=(*palette[1], 35), width=2)
        d.text((cx - 58, cy - 18), "SKILL", font=F_MONO, fill=(248, 250, 252, 230))
    elif theme == "plugins":
        for x, y in [(cx - 72, cy - 56), (cx + 14, cy - 56), (cx - 72, cy + 30), (cx + 14, cy + 30)]:
            d.rounded_rectangle((x, y, x + 72, y + 72), radius=10, outline=c, fill=(*palette[1], 45), width=3)
        d.line((cx, cy - 18, cx, cy + 30), fill=faint, width=4)
        d.line((cx - 30, cy + 12, cx + 44, cy + 12), fill=faint, width=4)
    elif theme == "rules":
        pts = [(cx, cy - 78), (cx + 88, cy - 38), (cx + 68, cy + 62), (cx, cy + 100), (cx - 68, cy + 62), (cx - 88, cy - 38)]
        d.polygon(pts, outline=c, fill=(*palette[1], 48))
        d.line((cx - 36, cy + 12, cx - 8, cy + 40, cx + 48, cy - 28), fill=(134, 239, 172, 240), width=7)
    elif theme == "subagents":
        d.ellipse((cx - 40, cy - 40, cx + 40, cy + 40), outline=c, width=5)
        for i, label in enumerate(["A", "B", "C"]):
            x = cx - 150 + i * 150
            y = cy + 96
            d.line((cx, cy + 40, x, y - 20), fill=faint, width=4)
            d.ellipse((x - 30, y - 30, x + 30, y + 30), outline=c, width=4)
            d.text((x - 9, y - 18), label, font=F_NO, fill=(248, 250, 252, 230))
    elif theme == "memory":
        for i in range(5):
            y = cy - 82 + i * 38
            d.rounded_rectangle((cx - 142, y, cx + 142, y + 24), radius=12, outline=faint, fill=(*palette[1], 30), width=2)
        d.text((cx - 78, cy - 18), "MEMORY", font=F_MONO, fill=(248, 250, 252, 230))
    elif theme in {"agents", "custom"}:
        nodes = [("AGENTS", cx, cy - 78), ("Skills", cx - 120, cy + 48), ("MCP", cx + 120, cy + 48)]
        for label, x, y in nodes:
            d.line((cx, cy, x, y), fill=faint, width=4)
            d.rounded_rectangle((x - 62, y - 26, x + 62, y + 26), radius=8, outline=c, fill=(*palette[1], 42), width=2)
            tw, _ = size(d, label, F_CHIP)
            d.text((x - tw / 2, y - 14), label, font=F_CHIP, fill=(248, 250, 252, 230))


def render(slug, meta):
    no = slug.split("-", 1)[0]
    img = background(meta["palette"])
    d = ImageDraw.Draw(img)
    draw_header(d, no, meta, meta["palette"])
    draw_title(d, meta)
    draw_icon(img, meta, meta["palette"])
    draw_terminal(img, meta, meta["palette"])
    draw_chips(img, meta, meta["palette"])
    edge = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ed = ImageDraw.Draw(edge)
    ed.rectangle((0, 0, W, H), outline=(0, 0, 0, 58), width=34)
    img.alpha_composite(edge.filter(ImageFilter.GaussianBlur(30)))
    out = OUT_DIR / f"{slug}.png"
    img.convert("RGB").save(out, "PNG", optimize=True)
    return out


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for slug, meta in ARTICLES.items():
        print(render(slug, meta))


if __name__ == "__main__":
    main()
