from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt


DATASET_DIR = Path("data/raw")
CHART_PATH = Path("data/class_distribution.png")
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".gif", ".tif", ".tiff", ".webp"}


def verify_dataset():
    if not DATASET_DIR.exists() or not any(DATASET_DIR.iterdir()):
        print("ERROR: data/raw folder is missing or empty.")
        return None

    class_dirs = sorted(path for path in DATASET_DIR.iterdir() if path.is_dir())

    if not class_dirs:
        print("ERROR: No class folders found in data/raw.")
        return None

    print("Class folders found:")
    for class_dir in class_dirs:
        print(f"- {class_dir.name}")

    class_counts = {}
    total_images = 0

    print("\nImages per class:")
    for class_dir in class_dirs:
        image_count = sum(
            1
            for file_path in class_dir.rglob("*")
            if file_path.is_file() and file_path.suffix.lower() in IMAGE_EXTENSIONS
        )
        class_counts[class_dir.name] = image_count
        total_images += image_count
        print(f"- {class_dir.name}: {image_count}")

    print(f"\nTotal classes: {len(class_counts)}")
    print(f"Total images: {total_images}")

    CHART_PATH.parent.mkdir(exist_ok=True)

    plt.figure(figsize=(max(8, len(class_counts) * 1.2), 6))
    plt.bar(class_counts.keys(), class_counts.values(), color="#4C956C")
    plt.title("Images per Class")
    plt.xlabel("Class")
    plt.ylabel("Number of Images")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(CHART_PATH)
    plt.close()

    print(f"Class distribution chart saved to {CHART_PATH}")

    return class_counts


if __name__ == "__main__":
    verify_dataset()
