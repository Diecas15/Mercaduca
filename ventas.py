import streamlit as st
from db_connection import conectar
from datetime import date

def registrar_venta():
    st.subheader("Registrar Venta Diaria")

    # 1️⃣ Seleccionar proveedor
    conn = conectar()
    cur = conn.cursor()
    cur.execute("SELECT id_proveedor, nombre, comercio FROM proveedores")
    proveedores = cur.fetchall()
    conn.close()

    proveedor_dict = {f"{nombre} ({comercio})": (id_prov, comercio) for id_prov, nombre, comercio in proveedores}
    proveedor_seleccionado = st.selectbox("Seleccione proveedor", list(proveedor_dict.keys()))
    id_proveedor, comercio = proveedor_dict[proveedor_seleccionado]

    # 2️⃣ Seleccionar producto de ese proveedor
    conn = conectar()
    cur = conn.cursor()
    cur.execute("""
        SELECT id_producto, nombre_producto 
        FROM productos 
        WHERE id_proveedor = %s
    """, (id_proveedor,))
    productos = cur.fetchall()
    conn.close()

    producto_dict = {nombre_producto: id_producto for id_producto, nombre_producto in productos}
    producto_seleccionado = st.selectbox("Seleccione producto", list(producto_dict.keys()))
    id_producto = producto_dict[producto_seleccionado]

    # 3️⃣ Seleccionar el número de precio (1 al 7)
    numero_precio = st.selectbox("Seleccione opción de precio (1 a 7)", [1,2,3,4,5,6,7])

    # 4️⃣ Consultar el precio vigente actual
    conn = conectar()
    cur = conn.cursor()
    cur.execute("""
        SELECT precio 
        FROM precios_producto 
        WHERE id_producto = %s 
          AND numero_precio = %s
          AND (fecha_inicio <= %s AND (fecha_fin IS NULL OR fecha_fin >= %s))
    """, (id_producto, numero_precio, date.today(), date.today()))
    precio_actual = cur.fetchone()
    conn.close()

    if precio_actual:
        precio_unitario = precio_actual[0]
        st.success(f"Precio vigente: ${precio_unitario:.2f}")
    else:
        st.warning("No hay precio vigente para esta opción.")
        return  # detenemos aquí si no hay precio vigente

    # 5️⃣ Ingresar cantidad
    cantidad = st.number_input("Cantidad vendida", min_value=1, step=1)
    subtotal = cantidad * precio_unitario
    st.write(f"Subtotal: ${subtotal:.2f}")

    # 6️⃣ Seleccionar forma de pago
    forma_pago = st.selectbox("Forma de pago", ["Efectivo", "Tarjeta", "Transferencia", "Otro"])

    # 7️⃣ Mostrar ID visual generado
    codigo_visual = comercio[:2].upper() + str(numero_precio)
    st.write(f"**ID Producto Visual:** {codigo_visual}")

    # 8️⃣ Botón para registrar la venta
    if st.button("Registrar venta"):
        conn = conectar()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO ventas (id_producto, numero_precio, cantidad, subtotal, forma_pago)
            VALUES (%s, %s, %s, %s, %s)
        """, (id_producto, numero_precio, cantidad, subtotal, forma_pago))
        conn.commit()
        conn.close()
        st.success("Venta registrada correctamente.")
