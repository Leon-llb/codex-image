# GPT Image (Codex CLI)

通过 Codex CLI + ChatGPT Plus 免费生图，不消耗 API 余额。

## 原理

调用 ChatGPT 桌面客户端内置的 Codex 引擎，走 Plus 订阅额度，不走 API 计费。

## 前置条件

- 已安装 [Codex.app](https://codex.chat) 并登录 ChatGPT Plus

## 使用

```bash
python3 generate.py "<prompt>" [size] [output_dir]
```

| 参数 | 说明 | 默认值 |
|------|------|--------|
| prompt | 生成提示词 | 必填 |
| size | 图片尺寸 | `1024x1024` |
| output_dir | 保存目录 | 当前目录 |

## 示例

```bash
# 方形
python3 generate.py "a cat sleeping on a sofa"

# 竖版海报
python3 generate.py "恭喜发财新年海报" 1024x1536 ~/Downloads

# 横版
python3 generate.py "futuristic city skyline" 1536x1024
```

## 集成到 Hermes Agent

注册为 `image_gen/gpt-image` 插件，让 Hermes 的 `image_generate` 工具直接调用本脚本。
