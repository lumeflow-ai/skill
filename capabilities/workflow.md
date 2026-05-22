# Generation Workflow

## Core Rules

**Every generation request MUST follow these steps in strict order. Do NOT skip any step — especially Step 2 (query price).**

- **Output at Every Step**: Each step **MUST** send a complete message to the user **BEFORE** proceeding to the next step. Never batch multiple steps into a single response.
- All API operations use `scripts/generate.py`. It handles sign generation, HTTP requests, and encoding internally.
- `<skill_path>` = absolute directory containing `SKILL.md`. Always execute `python <skill_path>/scripts/generate.py ...` with the absolute path resolved from the `SKILL.md` you read.
- Never rewrite it to `python scripts/generate.py` or any other workspace-relative path.
- `generate.py` loads runtime product config by itself. Do not read, print, or inspect private product config files directly.
- Do not probe private config paths with `read_file`, `exec`, shell snippets, or inline Python.

## Workflow Steps

### Step 0. Upload Local Files (MANDATORY — blocks ALL subsequent steps)

**This step is a HARD BLOCK.** When the user provides a local file (image / video / audio), you MUST upload and obtain a URL **before** anything else — no analysis, no parameter tables, no price query. No exceptions.

**Trigger** — run upload IMMEDIATELY when ANY of these is true:
- User provides a local file path (e.g. `C:\photos\cat.png`, `/Users/me/video.mp4`, `D:\music.mp3`)
- User attaches/pastes a file in the conversation
- The value for `image`, `image_tail`, `images[]`, or audio fields is a local path (not `http://` / `https://`)
- File path starts with `media://` (OpenClaw platform URI)

**What to do:** Run the upload command → get URL from response → proceed to Step 1.
**What NOT to do:** Do NOT analyze, build tables, query prices, or output anything before upload completes.

For formats, size limits, commands, and `media://` resolution details, see **[upload.md](upload.md)**.

### Step 1. Build Request Body & Show Parameter Summary — MANDATORY, DO NOT SKIP

Map user input parameters to the API body JSON string. **You MUST show a parameter summary table with ALL parameters (including defaults for ones the user didn't specify) and wait for user confirmation BEFORE proceeding to Step 2.** Even if the user only provided a prompt and no other parameters, you MUST still show the full table with defaults filled in.

This includes: model, prompt, ratio, duration, resolution, motion mode, audio, outputs (and any model-specific fields). The user must see every parameter and have a chance to modify before you query price.

See **[parameter-flow.md](parameter-flow.md)** for the collection flow and table examples.

For request body templates (text-to-video, image-to-video, text-to-image, image-to-image, Seedance Omni), prompt integrity rules, and the verification checklist, see **[request-templates.md](request-templates.md)**.

### Step 2. Query Price Before Confirmation — MANDATORY, DO NOT SKIP

**This step is MANDATORY.** You MUST call the price endpoint BEFORE asking the user to confirm. Never skip this step. Never ask for confirmation first and then query price.

**Video price:**
```bash
python <skill_path>/scripts/generate.py --action video-price --body-file scratch/req.json
```

**Image price:**
```bash
python <skill_path>/scripts/generate.py --action image-price --body-file scratch/req.json
```

Show `data.integral` to the user as the estimated cost. If `data.other_discount` is non-empty, show those discount options too.

**Insufficient balance handling:** If the price query indicates insufficient balance, inform the user in a friendly tone, **automatically open** https://www.lumeflow.ai/app/pricing/ in the browser (use `os.startfile` on Windows, `open` on macOS, `xdg-open` on Linux), and **stop the workflow here — do NOT proceed to Step 3.**

**STOP RULE**: After querying the price, you **MUST** immediately output the parameter summary and estimated cost. Do **NOT** proceed to Step 3 in the same response. **MUST** wait for user's explicit confirmation in a separate message.

After showing the price, wait for confirmation:
- Confirm directly (e.g. "confirm", "yes", "go", "start") → proceed to Step 3.
- Modify parameters → update values, **re-query price (repeat Step 2)**, show updated summary, wait again.

### Step 3. Send Generation Request (only after user confirms)

**Only send the API request after user confirms the quoted price and parameters.**

**CRITICAL — Body Consistency Rule**: The `--body` JSON in this step **MUST be copied verbatim** from the `--body` you already used in Step 2 (price query). **Do NOT rebuild the JSON from scratch** — directly reuse the exact same string. This eliminates field-dropping bugs.

If any parameter from the Step 2 body is missing from the Step 3 body, the request is **invalid** — fix it before sending.

Use `--action watch-video` / `--action watch-image` to submit AND poll. See **[result-handling.md](result-handling.md)** for watch commands, response formats, result presentation, and retry logic.

### Step 4. Polling — handled automatically by `watch`

`watch-video` / `watch-image` polls in the foreground until done. No separate query step needed.

### Step 5. Auto-Retry When Watch Times Out

If `watch` returns with `status: "processing"`, you MUST automatically continue polling. See **[result-handling.md](result-handling.md)** for the retry protocol.

### Step 6. Check Balance

```bash
python <skill_path>/scripts/generate.py --action balance
```

**Do NOT re-present the generation result in this step.** The result has already been shown after watch returned (Step 3 / result-handling). Only update the credits shown in the previous step if the balance query returns a different value. Never repeat the task ID, status, or download links.

### Step 7. View Local Task History

```bash
python <skill_path>/scripts/generate.py --action tasks
python <skill_path>/scripts/generate.py --action tasks --status completed --limit 10
```

Available statuses: `pending` | `processing` | `completed` | `failed`

**When presenting historical tasks**: show download link from `result_urls` only. Use `[下载视频资源](url)` or `[下载图片资源](url)` depending on task type. Never use `result_urls_watermark`.


## Auth

`generate.py` resolves runtime product config by default. It will fail fast if `LUMEFLOW_BASE_URL` or `LUMEFLOW_API_KEY` is missing.

All requests use these headers (built into `generate.py`):
```
api-key: loaded from private product config or env fallback
platform: openclaw
version: 1.0.0
```

### Missing / Expired api_key — Auto-Login

If `generate.py` reports a missing `LUMEFLOW_API_KEY`, or any API call returns HTTP 401 / 403:

1. **Do NOT** output "Please log in again" — strictly forbidden.
2. **Immediately** run `python <skill_path>/scripts/login.py` (foreground, no background).
3. The script handles everything: generates login_key, opens browser, polls for api_key, persists it.
4. stderr outputs the login URL — forward it to the user.
5. The script blocks until login succeeds or times out (~200s). When it returns, resume the original workflow.

**The user does nothing except click the login link. You run one command and wait.**
