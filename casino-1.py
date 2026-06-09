import random
import time
import streamlit as st

st.set_page_config(page_title="Test Your Luck", layout="centered")

# --- ESTILOS ---
st.markdown("""
<style>

.title-bar {
    background: linear-gradient(to right, #66ccff, #99ddff);
    color: #000;
    font-size: 36px;
    font-weight: bold;
    text-align: center;
    padding: 15px;
    border-radius: 12px;
    margin-bottom: 25px;
    box-shadow: 0px 0px 15px #66ccff;
}

.screen {
    background: #0a0a0a;
    padding: 25px;
    border-radius: 15px;
    border: 4px solid #444;
    margin-bottom: 20px;
    text-align: center;
}

/* CAJAS EN GRIS METÁLICO */
.cs2-box {
    display: inline-block;
    background: linear-gradient(145deg, #d9d9d9, #bfbfbf);
    border: 3px solid #00eaff;
    border-radius: 10px;
    padding: 15px 25px;
    margin: 5px;
    font-size: 45px;
    box-shadow: 0px 0px 15px #00eaffaa;
}

/* Línea horizontal */
.divider {
    width: 100%;
    height: 3px;
    background: #00eaff;
    margin: 10px 0;
    border-radius: 2px;
}

/
