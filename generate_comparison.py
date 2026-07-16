"""
Generate a before/after comparison image for portfolio.
Shows the summarization model's input and output side by side.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from textwrap import wrap

# ── Examples from the notebook ──────────────────────────────────────────

EXAMPLES = [
    {
        "title": "Example 1 — Single Review",
        "input": (
            "My experience with Events and Adventures was very disappointing. "
            "The staff didn't seem very helpful or interested in resolving our "
            "issues and getting accurate event details was frustrating. Customer "
            "support took a long time to respond and didn't really offer any "
            "clear solutions. Overall, the whole process felt disorganized. I "
            "expected a much smoother and more reliable experience from a site "
            "that handles event listings and ticketing."
        ),
        "output": (
            "Events and Adventures: disappointing experience, lack of customer "
            "support, and disorganized process. Site handles event listings, "
            "ticketing, etc."
        ),
        "highlights_in": [
            "disappointing",
            "staff didn't seem very helpful",
            "frustrating",
            "Customer support took a long time",
            "disorganized",
        ],
        "highlights_out": [
            "disappointing experience",
            "lack of customer support",
            "disorganized process",
            "event listings, ticketing",
        ],
    },
    {
        "title": "Example 2 — Multiple Reviews",
        "input": (
            "• Parking was terrible. Had to walk 20 minutes.\n"
            "• Sound system kept failing during the concert.\n"
            "• Food ran out within the first hour."
        ),
        "output": (
            "Parking was terrible, had to walk 20 minutes, and sound system "
            "kept failing during the concert. Food ran out within the first hour."
        ),
        "highlights_in": [
            "Parking was terrible",
            "walk 20 minutes",
            "Sound system kept failing",
            "Food ran out",
        ],
        "highlights_out": [
            "Parking was terrible",
            "walk 20 minutes",
            "sound system kept failing",
            "Food ran out",
        ],
    },
]

# ── Styling ─────────────────────────────────────────────────────────────

BG_COLOR = "#1e1e2e"
CARD_BG = "#2a2a3d"
INPUT_COLOR = "#89b4fa"
OUTPUT_COLOR = "#a6e3a1"
TEXT_COLOR = "#cdd6f4"
TITLE_COLOR = "#f5c2e7"
HIGHLIGHT_BG_IN = "rgba(243, 139, 168, 0.25)"   # pink for input highlights
HIGHLIGHT_BG_OUT = "rgba(166, 227, 161, 0.25)"   # green for output highlights
DIVIDER_COLOR = "#585b70"
BADGE_BG = "#45475a"


def highlight_text(text, highlights):
    """Wrap highlighted phrases with ANSI-style markers for display."""
    # We'll handle highlighting manually in the plot
    return text


def draw_rounded_rect(ax, x, y, w, h, color, radius=0.02):
    """Draw a rounded rectangle on the axes."""
    fancy = mpatches.FancyBboxPatch(
        (x, y), w, h,
        boxstyle=f"round,pad=0,rounding_size={radius}",
        facecolor=color,
        edgecolor=DIVIDER_COLOR,
        linewidth=1.2,
        transform=ax.transAxes,
        clip_on=False,
    )
    ax.add_patch(fancy)
    return fancy


def render_text_block(ax, x, y, w, h, lines, font_size=11, color=TEXT_COLOR,
                      bold_indices=None, bold_color=None):
    """Render wrapped text lines inside a region. Returns final y position."""
    if bold_indices is None:
        bold_indices = set()

    current_y = y
    line_height = 0.028

    for i, line in enumerate(lines):
        weight = "bold" if i in bold_indices else "normal"
        c = bold_color if (i in bold_indices and bold_color) else color
        ax.text(
            x, current_y, line,
            fontsize=font_size,
            fontweight=weight,
            color=c,
            transform=ax.transAxes,
            verticalalignment="top",
            fontfamily="sans-serif",
        )
        current_y -= line_height

    return current_y


def create_comparison_image(example, filename):
    """Create a single side-by-side comparison image."""
    fig, ax = plt.subplots(1, 1, figsize=(14, 8), dpi=150)
    fig.patch.set_facecolor(BG_COLOR)
    ax.set_facecolor(BG_COLOR)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    # ── Title ──
    ax.text(
        0.5, 0.96, example["title"],
        fontsize=20, fontweight="bold", color=TITLE_COLOR,
        transform=ax.transAxes, ha="center", va="top",
        fontfamily="sans-serif",
    )

    # ── Subtitle ──
    ax.text(
        0.5, 0.91,
        "T5 Summarization Model  ·  Input → Output",
        fontsize=11, color=DIVIDER_COLOR,
        transform=ax.transAxes, ha="center", va="top",
        fontfamily="sans-serif",
    )

    # ── Cards ──
    card_w = 0.44
    card_h = 0.62
    card_y = 0.22
    left_x = 0.03
    right_x = 0.53

    draw_rounded_rect(ax, left_x, card_y, card_w, card_h, CARD_BG)
    draw_rounded_rect(ax, right_x, card_y, card_w, card_h, CARD_BG)

    # ── Badges ──
    badge_w = 0.12
    badge_h = 0.035

    draw_rounded_rect(ax, left_x + 0.02, card_y + card_h - 0.06,
                      badge_w, badge_h, INPUT_COLOR, radius=0.012)
    ax.text(
        left_x + 0.02 + badge_w / 2, card_y + card_h - 0.06 + badge_h / 2,
        "INPUT", fontsize=9, fontweight="bold", color=BG_COLOR,
        transform=ax.transAxes, ha="center", va="center",
        fontfamily="sans-serif",
    )

    draw_rounded_rect(ax, right_x + 0.02, card_y + card_h - 0.06,
                      badge_w, badge_h, OUTPUT_COLOR, radius=0.012)
    ax.text(
        right_x + 0.02 + badge_w / 2, card_y + card_h - 0.06 + badge_h / 2,
        "OUTPUT", fontsize=9, fontweight="bold", color=BG_COLOR,
        transform=ax.transAxes, ha="center", va="center",
        fontfamily="sans-serif",
    )

    # ── Input text ──
    input_text = example["input"]
    wrapped_input = []
    for para in input_text.split("\n"):
        if para.strip().startswith("•"):
            # Keep bullet points together
            wrapped_input.append(para)
        else:
            wrapped_input.extend(wrap(para, width=52))

    # Find which lines contain highlight keywords
    input_bold_lines = set()
    for i, line in enumerate(wrapped_input):
        for hl in example["highlights_in"]:
            if hl.lower() in line.lower():
                input_bold_lines.add(i)
                break

    render_text_block(
        ax,
        x=left_x + 0.03,
        y=card_y + card_h - 0.11,
        w=card_w - 0.06,
        h=card_h - 0.15,
        lines=wrapped_input,
        font_size=10.5,
        color=TEXT_COLOR,
        bold_indices=input_bold_lines,
        bold_color="#f38ba8",
    )

    # ── Output text ──
    output_text = example["output"]
    wrapped_output = wrap(output_text, width=52)

    output_bold_lines = set()
    for i, line in enumerate(wrapped_output):
        for hl in example["highlights_out"]:
            if hl.lower() in line.lower():
                output_bold_lines.add(i)
                break

    render_text_block(
        ax,
        x=right_x + 0.03,
        y=card_y + card_h - 0.11,
        w=card_w - 0.06,
        h=card_h - 0.15,
        lines=wrapped_output,
        font_size=11,
        color=TEXT_COLOR,
        bold_indices=output_bold_lines,
        bold_color="#a6e3a1",
    )

    # ── Arrow in the middle ──
    ax.annotate(
        "",
        xy=(right_x - 0.01, card_y + card_h / 2),
        xytext=(left_x + card_w + 0.01, card_y + card_h / 2),
        arrowprops=dict(
            arrowstyle="-|>",
            color=TITLE_COLOR,
            lw=2.5,
            mutation_scale=20,
        ),
        transform=ax.transAxes,
    )
    ax.text(
        (left_x + card_w + right_x) / 2,
        card_y + card_h / 2 + 0.04,
        "summarize",
        fontsize=9,
        color=TITLE_COLOR,
        transform=ax.transAxes,
        ha="center",
        va="bottom",
        fontfamily="sans-serif",
        fontstyle="italic",
    )

    # ── Stats bar at the bottom ──
    input_words = len(input_text.split())
    output_words = len(output_text.split())
    compression = round((1 - output_words / input_words) * 100)

    stats_y = 0.08
    stats = [
        f"Input:  {input_words} words",
        f"Output: {output_words} words",
        f"Compression: {compression}%",
        "Model: T5-small fine-tuned",
    ]

    stat_x = 0.5
    for i, stat in enumerate(stats):
        x_pos = 0.1 + i * 0.22
        ax.text(
            x_pos, stats_y, stat,
            fontsize=9.5, color=DIVIDER_COLOR,
            transform=ax.transAxes, ha="center", va="center",
            fontfamily="monospace",
        )

    # ── Key-point legend ──
    ax.text(
        0.5, 0.03,
        "■ Key points extracted",
        fontsize=9, color="#585b70",
        transform=ax.transAxes, ha="center", va="center",
        fontfamily="sans-serif",
    )

    plt.tight_layout(pad=0.5)
    fig.savefig(filename, dpi=150, facecolor=BG_COLOR, bbox_inches="tight")
    plt.close(fig)
    print(f"✓ Saved: {filename}")


# ── Generate both examples ──────────────────────────────────────────────

if __name__ == "__main__":
    for i, example in enumerate(EXAMPLES):
        out = f"portfolio_comparison_{i+1}.png"
        create_comparison_image(example, out)

    print("\nDone! Images ready for your portfolio.")
