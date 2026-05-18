---
name: codex-image
description: "通过 Codex CLI (ChatGPT Plus) 免费生图，不消耗 API 余额。需要安装 Codex.app 并登录 ChatGPT 账号。特点：文字渲染精准、照片级真实度。"
allowed-tools: Bash(python3 *)
---

# Codex Image（Codex 通道）

通过 Codex CLI + ChatGPT Plus 订阅免费生图，**不走 API 计费**。

> 前提：已安装 Codex.app 并登录 ChatGPT Plus

## 使用方式

```bash
python3 ~/.claude/skills/codex-image/generate.py "<prompt>" [size] [output_dir]
```

| 参数 | 说明 | 默认值 |
|------|------|--------|
| prompt | 生图提示词 | 必填 |
| size | 尺寸 | `1024x1024` |
| output_dir | 保存目录 | 当前目录 |

## 示例

```bash
# 方形
python3 ~/.claude/skills/codex-image/generate.py "一只橘猫睡在沙发上，阳光洒落"

# 横版
python3 ~/.claude/skills/codex-image/generate.py "a futuristic city skyline" 1536x1024

# 指定目录
python3 ~/.claude/skills/codex-image/generate.py "日式庭院" 1024x1536 /Users/leon/Desktop
```

## 原理

Codex CLI 走 ChatGPT 订阅，生图不额外收费（Plus 包含额度）。
