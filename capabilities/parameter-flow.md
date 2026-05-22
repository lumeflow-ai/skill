# Parameter Collection Flow

When the user requests generation, **you MUST present ALL configurable parameters** for confirmation before sending the request. **Never skip this step, even if the user only provided a prompt.** If the user didn't specify a parameter, fill in the default and still show it in the table.

## Flow

1. **Determine generation type** from user intent (video/image, text/image input).
2. **Resolve model-specific constraints first**. For video generation, determine the selected model, then derive the allowed `duration` values/range from the models table before filling defaults or quoting price.
3. **Show a parameter summary table** with the current value for each parameter (user-provided or model-aware default). **The "Options" column must list concrete model names from the models table — never use vague text like "or other models".**

   > **Language Rule**: All output text (table labels, confirmation prompts, error messages, status updates, etc.) **MUST** be in the **same language as the user's input**. The English examples below are the default — translate to the user's language if they write in Chinese, Japanese, etc.

4. **Wait for user to confirm or modify parameters.** Do NOT proceed to price query until the user has explicitly confirmed the parameters (or you asked and they confirmed).
5. **Proceed to price query** — this is mandatory before asking for final confirmation.

## Example: Video

> About to generate a video with the following parameters:
>
> | Parameter | Current Value | Options |
> |-----------|---------------|---------|
> | Model | Pixverse C1 | Pixverse C1, Kling 3.0, Wan 2.7, Seedance 2.0, Hailuo 2.3, Google Veo 3.1, etc. |
> | Prompt | A flower swaying in the wind | - |
> | Ratio | 1:1 | 16:9, 9:16, 1:1 |
> | Duration | 5s | 2-15 |
> | Resolution | 720P | 360P, 540P, 720P, 1080P |
> | Motion Mode | Medium (2) | None (0), Slight (1), Medium (2), Strong (3) |
> | Audio | On (1) | Off (0), On (1) |
> | Outputs | 1 | 1-4 |
>
> Let me know if you'd like to change anything, or confirm to start generating.

**Hailuo note**: The example above uses **Pixverse C1** defaults (`720P` and the C1 resolution list). If the user selects **Hailuo** (`model_type` `3`, `23`, or `25`), replace the resolution row with values from **Video resolution (Hailuo)** — never offer or default to `720P` for Hailuo.

## Example: Image

> About to generate an image with the following parameters:
>
> | Parameter | Current Value | Options |
> |-----------|---------------|---------|
> | Model | Nano Banana V2 | Nano Banana V2, Nano Banana Pro, Seedream 5.0, Seedream 4.0, GPT Image 2 |
> | Prompt | An orange cat sitting by a spaceship window | - |
> | Ratio | auto | auto, 16:9, 9:16, 1:1, etc. |
> | Resolution | 1K | 1K, 2K, 4K |
> | Outputs | 1 | 1-4 |
>
> Let me know if you'd like to change anything, or confirm to start generating.
