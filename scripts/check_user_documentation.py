"""Validate user documentation before a release."""
from __future__ import annotations
import re, sys
from pathlib import Path

LINK_RE = re.compile(r"!?\\[[^]]*\\]\\(([^)]+)\\)")
REQUIRED = ["## Installation und Start","## Bedienung","## Konfiguration","## Fehler und Support","## Version und Gültigkeit"]

def validate(root: Path) -> list[str]:
    guide=root/"docs/user/README.md"; errors=[]
    if not guide.is_file(): return ["missing docs/user/README.md"]
    text=guide.read_text(encoding="utf-8")
    errors += [f"missing section: {x}" for x in REQUIRED if x not in text]
    for md in (root/"docs/user").rglob("*.md"):
        body=md.read_text(encoding="utf-8")
        for raw in LINK_RE.findall(body):
            target=raw.split("#",1)[0].strip()
            if not target or "://" in target or target.startswith(("mailto:","#")): continue
            resolved=(md.parent/target).resolve()
            try: rel=resolved.relative_to(root.resolve())
            except ValueError: errors.append(f"{md.relative_to(root)}: reference escapes repository: {target}"); continue
            if not resolved.exists(): errors.append(f"{md.relative_to(root)}: missing local reference: {target}")
            if resolved.suffix.lower() in {".png",".jpg",".jpeg",".webp"} and not rel.as_posix().startswith("docs/user/screenshots/"):
                errors.append(f"{md.relative_to(root)}: screenshot outside docs/user/screenshots/: {target}")
    return errors

def main() -> int:
    errors=validate(Path(sys.argv[1] if len(sys.argv)>1 else "."))
    for e in errors: print(f"ERROR: {e}")
    if errors: return 1
    print("User documentation release gate passed.")
    return 0

if __name__=="__main__": raise SystemExit(main())
