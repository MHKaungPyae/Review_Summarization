# Review Summarization Model

A T5-based text summarization model fine-tuned on customer reviews to generate concise summaries. Built as an educational experiment to explore how summarization models perform when integrated into a review analysis app.

## ⚠️ Disclaimer

This model is **not production-ready**. It was built for:

- **Educational purposes** — understanding how T5 fine-tuning works on domain-specific text
- **App prototyping** — testing how a summarization model would behave inside a [TripNest Application](https://github.com/linmyatoo/TripNest_admin) we developed

The model has limited training data (156 samples) and produces approximate summaries. Do not rely on it for critical or high-stakes use cases.

## What It Does

Takes raw customer reviews as input and generates a short summary capturing the key points.

```
Input:  "My experience was disappointing. The staff wasn't helpful...
         Customer support took forever... very disorganized process."

Output: "Events and Adventures: disappointing experience, lack of
         customer support, and disorganized process."
```

## Architecture

| Component | Detail |
|-----------|--------|
| Base model | `t5-small` (60M params) |
| Task | Text summarization (seq2seq) |
| Framework | PyTorch + HuggingFace Transformers |
| Max input length | 512 tokens |
| Max output length | 128 tokens |
| Training epochs | 10 (with early stopping, patience=3) |
| Batch size | 4 |
| Learning rate | 3e-5 |

## Results

ROUGE scores on the validation set:

| Metric | Score |
|--------|-------|
| ROUGE-1 (F1) | 0.2130 |
| ROUGE-2 (F1) | 0.0399 |
| ROUGE-L (F1) | 0.1513 |

> These scores reflect the limited training data. More data and a larger base model (e.g., `t5-base`) would significantly improve results.

## Project Structure

```
Summarization/
├── Summarization.ipynb          # Full training + evaluation notebook
├── generate_comparison.py       # Script to generate portfolio images
├── text_comparison.png          # Before/after demo (single review)
└── README.md
```

## How to Run

1. Open `Summarization.ipynb` in Google Colab
2. Upload your dataset to Google Drive at the expected path, or update `DATA_PATH`
3. Run all cells — training takes ~2 minutes on a GPU

### Requirements

```
torch
transformers
sentencepiece
pandas
numpy
rouge-score
```

## Future Improvements

- **More training data** — current model is limited by 156 samples
- **Larger base model** — `t5-base` or `bart-large` would improve summarization quality
- **Dynamic padding** — reduce training time by avoiding fixed-length padding
- **Proper train/val/test split** — avoid optimistic evaluation on the validation set
- **App integration** — deploy as an API endpoint for the review analysis pipeline

## License

This project is for educational and experimental use only.
