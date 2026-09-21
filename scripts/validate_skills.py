#!/usr/bin/env python3
"""Mechanical checks for skills/<name>/SKILL.md. See CONTRIBUTING-SKILLS.md."""

import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SKILLS = ROOT / "skills"
NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
DESC_MIN, DESC_MAX = 40, 500

errors = []
seen = {}


def fail(path, msg):
    errors.append(f"{path.relative_to(ROOT)}: {msg}")


def parse_frontmatter(text, path):
    if not text.startswith("---\n"):
        fail(path, "missing YAML frontmatter opening '---'")
        return None, text
    end = text.find("\n---\n", 3)
    if end == -1:
        fail(path, "unterminated frontmatter")
        return None, text
    block, body = text[4:end], text[end + 5 :]
    fields = {}
    key = None
    for line in block.splitlines():
        m = re.match(r"^([A-Za-z_-]+):\s*(.*)$", line)
        if m:
            key = m.group(1)
            fields[key] = m.group(2).strip()
        elif line.strip() and key:
            fields[key] += " " + line.strip()
        elif line.strip():
            fail(path, f"unparseable frontmatter line: {line!r}")
    return fields, body


def check(skill_dir):
    path = skill_dir / "SKILL.md"
    if not path.is_file():
        errors.append(f"skills/{skill_dir.name}: no SKILL.md")
        return
    text = path.read_text(encoding="utf-8")
    fields, body = parse_frontmatter(text, path)
    if fields is None:
        return

    extra = set(fields) - {"name", "description"}
    if extra:
        fail(path, f"unexpected frontmatter keys: {sorted(extra)}")

    name = fields.get("name", "")
    if not name:
        fail(path, "frontmatter is missing 'name'")
    else:
        if not NAME_RE.match(name):
            fail(path, f"name {name!r} is not kebab-case")
        if name != skill_dir.name:
            fail(path, f"name {name!r} does not match directory {skill_dir.name!r}")
        if name in seen:
            fail(path, f"duplicate name, also used by {seen[name]}")
        seen[name] = skill_dir.name

    desc = fields.get("description", "")
    if not desc:
        fail(path, "frontmatter is missing 'description'")
    elif not DESC_MIN <= len(desc) <= DESC_MAX:
        fail(path, f"description is {len(desc)} chars, want {DESC_MIN}-{DESC_MAX}")
    elif not re.search(r"\b(use|used|using|apply|applies|reach for|invoke|trigger|when|for)\b", desc, re.I):
        fail(path, "description does not say when to use the skill")

    heading = next((l for l in body.splitlines() if l.strip()), "")
    if not heading.startswith("# "):
        fail(path, f"first line after frontmatter is not an H1: {heading!r}")

    for target in LINK_RE.findall(body):
        if target.startswith(("http://", "https://", "#", "mailto:")):
            continue
        target = target.split("#", 1)[0]
        if not target:
            continue
        if not ((ROOT / target).exists() or (path.parent / target).exists()):
            fail(path, f"broken relative link: {target}")


def main():
    if not SKILLS.is_dir():
        print("no skills/ directory", file=sys.stderr)
        return 1
    dirs = sorted(d for d in SKILLS.iterdir() if d.is_dir())
    if not dirs:
        print("no skills found", file=sys.stderr)
        return 1
    for d in dirs:
        check(d)

    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    for d in dirs:
        if f"`skills/{d.name}/`" not in readme:
            errors.append(f"README.md: no table row for skills/{d.name}/")

    if errors:
        print(f"{len(errors)} problem(s):", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        return 1
    print(f"ok: {len(dirs)} skills valid")
    return 0


if __name__ == "__main__":
    sys.exit(main())
