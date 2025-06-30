import streamlit as st
from db_connection import conectar

def validar_login(username, password):
    conn = conectar()
    cur = conn.cursor()
    cur.execute("""
        SELECT id_empleado, nombre, apellido, rol
        FROM empleados
        WHERE username = %s AND password = %s
    """, (username, password))
    user = cur.fetchone()
    conn.close()
    return user

def crear_empleado():
    st.subheader("Registrar nuevo empleado")

    nombre = st.text_input("Nombre")
    apellido = st.text_input("Apellido")
    username = st.text_input("Usuario")
    password = st.text_input("Contraseña", type="password")
    rol = st.selectbox("Rol", ["administrador", "trabajador"])

    if st.button("Registrar empleado"):
        conn = conectar()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO empleados (nombre, apellido, username, password, rol)
            VALUES (%s, %s, %s, %s, %s)
        """, (nombre, apellido, username, password, rol))
        conn.commit()
        conn.close()
        st.success("Empleado registrado correctamente.")
