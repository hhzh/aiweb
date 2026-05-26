import {navbar} from "vuepress-theme-hope";

export default navbar([
    "/",
    {
        text: "Claude Code教程",
        icon: "snowflake",
        link: "/claudecode/",
    },
    {
        text: "Codex教程",
        icon: "file-code",
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
        icon: "diagram-project",
        link: "/openclaw/",
    },
    {
        text: "Hermes Agent",
        icon: "adn",
        link: "/hermes/",
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
