import streamlit as st
import psycopg2
from db_connection import conectar
from datetime import date

# ----------------- REGISTRAR PROVEEDOR -------------------
def registrar_proveedor():
    st.subheader("Registrar nuevo proveedor")

    nombre = st.text_input("Nombre del proveedor")
    comercio = st.text_input("Código del comercio (2 letras)").upper()

    if st.button("Registrar proveedor"):
        if len(comercio) != 2:
            st.warning("El código de comercio debe ser de 2 letras.")
        else:
            conn = conectar()
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO proveedores (nombre, comercio)
                VALUES (%s, %s)
            """, (nombre, comercio))
            conn.commit()
            conn.close()
            st.success("Proveedor registrado correctamente.")

# ----------------- REGISTRAR PRODUCTO -------------------
def registrar_producto():
    st.subheader("Registrar nuevo producto")

    conn = conectar()
    cur = conn.cursor()
    cur.execute("SELECT id_proveedor, nombre, comercio FROM proveedores")
    proveedores = cur.fetchall()
    conn.close()

    proveedor_dict = {f"{nombre} ({comercio})": id_prov for id_prov, nombre, comercio in proveedores}

    proveedor_seleccionado = st.selectbox("Seleccione proveedor", list(proveedor_dict.keys()))
    nombre_producto = st.text_input("Nombre del producto")

    if st.button("Registrar producto"):
        id_proveedor = proveedor_dict[proveedor_seleccionado]
        conn = conectar()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO productos (id_proveedor, nombre_producto)
            VALUES (%s, %s)
        """, (id_proveedor, nombre_producto))
        conn.commit()
        conn.close()
        st.success("Producto registrado correctamente.")

# ----------------- REGISTRAR PRECIOS -------------------
def registrar_precios():
    st.subheader("Registrar precios para producto")

    conn = conectar()
    cur = conn.cursor()
    cur.execute("""
        SELECT p.id_producto, p.nombre_producto, pr.comercio
        FROM productos p
        JOIN proveedores pr ON p.id_proveedor = pr.id_proveedor
    """)
    productos = cur.fetchall()
    conn.close()

    producto_dict = {f"{nombre_producto} ({comercio})": id_producto for id_producto, nombre_producto, comercio in productos}

    producto_seleccionado = st.selectbox("Seleccione producto", list(producto_dict.keys()))
    id_producto = producto_dict[producto_seleccionado]

    precios = {}
    for i in range(1, 8):
        precio = st.number_input(f"Precio #{i}", min_value=0.01, format="%.2f", key=f"precio{i}")
        precios[i] = precio

    if st.button("Registrar precios"):
        conn = conectar()
        cur = conn.cursor()

        for numero_precio, precio in precios.items():
            cur.execute("""
                INSERT INTO precios_producto (id_producto, numero_precio, precio)
                VALUES (%s, %s, %s)
            """, (id_producto, numero_precio, precio))

        conn.commit()
        conn.close()
        st.success("Precios registrados correctamente.")

# ----------------- REGISTRAR INVENTARIO POR PRECIO -------------------
def registrar_inventario_por_precio():
    st.subheader("Registrar cantidades por precio")

    conn = conectar()
    cur = conn.cursor()
    cur.execute("""
        SELECT p.id_producto, p.nombre_producto, pr.comercio
        FROM productos p
        JOIN proveedores pr ON p.id_proveedor = pr.id_proveedor
    """)
    productos = cur.fetchall()
    conn.close()

    producto_dict = {f"{nombre_producto} ({comercio})": id_producto for id_producto, nombre_producto, comercio in productos}
    producto_seleccionado = st.selectbox("Seleccione producto", list(producto_dict.keys()))
    id_producto = producto_dict[producto_seleccionado]

    cantidades = {}
    for i in range(1, 8):
        cantidad = st.number_input(f"Cantidad para precio #{i}", min_value=0, step=1, key=f"cantidad{i}")
        cantidades[i] = cantidad

    if st.button("Registrar inventario"):
        conn = conectar()
        cur = conn.cursor()

        for numero_precio, cantidad in cantidades.items():
            cur.execute("""
                INSERT INTO inventario_producto (id_producto, numero_precio, cantidad)
                VALUES (%s, %s, %s)
            """, (id_producto, numero_precio, cantidad))

        conn.commit()
        conn.close()
        st.success("Inventario registrado correctamente.")
