# AI Model Integration Parameter Analysis

> Generated: 2026-03-19 | Project: `memevid_web`

---

## 1. Model Overview

### Unified API Endpoints

| Category | HTTP Method | Endpoint Path |
|----------|-------------|---------------|
| Video generation (text/image/video-to-video) | POST | `/api/lumeflow/video-generate` |
| Image generation (text/image-to-image) | POST | `/api/lumeflow/image-generate` |
| AI image effects | POST | `/api/lumeflow/image-effects-generate` |

**Key discriminator fields**: `model_type` (numeric enum) + `generate_type` (0/1/3 for video; 3/4 for image)

---

## 2. Video Generation Models (`/api/lumeflow/video-generate`)

### 2.1 Model ID Reference

| Model Name | `model_type` | Version |
|------------|-------------|---------|
| Kling 1.6 | `1` | V1.6 |
| Kling 2.5 | `19` | V2.5 |
| Kling 3.0 | `65` | V3.0 |
| Lumeflow 3.0 | `9` | Lumeflow 3.0 |
| Pixverse V5 | `9` | V5 (distinct product from Lumeflow 3.0, shares `model_type` `9`) |
| Pixverse V5.5 | `28` | V5.5 |
| Hailuo 02 | `3` | V02 |
| Hailuo 2.3 | `23` | V2.3 |
| Hailuo 2.3 Fast | `25` | V2.3 fast |
| Google Veo 3.1 | `4` | V3 |
| Google Veo 3.1 Fast | `5` | V3 fast |
| Vidu Q1 | `6` | VQ1 |
| Vidu Q2 | `26` | VQ2 |
| Vidu Q2 Turbo | `24` | VQ2 turbo |
| Wan 2.5 | `63` | V2.5 |
| Wan 2.6 | `64` | V2.6 |
| Seedance 2.0 | `73` | V2.0 |
| Seedance 2.0 Fast | `76` | V2.0 fast |
| Pixverse C1 | `88` | C1 |
| Wan 2.7 | `89` | V2.7 |

> **Note**: `generate_type` values: `0` = text-to-video, `1` = image-to-video, `3` = video-to-video (not supported by this skill)

---

### 2.2 Common Parameters (shared by all video models)

| API Field | Frontend Field | Type | Required | Default | Description |
|-----------|---------------|------|----------|---------|-------------|
| `model_type` | `model_type` | `number` | Yes | — | Model enum ID |
| `generate_type` | `generate_type` | `0 \| 1 \| 3` | Yes | — | Generation mode |
| `prompt` | `prompt` | `string` | Conditional | `''` | Text prompt, required for text-to-video |
| `is_switch_audio` | `sound` | `0 \| 1` | No | `1` | Audio on/off (0=off, 1=on). Forced to 1 for Kling/Sora/Veo/Wan |
| `duration` | `duation` | `number` | No | Model default | Duration in seconds |
| `ratio` | `size` | `string` | No | Model default | Aspect ratio, e.g. `'16:9'` `'1:1'` `'9:16'` |
| `resolution` | `resolution` | `string` | No | Model default | Resolution, e.g. `'720P'` `'1080P'` |
| `style` | `style` | `string` | No | `'0'` | Style ID (Pixverse only) |
| `cfg_scale` | `creativeRelevance` | `number` | No | `0.5` | Creative relevance (frontend 0–100, divide by 100 for API, range 0–1) |
| `motion_mode` | `mode` | `string` | No | `'1'` | Motion mode: `'1'`=standard, `'2'`=expert |
| `moition_range` | `motionRange` | `string` | No | `''` | Motion range (note: `moition_range` is the actual API field name — typo preserved for compatibility) |
| `image` | `image1` | `string` | Conditional | `''` | Start frame image URL (required for image-to-video) |
| `image_tail` | `image2` | `string` | No | `''` | End frame image (required for first+last frame mode) |
| `outputs` | `outputs` | `number` | No | `1` | Number to generate (1–4) |
| `seed` | `seed` | `number` | No | Random | Random seed (`model_type` `9`: Lumeflow 3.0 & Pixverse V5; Wan, etc.) |
| `negative_prompt` | `negative_prompt` | `string` | No | `''` | Negative prompt (commented out, not yet enabled) |
| `shot_type` | `shot_type` | `'single' \| 'multi'` | No | Model dependent | Shot mode (Wan 2.6 only; frontend 1→`'multi'`, else→`'single'`) |
| `function_mode` | `function_mode` | `0 \| 1` | No | `0` | Function mode (Seedance 2.0 only: 0=first+last frame, 1=Omni reference) |
| `videos` | — | `string[]` | Conditional | — | Video URL array for Seedance 2.0 Omni mode |
| `images` | — | `string[]` | Conditional | — | Image URL array for Seedance 2.0 Omni mode |
| `inspiration_id` | — | `string` | No | — | Inspiration template ID (injected via URL query) |

