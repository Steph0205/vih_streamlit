import streamlit as st
import pandas as pd


st.markdown(
    """
    <style>
    .stApp {
        background-color: seashell;
    }
    </style>
    """,
    unsafe_allow_html=True
)



# Cargar base de datos
@st.cache_data
def load_data():
    return pd.read_csv("tabla_vih_corregida(112).csv", encoding="latin1")

df = load_data()

# Menú principal
menu = st.sidebar.selectbox("Ir a:", ["Inicio", "Datos Duros", "Conoce nuestra propuesta"])

# -------------------
# SECCIÓN DE INICIO
# -------------------
if menu == "Inicio":
    st.title("Rompe el silencio. Datos que salvan vidas.")
    st.header("VIH en México")

    st.subheader("Introducción teórica")
    st.text(
    "En México, hablar del VIH sigue siendo un tabú. Esta página busca generar "
    "concientización y verbalización sobre la importancia de conocer esta problemática. "
    "¿Por qué es importante hablar del VIH? Porque informar salva vidas."
)
    st.subheader("Imagen")
    st.image("Imagencanvavih.jpg", caption="Campaña de concientización", use_container_width=True)

    st.subheader("Video")
    st.video("https://youtu.be/l23Xi5Y2omI?si=bybilQpwn0afwMdi")

    st.subheader("Registro")
    st.text("Regístrate para recibir actualizaciones y noticias sobre el VIH en México.")

    nombre = st.text_input("Ingresa tu nombre:")
    if st.button("Registrarme"):
        if nombre.strip():
            st.success(f"Gracias por registrarte, {nombre}.")
        else:
            st.warning("Por favor, escribe tu nombre.")

