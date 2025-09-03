import streamlit as st

# Page title
st.title("🚀 My First Streamlit App")

# Text input
name = st.text_input("Enter your name:")

# Button
if st.button("Say Hello"):
    st.write(f"Hello, {name} 👋")

# Slider
age = st.slider("Select your age:", 1, 100, 25)
st.write(f"Your age is {age}")

# Checkbox
if st.checkbox("Show secret message"):
    st.success("🎉 Streamlit is awesome!")
