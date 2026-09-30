"""Move rendered HTML, .tex, and *_files/ into each assignment's _output/ folder.

Quarto runs this after every render (see post-render in _quarto.yml). The
.qmd source and the PDF stay in the assignment folder; everything else that
Quarto writes goes to assignment-NN/_output/.
"""

from pathlib import Path
import shutil

root = Path(__file__).resolve().parent.parent  # the assignments/ folder

for folder in sorted(root.glob("assignment-*/")):
    rendered = [*folder.glob("*.html"), *folder.glob("*.tex"), *folder.glob("*_files")]
    if not rendered:
        continue
    output = folder / "_output"
    output.mkdir(exist_ok=True)
    for item in rendered:
        target = output / item.name
        if target.is_dir():
            shutil.rmtree(target)  # replace the previous render
        elif target.exists():
            target.unlink()
        shutil.move(str(item), str(target))
