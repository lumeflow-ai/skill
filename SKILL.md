---
name: lumeflow-video
version: 1.0.0
description: >
  Generate videos and images with Lumeflow. Supports text-to-video,
  image-to-video, text-to-image, image-to-image, image & video & audio upload,
  login, and authorization.
visibility: internal
agent_keys:
  - lumeflow-default
---


# Lumeflow Generation

Generate videos and images via the Lumeflow API. Includes built-in login authentication.

- **Video**: text-to-video (prompt only) and image-to-video (prompt + image URL)
- **Image**: text-to-image (prompt only) and image-to-image (prompt + image URLs)
- **Upload**: when the user provides a local image, video, or audio file (not a URL), it is automatically uploaded first in Step 0 to obtain a remote URL before any other processing. Also handles `media://` platform URIs. See [capabilities/upload.md](capabilities/upload.md) for formats and commands.
- **Login**: browser-based login to obtain `api_key` (auto-triggered when missing)

---

## 🚨 CRITICAL — Login Pre-Check (before any generation)

Before any generation request, if `LUMEFLOW_API_KEY` is missing or returns 401/403, **immediately run**:

```bash
python <skill_path>/scripts/login.py
```

The script handles everything: generates login_key → opens browser → polls for api_key → persists it.
- stderr: outputs login URL (forward to user) and polling progress
- stdout: returns `{"status":"success","api_key":"sk-sp-..."}`

> **FORBIDDEN**: running in background, splitting into separate steps, asking user to confirm login manually.

---

## 🚨 CRITICAL — Generation Command Rule

When submitting a generation request (Step 3 of the workflow), you **MUST** use:
- `--action watch-video` for video generation
- `--action watch-image` for image generation

**FORBIDDEN**: `--action video` and `--action image` are deprecated and MUST NOT be used.

---

This skill has been split into capability modules. **You MUST read the relevant module files before proceeding:**

## Core Rules (Read these first)
- [Workflow](capabilities/workflow.md) - The mandatory step-by-step process (Upload -> Price -> Generate+Watch -> Done).
- [Output Format & Interaction](capabilities/rules.md) - Output format rules and interaction guidelines.

## Capabilities (Read based on user request)
- [Video Generation](capabilities/video.md) - Models, parameters, constraints for video generation.
- [Image Generation](capabilities/image.md) - Models, parameters for image generation.
- [Request Templates](capabilities/request-templates.md) - Request body JSON templates and prompt integrity rules.
- [Result Handling](capabilities/result-handling.md) - Watch responses, result presentation, and retry logic.
- [Parameter Flow](capabilities/parameter-flow.md) - Parameter collection flow and summary table examples.
- [File Upload](capabilities/upload.md) - Image/video/audio upload formats, commands, and `media://` resolution.
