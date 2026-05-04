import { sidebar } from "vuepress-theme-hope";

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
      text: "文档",
      icon: "book",
      prefix: "guide/",
      children: "structure",
    },
    {
      text: "幻灯片",
      icon: "person-chalkboard",
      link: "https://ecosystem.vuejs.press/zh/plugins/markdown/revealjs/demo.html",
    },
  ],
});
