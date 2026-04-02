# Tomato Plant Disease Detection

This project is a deep learning based tomato plant disease detection system that identifies common tomato leaf diseases from uploaded images. It uses MobileNetV2 transfer learning for classification and provides a Streamlit web app for easy prediction and treatment guidance.

## Team

- Ayush Chauhan
- Jai Karan Gupta
- Kakul Mittal
- Vanya Kulshreshtha
- Yuvraj Singh

## Supervisor

Dr. Abhay Pratap Singh Bhadauria

## Institution

GLA University, Mathura

## Features

- Detects 10 tomato leaf classes from images
- Uses a trained MobileNetV2 transfer learning model
- Simple Streamlit web interface for image upload and prediction
- Displays predicted disease with confidence percentage
- Shows top 3 predictions
- Provides treatment recommendations for each disease class
- Highlights healthy leaves with a congratulatory message

## Dataset Used

- PlantVillage dataset
- Tomato leaf disease images organized into 10 class folders

## Model Used

- MobileNetV2 Transfer Learning
- Pretrained on ImageNet
- Custom classification head for tomato disease detection

## Accuracy Achieved

- 88.31%

## Technologies Used

- Python
- TensorFlow
- Keras
- Streamlit
- OpenCV

## Project Structure

```text
.
|-- app/
|   `-- app.py
|-- data/
|   |-- raw/
|   `-- class_distribution.png
|-- models/
|-- preprocess.py
|-- train.py
|-- verify_dataset.py
|-- config.py
|-- requirements.txt
```

## How To Run The Project

### 1. Clone or open the project folder

Make sure you are inside the project directory.

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Verify the dataset

Place the PlantVillage tomato dataset inside `data/raw/` with one folder per class, then run:

```bash
python verify_dataset.py
```

### 4. Preprocess the dataset

```bash
python preprocess.py
```

This creates training and validation generators and saves class names.

### 5. Train the model

```bash
python train.py
```

This trains the MobileNetV2 model, saves the best model, and stores the training history plot.

### 6. Run the Streamlit app

```bash
streamlit run app/app.py
```

Then open the local Streamlit URL in your browser, upload a tomato leaf image, and view the prediction result with treatment suggestions.

## Disease Classes

- Tomato_Bacterial_spot
- Tomato_Early_blight
- Tomato_Late_blight
- Tomato_Leaf_Mold
- Tomato_Septoria_leaf_spot
- Tomato_Spider_mites_Two_spotted_spider_mite
- Tomato__Target_Spot
- Tomato__Tomato_YellowLeaf__Curl_Virus
- Tomato__Tomato_mosaic_virus
- Tomato_healthy

## App Overview

The Streamlit application loads the trained model, preprocesses uploaded leaf images to `224 x 224`, normalizes pixel values, predicts the disease class, and displays confidence scores along with treatment recommendations.
