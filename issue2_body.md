## 目的

Gemma 4 の日本語数理推論性能を確認するため、Japanese GSM8K 相当のベンチマークで評価する。
今回は公開データセットとして利用しやすく、評価形式も明確な `CohereLabs/global-mgsm` の日本語版 (`ja`) を採用した。これは GSM8K 系の日本語算数ベンチマークとして扱える。

## 内容

- モデル: `gemma4-e4b-it`
- 推論方式: ローカル `vLLM` サーバ (`OpenAI-compatible endpoint`)
- データセット: `CohereLabs/global-mgsm`, config `ja`, split `test`
- 問題数: 250
- プロンプト方針:
  - 日本語で解答
  - 推論過程を簡潔に出力
  - 最終行を `答え: <number>` 形式に固定
- 正解判定:
  - モデル出力の最終回答から数値を抽出
  - データセットの正解数値と一致した場合を正解とする

## 結果

| 項目 | 値 |
| --- | --- |
| correct | 185 |
| total | 250 |
| accuracy | **74.0%** |
| invalid | 0 |
| elapsed | 約 608.4 秒 |

`gemma4-e4b-it` は MGSM 日本語版テスト 250 問で **74.0%** だった。
回答形式の崩れはなく、`invalid=0` で最後まで安定して評価できた。

## 他モデルとの比較

Japanese MGSM の公開値が確認できるモデルカードと比較すると、以下の位置づけだった。

| モデル | Accuracy | 条件 | 出典 |
| --- | ---: | --- | --- |
| GPT-4o (`gpt-4o-2024-08-06`) | 86.4% | 4-shot | Swallow 公式モデルカード |
| Qwen2.5-72B-Instruct | 84.0% | 4-shot | Swallow 公式モデルカード |
| GPT-4o-mini (`gpt-4o-mini-2024-07-18`) | 83.2% | 4-shot | Swallow 公式モデルカード |
| Llama 3.3 Swallow 70B Instruct v0.4 | 81.2% | 4-shot | Swallow 公式モデルカード |
| Llama 3.3 70B Instruct | 78.4% | 4-shot | Swallow 公式モデルカード |
| Qwen2-72B-Instruct | 78.0% | 4-shot | Swallow 公式モデルカード |
| Llama 3.1 Swallow 70B Instruct v0.1 | 77.6% | 4-shot | Swallow 公式モデルカード |
| Llama 3 heron brain 70B v0.3 | 77.2% | 4-shot | Swallow 公式モデルカード |
| **gemma4-e4b-it (今回)** | **74.0%** | local vLLM, 実質 0-shot | 今回の実測 |
| Llama-3.1-70B-Japanese-Instruct-2407 | 74.8% | 4-shot | Swallow 公式モデルカード |
| Llama 3.1 70B Instruct | 73.2% | 4-shot | Swallow 公式モデルカード |
| Llama 3 Youko 70B Instruct | 72.0% | 4-shot | Swallow 公式モデルカード |
| Llama 3 70B Instruct | 71.6% | 4-shot | Swallow 公式モデルカード |
| Llama 3 Swallow 70B Instruct | 67.2% | 4-shot | Swallow 公式モデルカード |
| Sarashina2.2-3B | 63.6% | MGSM-ja | Sarashina 公式モデルカード |
| Sarashina2-70B | 54.0% | MGSM-ja | Sarashina 公式モデルカード |
| Sarashina2.2-1B | 39.6% | MGSM-ja | Sarashina 公式モデルカード |

今回の `gemma4-e4b-it` の **74.0%** は、公開されている日本語 MGSM 系スコアと比べると上位グループの一角ではあるが、GPT-4o や Qwen2.5-72B-Instruct、Llama 3.3 Swallow 70B Instruct などの最上位帯には届いていない。一方で、`Llama 3.1 70B Instruct` や `Llama 3 70B Instruct` と同程度かそれ以上で、`Sarashina2.2-3B` よりも高かった。

注意点:
- 今回の `gemma4-e4b-it` はローカル `vLLM` による **実質 0-shot** 評価
- 比較対象の多くは公式モデルカード上の **4-shot** 値
- そのため、完全な apples-to-apples 比較ではなく、**おおよその位置づけ**として見るのがよい

補足:
- 同一条件の公開 leaderboard と直接比較した値ではないため、まずはローカルの基準値として扱う
- 今後は few-shot 化、プロンプト改善、より大きい Gemma 4 系モデルとの比較も試す価値がある

参考:
- Swallow 公式モデルカード: https://huggingface.co/tokyotech-llm/Llama-3.3-Swallow-70B-Instruct-v0.4
- Sarashina2.2-3B 公式モデルカード: https://huggingface.co/sbintuitions/sarashina2.2-3b
- MGSM データセット: https://huggingface.co/datasets/CohereLabs/global-mgsm
