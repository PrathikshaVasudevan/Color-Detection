import streamlit as st
import pandas as pd
import cv2
from PIL import Image
import numpy as np
from streamlit_drawable_canvas import st_canvas

# Load the CSV file
@st.cache_data
def load_colors():
    return pd.read_csv("colors.csv", names=["color", "color_name", "hex", "R", "G", "B"], header=None)

df = load_colors()

def get_color_name(R, G, B):
    minimum = float('inf')
    cname = ""
    for i in range(len(df)):
        d = abs(R - int(df.loc[i, "R"])) + abs(G - int(df.loc[i, "G"])) + abs(B - int(df.loc[i, "B"]))
        if d <= minimum:
            minimum = d
            cname = df.loc[i, "color_name"]
    return cname

st.title("🎨 Color Detection App")
st.markdown("Upload an image and click on it to detect the color.")

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

    canvas_result = st_canvas(
        fill_color="rgba(255, 255, 255, 0)",
        stroke_width=5,
        stroke_color="#000",
        background_image=image,
        update_streamlit=True,
        height=image.height,
        width=image.width,
        drawing_mode="point",
        key="canvas"
    )

    if canvas_result.json_data and canvas_result.json_data["objects"]:
        last_object = canvas_result.json_data["objects"][-1]
        x = int(last_object["left"])
        y = int(last_object["top"])

        img_array = np.array(image)
        try:
            pixel = img_array[y, x]
            R, G, B = int(pixel[0]), int(pixel[1]), int(pixel[2])