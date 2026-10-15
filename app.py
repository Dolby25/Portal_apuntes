import streamlit as st
import os

# ========================================================
# PORTAL DE APUNTES COLABORATIVO - CÓDIGO UNIFICADO PILOTO
# ========================================================

# 1. Configuración del título y diseño de la página web
st.set_page_config(page_title="Portal de Apuntes", page_icon="📚", layout="centered")

st.title("📚 Portal de Apuntes Colaborativo")
st.subheader("Proyecto Piloto - Intercambio de Material de Estudio")
st.write("Sube tus apuntes, resúmenes o guías para ayudar a otros estudiantes.")

# 2. Definición de las opciones del menú
INSTITUCIONES = ["Universidad Mayor", "Inacap", "Duoc UC", "Universidad de Chile"]

# 3. Interfaz visual: Menús de filtro en la barra lateral
st.sidebar.header("🔍 Filtros y Categorías")
institucion_seleccionada = st.sidebar.selectbox("Selecciona tu Institución:", INSTITUCIONES)
ramo_ingresado = st.sidebar.text_input("Escribe el nombre del Ramo:", placeholder="Ej: Cálculo 1, Anatomía")

# 4. Crear la carpeta principal para guardar el material si no existe
CARPETA_BASE = "material_estudio"
if not os.path.exists(CARPETA_BASE):
    os.makedirs(CARPETA_BASE)

# --- SISTEMA DE CARGA DE ARCHIVOS ---
st.markdown("---")
st.header("📤 Sube tu Material")

# El alumno arrastra el archivo aquí
archivo_subido = st.file_uploader(
    "Selecciona un archivo (PDF, Word, Imagen, etc.)", 
    type=["pdf", "docx", "txt", "png", "jpg", "jpeg", "xlsx", "pptx"]
)

# Botón para confirmar la subida
if st.button("Guardar Material"):
    # Validamos que el usuario haya ingresado un ramo y seleccionado un archivo
    if not ramo_ingresado.strip():
        st.warning("⚠️ Por favor, ingresa el nombre del ramo antes de guardar.")
    elif archivo_subido is None:
        st.warning("⚠️ Por favor, selecciona un archivo para subir.")
    else:
        # Limpiamos el nombre del ramo para evitar problemas con carpetas
        ramo_limpio = "".join(x for x in ramo_ingresado if x.isalnum() or x in "._- ").strip()
        
        # Estructuramos la ruta: material_estudio/Universidad Mayor/Calculo 1/
        ruta_carpeta_destino = os.path.join(CARPETA_BASE, institucion_seleccionada, ramo_limpio)
        
        # Si la carpeta de ese ramo no existe para esa universidad, Python la crea automáticamente
        if not os.path.exists(ruta_carpeta_destino):
            os.makedirs(ruta_carpeta_destino)
            
        # Ruta completa final donde se guardará el archivo físico
        ruta_archivo_final = os.path.join(ruta_carpeta_destino, archivo_subido.name)
        
        # Escribimos el archivo en el disco del servidor/computador
        with open(ruta_archivo_final, "wb") as f:
            f.write(archivo_subido.getbuffer())
            
        st.success(f"🎉 ¡Éxito! El archivo **'{archivo_subido.name}'** se guardó correctamente en los ramos de **{institucion_seleccionada}**.")

# --- SISTEMA DE VISUALIZACIÓN Y DESCARGA ---
st.markdown("---")
st.header("📥 Material Disponible")

# Limpiamos el filtro de búsqueda igual que antes
ramo_busqueda = "".join(x for x in ramo_ingresado if x.isalnum() or x in "._- ").strip()
ruta_consulta = os.path.join(CARPETA_BASE, institucion_seleccionada, ramo_busqueda)

# Comprobamos si existen archivos para los filtros seleccionados
if ramo_busqueda and os.path.exists(ruta_consulta):
    archivos_en_ramo = os.listdir(ruta_consulta)
    
    if archivos_en_ramo:
        st.info(f"Se encontraron {len(archivos_en_ramo)} archivo(s) para **{ramo_ingresado}** en la **{institucion_seleccionada}**:")
        
        # Listamos cada archivo con un botón de descarga individual
        for archivo in archivos_en_ramo:
            ruta_descarga = os.path.join(ruta_consulta, archivo)
            with open(ruta_descarga, "rb") as file_to_download:
                st.download_button(
                    label=f"📄 Descargar: {archivo}",
                    data=file_to_download.read(),
                    file_name=archivo,
                    mime="application/octet-stream"
                )
    else:
        st.write("Aún no hay archivos subidos para este ramo. ¡Sé el primero en aportar!")
else:
    if not ramo_ingresado:
        st.write("💡 Escribe un ramo en la barra lateral izquierda para ver el material disponible.")
    else:
        st.write(f"Aún no hay material registrado para **{ramo_ingresado}** en **{institucion_seleccionada}**.")
