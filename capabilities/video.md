# Video Generation Capability

## Video Models (name -> model_type)
| Model Name | `model_type` | Notes |
|------------|-------------|-------|
| Pixverse V5.5 | `28` | Fast, simple videos |
| Lumeflow 3.0 | `9` | One of two catalog models that use **`9`**. Supports seed, V2V. Durations `5`, `8` s; **resolution depends on duration** — **Video resolution (`model_type` 9)**. |
| Pixverse V5 | `9` | One of two catalog models that use **`9`**. Supports seed, V2V. Durations `5`, `8` s; **resolution depends on duration** — **Video resolution (`model_type` 9)**. |
| Kling 1.6 | `1` | Audio forced on |
| Kling 2.5 | `19` | Audio forced on |
| Kling 2.6 | `29` | Duration 5, 10s |
| Kling 3.0 | `65` | duration 3-15s |
| Kling O1 | `30` | Duration 5, 10s |
| Hailuo 02 | `3` | No audio; **no `720P`** — use `768P` / `1080P` by duration (see **Video resolution (Hailuo / `model_type` 3, 23, 25)**) |
| Hailuo 2.3 | `23` | No audio; **no `720P`** — use `768P` / `1080P` by duration (see **Video resolution (Hailuo / `model_type` 3, 23, 25)**) |
| Hailuo 2.3 Fast | `25` | No audio; **no `720P`** — use `768P` / `1080P` by duration (see **Video resolution (Hailuo / `model_type` 3, 23, 25)**) |
| Google Veo 3.1 | `4` | Fixed 8s, audio forced on |
| Google Veo 3.1 Fast | `5` | Fixed 8s, audio forced on |
| Pixverse V4.5 | `41` | Duration 5, 8s |
| Vidu Q1 | `6` | Duration unknown — check [references/ai_models_analysis.md](references/ai_models_analysis.md) before use |
| Vidu Q2 | `26` | Duration unknown — check [references/ai_models_analysis.md](references/ai_models_analysis.md) before use |
| Vidu Q2 Turbo | `24` | Duration unknown — check [references/ai_models_analysis.md](references/ai_models_analysis.md) before use |
| Wan 2.5 | `63` | Supports seed, audio forced on |
| Wan 2.6 | `64` | duration 2-15s, supports shot_type, audio forced on |
| Seedance 2.0 | `73` | Audio forced on |
| Seedance 2.0 Fast | `76` | Audio forced on |
| Pixverse C1 | `88` | **Default**. duration 2-15s |
| Wan 2.7 | `89` | duration 2-15s, audio forced on |
| HappyHorseV1.0 | `104` | duration 2-15s, supports text-to-video and image-to-video |



## Video Parameters
| Parameter | Description | Options | Default |
|-----------|-------------|---------|---------|
| `prompt` | Text description of the video | - | *(must ask user)* |
| `generate_type` | Generation type | `0`=text-to-video, `1`=image-to-video | `0` |
| `model_type` | Model ID (user selects by **model name**, auto-converted) | See video models table | `88` (Pixverse C1) |
| `ratio` | Aspect ratio | `16:9`, `9:16`, `1:1` | `1:1` |
| `duration` | Video duration in seconds | Varies by model | Depends on model |
| `resolution` | Output resolution | Varies by model | `720P` when default model is Pixverse C1 (`88`); **Hailuo (`3`/`23`/`25`)** — see **Video resolution (Hailuo)** (use `768P`, not `720P`) |
| `motion_mode` | Motion intensity | `0`=none, `1`=slight, `2`=medium, `3`=strong | `2` |
| `is_switch_audio` | Enable audio | `0`=off, `1`=on | `1` |
| `outputs` | Number of videos to generate | `1` - `4` | `1` |
| `image` | Input image URL (**required if generate_type=1**) | Any valid image URL | `""` |
| `image_tail` | Tail frame image URL (first+last frame control) | Any valid image URL | `""` |
| `function_mode` | Reference mode (Seedance 2.0/Fast image-to-video only) | `0`=first+last frame, `1`=Omni reference | `0` |
| `images` | Reference image URL array (Omni mode, `function_mode=1`, required) | Array of image URLs | `[]` |


## Video Duration Constraints
Video duration must be selected from the current model's supported values. Do not reuse a generic `5s` default across models.

| Models | `model_type` | Allowed `duration` |
|--------|--------------|--------------------|
| Kling 1.6 / 2.5 | `1`, `19` | `5`, `10` |
| Kling 2.6 | `29` | `5`, `10` |
| Kling O1 | `30` | `5`, `10` |
| Kling 3.0 | `65` | `3`-`15` |
| Lumeflow 3.0 | `9` | `5`, `8` |
| Pixverse V5 | `9` | `5`, `8` |
| Pixverse V4.5 | `41` | `5`, `8` |
| Pixverse V5.5 | `28` | `5`, `8`, `10` |
| Hailuo 02 / 2.3 / 2.3 Fast | `3`, `23`, `25` | `6`, `10` |
| Google Veo 3.1 / 3.1 Fast | `4`, `5` | fixed `8` |
| Wan 2.5 | `63` | `5`, `10` |
| Wan 2.6 | `64` | `2`-`15` |
| Seedance 2.0 / 2.0 Fast | `73`, `76` | `5`, `10`, `15` |
| Pixverse C1 | `88` | `2`-`15` |
| Wan 2.7 | `89` | `2`-`15` |
| HappyHorseV1.0 | `104` | `2`-`15` |

