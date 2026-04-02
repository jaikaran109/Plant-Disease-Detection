from pathlib import Path

import numpy as np
import streamlit as st
from PIL import Image
from tensorflow.keras.models import load_model


PROJECT_ROOT = Path(__file__).resolve().parents[1]
MODEL_PATH = PROJECT_ROOT / "models" / "plant_disease_model.h5"
CLASS_NAMES_PATH = PROJECT_ROOT / "models" / "class_names.txt"
FALLBACK_MODEL_PATH = PROJECT_ROOT / "plant_disease_model.h5"
FALLBACK_CLASS_NAMES_PATH = PROJECT_ROOT / "class_names.txt"
IMAGE_SIZE = (224, 224)

CLASS_DISPLAY_NAMES = {
    "Tomato_Bacterial_spot": "Bacterial Spot",
    "Tomato_Early_blight": "Early Blight",
    "Tomato_Late_blight": "Late Blight",
    "Tomato_Leaf_Mold": "Leaf Mold",
    "Tomato_Septoria_leaf_spot": "Septoria Leaf Spot",
    "Tomato_Spider_mites_Two_spotted_spider_mite": "Spider Mites",
    "Tomato__Target_Spot": "Target Spot",
    "Tomato__Tomato_YellowLeaf__Curl_Virus": "Yellow Leaf Curl Virus",
    "Tomato__Tomato_mosaic_virus": "Mosaic Virus",
    "Tomato_healthy": "Healthy",
}

TREATMENT_RECOMMENDATIONS = {
    "Tomato_Bacterial_spot": [
        "Remove heavily infected leaves and avoid working with wet plants.",
        "Use copper-based bactericides as directed on the product label.",
        "Rotate crops and sanitize tools, trays, and stakes regularly.",
    ],
    "Tomato_Early_blight": [
        "Prune lower leaves and improve airflow around the plants.",
        "Apply a recommended fungicide and repeat according to label instructions.",
        "Mulch the soil surface to reduce splash spread from infected debris.",
    ],
    "Tomato_Late_blight": [
        "Remove infected leaves immediately and isolate badly affected plants.",
        "Apply a protective fungicide suitable for late blight management.",
        "Water at the base of the plant and avoid overhead irrigation.",
    ],
    "Tomato_Leaf_Mold": [
        "Reduce humidity in the growing area and increase ventilation.",
        "Remove infected foliage and avoid crowding plants together.",
        "Use a fungicide labeled for leaf mold if symptoms continue spreading.",
    ],
    "Tomato_Septoria_leaf_spot": [
        "Remove spotted lower leaves and destroy infected plant debris.",
        "Apply a fungicide as needed and keep leaves dry when watering.",
        "Rotate tomatoes away from the same soil for future seasons.",
    ],
    "Tomato_Spider_mites_Two_spotted_spider_mite": [
        "Spray the undersides of leaves with water to reduce mite populations.",
        "Use insecticidal soap or neem oil, covering the leaf undersides well.",
        "Remove badly infested leaves and monitor nearby plants closely.",
    ],
    "Tomato__Target_Spot": [
        "Remove infected leaves and improve spacing for better airflow.",
        "Avoid wet foliage for long periods and water early in the day.",
        "Apply an appropriate fungicide if the disease continues to spread.",
    ],
    "Tomato__Tomato_YellowLeaf__Curl_Virus": [
        "Remove severely infected plants to limit virus spread.",
        "Control whiteflies using sticky traps, reflective mulch, or safe insecticides.",
        "Use clean seedlings and keep weeds down around the crop area.",
    ],
    "Tomato__Tomato_mosaic_virus": [
        "Remove infected plants and avoid handling healthy plants after touching infected ones.",
        "Disinfect tools and wash hands frequently during plant care.",
        "Control weeds and avoid tobacco contamination near the crop.",
    ],
    "Tomato_healthy": [
        "Keep up balanced watering, proper nutrition, and regular monitoring.",
        "Continue good airflow, sanitation, and preventive care practices.",
        "Inspect leaves weekly so any future issue is caught early.",
    ],
}


def resolve_file_path(primary_path: Path, fallback_path: Path, label: str) -> Path:
    if primary_path.exists():
        return primary_path
    if fallback_path.exists():
        return fallback_path
    raise FileNotFoundError(f"{label} not found at {primary_path} or {fallback_path}.")


@st.cache_resource
def get_model():
    model_path = resolve_file_path(MODEL_PATH, FALLBACK_MODEL_PATH, "Model file")
    return load_model(model_path)


