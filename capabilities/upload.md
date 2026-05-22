# File Upload Reference (Image / Video / Audio)

All upload operations use the same endpoint: `POST /api/lumeflow/claw-upload-image`
The script auto-detects file type and validates format + size before uploading.

`<skill_path>` = absolute directory containing `SKILL.md`.

## Supported Formats & Limits

| Type | Formats | Max Size |
|------|---------|----------|
| Image | `jpg`, `jpeg`, `png`, `webp` | 10MB |
| Video | `mp4`, `mov`, `avi`, `webm`, `mkv` | 200MB |
| Audio | `mp3`, `wav`, `m4a`, `aac`, `ogg`, `flac`, `wma` | 50MB |

## Upload Commands

**Image:**
```bash
python <skill_path>/scripts/generate.py --action upload-image --file /path/to/image.png
```

**Video:**
```bash
python <skill_path>/scripts/generate.py --action upload-video --file /path/to/video.mp4
```

**Audio:**
```bash
python <skill_path>/scripts/generate.py --action upload-audio --file /path/to/audio.mp3
```

**Multiple files** (e.g. `images[]` for Seedance 2.0 Omni or image-to-image): upload each one separately, collect all URLs.

## Response

```json
{
    "code": 200,
    "msg": "success",
    "data": {
        "url": "https://lac-static.imyfone.com/lumeflow_web/mobile_image/xxx.png"
    }
}
```

Use `data.url` as the value for the corresponding API field (`image`, `image_tail`, `images[]`, etc.).

## `media://` Path Resolution

When the file path starts with `media://`, it is an OpenClaw platform URI — **not** a local filesystem path. The `generate.py` script will attempt to resolve it automatically. If it fails, search for the file by its filename in:

- `~/.openclaw/media/inbound/`
- `~/.openclaw/media/`
- `~/.openclaw/workspace/`
- Current working directory and subdirectories

Example: `media://inbound/1777288191014_xxx.jpg` → search for `1777288191014_xxx.jpg` in the directories above.

## Upload Rules

- The generation API only accepts remote URLs — passing a local file path directly will fail.
- Upload MUST complete before proceeding to price query or generation.
- Do NOT analyze file content or build parameter tables before upload completes.
