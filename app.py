import streamlit as st
import os
from openai import OpenAI
from utils import build_repo_context  # Asumiendo que guardaste el lector anterior en utils.py

# 1. Configuración de la página
st.set_page_config(page_title="Nemotron Code Auditor", page_icon="🛡️", layout="wide")

st.title("🛡️ Nemotron 3 Super: Auditoría de Código Soberana")
st.markdown("""
Esta herramienta utiliza el modelo **NVIDIA Nemotron 3 Super (120B)** para realizar un razonamiento profundo 
sobre repositorios completos, garantizando privacidad y precisión técnica.
""")

# 2. Sidebar para configuración
with st.sidebar:
    st.header("Configuración")
    api_key = st.text_input("NVIDIA API Key", type="password")
    project_path = st.text_input("Ruta local del repositorio", placeholder="/usuario/proyectos/mi-repo")
    
    st.info("Este modelo de 120B parámetros analiza vulnerabilidades, lógica y arquitectura.")

# 3. Lógica principal
if st.button("🚀 Iniciar Auditoría Profunda"):
    if not api_key or not project_path:
        st.error("Por favor, proporciona la API Key y la ruta del proyecto.")
    elif not os.path.exists(project_path):
        st.error("La ruta especificada no existe.")
    else:
        try:
            with st.spinner("Leyendo repositorio y preparando contexto masivo..."):
                # Llamamos a la función de lectura que creamos antes
                contexto = build_repo_context(project_path)
                
            st.success(f"Contexto preparado exitosamente.")

            # Inicializar cliente de NVIDIA
            client = OpenAI(base_url="https://integrate.api.nvidia.com/v1", api_key=api_key)

            with st.spinner("Nemotron está razonando sobre tu código..."):
                response = client.chat.completions.create(
                    model="nvidia/nemotron-3-super-120b",
                    messages=[
                        {"role": "system", "content": "Eres un auditor senior de ciberseguridad. Analiza el código y genera un reporte estructurado en Markdown con secciones de: Vulnerabilidades, Mejoras de Lógica y Plan de Despliegue."},
                        {"role": "user", "content": contexto}
                    ],
                    temperature=0.1
                )
                
                reporte = response.choices[0].message.content

            # 4. Mostrar Resultados
            st.divider()
            st.subheader("📊 Reporte de Auditoría")
            st.markdown(reporte)
            
            # Opción para descargar el reporte
            st.download_button("Descargar Reporte (MD)", reporte, file_name="auditoria_nemotron.md")

        except Exception as e:
            st.error(f"Ocurrió un error durante el análisis: {e}")

# Pie de página técnico
st.caption("Desarrollado con NVIDIA Nemotron 3 Super | Contexto: 1M Tokens | Inferencia FP8")
