import {navbar} from "vuepress-theme-hope";

export default navbar([
    "/",
    {
        text: "Claude Code教程",
        icon: "lightbulb",
        link: "/claudecode/",
    },
    {
        text: "Codex教程",
        icon: "computer",
        link: "/codex/",
    },
    {
        text: "Skills",
        icon: "laptop-code",
        link: "/skills/",
    },
    {
        text: "Agent",
        icon: "store",
        link: "/agent/",
    },
    {
        text: "OpenClaw",
        icon: "paper",
        link: "/openclaw/",
    },
    {
        text: "Tool",
        icon: "toolbox",
        link: "/tool/",
    },
    {
        text: "关于",
        icon: "circle-info",
        link: "/about/",
    },
]);