---

### 2.3 Model-Specific Parameter Details

#### Kling Series (model_type: 1/19/65)

| API Field | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `prompt` | `string` | Yes | — | V1.6/V2.5: max 2000 chars; V3.0: max 2500 chars (text-to-video) / all: max 2500 chars (image-to-video) |
| `duration` | `number` | Yes | `5` | V1.6/V2.5: `5,10`; V3.0: `3–15` |
| `ratio` | `string` | No | `'1:1'` | Text-to-video: `'16:9'` `'1:1'` `'9:16'` (not available for image-to-video) |
| `cfg_scale` | `number` | No | `0.5` | Creative relevance |
| `motion_mode` | `string` | No | `'1'` | `'1'`=standard `'2'`=expert |
| `is_switch_audio` | `0 \| 1` | No | `1` | V3.0 supports audio |
| `image` | `string` | Conditional | — | Start frame for image-to-video |
| `image_tail` | `string` | No | — | End frame (only when first+last frame enabled) |
| `outputs` | `number` | No | `1` | 1–4 |

**Parameter linkage**:
- `version = 'V3.0'` → `duration` range 3–15, UI switches to Slider
- `isFirstLastFrameEnabled = false` → do not pass `image_tail`

---

#### Pixverse Series (model_type: 9/28/88)

**`model_type` `9`** covers two distinct product lines: **Lumeflow 3.0** and **Pixverse V5** (not aliases); both use `model_type: 9` in the request body with identical parameter constraints.

| API Field | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `prompt` | `string` | Yes | — | Max 2000 chars |
| `duration` | `number` | Yes | — | **`9` (Lumeflow 3.0, Pixverse V5)**: `5,8`; V5.5: `5,8,10`; C1: `2–15` (Slider) |
| `resolution` | `string` | Yes | `'540P'` | **`9` (Lumeflow 3.0, Pixverse V5)**: `duration=5` → `360P,540P,720P,1080P`; `duration=8` → `360P,540P,720P` (no 1080P); V5.5/C1 see below |
| `ratio` | `string` | No | — | Text-to-video: `'16:9'` `'1:1'` `'9:16'` (not for image-to-video) |
| `style` | `string` | No | `'0'` | V5: `0–5` (auto/anime/3d/comic/cyberpunk/clay); V5.5: `0–4` |
| `is_switch_audio` | `0 \| 1` | No | `0` | Supported by `9`, V5.5, C1 |
| `seed` | `number` | No | `1` | Supported by `9`, V5.5, C1 |
| `image` | `string` | Conditional | — | Start frame for image-to-video |
| `image_tail` | `string` | No | — | End frame (supported by `9`, V5.5, C1) |
| `video` | `string` | Conditional | — | Source video for V2V (`model_type`=`9`, i.e. Lumeflow 3.0 or Pixverse V5) |
| `outputs` | `number` | No | `1` | 1–4 (discount: 2 items 95%, 3 items 90%, 4 items 85%) |

**Parameter linkage**:
- **`model_type` `9` (Lumeflow 3.0 & Pixverse V5)**: `duration=5` → resolution `360P`–`1080P`; `duration=8` → only `360P`–`720P` (no `1080P`)
- **V5.5 (`28`)**: `duration=8` → max `720P`; `duration=10` → max `720P`
- `seed` applies to: `9`, V5.5, C1
- `type='video'` → pass `video` (source video URL) instead of `image`