# --------------------------
# SECCIÓN DE DATOS DUROS
# --------------------------
elif menu == "Datos Duros":
    st.title("Datos Duros sobre VIH en México")

    opcion = st.sidebar.selectbox("Selecciona un análisis:", [
        "Casos por sexo",
        "Casos por edad",
        "Casos y Seguro Social",
        "Resistencia a los medicamentos",
        "Edad vs Carga viral",
        "Mapa ilustrativo"
    ])

    if opcion == "Casos por sexo":
        st.subheader("Distribución de casos por sexo")
        conteo_sexo = df["sexo"].value_counts()
        st.bar_chart(conteo_sexo)

        st.subheader("Interpretación")
        st.text("La gráfica muestra que la mayoría de los casos se concentran en hombres cis, con una cifra muy superior al resto de los grupos. Las mujeres cis presentan una cantidad considerablemente menor, y los casos en personas trans (tanto hombres como mujeres) son significativamente bajos. Esta distribución sugiere una posible sobrerrepresentación en hombres cis, pero también podría reflejar subregistro o barreras en el acceso al diagnóstico en poblaciones trans.")

        st.subheader("Tabla filtrable")
        filtro_sexo = st.selectbox("Filtrar por sexo:", df["sexo"].unique())
        tabla_filtrada = df[df["sexo"] == filtro_sexo]
        st.dataframe(tabla_filtrada)
        
    elif opcion == "Casos por edad":
        st.subheader("Distribución de casos por edad")
        edades = df["edad"].value_counts().sort_index()
        st.line_chart(edades)

        st.subheader("Interpretación")
        st.text("La gráfica muestra que la mayoría de los casos de VIH en México se concentran entre los 20 y 35 años de edad, con un pico claro alrededor de los 25 a 30 años. A partir de los 35 años, la incidencia disminuye progresivamente, lo que sugiere que la población joven-adulta es la más afectada por esta enfermedad. Esta tendencia resalta la importancia de enfocar campañas de prevención y detección en personas en edad reproductiva y sexualmente activa.")

        st.subheader("Tabla filtrable")
        edades_unicas = sorted(df["edad"].dropna().unique())
        filtro_edad = st.selectbox("Filtrar por edad:", edades_unicas)
        tabla_filtrada_edad = df[df["edad"] == filtro_edad]
        st.dataframe(tabla_filtrada_edad)
        
    elif opcion == "Casos y Seguro Social":
        st.subheader("Distribución por tipo de seguridad social")

    # Filtrar los valores no deseados
        df_seguridad = df

    # Gráfica
        conteo_seguridad = df_seguridad["seguridad_social"].value_counts()
        st.bar_chart(conteo_seguridad)

    # Interpretación
        st.subheader("Interpretación")
        st.text("La mayoría de las personas diagnosticadas con VIH reportan no tener acceso a un sistema de seguridad social. "
            "Esto puede reflejar condiciones de vulnerabilidad, menor acceso a servicios médicos o "
            "precariedad en el seguimiento del tratamiento. También sugiere la importancia de fortalecer "
            "servicios públicos de salud para poblaciones sin afiliación.")

    # Tabla filtrable
        st.subheader("Tabla filtrable")
        opciones_seguridad = sorted(df_seguridad["seguridad_social"].dropna().unique())
        filtro_seguridad = st.selectbox("Filtrar por seguridad social:", opciones_seguridad)
        tabla_filtrada_seguridad = df_seguridad[df_seguridad["seguridad_social"] == filtro_seguridad]
        st.dataframe(tabla_filtrada_seguridad)
        
    elif opcion == "Resistencia a los medicamentos":
        st.subheader("Distribución por tipo de resistencia")

    # Filtrar los casos válidos (excluyendo 'Pendiente' y valores vacíos)
        resistencia_filtrada = df[df["resistencia"].isin(["NNRTI", "NRTI", "PI", "INSTI", "Compleja", "Susceptible"])]
        conteo_resistencia = resistencia_filtrada["resistencia"].value_counts()
        st.bar_chart(conteo_resistencia)

    # Interpretación
        st.subheader("Interpretación")
        st.text("La mayoría de los casos con resistencia detectada corresponden a la categoría NNRTI.\n"
            "Esto sugiere una alta exposición o falla terapéutica asociada a este tipo de medicamentos.\n"
            "La presencia de otros tipos como NRTI, PI o INSTI puede indicar un historial de tratamientos complejos.\n"
            "La información es clave para ajustar esquemas terapéuticos eficaces.")

    # Tabla filtrable
        st.subheader("Tabla filtrable")
        tipos_resistencia = sorted([r for r in df["resistencia"].dropna().unique() if r != "Pendiente"])
        filtro_resistencia = st.selectbox("Filtrar por tipo de resistencia:", tipos_resistencia)
        tabla_filtrada_resistencia = df[df["resistencia"] == filtro_resistencia]
        st.dataframe(tabla_filtrada_resistencia)
        
    elif opcion == "Edad vs Carga viral":
        st.subheader("Relación entre edad y carga viral")

    # Filtrar datos válidos
        datos_validos = df[df["carga_viral"] >= 0]

    # Agrupar por edad y calcular promedio de carga viral
        agrupado = datos_validos.groupby("edad")["carga_viral"].mean().reset_index()

    # Gráfica de línea
        st.line_chart(agrupado.rename(columns={"edad": "index"}).set_index("index"))

    # Interpretación
        st.subheader("Interpretación")
        st.text(
        "Se observa la carga viral promedio en distintos rangos de edad.\n"
        "Esto permite identificar si hay grupos etarios con mayor riesgo o concentración de carga viral.\n"
        "Puede ser útil para enfocar campañas de salud pública o intervenciones específicas."
    )

    # Tabla filtrable
        st.subheader("Tabla filtrable")
        edades_unicas = sorted(df["edad"].dropna().unique())
        filtro_edad = st.selectbox("Filtrar por edad:", edades_unicas)
        tabla_filtrada_edad = df[df["edad"] == filtro_edad]
        st.dataframe(tabla_filtrada_edad)
        
    elif opcion == "Mapa ilustrativo":
        st.title("🗺️ Mapa de Casos de VIH en México")
        st.write("Visualización geográfica de los casos registrados con coordenadas disponibles.")

        df_mapa = df[['y_lat', 'x_long']].dropna().rename(columns={'y_lat': 'lat', 'x_long': 'lon'})
        st.map(df_mapa)

        st.subheader("Interpretación geoespacial")
        st.write("Este mapa muestra dónde se concentran los casos de VIH según los datos disponibles.")
        st.write("La mayoría están en zonas urbanas, probablemente por mayor población y acceso a pruebas.")
        
        #Boton para propuesta
elif menu == "Conoce nuestra propuesta":
    st.title("Propuesta de emprendimiento público")
    st.header("La barrera invisible contra el VIH")
    
    st.subheader(
    "Pese a los avances médicos, el silencio, los prejuicios y la desinformación "
    "siguen siendo una barrera estructural que impide diagnósticos tempranos, "
    "apoyo social y políticas eficaces. Por eso deseamos crear esta propuesta "
    "de emprendimiento público para hablarlo con naturalidad en los espacios "
    "donde las juventudes están activas, y ese lugar es sin lugar a dudas las "
    "redes sociales, actualmente una vía clave de intervención pública."
)

    st.text("Haz click para conocer más")
    st.subheader("Video de nuestra propuesta")
    st.video("https://youtu.be/43rEh8vDdwA?si=tRPNt46zpgazKyjU")
    