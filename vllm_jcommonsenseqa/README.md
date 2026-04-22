# vLLM + JCommonsenseQA

Gemma 4 を `vLLM` で起動し、`JCommonsenseQA` を評価するための最小構成です。

## Files

- `start_vllm_gemma4.sh`: Gemma 4 を `vllm serve` で起動
- `evaluate_jcommonsenseqa.py`: `sbintuitions/JCommonsenseQA` を評価

## Setup

```bash
conda activate gemma4
```

## Start server

```bash
bash /home/ubuntu/gemma4/vllm_jcommonsenseqa/start_vllm_gemma4.sh
```

## Smoke test

```bash
conda activate gemma4
python /home/ubuntu/gemma4/vllm_jcommonsenseqa/evaluate_jcommonsenseqa.py \
  --model gemma4-e4b-it \
  --limit 20
```

## Full validation

```bash
conda activate gemma4
python /home/ubuntu/gemma4/vllm_jcommonsenseqa/evaluate_jcommonsenseqa.py \
  --model gemma4-e4b-it \
  --split validation
```
