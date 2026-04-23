JCommonsenseQA の評価結果を、公開されている Open Japanese LLM Leaderboard の `jcommonsenseqa_exact_match` と比較しました。

今回のローカル評価結果は以下でした。

| モデル | 条件 | 正解数 / 総数 | Accuracy |
| --- | --- | ---: | ---: |
| gemma4-e4b-it | local vLLM, validation, 実質 0-shot | 1041 / 1119 | **93.03%** |

比較用に、公開 leaderboard にある代表的なモデルの `JCommonsenseQA` スコアを並べると次の通りです。

| モデル | 公開条件 | Accuracy |
| --- | --- | ---: |
| tokyotech-llm/Llama-3.3-Swallow-70B-Instruct-v0.4 | 4-shot | 97.86% |
| abeja/ABEJA-Qwen2.5-32b-Japanese-v1.0 | 4-shot | 97.14% |
| llm-jp/llm-jp-3.1-13b-instruct4 | 0-shot | 97.05% |
| deep-analysis-research/test-qwen2.5-14b-wo-system-v1 | 0-shot | 96.43% |
| tokyotech-llm/Llama-3.3-Swallow-70B-Instruct-v0.4 | 0-shot | 95.08% |
| **gemma4-e4b-it (今回)** | local vLLM, 実質 0-shot | **93.03%** |
| google/gemma-2-27b-it | 4-shot | 92.67% |
| google/gemma-2-27b-it | 0-shot | 83.65% |
| google/gemma-2-9b-it | 4-shot | 86.95% |
| google/gemma-2-9b-it | 0-shot | 76.05% |
| google/gemma-2-2b-it | 4-shot | 78.19% |

所感としては、`gemma4-e4b-it` の **93.03%** はかなり高く、公開 leaderboard の最上位帯には少し届かないものの、Gemma 系の公開スコアと比べるとかなり良好です。特に `google/gemma-2-27b-it` の公開 `0-shot` スコア `83.65%` を大きく上回っており、小さめのモデルとしてはかなり健闘していると言えます。

注意点として、今回のローカル評価と Open Japanese LLM Leaderboard は完全に同一条件ではありません。leaderboard 側は `llm-jp-eval` ベースで、`0-shot` と `4-shot` の結果が公開されています。一方、今回の計測はローカルの OpenAI-compatible vLLM サーバに対して単純な単一プロンプトで評価した結果です。そのため、上の表は厳密なランキングというより、**だいたいの位置づけを把握するための比較**です。

参考:
- Open Japanese LLM Leaderboard: https://huggingface.co/datasets/llm-jp/leaderboard-contents
- Leaderboard の説明: https://huggingface.co/blog/leaderboard-japanese
