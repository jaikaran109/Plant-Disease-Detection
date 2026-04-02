import sys
from pathlib import Path

from tensorflow.keras.preprocessing.image import ImageDataGenerator

from config import BATCH_SIZE, DATA_DIR, IMAGE_SIZE

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".gif", ".tif", ".tiff", ".webp"}


def get_class_image_counts(data_dir):
    class_dirs = sorted(path for path in data_dir.iterdir() if path.is_dir())
    class_counts = {}

    for class_dir in class_dirs:
        class_counts[class_dir.name] = sum(
            1
            for file_path in class_dir.rglob("*")
            if file_path.is_file() and file_path.suffix.lower() in IMAGE_EXTENSIONS
        )

    return class_counts


def preprocess():
    data_dir = Path(DATA_DIR)

    if not data_dir.exists() or not any(data_dir.iterdir()):
        print("ERROR: data/raw folder is empty or missing!")
        print("Please download PlantVillage dataset and put it in data/raw/")
        sys.exit(1)

    class_counts = get_class_image_counts(data_dir)

    if not class_counts:
        print("ERROR: No class folders found in data/raw/")
        sys.exit(1)

    print("Images found per class:")
    for class_name, image_count in class_counts.items():
        print(f"- {class_name}: {image_count}")

    train_datagen = ImageDataGenerator(
        rescale=1.0 / 255,
        rotation_range=20,
        width_shift_range=0.2,
        height_shift_range=0.2,
        horizontal_flip=True,
        validation_split=0.2,
    )

    val_datagen = ImageDataGenerator(
        rescale=1.0 / 255,
        validation_split=0.2,
    )

    train_generator = train_datagen.flow_from_directory(
        DATA_DIR,
        target_size=IMAGE_SIZE,
        batch_size=BATCH_SIZE,
        class_mode="categorical",
        subset="training",
    )

    val_generator = val_datagen.flow_from_directory(
        DATA_DIR,
        target_size=IMAGE_SIZE,
        batch_size=BATCH_SIZE,
        class_mode="categorical",
        subset="validation",
    )

    print(f"Total training samples: {train_generator.samples}")
    print(f"Total validation samples: {val_generator.samples}")
    print(f"Number of classes found: {train_generator.num_classes}")

    class_names = [
        class_name
        for class_name, _ in sorted(
            train_generator.class_indices.items(), key=lambda item: item[1]
        )
    ]

    models_dir = Path("models")
    models_dir.mkdir(exist_ok=True)
    class_names_path = models_dir / "class_names.txt"

    with class_names_path.open("w", encoding="utf-8") as file:
        if class_names:
            file.write("\n".join(class_names))
            file.write("\n")

    print(f"Class names saved to {class_names_path}")

    return train_generator, val_generator


if __name__ == "__main__":
    preprocess()
