# Gemma 4 セットアップ

このディレクトリには、ローカルで Gemma 4 の推論環境を構築するための最小構成ファイルが入っています。

## 想定構成

- `/home/ubuntu/gemma4/run_gemma4.py`
- `/home/ubuntu/gemma4/README.md`
- `conda` environment: `gemma4`

## デフォルトモデル

- `google/gemma-4-E4B-it`

## すぐに試す

```bash
conda activate gemma4
python /home/ubuntu/gemma4/run_gemma4.py --prompt "日本語で自己紹介してください。"
```

## 軽い動作確認

```bash
conda activate gemma4
python /home/ubuntu/gemma4/run_gemma4.py \
  --model google/gemma-4-E2B-it \
  --prompt "日本語で一文だけ挨拶してください。" \
  --max-new-tokens 32 \
  --no-sample
```
