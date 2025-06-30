import streamlit as st
from PIL import Image

def app():
    st.title("📦 Sistema MERCADUCA")

    # Mostrar logo
    try:
        logo = Image.open("assets/Logo_UCA.png")
        st.image(logo, width=200)
    except FileNotFoundError:
        st.warning("⚠️ No se encontró el logo.")

    # Descripción
    st.markdown("""
    ### ¿Qué es MERCADUCA?

    **MERCADUCA** es un sistema ERP desarrollado para ofrecer a los emprendedores universitarios un entorno práctico, real y funcional para gestionar sus operaciones comerciales.

    Con **MERCADUCA** podrás:

    - Registrar y administrar proveedores.
    - Gestionar productos e inventario en tiempo real.
    - Controlar procesos de ventas y facturación.
    - Monitorear operaciones logísticas y comerciales.
    - Obtener reportes automáticos de gestión.
    - Controlar el flujo de usuarios y roles.

    > *Ayudar a los emprendedores es desarrollar su entorno universitario y práctico.*
    """)
