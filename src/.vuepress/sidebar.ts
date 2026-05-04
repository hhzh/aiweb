import {sidebar} from "vuepress-theme-hope";

export default sidebar({
    "/": [
        "",
        {
            text: "Claude Code",
            icon: "laptop-code",
            prefix: "claudecode/",
            link: "claudecode/",
            children: "structure",
        },
        {
            text: "codex",
            icon: "book",
            prefix: "codex/",
            link: "codex/",
            children: "structure",
        },
        {
            text: "skills",
            icon: "laptop-code",
            prefix: "skills/",
            link: "skills/",
            children: "structure",
        },
        {
            text: "agent",
            icon: "laptop-code",
            prefix: "agent/",
            link: "agent/",
            children: "structure",
        },
        {
            text: "openclaw",
            icon: "person-chalkboard",
            prefix: "openclaw/",
            link: "openclaw/",
            children: "structure",
        },
        {
            text: "obsidian",
            icon: "signs-post",
            prefix: "obsidian/",
            link: "obsidian/",
            children: "structure",
        },
        {
            text: "tool",
            icon: "gears",
            prefix: "tool/",
            link: "tool/",
            children: "structure",
        },
    ],
});
