import streamlit as st
from PIL import Image
import empleados

def app():
    st.title("🔐 Inicio de Sesión - MERCADUCA")

    try:
        logo = Image.open("assets/Logo_UCA.png")
        st.image(logo, width=200)
    except FileNotFoundError:
        st.warning("⚠️ No se encontró el logo.")

    st.markdown("> *Ayudar a los emprendedores es desarrollar su entorno universitario y práctico.*")

    username = st.text_input("Usuario")
    password = st.text_input("Contraseña", type="password")

    if st.button("Ingresar"):
        user = empleados.validar_login(username, password)
        if user:
            st.session_state['logged_in'] = True
            st.session_state['rol'] = user[3]
            st.session_state['username'] = username
            st.success(f"Bienvenido {user[1]} {user[2]} - Rol: {user[3]}")
            st.rerun()
        else:
            st.error("Credenciales incorrectas")
