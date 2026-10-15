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

Current catalog: [33 supported video models and parameter rules](references/video-model-catalog.md). Inspect locally with `python scripts/generate.py --action models`.

| Model | Versions | Duration | Resolution |
|-------|----------|----------|------------|
| Kling | 1.6 / 2.5 / 3.0 | 5/10s; 3.0: 3-15s | 3.0: 720P / 1080P / 4K; others use mode |
| LumeFlow / Pixverse | pix6 (4.0) / pix5 (3.0) / pix4.5 / V5.5 / C1 | 5/8/10s by version; pix6/C1: 2-15s | 360P / 540P / 720P / 1080P by duration |
| Hailuo | 02 / 2.3 / 2.3 Fast | 6/10s | 768P; 6s also 1080P |
| Google Veo | 3.1 / 3.1 Fast | 8s | No resolution parameter |
| Wan | 2.5 / 2.6 / 2.7 | 2.5: 5/10s; 2.6/2.7: 2-15s | 480P / 720P / 1080P by version |
| Seedance | 1.5 Pro / 2.0 / Fast / VIP / VIP Fast / Mini / 2.5 | 1.5: 4-12s; 2.0: 4-15s; 2.5: 4-30s | 480P / 720P; 1.5/2.0/VIP also 1080P |
| Vidu | Q1 / Q2 / Q2 Turbo | Q1: no duration parameter; Q2/Turbo: 5/10s | Q1: no resolution parameter; Q2/Turbo: 540P / 720P / 1080P |
| Sora | 2 / 2 Pro | 10/15s; Pro also 25s | 2: 720P; Pro: 1080P |
| Happy Horse | 1.0 / 1.1 | 3-15s | 720P / 1080P |
| Grok Imagine | 1.5 (image-to-video) | 10/15s | 720P |
| Gemini Omni | Text / single image | 6/8/10s | 720P / 1080P |
| MiniMax | H3 | 4-15s | 768P / 2K |

### Image Models

| Model | Versions | Resolution |
|-------|----------|------------|
| Nano Banana | V1 / V2 / V2.1 (179) / Pro | V1: omitted; V2/V2.1/Pro: 1K / 2K / 4K by mode |
| Seedream | 4.0 / 5.0 Lite / 5.0 Pro | 4.0: 1K/2K/4K; Lite: 2K/3K; Pro: 1K/2K |
| Kling O1 Image | Image-to-image (38) | 1K / 2K |
| GPT Image | 2 / 2.5 Flare / 2.5 Sunburst | 1K / 2K / 4K; selectable quality |

Image rules: [current image catalog](references/image-model-catalog.md). Inspect with `python scripts/generate.py --action image-models`.

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
    ├── image_catalog.py      # Image IDs and request validation
    ├── model_catalog.py      # Current website model IDs and request validation
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
