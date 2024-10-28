import streamlit as st

# Title
st.title("Hello, Streamlit!")

# Text
st.write("This is a simple Streamlit app.")

# Input
name = st.text_input("What's your name?")
if name:
    st.write(f"Hello, {name}!")

# Slider
age = st.slider("How old are you?", 0, 100)
st.write(f"You are {age} years old.")
