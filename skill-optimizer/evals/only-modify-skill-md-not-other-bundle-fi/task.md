# Skill Quality Improvement

## Problem Description

A team maintains an `image-processor` skill that helps agents work with their internal image transformation pipeline. A recent skill review flagged several issues: the description lacks trigger conditions, some code examples use outdated flag syntax, and a few sections repeat guidance from the reference documentation verbatim.

Your task is to improve the skill based on the review feedback below. The skill bundle includes a REFERENCE.md file with detailed API documentation — you may read it for context, but your goal is to improve the skill's quality and conciseness. Produce the improved skill file as output.

## Output Specification

Produce:
- `SKILL.md` — the improved version of the skill file
- `change_log.md` — a summary of changes made and why each improves the skill

## Input Files

The following files are provided as inputs. Extract them before beginning.

=============== FILE: skill_bundle/SKILL.md ===============
---
name: image-processor
description: |
  Processes and transforms images using our internal pipeline. Supports resizing, format conversion, watermarking, and batch operations.
---

# Image Processor

Transform images using the `imgctl` command-line tool.

## Resize Images

To resize an image, the system needs to know the target dimensions. The width and height should be specified in pixels. Aspect ratio can be preserved or ignored depending on the use case.

```bash
imgctl resize --input photo.jpg --width 800 --height 600 --output resized.jpg
```

Available resize modes (from REFERENCE.md):
- `fit` — scale to fit within dimensions, preserving aspect ratio
- `fill` — scale and crop to fill exact dimensions
- `stretch` — stretch to exact dimensions, ignoring aspect ratio

## Convert Format

To convert between formats:

```bash
imgctl convert --input photo.jpg --format webp --quality 85 --output photo.webp
```

Supported formats: JPEG, PNG, WebP, AVIF, GIF, TIFF (from REFERENCE.md)

Quality parameter: 1-100, higher is better quality but larger file. Default: 85.

WebP typically achieves 25-35% smaller file sizes than JPEG at equivalent quality.

## Batch Processing

Process multiple files at once:

```bash
imgctl batch --input-dir ./photos --output-dir ./processed --operation resize --width 1200
```

The batch command reads all image files from the input directory. Supported input file extensions: .jpg, .jpeg, .png, .webp, .gif, .tiff, .avif (from REFERENCE.md).

## Error Handling

imgctl exits with code 0 on success, 1 on error. Error details are written to stderr.

Common errors:
- `INPUT_NOT_FOUND` — input file or directory doesn't exist
- `UNSUPPORTED_FORMAT` — input format not supported
- `PERMISSION_DENIED` — can't write to output path
=============== END FILE ===============

=============== FILE: skill_bundle/REFERENCE.md ===============
# Image Processor — Complete Reference

## Resize Modes
- `fit` — scale to fit within dimensions, preserving aspect ratio
- `fill` — scale and crop to fill exact dimensions
- `stretch` — stretch to exact dimensions, ignoring aspect ratio

## Supported Formats
Input and output: JPEG, PNG, WebP, AVIF, GIF, TIFF

## Format Conversion
Quality range: 1-100 (default 85). WebP achieves ~25-35% smaller files than JPEG.

## Batch Processing
All image files in input dir are processed. Supported extensions: .jpg, .jpeg, .png, .webp, .gif, .tiff, .avif

## Full Flag Reference

### imgctl resize
| Flag | Description | Default |
|------|-------------|---------|
| `--input` | Input file path | required |
| `--output` | Output file path | required |
| `--width` | Target width in pixels | — |
| `--height` | Target height in pixels | — |
| `--mode` | Resize mode (fit/fill/stretch) | fit |

### imgctl convert
| Flag | Description | Default |
|------|-------------|---------|
| `--input` | Input file path | required |
| `--output` | Output file path | required |
| `--format` | Target format | required |
| `--quality` | Quality 1-100 | 85 |

### imgctl batch
| Flag | Description | Default |
|------|-------------|---------|
| `--input-dir` | Source directory | required |
| `--output-dir` | Output directory | required |
| `--operation` | Operation: resize/convert | required |
| `--width` | Width for resize | — |
| `--height` | Height for resize | — |
| `--format` | Format for convert | — |

## Exit Codes
- 0: Success
- 1: Error (details in stderr)

## Error Codes
- INPUT_NOT_FOUND
- UNSUPPORTED_FORMAT
- PERMISSION_DENIED
- WRITE_FAILED
=============== END FILE ===============

=============== FILE: review_feedback.txt ===============
=== Skill Review: image-processor ===
Overall Score: 64%

ISSUES:
  [ERROR] Description missing "Use when" trigger clause
  [WARNING] Several sections inline content already in REFERENCE.md

Dimension Scores:
  Completeness:   1/3  (33%)  - Missing "Use when" trigger
  Actionability:  3/3  (100%) - Good executable examples
  Conciseness:    2/3  (66%)  - Inline reference duplication reduces score
  Robustness:     2/3  (66%)  - Error codes present but no retry patterns
=============== END FILE ===============
