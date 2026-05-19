#!/usr/bin/env python3
"""Convert script_plan.xlsx → README.md for a video-edits project.

Reads the first sheet, expects 4 columns: Time | Visual | Voice script | Title.
Writes a Markdown README with storyboard table.
Idempotent: only writes if xlsx is newer than README (or README missing).
"""
import sys
import os
from pathlib import Path

try:
    import openpyxl
except ImportError:
    print("ERR: openpyxl missing", file=sys.stderr)
    sys.exit(1)


def convert(xlsx_path: Path, readme_path: Path, project_name: str) -> bool:
    wb = openpyxl.load_workbook(xlsx_path, data_only=True)
    ws = wb[wb.sheetnames[0]]

    rows = []
    header = None
    for row in ws.iter_rows(values_only=True):
        first4 = [str(c).strip() if c is not None else "" for c in row[:4]]
        if not any(first4):
            continue
        if header is None:
            header = first4
            continue
        rows.append(first4)

    if not rows:
        return False

    lines = [
        f"# {project_name}",
        "",
        "> Auto-generated from `sources/script_plan.xlsx` by session-start hook.",
        "> If you edit xlsx, this README is regenerated on next session start.",
        "",
        "## Раскадровка",
        "",
        f"| {' | '.join(header)} |",
        f"| {' | '.join(['---'] * len(header))} |",
    ]
    for r in rows:
        cells = [c.replace("\n", " ").replace("|", "\\|") for c in r]
        lines.append(f"| {' | '.join(cells)} |")

    lines += [
        "",
        "## Исходники",
        "",
        "- `sources/narrator_audio*.ogg` — голос диктора",
        "- `sources/footage/` — видео-исходники",
        "- `sources/photos/` — студийные PNG (продукт на чёрном)",
        "- `sources/photos_lifestyle/` — lifestyle JPEG (продукт в среде, если есть)",
        "- `sources/stock/` — стоки (только контекст, не продукт)",
        "",
        "## Следующие шаги (см. CLAUDE.md → workflow A→B)",
        "",
        "- [ ] A1: voice-маркеры через `silencedetect`",
        "- [ ] A2: раскадровка — таблица выше, подтвердить",
        "- [ ] A2.5: gap-list — каких кадров не хватает в footage",
        "- [ ] A3: SFX-палитра",
        "- [ ] A4: музыка-категория",
        "- [ ] B5-B9: layered render",
        "",
    ]
    readme_path.write_text("\n".join(lines), encoding="utf-8")
    return True


def main():
    projects_root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("video-edits/projects")
    if not projects_root.is_dir():
        return

    status = []
    for proj in sorted(projects_root.iterdir()):
        if not proj.is_dir():
            continue
        xlsx = proj / "sources" / "script_plan.xlsx"
        readme = proj / "README.md"
        if not xlsx.exists():
            continue
        # Preserve manually-curated README. Only overwrite if README missing
        # OR previously auto-generated (contains the marker line).
        AUTO_MARKER = "Auto-generated from `sources/script_plan.xlsx`"
        readme_is_auto = (
            readme.exists()
            and AUTO_MARKER in readme.read_text(encoding="utf-8", errors="ignore")
        )
        if not readme.exists():
            should_write = True
        elif readme_is_auto and xlsx.stat().st_mtime > readme.stat().st_mtime:
            should_write = True
        else:
            should_write = False

        if should_write:
            try:
                if convert(xlsx, readme, proj.name):
                    status.append(f"{proj.name} (xlsx→README updated)")
                else:
                    status.append(f"{proj.name} (xlsx empty?)")
            except Exception as e:
                status.append(f"{proj.name} (ERR: {e})")
        else:
            note = "manual README — preserved" if readme.exists() and not readme_is_auto else "up-to-date"
            status.append(f"{proj.name} ({note})")

    if status:
        print(f"Active video projects: {', '.join(status)}")


if __name__ == "__main__":
    main()
