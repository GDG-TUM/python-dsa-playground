#!/usr/bin/env python3
"""Create the folder for a new day.

Usage: python scripts/new_day.py <week> <day>
Example: python scripts/new_day.py 2 1
"""
import sys
from pathlib import Path


def main():
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(1)
    week, day = int(sys.argv[1]), int(sys.argv[2])
    root = Path(__file__).resolve().parent.parent
    dest = root / "weeks" / f"week-{week:02d}" / f"day-{day:02d}"
    if dest.exists():
        print(f"{dest} already exists")
        sys.exit(1)
    (dest / "solutions").mkdir(parents=True)
    (dest / "solutions" / ".gitkeep").touch()
    for name in ["plan.md", "quiz.md", "answers.md", "notes.md"]:
        text = (root / "templates" / name).read_text()
        text = text.replace("{{WEEK}}", str(week)).replace("{{DAY}}", str(day))
        (dest / name).write_text(text)
    print(f"Created {dest}")


if __name__ == "__main__":
    main()
