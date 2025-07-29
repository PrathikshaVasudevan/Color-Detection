import cv2
import pandas as pd
import streamlit as st
from streamlit_drawable_canvas import st_canvas

# Load the color data
@st.cache_data
def load_colors():
    return pd.read_csv("colors.csv", names=["color", "color_name", "hex", "R", "G", "B"], header=None)

df = load_colors()

# Title
st.title("🎨 Color Detection App")
st.markdown("Upload an image, click on it, and get the color name and RGB values.")

# Upload image
uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    file_bytes = uploaded_file.read()
    np_arr = np.frombuffer(file_bytes, np.uint8)
    image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    st.image(image, caption="Uploaded Image", use_column_width=True)

    # Drawable canvas
    canvas_result = st_canvas(
        fill_color="rgba(255, 255, 255, 0)",
        stroke_width=3,
        stroke_color="#000",
        background_image=image,
        update_streamlit=True,
        height=image.shape[0],
        width=image.shape[1],
        drawing_mode="point",
        key="canvas",
    )

    if canvas_result.json_data and canvas_result.json_data["objects"]:
        last_point = canvas_result.json_data["objects"][-1]
        x, y = int(last_point["left"]), int(last_point["top"])
        r, g, b = image[y, x]
        
        # Get closest color name
        def get_color_name(R, G, B):
            min_dist = float("inf")
            cname = None
            for i in range(len(df)):
                d = abs(R - int(df.loc[i, "R"])) + abs(G - int(df.loc[i, "G"])) + abs(B - int(df.loc[i, "B"]))
                if d <= min_dist:
                    min_dist = d
                    cname = df.loc[i, "color_name"]
            return cname

        color_name = get_color_name(r, g, b)

        st.markdown(f"**Detected Color:** {color_name}")
        st.markdown(f"**RGB Values:** R={r}, G={g}, B={b}")