For any video model not listed above, do not guess a duration. Check [references/ai_models_analysis.md](references/ai_models_analysis.md) first before quoting price or sending the request.


## Video resolution (`model_type` 9)
**Lumeflow 3.0** and **Pixverse V5** are **two separate models** in the catalog; **both** use `model_type` **`9`** in the request body. The API uses the same rules for this id. Allowed `resolution` **depends on `duration`**:

| `duration` | Allowed `resolution` values |
|------------|----------------------------|
| `5` | `360P`, `540P`, `720P`, `1080P` |
| `8` | `360P`, `540P`, `720P` only (do **not** use `1080P`) |

When **either** Lumeflow 3.0 or Pixverse V5 is selected (`model_type` `9`), the parameter summary table **must** list resolution options that match the **current** `duration`. If the user changes `duration`, recompute the allowed resolutions before Step 2 (price) or Step 3 (generate).


## Video resolution (Hailuo)
**Hailuo does not support `720P`.** Allowed `resolution` depends on `duration`:

| `duration` | Allowed `resolution` values |
|------------|----------------------------|
| `6` | `768P`, `1080P` |
| `10` | `768P` only (do **not** use `1080P` or `720P`) |

When Hailuo is selected, the parameter summary table **must** list these options (not the Pixverse C1 list `360P` … `1080P`). If the user changes `duration`, recompute allowed resolutions before Step 2 or Step 3.


## Parameter Rules (Video)
- **Model selection**: Show model **name** to the user (e.g. "Pixverse V5.5"), convert to `model_type` number in the request body. User says "use Kling 3.0" → `model_type: 65`. User says "use Lumeflow 3.0" **or** "use Pixverse V5" → **`model_type: 9`** (two different product names, **same** numeric id).
- **Video duration is model-bound**: choose `duration` only from the current model's supported values/range. When the model changes, recompute the duration options before building the body or querying price.
- **`model_type` 9 (Lumeflow 3.0 or Pixverse V5) — resolution vs duration**: Applies to **both** models. When `duration` is `5`, `resolution` may be `360P`, `540P`, `720P`, or `1080P`. When `duration` is `8`, `resolution` may only be `360P`, `540P`, or `720P` (not `1080P`). If the user picks 8s and 1080P, change duration to `5` or lower resolution before quoting price or generating.
- **Hailuo (`model_type` 3, 23, 25) — resolution vs duration**: Do **not** use `720P`. When `duration` is `6`, `resolution` may be `768P` or `1080P`. When `duration` is `10`, `resolution` must be `768P` only. If the user asks for 1080P at 10s, explain that only `768P` is allowed for that duration (or switch to `6`s for `1080P`).
- **Audio forced on models**: The following models do NOT support disabling audio — always set `is_switch_audio` to `1` and do NOT show audio as a toggleable option in the parameter summary table: Seedance 2.0 (`73`), Seedance 2.0 Fast (`76`), Wan 2.7 (`89`), Wan 2.6 (`64`), Wan 2.5 (`63`), Kling 2.5 (`19`), Kling 1.6 (`1`), Google Veo 3.1 (`4`), Google Veo 3.1 Fast (`5`). When the user selects one of these models, override `is_switch_audio` to `1` silently and display audio as "On (1) (cannot be disabled for this model)" in the summary table.

- `generate_type` is an internal parameter — do not ask user to change.
- All parameters must be included in the request body.
- If user describes preference like "landscape" → `ratio: "16:9"`, "portrait" → `ratio: "9:16"`, "HD" → video `resolution: "1080P"` or image `resolution: "4K"` — **except** for **Hailuo** with `duration: 10`, where the maximum video resolution is **`768P`** (not `1080P`).
- Refer to [references/ai_models_analysis.md](references/ai_models_analysis.md) for model-specific parameter constraints (e.g. duration ranges, forced audio, resolution limits).
- **Seedance 2.0 `function_mode`** (only when `model_type=73/76` AND `generate_type=1` image-to-video):
  - `function_mode=0` (first+last frame): pass `image` (start frame) + `image_tail` (end frame), along with `duration`, `is_switch_audio`, `resolution`, `motion_mode`. This is the default mode.
  - `function_mode=1` (Omni reference): pass `images[]` with all reference image URLs and **`resolution`** (`480P`, `720P`, or `1080P`, default `720P`). Do **NOT** pass `duration`, `is_switch_audio`, `motion_mode`, `image`, or `image_tail`.
  - When reference images **< 3**: both modes are available — default to `function_mode=0`, but allow the user to choose `function_mode=1`.
  - When reference images **>= 3**: force `function_mode=1` (Omni). Do not show the first+last frame option in the parameter summary table.
  - In the parameter summary table, show a "Reference Mode (function_mode)" row when Seedance 2.0/Fast image-to-video is selected. Options: "First+Last Frame (0), Omni Reference (1)" — or only "Omni Reference (1)" if images >= 3.
  - For **Omni (`function_mode=1`)**, always include a **Resolution** row in the summary table (options: `480P`, `720P`, `1080P`) — same as first+last frame for Seedance 2.0/Fast.
  - Use the **Seedance 2.0 Omni mode** request body template when `function_mode=1`.



