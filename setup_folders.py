import os
import sys
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from config import IMAGE_SIZE, BATCH_SIZE, DATA_DIR

def preprocess():
    if not os.path.exists(DATA_DIR) or len(os.listdir(DATA_DIR)) == 0:
        print("ERROR: data/raw folder is empty or missing!")
        print("Please download PlantVillage dataset and put it in data/raw/")
        sys.exit(1)

    train_datagen = ImageDataGenerator(
        rescale=1./255,
        rotation_range=20,
        width_shift_range=0.2,
        height_shift_range=0.2,
        horizontal_flip=True,
        validation_split=0.2
    )

    val_datagen = ImageDataGenerator(
        rescale=1./255,
        validation_split=0.2
    )

    train_generator = train_datagen.flow_from_directory(
        DATA_DIR,
        target_size=IMAGE_SIZE,
        batch_size=BATCH_SIZE,
        class_mode='categorical',
        subset='training'
    )

    val_generator = val_datagen.flow_from_directory(
        DATA_DIR,
        target_size=IMAGE_SIZE,
        batch_size=BATCH_SIZE,
        class_mode='categorical',
        subset='validation'
    )

    print(f"\nTraining samples: {train_generator.samples}")
    print(f"Validation samples: {val_generator.samples}")
    print(f"Number of classes: {train_generator.num_classes}")

    os.makedirs("models", exist_ok=True)
    with open("models/class_names.txt", "w") as f:
        for class_name in train_generator.class_indices.keys():
            f.write(class_name + "\n")
    print("Class names saved to models/class_names.txt")

    return train_generator, val_generator

if __name__ == "__main__":
    preprocess()
