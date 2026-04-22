# Gemma 4 bootstrap

This directory contains the minimal files used to set up a local Gemma 4 inference environment.

## Target layout

- `/home/ubuntu/gemma4/run_gemma4.py`
- `/home/ubuntu/gemma4/README.md`
- `conda` environment: `gemma4`

## Default model

- `google/gemma-4-E4B-it`

## Quick run

```bash
conda activate gemma4
python /home/ubuntu/gemma4/run_gemma4.py --prompt "日本語で自己紹介してください。"
```

## Smaller smoke test

```bash
conda activate gemma4
python /home/ubuntu/gemma4/run_gemma4.py \
  --model google/gemma-4-E2B-it \
  --prompt "日本語で一文だけ挨拶してください。" \
  --max-new-tokens 32 \
  --no-sample
```
