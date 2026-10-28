#!/usr/bin/env python3
"""Build a static, visual navigation site from the repository's weekly content."""
from __future__ import annotations

import html
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "site"
OWNER_REPO = "Markkaruga254/python-dsa-playground"
REPO_URL = f"https://github.com/{OWNER_REPO}"

ROADMAP = [
    "Python basics, arrays, hashing, first easy problems",
    "Finish Arrays and Hashing, start Two Pointers, sorting",
    "Two Pointers, Stack, queues",
    "Binary Search, Sliding Window",
    "Linked Lists",
    "Trees I",
    "Trees II, Tries",
    "Heap and Priority Queue, Backtracking",
    "Graphs I — BFS and DFS",
    "Graphs II — advanced graphs",
    "1-D Dynamic Programming",
    "2-D DP, Greedy, Intervals",
    "Math, bit tricks, weak-topic review",
    "Timed medium problems",
    "Mock assessments — Andela and Safaricom style",
    "Final mocks, polish, rest",
]


def esc(value: str) -> str:
    return html.escape(value, quote=True)


def day_title(plan: Path, day_num: int) -> str:
    if plan.exists():
        first_line = plan.read_text(encoding="utf-8").splitlines()[0:1]
        if first_line:
            title = re.sub(r"^#+\\s*", "", first_line[0]).strip()
            title = re.sub(r"^Day\\s+\\d+\\s*[·|—-]\\s*", "", title, flags=re.I)
            return title or f"Day {day_num:02d}"
    return f"Day {day_num:02d}"


def build() -> None:
    SITE.mkdir(exist_ok=True)
    weeks = []
    total_days = 0

    for week_num, focus in enumerate(ROADMAP, start=1):
        week_dir = ROOT / "weeks" / f"week-{week_num:02d}"
        days = []
        if week_dir.exists():
            for day_dir in sorted(week_dir.glob("day-[0-9][0-9]")):
                match = re.search(r"day-(\\d+)$", day_dir.name)
                if not match:
                    continue
                day_num = int(match.group(1))
                plan = day_dir / "plan.md"
                title = day_title(plan, day_num)
                files = []
                for filename, label in [
                    ("plan.md", "Learning plan"),
                    ("quiz.md", "Quiz"),
                    ("answers.md", "Answer key"),
                    ("notes.md", "Notes"),
                ]:
                    if (day_dir / filename).exists():
                        files.append(
                            f'<a class="file-link" href="{esc(REPO_URL + "/blob/main/" + (day_dir / filename).relative_to(ROOT).as_posix())}">{label}</a>'
                        )
                solution_path = (day_dir / "solutions").relative_to(ROOT).as_posix()
                if (day_dir / "solutions").exists():
                    files.append(f'<a class="file-link" href="{esc(REPO_URL + "/tree/main/" + solution_path)}">Solutions</a>')
                days.append(
                    '<article class="day-card">'
                    f'<div class="day-kicker">DAY {day_num:02d}</div>'
                    f'<h3>{esc(title)}</h3>'
                    '<p>Open the session materials and work through them in order.</p>'
                    f'<div class="file-links">{"".join(files)}</div>'
                    '</article>'
                )
            total_days += len(days)

        if days:
            status = f"{len(days)} session{'s' if len(days) != 1 else ''} published"
            content = f'<div class="day-grid">{"".join(days)}</div>'
            state_class = "available"
        else:
            status = "Coming as the course progresses"
            content = '<div class="coming"><span class="coming-mark">↗</span><div><strong>Content not published yet</strong><p>When the weekly folders are added to the repository, sessions will appear here automatically.</p></div></div>'
            state_class = "upcoming"

        weeks.append(
            f'<section class="week-card {state_class}" id="week-{week_num:02d}">'
            '<div class="week-heading">'
            f'<div><div class="week-label">WEEK {week_num:02d}</div><h2>{esc(focus)}</h2></div>'
            f'<span class="week-status">{esc(status)}</span>'
            '</div>'
            f'{content}'
            '</section>'
        )

    page = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="theme-color" content="#11140f">
