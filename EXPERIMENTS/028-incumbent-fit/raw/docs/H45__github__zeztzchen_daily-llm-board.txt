# Daily LLM Board

A lightweight daily dashboard for tracking LLM news, papers, research updates, model releases, and weekly notes.

Live site: [https://zeztzchen.github.io/daily-llm-board/](https://zeztzchen.github.io/daily-llm-board/)

## 功能介绍

Daily LLM Board 是一个纯静态的每日 LLM 信息巡检面板，适合每天快速过一遍新闻、论文、研究博客和模型动态。

- 每个信息源都可以勾选完成，并自动更新总进度和分组进度。
- 每个条目右侧提供打开按钮，方便快速跳转原站。
- 左侧展示日期、今日诗句、巡检进度和关注方向。
- 本周记录支持按日期保存笔记，内容存储在当前浏览器的 `localStorage`。
- 新的一周会自动开启新周并重置巡检状态。
- 支持一键导出当前周 Markdown 笔记。

## 用到的链接

### 论文

- [Hugging Face Trending Papers](https://huggingface.co/papers/trending)
- [alphaXiv Trending](https://www.alphaxiv.org/?sort=Trending)
- [Papers with Code](https://paperswithcode.co/)

### 博客

- [Anthropic Research](https://www.anthropic.com/research)
- [OpenAI Research](https://openai.com/research/index/)

### 新闻

- [X List 1](https://x.com/i/lists/2018885117041942711)
- [X List 2](https://x.com/i/lists/1597115448146898944)
- [AIHOT](https://aihot.virxact.com/)

### 模型

- [OpenRouter Models](https://openrouter.ai/models)
- [LLM Stats](https://llm-stats.com/llm-updates)
- [Arena WebDev Leaderboard](https://arena.ai/leaderboard/code/webdev)
- [Artificial Analysis](https://artificialanalysis.ai/)

### 其他资源推荐

- https://web.stanford.edu/class/cs25/
- https://github.com/karpathy/nn-zero-to-hero
- https://github.com/rohitg00/ai-engineering-from-scratch
- https://neetcode.io/practice/machine-learning

### API

- [今日诗词 API](https://v1.jinrishici.com/all.json)

## 参考

信息源整理和页面思路参考：[闪客-每天扫一遍这些内容，不怕 AI 时代掉队了](https://mp.weixin.qq.com/s/P-mwic1wiSvzwZiPKc077Q?scene=1&click_id=1337508649)。
> 目前的版本还没添加太多更多的自己查看过的内容，与其说是参考不如说是把up做的事情vibe了一个网页
