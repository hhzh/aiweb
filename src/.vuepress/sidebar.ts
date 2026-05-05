import {sidebar} from "vuepress-theme-hope";

export default sidebar({
    "/": [
        "",
        {
            text: "Claude Code",
            icon: "book",
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
            icon: "book",
            prefix: "skills/",
            link: "skills/",
            collapsible: true,
            children: "structure",
        },
        {
            text: "agent",
            icon: "book",
            prefix: "agent/",
            link: "agent/",
            collapsible: true,
            children: "structure",
        },
        {
            text: "openclaw",
            icon: "book",
            prefix: "openclaw/",
            link: "openclaw/",
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
