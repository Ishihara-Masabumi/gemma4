#!/usr/bin/env python3
import argparse
import json
import re
import time
from pathlib import Path

from datasets import load_dataset
from openai import OpenAI


SYSTEM_PROMPT = """You are solving Japanese multiple-choice commonsense questions.
Return only the index of the best answer as a single digit: 0, 1, 2, 3, or 4.
Do not output any explanation or any other text."""


def build_user_prompt(row: dict) -> str:
    choices = [row[f"choice{i}"] for i in range(5)]
    lines = [
        "次の日本語の常識問題に答えてください。",
        "出力は正解の番号 0, 1, 2, 3, 4 のいずれか1文字だけにしてください。",
        "",
        f"質問: {row['question']}",
        "選択肢:",
    ]
    lines.extend([f"{i}. {choice}" for i, choice in enumerate(choices)])
    return "\n".join(lines)


def parse_prediction(text: str) -> int | None:
    text = text.strip()
    if text in {"0", "1", "2", "3", "4"}:
        return int(text)
    match = re.search(r"\b([0-4])\b", text)
    if match:
        return int(match.group(1))
    return None


def main():
    parser = argparse.ArgumentParser(description="Evaluate JCommonsenseQA with a local vLLM server")
    parser.add_argument("--model", default="gemma4-e4b-it", help="Served model name")
    parser.add_argument("--base-url", default="http://127.0.0.1:8000/v1", help="OpenAI-compatible vLLM endpoint")
    parser.add_argument("--api-key", default="EMPTY", help="Dummy API key for local vLLM")
    parser.add_argument("--split", default="validation", help="Dataset split to evaluate")
    parser.add_argument("--limit", type=int, default=None, help="Optional number of examples")
    parser.add_argument("--output-dir", default="/home/ubuntu/gemma4/jcommonsenseqa_results", help="Directory to save outputs")
    parser.add_argument("--max-tokens", type=int, default=8, help="Generation length")
    parser.add_argument("--temperature", type=float, default=0.0, help="Sampling temperature")
    args = parser.parse_args()

    client = OpenAI(base_url=args.base_url, api_key=args.api_key)

    dataset = load_dataset("sbintuitions/JCommonsenseQA", split=args.split)
    if args.limit is not None:
        dataset = dataset.select(range(min(args.limit, len(dataset))))

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    pred_path = output_dir / f"predictions_{args.split}.jsonl"
    summary_path = output_dir / f"summary_{args.split}.json"

    total = 0
    correct = 0
    invalid = 0
    started = time.time()

    with pred_path.open("w", encoding="utf-8") as f:
        for row in dataset:
            total += 1
            response = client.chat.completions.create(
                model=args.model,
                temperature=args.temperature,
                max_tokens=args.max_tokens,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": build_user_prompt(row)},
                ],
            )
            text = response.choices[0].message.content or ""
            pred = parse_prediction(text)
            gold = int(row["label"])
            is_correct = pred == gold
            if pred is None:
                invalid += 1
            if is_correct:
                correct += 1

            record = {
                "q_id": row["q_id"],
                "question": row["question"],
                "gold": gold,
                "prediction": pred,
                "raw_output": text,
                "correct": is_correct,
            }
            f.write(json.dumps(record, ensure_ascii=False) + "\n")

            if total % 50 == 0:
                acc = correct / total
                print(f"{total} examples processed, accuracy={acc:.4f}, invalid={invalid}")

    elapsed = time.time() - started
    summary = {
        "model": args.model,
        "base_url": args.base_url,
        "split": args.split,
        "total": total,
        "correct": correct,
        "invalid": invalid,
        "accuracy": (correct / total) if total else 0.0,
        "elapsed_sec": elapsed,
        "predictions_path": str(pred_path),
    }
    summary_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")

    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