---

#### Pixverse C1 (model_type: 88)

| API Field | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `prompt` | `string` | Yes | — | Max 2000 chars |
| `duration` | `number` | Yes | — | `2–15` (Slider, integer) |
| `resolution` | `string` | Yes | `'720P'` | Supports `360P,540P,720P,1080P` |
| `ratio` | `string` | No | — | Text-to-video: `'16:9'` `'1:1'` `'9:16'` |
| `is_switch_audio` | `0 \| 1` | No | `0` | Toggleable |
| `image` | `string` | Conditional | — | Start frame |
| `image_tail` | `string` | No | — | End frame |
| `outputs` | `number` | No | `1` | 1–4 (discount: 2 items 95%, 3 items 90%, 4 items 85%) |

---

#### Hailuo Series (model_type: 3/23/25)

| API Field | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `model_type` | `3 \| 23 \| 25` | Yes | `0` (dynamic) | 3=Hailuo02, 23=V2.3, 25=V2.3 Fast |
| `prompt` | `string` | Yes | — | Max 2000 chars |
| `duration` | `number` | Yes | — | `6` or `10` |
| `resolution` | `string` | Yes | `'768P'` | Duration 6: `768P,1080P`; duration 10: only `768P` |
| `image` | `string` | Conditional | — | Start frame |
| `outputs` | `number` | No | `1` | 1–4 (same discount as Pixverse) |

> **Note**: Hailuo does **not** support `720P` (API has no such option). Hailuo series does **not** support audio. `model_type` switches dynamically within the same component (23↔25); the main composable's `hailuo02` key maps to type `3` (Hailuo02 version).

---

#### Google Veo 3.1 (model_type: 4/5)

| API Field | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `model_type` | `4 \| 5` | Yes | `5` | 4=Veo3.1, 5=Veo3.1 Fast |
| `prompt` | `string` | Yes | — | Max 2000 chars |
| `duration` | `number` | Yes | `8` | Fixed `8` seconds |
| `ratio` | `string` | No | `'16:9'` | `'16:9'` `'9:16'` |
| `is_switch_audio` | `0 \| 1` | — | `1` | Forced to 1 |
| `image` | `string` | Conditional | — | Start frame |
| `outputs` | `number` | No | `1` | 1–4 (discount: 2 items 95%, 3 items 90%, 4 items 85%) |

---

#### Wan Series (model_type: 63/64/89)

| API Field | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `prompt` | `string` | Yes | — | V2.5/V2.6: max 1500 chars; V2.7: max 5000 chars |
| `duration` | `number` | Yes | — | V2.5: `5,10`; V2.6: `2–15` (Slider); V2.7: `2–15` (Slider) |
| `resolution` | `string` | Yes | `'768P'` | V2.5: `480P/720P/1080P`; V2.6: `720P/1080P`; V2.7: `720P/1080P` |
| `ratio` | `string` | Conditional | `'1:1'` | Required for text-to-video: `'16:9'` `'9:16'` `'1:1'` `'4:3'` `'3:4'`; not for image-to-video |
| `is_switch_audio` | `0 \| 1` | — | `1` | Displayed in UI but disabled (forced to 1) |
| `shot_type` | `'single' \| 'multi'` | No | `'single'` | V2.6 only; frontend 1→`'multi'`, else→`'single'` |
| `seed` | `number` | No | Random | Random integer seed |
| `image` | `string` | Conditional | — | Start frame |
| `outputs` | `number` | No | `1` | 1–4 (Wan/Kling: no tiered discount) |

**Parameter linkage (V2.5 text-to-video)**: `resolution` determines available `ratio` options (480P has 3 ratios, 720P/1080P have 5)

---

#### Seedance 2.0 (model_type: 73/76)

