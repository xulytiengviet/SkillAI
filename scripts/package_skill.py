from pathlib import Path
import zipfile

root = Path(__file__).resolve().parents[1]
skill = root / "skills" / "quy-hoach-kmz-osm"
out = root / "dist"
out.mkdir(exist_ok=True)
target = out / "quy-hoach-kmz-osm.zip"

skip_parts = {"__pycache__", ".DS_Store"}
skip_suffix = {".pyc", ".pyo"}

with zipfile.ZipFile(target, "w", zipfile.ZIP_DEFLATED) as z:
    for p in sorted(skill.rglob("*")):
        if p.is_dir():
            continue
        if any(part in skip_parts for part in p.parts) or p.suffix in skip_suffix:
            continue
        arc = Path(skill.name) / p.relative_to(skill)
        z.write(p, arc.as_posix())

print(target)
