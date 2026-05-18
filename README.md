# GPT Image —— 通过 Codex CLI 免费生图

[![Version](https://img.shields.io/badge/version-1.0.0-blue)](https://github.com/Leon-llb/codex-image/releases)
[![Platform](https://img.shields.io/badge/platform-macOS-lightgrey)]()
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Requires](https://img.shields.io/badge/requires-ChatGPT%20Plus%20%7C%20Codex.app-orange)](https://codex.chat)

调用 ChatGPT 桌面客户端内置的 Codex 引擎，走 **ChatGPT Plus 订阅** 生图，**不消耗 API 余额**。

## 前置条件（硬性要求）

| 条件 | 说明 |
|------|------|
| macOS | Codex.app 仅支持 macOS（Windows 用户可尝试 `codex` CLI） |
| [Codex.app](https://codex.chat) 已安装 | 桌面客户端，提供 `codex` 命令行工具 |
| ChatGPT Plus 订阅 | 生图走 Plus 额度，不额外收费 |

> **没有 Plus 订阅？** 本工具无法使用。请先升级到 ChatGPT Plus。

## 安装

```bash
git clone https://github.com/Leon-llb/codex-image.git ~/.claude/skills/codex-image
```

## 命令行使用

```bash
python3 ~/.claude/skills/codex-image/generate.py "<prompt>" [size] [output_dir]
```

| 参数 | 说明 | 默认值 |
|------|------|--------|
| prompt | 生图提示词 | 必填 |
| size | 尺寸 `WxH` | `1024x1024` |
| output_dir | 保存目录 | 当前目录 |

```bash
# 方形
python3 generate.py "a cat sleeping on a sofa, warm sunlight"

# 竖版海报
python3 generate.py "恭喜发财新年海报，红色金色" 1024x1536 ~/Downloads

# 横版
python3 generate.py "futuristic city skyline at dusk" 1536x1024
```

## 集成到 Claude Code

Claude Code 自动发现 `SKILL.md`，对话中说"生成一张 xxx 的图"即可触发。

确保 skill 在 Claude Code 的 skills 目录：
```bash
ln -sf ~/.claude/skills/codex-image ~/.claude/skills/codex-image
```

## 集成到 Hermes / OpenClaw Agent

将本工具注册为 Agent 的 `image_gen` provider，让 Telegram/微信消息也能生图。

### 1. 安装插件

```bash
mkdir -p ~/.hermes/hermes-agent/plugins/image_gen/codex-image
cp hermes-plugin/plugin.yaml ~/.hermes/hermes-agent/plugins/image_gen/codex-image/
cp hermes-plugin/__init__.py ~/.hermes/hermes-agent/plugins/image_gen/codex-image/
```

### 2. 配置 config.yaml

```yaml
plugins:
  enabled:
  - image_gen/codex-image
  disabled: []

image_gen:
  provider: codex-image
```

### 3. 重启 Gateway

```bash
hermes gateway restart
```

之后在 Telegram/微信跟 Hermes 说"帮我生成一张 xxx 的图"，Agent 会调用 `image_generate` 工具 → 路由到 `codex-image` provider → 执行 `generate.py` → 图片保存到 `~/Downloads`。

## 原理

```
用户消息 → Hermes Agent → image_generate 工具
                              ↓
                     codex-image provider
                              ↓
                   generate.py 脚本
                              ↓
                    codex exec (ChatGPT Plus)
                              ↓
                      图片 → ~/Downloads
```

不走 API 计费，不消耗 token，纯 Plus 订阅额度。