| API Field | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `model_type` | `73 \| 76` | Yes | `76` | 73=Seedance2.0, 76=Seedance2.0 Fast |
| `prompt` | `string` | Yes | — | Max 5000 chars |
| `duration` | `number` | Yes | `5` | `5,10,15` |
| `ratio` | `string` | No | `'1:1'` | `'auto'` `'16:9'` `'9:16'` `'4:3'` `'3:4'` |
| `resolution` | `string` | Yes | — | Options: `480P / 720P / 1080P` |
| `is_switch_audio` | `0 \| 1` | Yes | `1` | Audio forced on for both text-to-video and image-to-video |
| `function_mode` | `0 \| 1` | Conditional (i2v) | `0` | Image-to-video only: `0`=first+last frame, `1`=Omni reference |
| `image` | `string` | Conditional | — | Start frame for first+last frame mode (`function_mode=0`) |
| `image_tail` | `string` | Yes (first+last) | — | End frame for first+last frame mode |
| `videos` | `string[]` | Conditional | — | Video URL array for Omni mode (`function_mode=1`) |
| `images` | `string[]` | Conditional | — | Image URL array for Omni mode (`function_mode=1`) |
| `outputs` | `number` | No | `1` | 1–4 |

**Parameter linkage**:
- `function_mode = 0` (first+last frame) → pass `image` + `image_tail` + `is_switch_audio` + `duration` + `resolution` + `motion_mode`, etc.
- `function_mode = 1` (Omni reference) → pass `videos[]` + `images[]` (filtered from `mediaList`) + **`resolution`** (`480P` / `720P` / `1080P`); do NOT pass `duration`, `is_switch_audio`, `motion_mode`, `image`, `image_tail`
- `resolution` same as first+last frame mode: `480P / 720P / 1080P`

---

## 3. Image Generation Models (`/api/lumeflow/image-generate`)

### 3.1 Model ID Reference

| Model Name | `model_type` |
|------------|-------------|
| Nano Banana V1 | `18` |
| Nano Banana V2 | `72` |
| Nano Banana Pro | `37` |
| Seedream 4.0 | `12` |
| Seedream 5.0 | `80` |
| GPT Image 2 | `101` |

> `generate_type`: `3` = text-to-image, `4` = image-to-image

### 3.2 Common Parameters

| API Field | Frontend Field | Type | Required | Description |
|-----------|---------------|------|----------|-------------|
| `model_type` | `model_type` | `number` | Yes | Same as above |
| `generate_type` | `generate_type` | `3 \| 4` | Yes | Generation mode |
| `prompt` | `prompt` | `string` | Yes | Prompt (required for both text-to-image and image-to-image) |
| `ratio` | `size` | `string` | No | Aspect ratio |
| `style` | `style` | `string` | No | Style |
| `cfg_scale` | `creativeRelevance` | `number` | No | Frontend 0–100, divide by 100 for API |
| `image` | `image1` | `string` | Conditional | Start image URL (required for image-to-image) |
| `image_tail` | `image2` | `string` | No | Second image URL |
| `images` | `images` | `string[]` | Conditional | Image URL array (used by some Flux models) |
| `outputs` | `outputs` | `number` | No | Number to generate |
| `resolution` | `resolution` | `string` | No | Resolution |
| `inspiration_id` | — | `string` | No | Injected via URL query |

---

## 4. AI Image Effects (`/api/lumeflow/image-effects-generate`)

### 4.1 Request Parameters

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `special_id` | `number` | Yes | — | Effect ID (from effects list endpoint) |
| `images` | `string[]` | Yes | — | Input image URL array |
| `outputs` | `number` | No | — | Number to generate |
| `inspiration_id` | `number` | No | — | Inspiration template ID |

---

## 5. TypeScript Interface Definitions

