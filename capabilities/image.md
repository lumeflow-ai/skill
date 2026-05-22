# Image Generation Capability

## Image Models (name -> model_type)
| Model Name | `model_type` | Notes |
|------------|-------------|-------|
| Nano Banana V2 | `72` | **Default**. Fast, icons/stickers/illustrations |
| Nano Banana V1 | `18` | V2 predecessor, similar style |
| Nano Banana Pro | `37` | Higher quality Banana variant |
| Seedream 4.0 | `12` | Realistic & artistic, ByteDance model |
| Seedream 5.0 | `80` | Latest Seedream, improved quality. **Resolution only supports `2K`、`3K`** |
| GPT Image 2 | `101` | OpenAI GPT Image 2. **No `resolution` parameter** |



## Image Parameters
| Parameter | Description | Options | Default |
|-----------|-------------|---------|---------|
| `prompt` | Text description of the image | - | *(must ask user)* |
| `generate_type` | Generation type | `3`=text-to-image, `4`=image-to-image | `3` |
| `model_type` | Model ID (user selects by **model name**, auto-converted) | See image models table | `72` (Nano Banana V2) |
| `ratio` | Aspect ratio | `auto`, `16:9`, `9:16`, `1:1`, ... | `auto` |
| `resolution` | Output resolution | `1K`, `2K`, `4K` (**Seedream 5.0** only supports `2K`, `3K`; **GPT Image 2** does not use this parameter) | `1K` |
| `outputs` | Number of images to generate | `1` - `4` | `1` |
| `images` | Input image URL list (**required if generate_type=4**) | Array of image URLs | `[]` |


## Parameter Rules (Image)
- **Model selection**: Show model **name** to the user (e.g. "Nano Banana V2"), convert to `model_type` number in the request body.
- If user provides an image URL and wants an image, set `generate_type` to `4` automatically.
- `generate_type` is an internal parameter — do not ask user to change.
- All parameters must be included in the request body.
- If user describes preference like "landscape" → `ratio: "16:9"`, "portrait" → `ratio: "9:16"`, "HD" → image `resolution: "4K"`.
- **Seedream 5.0 (`model_type` 80)**: resolution only supports `2K` and `3K` and `4K`. If user selects `1K`, switch to `2K` before sending.
- **GPT Image 2 (`model_type` 101)**: does not accept a `resolution` parameter. Remove it from the request body.
