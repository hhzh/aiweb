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
            text: "Codex",
            icon: "book",
            prefix: "codex/",
            link: "codex/",
            collapsible: true,
            children: "structure",
        },
        {
            text: "Skills",
            icon: "book",
            prefix: "skills/",
            link: "skills/",
            collapsible: true,
            children: "structure",
        },
        {
            text: "Agent",
            icon: "book",
            prefix: "agent/",
            link: "agent/",
            collapsible: true,
            children: "structure",
        },
        {
            text: "OpenClaw",
            icon: "book",
            prefix: "openclaw/",
            link: "openclaw/",
            collapsible: true,
            children: "structure",
        },
        {
            text: "Tool",
            icon: "toolbox",
            prefix: "tool/",
            link: "tool/",
            collapsible: true,
            children: "structure",
        },
        {
            text: "关于",
            icon: "circle-info",
            prefix: "about/",
            link: "about/",
            collapsible: true,
            children: "structure",
        },
    ],
});
