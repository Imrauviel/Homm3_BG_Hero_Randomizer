import base64
import random
import string
from pathlib import Path

import streamlit as st

st.set_page_config(layout="wide")

st.markdown("""
    <style>
.custom-container {
    display: flex;
    justify-content: center;
    gap: 16px;
    padding: 16px;
}
.custom-column {
    flex: 1;
    max-width: 240px;
    text-align: center;
}
.hero-column {
    flex: 2;
    max-width: 400px;
}
.custom-column img {
    width: 100%;
    max-height: 300px;
    object-fit: contain;
    margin-bottom: 16px;
}
</style>
    """, unsafe_allow_html=True)

path = "assets"
all_paths = list(Path(path).glob("*.webp"))

heroes = [x for x in all_paths if "heroes" in str(x)]
level1 = [x for x in all_paths if "1" in str(x) and "hero_specialties" in str(x)]
level4 = [x for x in all_paths if "4" in str(x) and "hero_specialties" in str(x)]
level6 = [x for x in all_paths if "7" in str(x) and "hero_specialties" in str(x)]
abilities = [x for x in all_paths if "abilities" in str(x)]

cols_names = ["Hero Card", "Abilities", "Level 1", "Level 4", "Level 6"]
groups = [heroes, abilities, level1, level4, level6]


def generate_seed(length=8):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

if "options" not in st.session_state:
    st.session_state.options = []

if "seed" not in st.session_state:
    st.session_state.seed = generate_seed()


def pick_images(group, number_of_images=2):
    return random.sample(group, number_of_images) if len(group) >= number_of_images else []


def image_to_base64(path: Path) -> str:
    with open(path, "rb") as img_file:
        encoded = base64.b64encode(img_file.read()).decode("utf-8")
    return f"data:image/webp;base64,{encoded}"


def generate_new_options(seed_value=None):
    if not seed_value:
        seed_value = generate_seed()

    random.seed(seed_value)
    st.session_state.seed = seed_value
    st.session_state.options = [pick_images(group) for group in groups]
    return seed_value


left, center, right = st.columns([1, 2, 1])
with center:
    seed_value = st.text_input("Seed", value=st.session_state.seed)

    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("🎲 Random Again"):
            new_seed = generate_seed()
            generate_new_options(new_seed)

    with col2:
        if st.button("Random with Seed"):
            generate_new_options(seed_value)

if not st.session_state.options:
    generate_new_options(seed_value)

html = '<div class="custom-container">'
for name, options in zip(cols_names, st.session_state.options):
    column_class = "custom-column"
    if name == "Hero Card":
        column_class += " hero-column"

    html += f'<div class="{column_class}">'
    html += f"<h4>{name}</h4>"

    if len(options) < 2:
        html += "<p><em>Too few images to select from.</em></p>"
    else:
        for img_path in options:
            img_data = image_to_base64(img_path)
            html += f'<img src="{img_data}" alt="{img_path.name}">'

    html += "</div>"
html += "</div>"

st.markdown(html, unsafe_allow_html=True)
