import {sidebar} from "vuepress-theme-hope";

export default sidebar({
    "/": [
        "",
        {
            text: "Claude Code",
            icon: "laptop-code",
            prefix: "claudecode/",
            link: "claudecode/",
            collapsible: true,
            children: "structure",
        },
        {
            text: "codex",
            icon: "book",
            prefix: "codex/",
            link: "codex/",
            collapsible: true,
            children: "structure",
        },
        {
            text: "skills",
            icon: "laptop-code",
            prefix: "skills/",
            link: "skills/",
            collapsible: true,
            children: "structure",
        },
        {
            text: "agent",
            icon: "laptop-code",
            prefix: "agent/",
            link: "agent/",
            collapsible: true,
            children: "structure",
        },
        {
            text: "openclaw",
            icon: "person-chalkboard",
            prefix: "openclaw/",
            link: "openclaw/",
            collapsible: true,
            children: "structure",
        },
        {
            text: "obsidian",
            icon: "signs-post",
            prefix: "obsidian/",
            link: "obsidian/",
            collapsible: true,
            children: "structure",
        },
        {
            text: "tool",
            icon: "gears",
            prefix: "tool/",
            link: "tool/",
            collapsible: true,
            children: "structure",
        },
    ],
});