```typescript
// ===================================================
// Common Enums
// ===================================================

/** Video generation model IDs */
export type VideoModelType =
  | 1   // Kling 1.6
  | 19  // Kling 2.5
  | 65  // Kling 3.0
  | 9   // Lumeflow 3.0, Pixverse V5 (two products, same model_type)
  | 28  // Pixverse V5.5
  | 3   // Hailuo 02
  | 23  // Hailuo 2.3
  | 25  // Hailuo 2.3 Fast
  | 4   // Google Veo 3.1
  | 5   // Google Veo 3.1 Fast
  | 6   // Vidu Q1
  | 26  // Vidu Q2
  | 24  // Vidu Q2 Turbo
  | 63  // Wan 2.5
  | 64  // Wan 2.6
  | 73  // Seedance 2.0
  | 76  // Seedance 2.0 Fast
  | 88  // Pixverse C1
  | 89; // Wan 2.7

/** Image generation model IDs */
export type ImageModelType =
  | 18  // Nano Banana V1
  | 72  // Nano Banana V2
  | 37  // Nano Banana Pro
  | 12  // Seedream 4.0
  | 80  // Seedream 5.0
  | 101; // GPT Image 2

/** Video generation modes */
export type VideoGenerateType =
  | 0   // text-to-video
  | 1   // image-to-video
  | 3;  // video-to-video

/** Image generation modes */
export type ImageGenerateType =
  | 3   // text-to-image
  | 4;  // image-to-image

// ===================================================
// Video Generation Request Body
// ===================================================

/**
 * POST /api/lumeflow/video-generate
 * Full video generation payload
 */
export interface VideoGeneratePayload {
  /** Model ID */
  model_type: VideoModelType;

  /** Generation mode: 0=text-to-video, 1=image-to-video, 3=video-to-video */
  generate_type: VideoGenerateType;

  /** Positive prompt */
  prompt?: string;

  /**
   * Audio toggle
   * 0=off, 1=on
   * Forced to 1 for Kling/Sora/Veo/Wan series
   */
  is_switch_audio?: 0 | 1;

  /**
   * Video duration in seconds
   * Kling V1.6/V2.5: 5|10; V3.0: 3–15
   * model_type 9 (Lumeflow 3.0, Pixverse V5): 5|8; V5.5: 5|8|10; C1 (88): 2–15
   * Hailuo: 6|10; Veo 3.1: fixed 8
   * Wan 2.5: 5|10; Wan 2.6: 2–15; Seedance 2.0: 5|10|15
   */
  duration?: number;

  /**
   * Aspect ratio
   * Examples: '16:9' | '1:1' | '9:16' | '4:3' | '3:4' | '21:9' | 'auto'
   */
  ratio?: string;

  /**
   * Resolution
   * Examples: '360P' | '480P' | '512P' | '540P' | '720P' | '768P' | '1080P'
   * Note: some models restrict options by duration (e.g. `model_type` `9`: `duration=5` up to 1080P, `duration=8` max 720P)
   */
  resolution?: string;

  /**
   * Style ID (Pixverse only)
   * V4.5/V5: '0'=auto '1'=anime '2'=3d_animation '3'=comic '4'=cyberpunk '5'=clay
   * V5.5: '0'=anime '1'=3d_animation '2'=clay '3'=comic '4'=cyberpunk
   */
  style?: string;

  /**
   * Creative relevance (CFG Scale)
   * Frontend range 0–100, divide by 100 for API → 0.0–1.0
   */
  cfg_scale?: number;

  /**
   * Motion mode
   * '1'=standard '2'=expert
   */
  motion_mode?: string;

  /** Motion range */
  moition_range?: string;

  /** Start frame image URL (required for image-to-video) */
  image?: string;

  /** End frame image URL (required for first+last frame mode) */
  image_tail?: string;

  /**
   * Source video URL (required for video-to-video mode)
   * Currently mainly for V2V: `model_type`=`9` (Lumeflow 3.0 or Pixverse V5)
   */
  video?: string;

  /** Number to generate (1–4), some models support tiered discounts */
  outputs?: number;

  /**
   * Random seed
   * Supported by `model_type` `9` (Lumeflow 3.0, Pixverse V5) and Wan series
   */
  seed?: number;

  /** Negative prompt (not yet enabled) */
  negative_prompt?: string;

  /**
   * Shot mode (Wan 2.6 only)
   * Frontend 1 → 'multi', else → 'single'
   */
  shot_type?: 'single' | 'multi';

  /**
   * Reference mode (Seedance 2.0 image-to-video only)
   * 0=first+last frame, 1=Omni reference
   */
  function_mode?: 0 | 1;

  /**
   * Omni mode video URL array (Seedance 2.0 function_mode=1, required)
   * Filter type==='video' URLs from mediaList
   */
  videos?: string[];

  /**
   * Omni mode image URL array (Seedance 2.0 function_mode=1, required)
   * Filter type==='image' URLs from mediaList
   */
  images?: string[];

  /** Inspiration template ID (injected via URL query, not user-configurable) */
  inspiration_id?: string;
}

// ===================================================
// Image Generation Request Body
// ===================================================

/**
 * POST /api/lumeflow/image-generate
 * Full image generation payload
 */
export interface ImageGeneratePayload {
  /** Image model ID */
  model_type: ImageModelType;

  /** Generation mode: 3=text-to-image, 4=image-to-image */
  generate_type: ImageGenerateType;

  /** Prompt (required) */
  prompt: string;

  /** Aspect ratio */
  ratio?: string;

  /** Style */
  style?: string;

  /** Creative relevance (0.0–1.0) */
  cfg_scale?: number;

  /** Start image URL (required for image-to-image) */
  image?: string;

  /** Second image URL */
  image_tail?: string;

  /**
   * Image URL array (used by some Flux models)
   * Primary param for image-to-image
   */
  images?: string[];

  /** Number to generate */
  outputs?: number;

  /** Resolution */
  resolution?: string;

  /** Inspiration template ID */
  inspiration_id?: string;
}

// ===================================================
// Image Effects Request Body
// ===================================================

/**
 * POST /api/lumeflow/image-effects-generate
 * AI image effects payload
 */
export interface ImageEffectsPayload {
  /** Effect ID (from /api/lumeflow/image-effects-special-list) */
  special_id: number;

  /** Input image URL array */
  images: string[];

  /** Number to generate */
  outputs?: number;

  /** Inspiration template ID */
  inspiration_id?: number;
}
```

