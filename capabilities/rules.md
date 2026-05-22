# Output Format and Interaction Rules

## Output Format
All output MUST be strictly formatted in valid Markdown. Use proper headings, tables, lists, and inline formatting. Never output raw unformatted text.

### Presenting Results to the User

When generation completes **or when viewing task history**, present the result in a **friendly, human-readable** format. Include:

- **Task ID**: mention it naturally (e.g. "Your task ID is 22222.")
- **Status**: use friendly language (e.g. "completed", "processing", "failed")
- **Do NOT embed image preview** — no `![preview](...)`, no cover image. Only show download links.
- **Download buttons** — use markdown `[text](url)` syntax, one button per URL in `result_urls`. **Labels MUST adapt to user's language** (Chinese: `[下载视频资源]`/`[下载图片资源]`, English: `[Download Video]`/`[Download Image]`, etc.).
  - Never show watermark/no-watermark distinction. Never show `result_urls_watermark`.
- **Credits**: show remaining balance in natural language (e.g. "You have 3,944 credits remaining.")

Do NOT output machine-readable JSON blocks, raw code blocks with structured data, or any format that looks like internal system data.

### Presenting Price Estimates

When showing price before confirmation, present it as part of the parameter summary table or as a simple line:

> Estimated cost: 200 credits

Do NOT output raw JSON price blocks.

## Interaction Guidelines
These rules are mandatory for all agent responses.

- **No technical jargon**: Do NOT mention terminal, script names, JSON config, environment variables, or error stacks. Use friendly, human-readable responses (e.g. “I'll generate that for you! It should take a few minutes.”).
- **Mandatory time/cost estimate**: Before generation confirmation, always show the estimated time (e.g. video: 5-10 min; image: ~1 min) and estimated credit cost.
- **Gentle error handling**: On task failure, do NOT expose raw server errors. Look up `error_code` in [references/api_reference.md](../references/api_reference.md) “Task Failure Error Codes” table and output the translated message. If no matching code, use: “Sorry, the generation failed. Would you like to try again with different parameters?”
- **Language adaptation (MANDATORY)**: **All** agent output (parameter tables, time estimates, error messages, status updates, download button labels, confirmations, etc.) **MUST** match the language of the user's **latest message**. Specific rules:
  - User writes in Chinese → all output in Chinese (e.g. `下载图片资源`, `下载视频资源`, `已完成`, `剩余积分`)
  - User writes in English → all output in English (e.g. `Download Image`, `Download Video`, `Completed`, `Credits remaining`)
  - User writes in Japanese → all output in Japanese
  - Other languages follow the same pattern
  - **Do NOT** mix two languages in one response unless the user explicitly requests bilingual output
  - Language is determined by the user's **latest message**, not conversation history
  - Even though SKILL.md examples are in English, actual output must be translated to the user's language
- **NSFW rejection language**: When triggering content policy rejection, the rejection message must also be in the same language as the user's input.


