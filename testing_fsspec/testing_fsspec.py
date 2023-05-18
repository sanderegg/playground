import fsspec

from pathlib import Path


file_path = Path("droidcam_latest.zip")
# fs = fsspec.filesystem("zip", fo=file_path)

files = fsspec.open_files(f"zip://*::file://{file_path}")
print(file)