---

## 6. Parameter Mapping (Frontend → API)

Video generation composable (`useCommonVideoGenerator`) complete mapping:

| Frontend Field (`modelData.xxx`) | API Field (`param.xxx`) |
|----------------------------------|------------------------|
| `prompt` | `prompt` |
| `sound` | `is_switch_audio` |
| `duation` | `duration` (convert to Number) |  <!-- typo in frontend code: should be "duration" -->
| `creativeRelevance` | `cfg_scale` (÷100) |
| `image1` | `image` |
| `image2` | `image_tail` |
| `mode` | `motion_mode` |
| `resolution` | `resolution` |
| `motionRange` | `moition_range` |
| `size` | `ratio` |
| `seed` | `seed` |
| `negative_prompt` | `negative_prompt` |
| `style` | `style` |
| `outputs` | `outputs` (convert to Number) |
| `shot_type` | `shot_type` (1→`'multi'` or `'single'`) |
| `function_mode` | `function_mode` |

---

## 7. Key Business Rules

1. **Forced audio**: When `model_type` is in `[1,4,5,19,63,64,73,76,89]`, the backend ignores `is_switch_audio`; the composable forces it to `1`. (Note: legacy IDs `22`→`63`, `32`→`64` were remapped.)
2. **First+last frame logic**: When `isFirstLastFrameEnabled=false`, do not pass `image_tail`; when `true`, `image_tail` must have a value.
3. **Outputs discount**: Except for Kling and Wan series, other models offer tiered discounts: 2 items ×0.95, 3 items ×0.90, 4 items ×0.85.
4. **model_type adjustment**: Some legacy keys are remapped via `keyAdjustment` (e.g. `70→76`, `32→64`, `22→63`).
5. **Seedance 2.0 Omni mode**: When `function_mode=1`, pass `videos[]`, `images[]` (filtered from `mediaList`) and **`resolution`** (`480P`/`720P`/`1080P`); do NOT pass `duration`, `is_switch_audio`, `motion_mode`, or first+last frame `image`/`image_tail`.
