from __future__ import annotations

import argparse
import csv
from pathlib import Path

from slugify import slugify


def score_idea(pain: int, urgency: int, competition: int, complexity: int) -> tuple[float, str]:
    demand = (pain * 0.35) + (urgency * 0.35)
    burden = (competition * 0.15) + (complexity * 0.15)
    score = max(0.0, min(10.0, demand - burden + 3.0))

    if score >= 7.5:
        tier = "A"
    elif score >= 6.0:
        tier = "B"
    elif score >= 4.5:
        tier = "C"
    else:
        tier = "D"
    return round(score, 2), tier


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate micro-SaaS idea validation reports")
    parser.add_argument("--input", required=True, help="Input CSV")
    parser.add_argument("--output", default="out", help="Output directory")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    out_dir = Path(args.output)
    out_dir.mkdir(parents=True, exist_ok=True)

    summary = []
    with open(args.input, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["idea_name"].strip()
            segment = row.get("segment", "general")
            pain = int(row.get("pain", "5"))
            urgency = int(row.get("urgency", "5"))
            competition = int(row.get("competition", "5"))
            complexity = int(row.get("complexity", "5"))

            score, tier = score_idea(pain, urgency, competition, complexity)

            rec = {
                "idea_name": name,
                "segment": segment,
                "score": score,
                "tier": tier,
            }
            summary.append(rec)

            slug = slugify(name)
            report = (
                f"# Validation Report - {name}\n\n"
                f"- Segment: {segment}\n"
                f"- Score: {score}/10\n"
                f"- Priority tier: {tier}\n\n"
                f"## Suggested 2-week MVP scope\n"
                f"- Core workflow: one job done end-to-end\n"
                f"- Data model: minimal entities only\n"
                f"- Monetization: paid pilot + manual onboarding\n\n"
                f"## Risks\n"
                f"- Competition intensity and distribution access\n"
                f"- Customer acquisition cost uncertainty\n"
            )
            (out_dir / f"report_{slug}.md").write_text(report, encoding="utf-8")

    summary.sort(key=lambda x: x["score"], reverse=True)
    with open(out_dir / "priority_table.csv", "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["idea_name", "segment", "score", "tier"])
        writer.writeheader()
        writer.writerows(summary)

    print(f"Generated {len(summary)} idea reports -> {out_dir / 'priority_table.csv'}")


if __name__ == "__main__":
    main()
