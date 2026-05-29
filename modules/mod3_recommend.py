import streamlit as st
import sys
import os
import pandas as pd

# Añadir el directorio raíz para poder importar el script
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

@st.cache_resource
def load_recommender():
    try:
        from para_web_modulo_3 import recommend
        return recommend, True
    except Exception as e:
        return str(e), False

def app():
    st.title("🗺️ Módulo 3: Recomendación de Destinos de Viaje")
    st.markdown("Sistema de recomendación híbrido (NeuMF-H) basado en tu perfil para sugerirte las mejores aventuras.")
    
    recommend_fn, is_loaded = load_recommender()
    
    if not is_loaded:
        st.warning(f"⚠️ Error cargando el modelo de recomendación: {recommend_fn}")
        return
        
    st.success("✅ Modelo NeuMF-H cargado correctamente.")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("### Tu Perfil de Viajero")
        gender = st.selectbox("Género:", ["Female", "Male"])
        num_adults = st.number_input("Número de Adultos:", min_value=1, max_value=10, value=2)
        num_children = st.number_input("Número de Niños:", min_value=0, max_value=10, value=0)
        
        preferences = st.multiselect(
            "Preferencias de Destino:",
            ["Beach", "Historical", "Nature", "Adventure", "City"],
            default=["Beach", "Nature"]
        )
        
        get_recs_btn = st.button("Buscar Destinos")
        
    with col2:
        if get_recs_btn:
            if not preferences:
                st.error("Por favor, selecciona al menos una preferencia.")
            else:
                with st.spinner("Analizando tus gustos con IA..."):
                    try:
                        recs = recommend_fn(
                            preferences=preferences,
                            gender=gender,
                            num_adults=num_adults,
                            num_children=num_children
                        )
                        
                        st.markdown("### Top 5 Destinos Recomendados")
                        
                        for i, rec in enumerate(recs):
                            # Mapear algunos emojis por tipo
                            emoji = "🌴" if rec['type'] == "Beach" else "🏛️" if rec['type'] == "Historical" else "🌲" if rec['type'] == "Nature" else "🧗" if rec['type'] == "Adventure" else "🏙️"
                            
                            st.markdown(f"""
                            <div class='metric-card' style='padding:15px; margin-bottom:10px;'>
                                <h4 style='margin:0; color:#4CAF50;'>#{rec['rank']} - {emoji} {rec['destination']}</h4>
                                <p style='margin:5px 0 0 0;'><b>Estado:</b> {rec['state']} | <b>Tipo:</b> {rec['type']}</p>
                                <p style='margin:0;'><b>Mejor Época:</b> {rec['best_time']} | <b>Popularidad:</b> ⭐ {rec['popularity']}/10.0</p>
                                <p style='margin:0; font-size:12px; color:#888;'>Match Score (NeuMF-H): {rec['score']:.4f}</p>
                            </div>
                            """, unsafe_allow_html=True)
                            
                    except Exception as e:
                        st.error(f"Error generando recomendaciones: {str(e)}")
        else:
            st.info("Cuéntanos sobre ti y haz clic en 'Buscar Destinos'.")
