import streamlit as st
from PyPDF2 import PdfReader
import os

st.header("hello")

st.write(os.getenv("GEMINI_API"))