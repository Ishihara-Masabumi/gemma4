#!/usr/bin/env python3
import argparse
import json
import re
import time
from decimal import Decimal, InvalidOperation
from pathlib import Path

from datasets import load_dataset
from openai import OpenAI


SYSTEM_PROMPT = """You are solving Japanese grade-school math word problems.
Show your reasoning briefly in Japanese.
On the final line, output only: 答え: <number>
Do not add any extra text after the final answer line."""


def build_user_prompt(row: dict) -> str:
    return f"{row['instruction']}\n\n問題: {row['question']}"


def normalize_number(text: str) -> str | None:
    cleaned = text.strip()
    cleaned = cleaned.replace(",", "").replace("，", "").replace("．", ".")
    cleaned = cleaned.replace("−", "-").replace("ー", "-").replace("–", "-")
    cleaned = cleaned.replace(" ", "")
    if not cleaned:
        return None
    try:
        value = Decimal(cleaned)
    except InvalidOperation:
        return None
    normalized = format(value.normalize(), "f")
    if "." in normalized:
        normalized = normalized.rstrip("0").rstrip(".")
    return normalized


def parse_prediction(text: str, answer_prefix: str) -> str | None:
    lines = [line.strip() for line in text.strip().splitlines() if line.strip()]
    prefix_patterns = [
        rf"^{re.escape(answer_prefix)}\s*[:：]\s*(.+?)\s*$",
        r"^答え\s*[:：]\s*(.+?)\s*$",
        r"^answer\s*[:：]\s*(.+?)\s*$",
    ]

    for line in reversed(lines):
        for pattern in prefix_patterns:
            match = re.match(pattern, line, flags=re.IGNORECASE)
            if match:
                candidate = re.search(r"-?\d+(?:\.\d+)?", match.group(1))
                if candidate:
                    return normalize_number(candidate.group(0))

    candidate = re.search(r"-?\d+(?:\.\d+)?", text)
    if candidate:
        return normalize_number(candidate.group(0))
    return None


def main():
    parser = argparse.ArgumentParser(description="Evaluate MGSM Japanese with a local vLLM server")
    parser.add_argument("--model", default="gemma4-e4b-it", help="Served model name")
    parser.add_argument("--base-url", default="http://127.0.0.1:8000/v1", help="OpenAI-compatible vLLM endpoint")
    parser.add_argument("--api-key", default="EMPTY", help="Dummy API key for local vLLM")
    parser.add_argument("--limit", type=int, default=None, help="Optional number of examples")
    parser.add_argument("--output-dir", default="/home/ubuntu/gemma4/mgsm_ja_results", help="Directory to save outputs")
    parser.add_argument("--max-tokens", type=int, default=256, help="Generation length")
    parser.add_argument("--temperature", type=float, default=0.0, help="Sampling temperature")
    args = parser.parse_args()

    client = OpenAI(base_url=args.base_url, api_key=args.api_key)

    dataset = load_dataset("CohereLabs/global-mgsm", "ja", split="test")
    if args.limit is not None:
        dataset = dataset.select(range(min(args.limit, len(dataset))))

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    pred_path = output_dir / "predictions_test.jsonl"
    summary_path = output_dir / "summary_test.json"

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
            pred = parse_prediction(text, row["answer_prefix"])
            gold = normalize_number(str(row["answer"]))
            is_correct = pred == gold
            if pred is None:
                invalid += 1
            if is_correct:
                correct += 1

            record = {
                "question": row["question"],
                "gold": gold,
                "prediction": pred,
                "raw_output": text,
                "correct": is_correct,
            }
            f.write(json.dumps(record, ensure_ascii=False) + "\n")

            if total % 25 == 0:
                acc = correct / total
                print(f"{total} examples processed, accuracy={acc:.4f}, invalid={invalid}")

    elapsed = time.time() - started
    summary = {
        "model": args.model,
        "dataset": "CohereLabs/global-mgsm",
        "config": "ja",
        "split": "test",
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