<meta name="description" content="A visual navigation hub for the Python and data structures and algorithms learning path.">
<title>Python & DSA — Learning Path</title>
<style>
:root{{--bg:#10120f;--panel:#181c17;--panel2:#20261e;--line:#30392d;--text:#f1f3ec;--muted:#a3ad9a;--accent:#c3f36b;--accent-dark:#1b2810;--blue:#b5d5ff}}
*{{box-sizing:border-box}}html{{scroll-behavior:smooth;scroll-padding-top:24px}}body{{margin:0;background:radial-gradient(ellipse at 85% 0%,#27351d 0,transparent 38%),var(--bg);color:var(--text);font:15px/1.6 Inter,ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}}a{{color:inherit}}.wrap{{max-width:1180px;margin:auto;padding:0 26px}}header{{border-bottom:1px solid var(--line);background:#10120fe8}}.top{{height:76px;display:flex;justify-content:space-between;align-items:center;gap:18px}}.brand{{display:flex;align-items:center;gap:12px;font-weight:850;letter-spacing:-.04em;font-size:17px}}.mark{{width:39px;height:39px;display:grid;place-items:center;background:var(--accent);color:var(--accent-dark);border-radius:12px;font-weight:950}}.brand small{{display:block;color:var(--muted);font-size:10px;text-transform:uppercase;letter-spacing:.15em;font-weight:650}}.top-link,.button{{display:inline-flex;align-items:center;justify-content:center;text-decoration:none;border:1px solid var(--line);border-radius:10px;padding:9px 13px;font-weight:700;font-size:12px}}.top-link:hover,.file-link:hover,.toc a:hover{{border-color:var(--accent);color:var(--accent)}}.hero{{padding:66px 0 43px;display:grid;grid-template-columns:1.3fr .7fr;gap:40px;align-items:end}}.eyebrow,.week-label{{font-size:10px;letter-spacing:.17em;text-transform:uppercase;font-weight:850;color:var(--accent)}}h1{{font-size:clamp(37px,6vw,68px);line-height:.99;letter-spacing:-.07em;margin:13px 0 18px;max-width:720px}}.hero p{{color:var(--muted);max-width:650px;margin:0;font-size:16px}}.hero-panel{{border:1px solid var(--line);border-radius:17px;padding:20px;background:linear-gradient(145deg,#20271c,#151914)}}.hero-panel .number{{font-size:35px;font-weight:900;letter-spacing:-.06em;color:var(--accent)}}.hero-panel p{{font-size:12px;margin-top:5px}}.hero-actions{{display:flex;gap:10px;flex-wrap:wrap;margin-top:24px}}.button.primary{{background:var(--accent);border-color:var(--accent);color:var(--accent-dark)}}.section-top{{display:flex;justify-content:space-between;align-items:end;gap:20px;margin:8px 0 17px}}.section-top h2{{font-size:22px;letter-spacing:-.04em;margin:0}}.section-top p{{margin:4px 0 0;color:var(--muted);font-size:12px}}.toc{{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:28px}}.toc a{{text-decoration:none;font-size:11px;border:1px solid var(--line);border-radius:8px;padding:7px 10px;color:var(--muted)}}.week-card{{border:1px solid var(--line);border-radius:17px;background:var(--panel);padding:23px;margin:14px 0}}.week-heading{{display:flex;justify-content:space-between;align-items:start;gap:18px;margin-bottom:17px}}.week-heading h2{{font-size:20px;letter-spacing:-.035em;margin:4px 0 0}}.week-status{{font-size:11px;color:var(--muted);border:1px solid var(--line);border-radius:99px;padding:6px 9px;white-space:nowrap}}.available .week-status{{color:var(--accent);border-color:#52683b}}.day-grid{{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:11px}}.day-card{{border:1px solid var(--line);border-radius:12px;padding:16px;background:#121510}}.day-kicker{{font-size:9px;letter-spacing:.14em;color:var(--accent);font-weight:850}}.day-card h3{{font-size:15px;line-height:1.35;margin:7px 0}}.day-card p,.coming p{{font-size:12px;color:var(--muted);margin:0 0 13px}}.file-links{{display:flex;gap:7px;flex-wrap:wrap}}.file-link{{font-size:10px;font-weight:750;text-decoration:none;padding:6px 8px;border:1px solid var(--line);border-radius:7px;color:var(--blue)}}.coming{{display:flex;align-items:center;gap:13px;border:1px dashed #394332;background:#151912;padding:17px;border-radius:12px}}.coming-mark{{width:34px;height:34px;flex:none;border-radius:10px;background:var(--panel2);display:grid;place-items:center;color:var(--accent);font-size:18px}}.coming strong{{font-size:13px}}.coming p{{margin:3px 0 0}}.how{{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin:24px 0 44px}}.how article{{border:1px solid var(--line);border-radius:13px;padding:17px;background:var(--panel)}}.how b{{display:block;font-size:13px;margin-bottom:5px}}.how p{{color:var(--muted);font-size:12px;margin:0}}footer{{border-top:1px solid var(--line);padding:22px 0 32px;color:var(--muted);font-size:11px;display:flex;justify-content:space-between;gap:12px;flex-wrap:wrap}}
@media(max-width:760px){{.hero{{grid-template-columns:1fr;padding-top:44px;gap:23px}}.hero-panel{{max-width:400px}}.day-grid{{grid-template-columns:1fr}}.how{{grid-template-columns:1fr}}.week-card{{padding:16px}}.week-heading{{flex-direction:column;gap:10px}}.wrap{{padding:0 16px}}.top{{height:66px}}}}
</style>
</head>
<body>
<header><div class="wrap top"><div class="brand"><div class="mark">P/DSA</div><div>Python & DSA<small>Learning path · member hub</small></div></div><a class="top-link" href="{REPO_URL}">Open repository ↗</a></div></header>
<main class="wrap">
<section class="hero"><div><div class="eyebrow">Learn by doing · one day at a time</div><h1>Build the skill.<br>Prove the work.</h1><p>A clear route through Python, data structures and algorithms. Choose a week, open the day's plan, complete the work, then use the quiz and answer key to check your understanding.</p><div class="hero-actions"><a class="button primary" href="#week-01">Browse available sessions ↓</a><a class="button" href="{REPO_URL}/blob/main/README.md">Read the guide ↗</a></div></div><aside class="hero-panel"><div class="eyebrow">Course map</div><div class="number">16 weeks</div><p>{total_days} daily session folders currently published in the repository. This page is a static guide; lessons, quizzes, notes and solutions live in GitHub.</p></aside></section>
<div class="section-top"><div><h2>Navigate the curriculum</h2><p>Jump to a week or browse the course in order.</p></div></div>
<nav class="toc" aria-label="Jump to week">{"".join(f'<a href="#week-{n:02d}">W{n:02d}</a>' for n in range(1, 17))}</nav>
<div class="section-top"><div><h2>Weekly roadmap</h2><p>Published sessions link directly to their source files.</p></div></div>
{"".join(weeks)}
<div class="section-top"><div><h2>Your daily workflow</h2><p>Keep the routine simple and consistent.</p></div></div>
<div class="how"><article><b>01 / Learn</b><p>Follow the plan in order. Use the linked free lessons and attempt the problem before reading hints.</p></article><article><b>02 / Recall</b><p>Take the quiz closed-book, then check the answer key and write notes in your own words.</p></article><article><b>03 / Publish</b><p>Save your solution and notes in the repository, then commit your work so progress is visible.</p></article></div>
</main>
<footer><div class="wrap" style="display:flex;justify-content:space-between;gap:12px;flex-wrap:wrap;width:100%"><span>Python & DSA Learning Path · Static navigation hub</span><span><a href="{REPO_URL}">Repository source of truth ↗</a></span></div></footer>
</body></html>
"""
    (SITE / "index.html").write_text(page, encoding="utf-8")
    print(f"Built {SITE / 'index.html'} with {total_days} published day folders.")


if __name__ == "__main__":
    build()
