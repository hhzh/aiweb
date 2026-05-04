import { defineUserConfig } from "vuepress";

import theme from "./theme.js";

export default defineUserConfig({
  base: "/",

  lang: "zh-CN",
  title: "小林学AI",
  description: "小林学AI，专业的 AI 教程网站",

  theme,

});
