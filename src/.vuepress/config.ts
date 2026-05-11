import { defineUserConfig } from "vuepress";

import theme from "./theme.js";

export default defineUserConfig({
  base: "/",

  lang: "zh-CN",
  title: "小林学AI",
  description: "小林学AI，专业的 AI 教程网站",

  // 添加 head 配置
  head: [
    ["link", { rel: "icon", href: "/logo_black.svg" }],
    // 或使用 PNG 格式
    // ["link", { rel: "icon", type: "image/png", sizes: "32x32", href: "/logo.png" }],
  ],

  theme,

});
