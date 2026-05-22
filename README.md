# Lumeflow Skill Hub

An AI Agent skill package for the OpenClaw platform. Generate professional videos and images by simply describing what you want in natural language — no manual operations, no learning curve.

This skill follows the Agent Skills specification and works with any compatible AI coding assistant (Cursor, Claude Code, etc.).

**Languages**: [English](README.md) | [中文](README.zh-CN.md) | [日本語](README.ja-JP.md) | [한국어](README.ko-KR.md)

## Installation

Tell the AI in OpenClaw to install the skill:

```
Help me install this skill: https://github.com/lumeflow-ai/skill
```

## What Can You Do With This?

Install the skill, then just tell the AI what you need. Here are some examples:

### One-Sentence Creation

| You say... | You get... |
|------------|------------|
| "Generate 5 product photos in different styles" | 5 AI-generated images, batch-produced in parallel |
| "Make a 10-second video of a cat walking on the beach at sunset" | An AI-generated video clip |
| "Use this photo to create a video" | An image-to-video generated from your reference |
| "Put this water bottle on a fashion model" | A composite image of a model holding your product |
| "Draw an orange cat, 9:16 portrait" | An AI-generated image |
| "Remove the background from this product photo" | A clean cutout PNG |
| "Change the background of this photo to a tropical beach" | An AI-edited image |
| "Create a new video that mimics the style of this reference clip" | A style-transferred video |

### Usage

Simply chat with the AI Agent in OpenClaw using natural language:

- **Generate video** — "Generate a video of a cat cooking in the kitchen, using Pixverse C1, 720P, 5 seconds"
- **Generate image** — "Draw an orange cat using GPT Image 2, 9:16 portrait, 2K resolution"
- **Image-to-Video / Image-to-Image** — Send or describe a reference image, the Agent will auto-upload and use it as input
- **Check balance** — "How many credits do I have left?"
- **View history** — "Show me my previous generation tasks"

The Agent will display a parameter summary and estimated credit cost before generation, and only submit after confirmation.

**Your imagination is the only limit** — the examples above are just starting points. Freely combine image generation, video creation, and more into any workflow you can imagine. Describe your creative vision in your own words, and the AI will figure out how to make it happen.

## Supported Models

### Video Models

| Model | Versions | Duration | Resolution |
|-------|----------|----------|------------|
| Kling | 1.6 / 2.5 / 2.6 / 3.0 / O1 | 5-10s | 720P / 1080P |
| Pixverse | V4.5 / V5 / V5.5 / C1 | 5-8s | 720P / 1080P |
| Hailuo | 02 / 2.3 | 6s | 1080P |
| Google Veo | 3.1 | 8s | 1080P |
| Wan | 2.5 / 2.6 / 2.7 | 5-10s | 720P / 1080P |
| Seedance | 2.0 | 5-10s | 720P / 1080P |
| Vidu | Q1 / Q2 | 4-8s | 720P / 1080P |

### Image Models

| Model | Versions | Resolution |
|-------|----------|------------|
| Nano Banana | V1 / V2 / Pro | 1K / 2K |
| Seedream | 4.0 / 5.0 | 1K / 2K / 3K |
| GPT Image | 2 | Auto |

## Project Structure

```
lumeflow-video/
├── SKILL.md                  # Skill manifest (v1.0.0)
├── capabilities/             # Capability definitions (workflow, rules, model params)
│   ├── workflow.md           # Mandatory 7-step workflow
│   ├── rules.md              # Output format & interaction rules
│   ├── video.md              # Video models & parameter constraints
│   ├── image.md              # Image models & parameter constraints
│   ├── request-templates.md  # JSON request templates
│   ├── result-handling.md    # Result handling & auto-retry
│   ├── parameter-flow.md     # Parameter collection flow
│   └── upload.md             # File upload formats & media:// protocol
├── references/
│   ├── api_reference.md      # API endpoint reference & error codes
│   └── ai_models_analysis.md # Deep model parameter analysis
└── scripts/
    ├── generate.py           # Main entry script (generate, query, upload, balance)
    ├── login.py              # Browser login flow
    ├── sign.py               # API request signing (MD5)
    ├── write_body.py         # JSON body writer (UTF-8 no BOM)
    ├── task_store.py         # Local task storage
    └── product_config.py     # Runtime config resolver
```

## Requirements

- Python 3.10+
- No third-party dependencies, standard library only

## License

[Apache-2.0](LICENSE)