@st.cache_data
def get_class_names():
    class_names_path = resolve_file_path(
        CLASS_NAMES_PATH, FALLBACK_CLASS_NAMES_PATH, "Class names file"
    )
    return [
        line.strip()
        for line in class_names_path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def preprocess_image(image: Image.Image):
    image = image.convert("RGB")
    image = image.resize(IMAGE_SIZE)
    image_array = np.asarray(image, dtype=np.float32) / 255.0
    image_array = np.expand_dims(image_array, axis=0)
    return image_array


def format_class_name(class_name: str) -> str:
    return CLASS_DISPLAY_NAMES.get(class_name, class_name.replace("_", " ").strip())


def show_treatment_recommendation(class_name: str):
    recommendations = TREATMENT_RECOMMENDATIONS.get(class_name, [])

    if class_name == "Tomato_healthy":
        st.success("Congratulations! The tomato leaf looks healthy.")
    else:
        st.subheader("Treatment Recommendation")

    for recommendation in recommendations:
        st.write(f"- {recommendation}")


def render_header():
    st.markdown(
        """
        <style>
        .app-header {
            background: linear-gradient(135deg, #2f855a 0%, #48bb78 100%);
            color: white;
            padding: 1.25rem 1.5rem;
            border-radius: 16px;
            margin-bottom: 1.5rem;
            box-shadow: 0 10px 24px rgba(47, 133, 90, 0.18);
        }
        .app-header h1 {
            margin: 0;
            font-size: 2rem;
            font-weight: 700;
        }
        .app-header p {
            margin: 0.35rem 0 0;
            font-size: 1rem;
            opacity: 0.95;
        }
        .app-footer {
            margin-top: 2rem;
            padding-top: 1rem;
            text-align: center;
            color: #4a5568;
            font-size: 0.95rem;
        }
        </style>
        <div class="app-header">
            <h1>🌿 Tomato Plant Disease Detector</h1>
            <p>Upload a tomato leaf image to detect likely disease symptoms and review treatment guidance.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_sidebar():
    st.sidebar.title("About")
    st.sidebar.write(
        "This app uses a trained deep learning model to identify tomato leaf diseases from uploaded images."
    )
    st.sidebar.subheader("Instructions")
    st.sidebar.write("1. Upload a clear tomato leaf photo in JPG, JPEG, or PNG format.")
    st.sidebar.write("2. Make sure the leaf is centered and well lit.")
    st.sidebar.write("3. Review the predicted disease, confidence score, and treatment suggestions.")


def show_top_predictions(predictions, class_names, top_k=3):
    st.subheader("Top Predictions")
    top_indices = np.argsort(predictions)[::-1][:top_k]

    for rank, index in enumerate(top_indices, start=1):
        class_name = class_names[int(index)]
        confidence = float(predictions[int(index)]) * 100
        st.write(f"{rank}. {format_class_name(class_name)} - {confidence:.2f}%")


def render_enhanced_header():
    st.markdown(
        """
        <style>
        .stApp {
            background: linear-gradient(180deg, #f4fbf6 0%, #ffffff 24%);
        }
        .app-header-v2 {
            background: linear-gradient(135deg, #1f7a45 0%, #48bb78 100%);
            color: white;
            padding: 1.5rem 1.75rem;
            border-radius: 18px;
            margin-bottom: 1.25rem;
            box-shadow: 0 14px 28px rgba(31, 122, 69, 0.18);
        }
        .app-header-v2 h1 {
            margin: 0;
            font-size: 2.1rem;
            font-weight: 800;
            letter-spacing: 0.01em;
        }
        .app-header-v2 p {
            margin: 0.45rem 0 0;
            font-size: 1rem;
            opacity: 0.95;
        }
        .confidence-wrap {
            margin: 0.75rem 0 1rem;
        }
        .confidence-label {
            display: flex;
            justify-content: space-between;
            margin-bottom: 0.4rem;
            color: #1f2937;
            font-weight: 600;
        }
        .confidence-track {
            width: 100%;
            height: 14px;
            border-radius: 999px;
            background: #e5e7eb;
            overflow: hidden;
        }
        .confidence-fill {
            height: 100%;
            border-radius: 999px;
        }
        .prediction-card {
            background: #ffffff;
            border: 1px solid #d9eadf;
            border-left: 6px solid #48bb78;
            border-radius: 14px;
            padding: 0.9rem 1rem;
            margin-bottom: 0.75rem;
            box-shadow: 0 8px 18px rgba(72, 187, 120, 0.08);
        }
        .prediction-card strong {
            color: #14532d;
        }
        .treatment-box {
            background: #fff8e6;
            border: 1px solid #f3d27a;
            border-left: 6px solid #d69e2e;
            border-radius: 16px;
            padding: 1rem 1.15rem;
            margin-top: 1rem;
        }
        .healthy-box {
            background: #edfdf3;
            border: 1px solid #86efac;
            border-left: 6px solid #16a34a;
            border-radius: 16px;
            padding: 1rem 1.15rem;
            margin-top: 1rem;
        }
        .treatment-box h3, .healthy-box h3 {
            margin: 0 0 0.65rem;
            color: #1f2937;
        }
        .treatment-box ul, .healthy-box ul {
            margin: 0;
            padding-left: 1.15rem;
        }
        .app-footer-v2 {
            margin-top: 2rem;
            padding-top: 1rem;
            text-align: center;
            color: #4b5563;
            font-size: 0.95rem;
        }
        </style>
        <div class="app-header-v2">
            <h1>Tomato Plant Disease Detector</h1>
            <p>Upload a leaf image to predict the disease class and review treatment guidance.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_enhanced_sidebar():
    st.sidebar.title("Tomato Detector")
    st.sidebar.subheader("App Description")
    st.sidebar.write(
        "This app uses a trained MobileNetV2 model to detect common tomato leaf diseases from uploaded images."
    )
    st.sidebar.subheader("How To Use")
    st.sidebar.write("1. Upload a tomato leaf image in JPG, JPEG, or PNG format.")
    st.sidebar.write("2. Use a clear, well-lit photo with the leaf centered in the frame.")
    st.sidebar.write("3. Review the prediction, confidence score, and treatment guidance.")
    st.sidebar.subheader("Detectable Diseases")
    for disease_name in CLASS_DISPLAY_NAMES.values():
        st.sidebar.write(f"- {disease_name}")


def get_confidence_color(confidence: float) -> str:
    if confidence > 80:
        return "#22c55e"
    if confidence >= 50:
        return "#f59e0b"
    return "#ef4444"


def render_confidence_bar(confidence: float):
    safe_confidence = min(max(confidence, 0.0), 100.0)
    color = get_confidence_color(safe_confidence)
    st.markdown(
        f"""
        <div class="confidence-wrap">
            <div class="confidence-label">
                <span>Model Confidence</span>
                <span>{safe_confidence:.2f}%</span>
            </div>
            <div class="confidence-track">
                <div class="confidence-fill" style="width: {safe_confidence}%; background: {color};"></div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def show_top_predictions_cards(predictions, class_names, top_k=3):
    st.subheader("Top 3 Predictions")
    top_indices = np.argsort(predictions)[::-1][:top_k]

    for rank, index in enumerate(top_indices, start=1):
        class_name = class_names[int(index)]
        confidence = float(predictions[int(index)]) * 100
        st.markdown(
            f"""
            <div class="prediction-card">
                <strong>{rank}. {format_class_name(class_name)}</strong><br>
                Confidence: {confidence:.2f}%
            </div>
            """,
            unsafe_allow_html=True,
        )


def show_treatment_recommendation_cards(class_name: str):
    recommendations = TREATMENT_RECOMMENDATIONS.get(class_name, [])
    box_class = "healthy-box" if class_name == "Tomato_healthy" else "treatment-box"
    heading = (
        "Healthy Leaf Status" if class_name == "Tomato_healthy" else "Treatment Recommendations"
    )
    items_html = "".join(f"<li>{recommendation}</li>" for recommendation in recommendations)

    st.markdown(
        f"""
        <div class="{box_class}">
            <h3>{heading}</h3>
            <ul>{items_html}</ul>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if class_name == "Tomato_healthy":
        st.success("Congratulations! The tomato leaf looks healthy.")


def render_footer_note():
    st.markdown(
        (
            '<div class="app-footer-v2">'
            "Developed by Ayush Chauhan, Jai Karan Gupta, Kakul Mittal, "
            "Vanya Kulshreshtha, Yuvraj Singh | GLA University 2025-26"
            "</div>"
        ),
        unsafe_allow_html=True,
    )


def main():
    st.set_page_config(page_title="Tomato Plant Disease Detector", page_icon="🌿")
    render_enhanced_sidebar()
    render_enhanced_header()

    try:
        model = get_model()
        class_names = get_class_names()
    except FileNotFoundError as error:
        st.error(str(error))
        render_footer_note()
        return
    except Exception as error:
        st.error(f"Unable to load model assets: {error}")
        render_footer_note()
        return

    if model.output_shape[-1] != len(class_names):
        st.error(
            "The number of class names does not match the model output size. "
            f"Model outputs: {model.output_shape[-1]}, class names: {len(class_names)}"
        )
        render_footer_note()
        return

    uploaded_file = st.file_uploader(
        "Upload a tomato leaf image",
        type=["jpg", "jpeg", "png"],
    )

    if uploaded_file is None:
        st.info("Upload a tomato leaf image to start the diagnosis.")
        render_footer_note()
        return

    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Leaf Image", use_container_width=True)

    processed_image = preprocess_image(image)

    with st.spinner("Analyzing leaf image..."):
        predictions = model.predict(processed_image, verbose=0)[0]

    predicted_index = int(np.argmax(predictions))
    confidence = float(predictions[predicted_index]) * 100
    predicted_class = class_names[predicted_index]
    display_name = format_class_name(predicted_class)

    st.subheader("Prediction Result")
    st.write(f"Predicted Disease: {display_name}")
    render_confidence_bar(confidence)

    if confidence < 70:
        st.warning("Please upload a clearer leaf image")

    show_top_predictions_cards(predictions, class_names)

    show_treatment_recommendation_cards(predicted_class)

    render_footer_note()


if __name__ == "__main__":
    main()
