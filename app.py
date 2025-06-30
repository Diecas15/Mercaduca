import streamlit as st
import home
import login
import inventario
import empleados
import ventas

def main():
    st.set_page_config(page_title="Sistema MERCADUCA", page_icon="📦")

    # Inicializamos las variables de sesión al iniciar la app
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False
        st.session_state['rol'] = None
        st.session_state['username'] = None

    st.sidebar.title("MERCADUCA ERP")

    # Si el usuario NO está logueado:
    if not st.session_state['logged_in']:
        menu = ["Inicio", "Login"]
        choice = st.sidebar.selectbox("Menú", menu)

        if choice == "Inicio":
            home.app()
        elif choice == "Login":
            login.app()

    # Si el usuario ya está logueado:
    else:
        st.sidebar.write(f"Usuario: {st.session_state['username']}")
        st.sidebar.write(f"Rol: {st.session_state['rol']}")

        # Administrador ve todo
        if st.session_state['rol'] == "administrador":
            menu = ["Inicio", "Inventario", "Empleados", "Ventas Diarias", "Cerrar sesión"]
        else:  # Trabajador solo ve ventas
            menu = ["Inicio", "Ventas Diarias", "Cerrar sesión"]

        choice = st.sidebar.selectbox("Menú", menu)

        if choice == "Inicio":
            home.app()

        elif choice == "Inventario":
            opciones = ["Registrar proveedor", "Registrar producto", "Registrar precios", "Registrar cantidades por precio"]
            seleccion = st.selectbox("Inventario - Seleccione opción", opciones)

            if seleccion == "Registrar proveedor":
                inventario.registrar_proveedor()
            elif seleccion == "Registrar producto":
                inventario.registrar_producto()
            elif seleccion == "Registrar precios":
                inventario.registrar_precios()
            elif seleccion == "Registrar cantidades por precio":
                inventario.registrar_inventario_por_precio()

        elif choice == "Empleados":
            empleados.crear_empleado()

        elif choice == "Ventas Diarias":
            ventas.registrar_venta()

        elif choice == "Cerrar sesión":
            # Reiniciamos las variables de sesión
            st.session_state['logged_in'] = False
            st.session_state['rol'] = None
            st.session_state['username'] = None
            st.rerun()

if __name__ == "__main__":
    main()
