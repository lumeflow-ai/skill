# Request Body Templates

`<skill_path>` = absolute directory containing `SKILL.md`.

## Prompt Integrity

The `prompt` field MUST contain the ENTIRE, exact text of the optimized prompt (including all formatting like `[Title]`, `[00:00-00:03] Shot 1`, etc.). Do NOT truncate, summarize, or remove formatting. The downstream model requires the FULL text to generate correctly.

**Handling Long/Multi-line Prompts**: If the prompt is long and contains newlines (like Seedance prompts), do **not** pass it via `--body '...'` inline on the command line because escaping quotes and newlines in PowerShell usually fails or causes truncation. Instead:
1. Use the `write_to_file` tool to save the complete JSON request body to a temporary file (e.g., `scratch/req.json`).
2. Run the script using `--body-file` instead of `--body`:
   `python <skill_path>/scripts/generate.py --action video-price --body-file scratch/req.json`

## Templates

**Text-to-video** (generate_type = `0`):
```json
{"generate_type":0,"model_type":88,"prompt":"{prompt}","is_switch_audio":1,"ratio":"1:1","duration":5,"resolution":"720P","motion_mode":"2","outputs":1}
```

**Image-to-video** (generate_type = `1`):
```json
{"generate_type":1,"model_type":88,"prompt":"{prompt}","is_switch_audio":1,"ratio":"1:1","duration":5,"resolution":"720P","motion_mode":"2","outputs":1,"image":"{image}","image_tail":""}
```

**Image-to-video — Seedance 2.0 Omni mode** (generate_type = `1`, model_type = `73`/`76`, function_mode = `1`):
```json
{"generate_type":1,"model_type":73,"prompt":"{prompt}","ratio":"1:1","resolution":"720P","outputs":1,"function_mode":1,"images":["{image_url_1}","{image_url_2}","{image_url_3}"]}
```
Omni mode includes `resolution` (same options as first+last frame: `480P`, `720P`, `1080P`). It does **not** include `duration`, `is_switch_audio`, `motion_mode`, `image`, or `image_tail`.

**Text-to-image** (generate_type = `3`):
```json
{"generate_type":3,"model_type":72,"prompt":"{prompt}","ratio":"auto","resolution":"1K","outputs":1}
```

**Image-to-image** (generate_type = `4`):
```json
{"generate_type":4,"model_type":72,"prompt":"{prompt}","ratio":"auto","resolution":"1K","outputs":1,"images":["{image_url_1}"]}
```

## Verification Checklist

Use only if you cannot copy the price query body verbatim:
- **Video** (excluding Seedance 2.0 Omni): `generate_type`, `model_type`, `prompt`, `is_switch_audio`, `ratio`, `duration`, `resolution`, `motion_mode`, `outputs` (and `image`, `image_tail` if image-to-video)
- **Video (Seedance 2.0 Omni)**: `generate_type`, `model_type`, `prompt`, `ratio`, `resolution`, `outputs`, `function_mode`, `images` — do NOT include `duration`, `is_switch_audio`, `motion_mode`, `image`, `image_tail`
- **Image**: `generate_type`, `model_type`, `prompt`, `ratio`, `resolution`, `outputs` (and `images` if image-to-image)
