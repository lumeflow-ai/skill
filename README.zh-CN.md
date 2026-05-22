# Lumeflow Skill Hub

OpenClaw 平台的 AI Agent 技能包，只需用自然语言描述你想要的内容，即可生成专业的视频和图片——无需手动操作，无需学习曲线。

该技能遵循 Agent Skills 规范，可与任何兼容的 AI 编码助手（Cursor、Claude Code 等）配合使用。

**语言**: [English](README.md) | [中文](README.zh-CN.md) | [日本語](README.ja-JP.md) | [한국어](README.ko-KR.md)

## 安装

在 OpenClaw 中告诉 AI 安装该技能即可：

```
帮我安装这个技能：https://github.com/lumeflow-ai/skill
```

## 你能用它做什么？

安装该技能后，只需告诉 AI 你的需求即可。以下是一些示例：

### 一句话创作

| 你说…… | 你会得到…… |
|--------|-----------|
| "生成 5 张不同风格的产品照片" | 5 张 AI 生成的图片，批量并行生成 |
| "拍一段 10 秒的视频，日落时分一只猫在沙滩上散步" | 一段 AI 生成的视频 |
| "用这张照片制作一段视频" | 以图片为参考的图生视频 |
| "把这个水瓶放在时装模特身上" | 模型手持产品的合成图 |
| "画一只橘猫，9:16 竖版" | 一张 AI 生成的图片 |
| "移除这张产品照片的背景" | 干净的抠图 PNG |
| "将这张照片的背景换成热带海滩" | 一张 AI 编辑后的图片 |
| "制作一个模仿此参考视频风格的新视频" | 风格迁移视频 |

### 使用方式

在 OpenClaw 中直接用自然语言与 AI Agent 对话即可：

- **生成视频** — "帮我生成一段猫咪在厨房做饭的视频，用 Pixverse C1，720P，5 秒"
- **生成图片** — "使用 GPT Image 2 画一只橘猫，9:16 竖版，2K 分辨率"
- **图生视频 / 图生图** — 直接发送或描述一张参考图片，Agent 会自动上传并作为输入
- **查询余额** — "看看我还有多少积分"
- **查看历史** — "看看我之前生成的任务"

Agent 会在生成前自动展示参数摘要和预估积分消耗，确认后才会提交任务。

**你的想象力就是唯一的限制** —— 以上示例只是起点。你可以自由组合图片生成、视频制作等功能，构建任何你想象得到的工作流。用你自己的语言描述创意构想，AI 就会想办法帮你实现。

## 支持的模型

### 视频模型

| 模型 | 版本 | 时长 | 分辨率 |
|------|------|------|--------|
| Kling | 1.6 / 2.5 / 2.6 / 3.0 / O1 | 5-10s | 720P / 1080P |
| Pixverse | V4.5 / V5 / V5.5 / C1 | 5-8s | 720P / 1080P |
| Hailuo | 02 / 2.3 | 6s | 1080P |
| Google Veo | 3.1 | 8s | 1080P |
| Wan | 2.5 / 2.6 / 2.7 | 5-10s | 720P / 1080P |
| Seedance | 2.0 | 5-10s | 720P / 1080P |
| Vidu | Q1 / Q2 | 4-8s | 720P / 1080P |

### 图片模型

| 模型 | 版本 | 分辨率 |
|------|------|--------|
| Nano Banana | V1 / V2 / Pro | 1K / 2K |
| Seedream | 4.0 / 5.0 | 1K / 2K / 3K |
| GPT Image | 2 | 自动 |

## 项目结构

```
lumeflow-video/
├── SKILL.md                  # 技能清单 (v1.0.0)
├── capabilities/             # 能力定义（工作流、规则、模型参数等）
│   ├── workflow.md           # 强制执行的 7 步工作流
│   ├── rules.md              # 输出格式与交互规则
│   ├── video.md              # 视频模型及参数约束
│   ├── image.md              # 图片模型及参数约束
│   ├── request-templates.md  # JSON 请求模板
│   ├── result-handling.md    # 结果处理与自动重试
│   ├── parameter-flow.md     # 参数收集流程
│   └── upload.md             # 文件上传格式与 media:// 协议
├── references/
│   ├── api_reference.md      # API 端点参考与错误码
│   └── ai_models_analysis.md # 模型参数深度分析
└── scripts/
    ├── generate.py           # 主入口脚本（生成、查询、上传、余额）
    ├── login.py              # 浏览器登录流程
    ├── sign.py               # API 请求签名（MD5）
    ├── write_body.py         # JSON 请求体写入（UTF-8 无 BOM）
    ├── task_store.py         # 本地任务存储
    └── product_config.py     # 运行时配置解析
```

## 环境要求

- Python 3.10+
- 无第三方依赖，全部使用标准库

## License

[Apache-2.0](LICENSE)
