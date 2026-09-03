from pathlib import Path
image_paths = []
for ext in ("*.jpg", "*.jpeg", "*.png"):
    image_paths.extend([str(p) for p in Path("ocr_output/s12249-023-02680-y").rglob(ext)])
print(len(image_paths), image_paths)
