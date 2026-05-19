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
        icon: "dumbbell",
        link: "/codex/",
    },
    {
        text: "Skills",
        icon: "laptop-code",
        link: "/skills/",
    },
    {
        text: "Agent",
        icon: "book",
        link: "/agent/",
    },
    {
        text: "OpenClaw",
        icon: "book",
        link: "/openclaw/",
    },
    {
        text: "Tool",
        icon: "gears",
        link: "/tool/",
    },
    {
        text: "关于",
        icon: "gears",
        link: "/about/",
    },
]);
