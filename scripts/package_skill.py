from pathlib import Path
import shutil

root=Path(__file__).resolve().parents[1]
src=root/"skills"/"quy-hoach-kmz-osm"
out=root/"dist"
out.mkdir(exist_ok=True)
archive=shutil.make_archive(str(out/"quy-hoach-kmz-osm"),"zip",root/"skills","quy-hoach-kmz-osm")
print(archive)
