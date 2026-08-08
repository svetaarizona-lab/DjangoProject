from pathlib import Path

data = Path("data.json").read_text(encoding="utf-16")
Path("data.json").write_text(data, encoding="utf-8")
print("Done")
