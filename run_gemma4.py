#!/usr/bin/env python3
import argparse
import sys

import torch
from transformers import AutoProcessor, Gemma4ForConditionalGeneration


DEFAULT_MODEL = "google/gemma-4-E4B-it"


def build_messages(prompt: str, system: str | None):
    messages = []
    if system:
        messages.append({"role": "system", "content": [{"type": "text", "text": system}]})
    messages.append({"role": "user", "content": [{"type": "text", "text": prompt}]})
    return messages


def main():
    parser = argparse.ArgumentParser(description="Run local Gemma 4 inference")
    parser.add_argument("--model", default=DEFAULT_MODEL, help="Hugging Face model id")
    parser.add_argument("--prompt", required=True, help="User prompt")
    parser.add_argument("--system", default="You are a helpful assistant.", help="System prompt")
    parser.add_argument("--max-new-tokens", type=int, default=256, help="Generation length")
    parser.add_argument("--temperature", type=float, default=0.7, help="Sampling temperature")
    parser.add_argument("--top-p", type=float, default=0.95, help="Top-p sampling")
    parser.add_argument("--no-sample", action="store_true", help="Disable sampling")
    args = parser.parse_args()

    if not torch.cuda.is_available():
        raise SystemExit("CUDA is not available. Confirm NVIDIA driver and PyTorch CUDA install.")

    dtype = torch.bfloat16
    processor = AutoProcessor.from_pretrained(args.model)
    model = Gemma4ForConditionalGeneration.from_pretrained(
        args.model,
        torch_dtype=dtype,
        device_map="auto",
    )

    messages = build_messages(args.prompt, args.system)
    inputs = processor.apply_chat_template(
        messages,
        add_generation_prompt=True,
        tokenize=True,
        return_dict=True,
        return_tensors="pt",
    )
    inputs = {k: v.to(model.device) for k, v in inputs.items()}

    with torch.inference_mode():
        outputs = model.generate(
            **inputs,
            max_new_tokens=args.max_new_tokens,
            do_sample=not args.no_sample,
            temperature=args.temperature,
            top_p=args.top_p,
        )

    prompt_len = inputs["input_ids"].shape[-1]
    text = processor.decode(outputs[0][prompt_len:], skip_special_tokens=True)
    sys.stdout.write(text.strip() + "\n")


if __name__ == "__main__":
    main()
