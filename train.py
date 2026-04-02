from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
from tensorflow.keras.layers import Dense, Dropout, GlobalAveragePooling2D
from tensorflow.keras.models import Model

from config import MODEL_DIR, MODEL_NAME
from preprocess import preprocess


NUM_CLASSES = 10
INPUT_SHAPE = (224, 224, 3)
EPOCHS = 10


def build_model():
    base_model = MobileNetV2(
        weights="imagenet",
        include_top=False,
        input_shape=INPUT_SHAPE,
    )
    base_model.trainable = False

    x = base_model.output
    x = GlobalAveragePooling2D()(x)
    x = Dense(256, activation="relu")(x)
    x = Dropout(0.5)(x)
    outputs = Dense(NUM_CLASSES, activation="softmax")(x)

    return Model(inputs=base_model.input, outputs=outputs)


def plot_training_history(history, output_path):
    accuracy = history.history.get("accuracy", [])
    val_accuracy = history.history.get("val_accuracy", [])
    epochs = range(1, len(accuracy) + 1)

    plt.figure(figsize=(8, 6))
    plt.plot(epochs, accuracy, label="Training Accuracy")
    plt.plot(epochs, val_accuracy, label="Validation Accuracy")
    plt.title("Training vs Validation Accuracy")
    plt.xlabel("Epoch")
    plt.ylabel("Accuracy")
    plt.legend()
    plt.grid(True, linestyle="--", alpha=0.4)
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()


def train():
    train_generator, val_generator = preprocess()

    if train_generator.num_classes != NUM_CLASSES:
        raise ValueError(
            f"Expected {NUM_CLASSES} classes, but found {train_generator.num_classes}."
        )

    models_dir = Path(MODEL_DIR)
    models_dir.mkdir(exist_ok=True)
    model_path = models_dir / MODEL_NAME
    history_path = models_dir / "training_history.png"

    model = build_model()
    model.compile(
        optimizer="adam",
        loss="categorical_crossentropy",
        metrics=["accuracy"],
    )

    callbacks = [
        ModelCheckpoint(
            filepath=str(model_path),
            monitor="val_accuracy",
            save_best_only=True,
            mode="max",
            verbose=1,
        ),
        EarlyStopping(
            monitor="val_accuracy",
            patience=3,
            restore_best_weights=True,
            verbose=1,
        ),
    ]

    history = model.fit(
        train_generator,
        validation_data=val_generator,
        epochs=EPOCHS,
        callbacks=callbacks,
    )

    plot_training_history(history, history_path)
    print(f"Training history plot saved to {history_path}")

    final_train_accuracy = history.history["accuracy"][-1]
    final_val_accuracy = history.history["val_accuracy"][-1]

    print(f"Final training accuracy: {final_train_accuracy:.4f}")
    print(f"Final validation accuracy: {final_val_accuracy:.4f}")

    return model, history


if __name__ == "__main__":
    train()
