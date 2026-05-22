# Result Handling, Watch Responses & Retry Logic

`<skill_path>` = absolute directory containing `SKILL.md`.

## Watch Command

**You MUST use `--action watch-video` or `--action watch-image` to submit AND poll in a single blocking call.**

**FORBIDDEN**: Do NOT use `--action video` or `--action image` without watch. Those actions only submit and do NOT poll — using them alone will leave the task unresolved.

**Video generation (submit + continuous foreground poll):**
```bash
python <skill_path>/scripts/generate.py --action watch-video --body-file scratch/req.json
```

**Image generation (submit + continuous foreground poll):**
```bash
python <skill_path>/scripts/generate.py --action watch-image --body-file scratch/req.json
```

The script will block in the foreground and:
1. Submit the generation request
2. Persist the task locally (ID, status, prompt, model, cost) to a JSON store
3. Poll every 8 seconds in the foreground until the task completes or 10 minutes elapse
4. Return the final result (with `result_urls` if completed)

**You MUST wait for the `watch` command to return before outputting anything to the user.**
Do NOT send an intermediate response while watch is running — wait for the full result, then output.

## Watch Response Formats

**When completed:**
```json
{
  "local_id": "uuid-v4",
  "task_ids": [22222],
  "type": "video",
  "status": "completed",
  "result_urls": ["https://cdn.example.com/video.mp4"],
  "result_urls_watermark": ["https://cdn.example.com/video_digital.mp4"],
  "result_cover_urls": ["https://cdn.example.com/cover.jpg"],
  "integral_used": 50,
  "integral_remaining": 3944
}
```

**When timeout (still processing on server):**
```json
{
  "local_id": "uuid-v4",
  "task_ids": [22222],
  "type": "video",
  "status": "processing",
  "result_urls": [],
  "error": "Client timeout after 600s — task may still be running on server"
}
```

## Result Handling Rules

- If `result_urls_watermark` is non-empty (has URL from `images[*].image` or `video`) → show the download link(s). Show preview image if available.
- If `result_urls` is also non-empty (has `origin_thumbnail` or `digital_video`) → show **two** download links (no-watermark + watermark).
- If **only** `result_urls_watermark` has URLs and `result_urls` is empty → show a single download link labeled `[Download]` (do NOT hide the result just because no-watermark URL is unavailable).
- If `result_urls` is empty **AND** `result_urls_watermark` is empty **AND** `raw_query_response` is present in the watch output:
  - **You MUST inspect `raw_query_response` yourself and extract any image/video URL from it.**
  - Video: `data[*].digital_video` (no-watermark), `data[*].video` (watermark), `data[*].cover_url` (cover)
  - Image: `data[*].images[*].origin_thumbnail` (no-watermark), `data[*].images[*].image` (watermark), `data[*].images[*].thumbnail` (watermark thumbnail)
  - **Do NOT say "platform didn't return a URL"** — if the task status is completed, the URL is in the raw response; find it.
  - If you genuinely cannot find a URL anywhere in `raw_query_response`, run `--action image-query` / `--action video-query` once more and inspect that output.
- If `status == "processing"` (watch timed out) → **AUTOMATICALLY ENTER RETRY LOOP** (see below).
- If `status == "failed"` → check `error_code` in the result or `raw_query_response`. Look up the code in [references/api_reference.md](../references/api_reference.md) "Task Failure Error Codes" table. **Translate the message to the user's language** and output it. Always tell the user: **失败不扣积分** (credits are not deducted for failed tasks). If no `error_code` is found, use a generic friendly message.
  - **Special case: `error_code` 2002** — Tell the user: "Sensitive content has been detected and will be removed after review and confirmation. Please check." Then guide them to view the result at https://www.lumeflow.ai/app/mycreations/ (open the browser automatically).

## Presenting Results

After watch returns successfully, present the result in a friendly, human-readable format:

- Mention the task ID naturally (e.g. "Your task ID is 22222.")
- Show the status (e.g. "completed", "processing", "failed")
- **Do NOT embed image preview** (`![preview](...)` is forbidden). Only show download links.
- **Download buttons** — use markdown `[text](url)` syntax, one button per URL in `result_urls`. **Labels MUST adapt to the user's language** (e.g. Chinese: `[下载视频资源]`/`[下载图片资源]`, English: `[Download Video]`/`[Download Image]`).
  - Never show watermark/no-watermark distinction. Never show `result_urls_watermark`.
- Show remaining credits in natural language — use `integral_remaining` from the watch response if available

**Example output (Chinese user):**
```
任务 ID：27502
状态：已完成
[下载图片资源](https://resource.utdownload.com/.../image.jpeg)
剩余积分：209
```

**Example output (English user):**
```
Task ID: 27502
Status: Completed
[Download Image](https://resource.utdownload.com/.../image.jpeg)
Credits remaining: 209
```

## Auto-Retry When Watch Times Out (`status == "processing"`)

> ⚠️ **MANDATORY AUTOMATIC BEHAVIOR** — No user input required.

The OpenClaw exec tool has a 120-second hard timeout. If image/video generation takes longer, `watch` returns early with `status: "processing"`. **You MUST continue polling automatically:**

```
LOOP:
  1. Wait ~30 seconds (brief message: "Generating, please wait...")
  2. Run:
       python <skill_path>/scripts/generate.py --action image-query --ids {task_id}
       # or: --action video-query for videos
  3. Parse the JSON output:
       - If any data[*].status == 1 (or "completed"/"finish") → DONE, extract URL
       - If any data[*].status == 0 (or "processing") → continue loop
       - If any data[*].status >= 2 (or "failed") → report failure, exit loop
  4. Repeat until done or 10 minutes total elapsed
ENDLOOP
```

**URL extraction for image tasks:**
- No-watermark:  `data[*].origin_thumbnail` or `data[*].images[*].origin_thumbnail`
- Watermark:     `data[*].images[*].image` or `data[*].images[*].thumbnail` or `data[*].images[*].digital_image`

**URL extraction for video tasks:**
- No-watermark:  `data[*].digital_video`  → `result_urls`
- Watermark:     `data[*].video`          → `result_urls_watermark`
- Cover image:   `data[*].cover_url` or `data[*].cover` (single)

**Example re-query commands:**
```bash
python <skill_path>/scripts/generate.py --action image-query --ids {task_id}
python <skill_path>/scripts/generate.py --action video-query --ids {task_id}
```
