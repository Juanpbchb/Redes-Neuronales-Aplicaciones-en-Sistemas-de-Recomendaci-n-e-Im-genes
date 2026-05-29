import os
# FIX: Evitar Segmentation Fault por colisión de librerías de C++ (PyTorch vs TensorFlow)
os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2' # Reducir logs innecesarios de TF

import streamlit as st

st.set_page_config(
    page_title="Sistema Inteligente de Transporte",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos CSS Personalizados
st.markdown("""
    <style>
    .main {
        background-color: #0E1117;
    }
    h1, h2, h3 {
        color: #4CAF50;
        font-family: 'Inter', sans-serif;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border-radius: 8px;
        border: none;
        padding: 10px 24px;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #45a049;
        transform: scale(1.05);
    }
    .metric-card {
        background-color: #1E1E1E;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #4CAF50;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

def main():
    st.sidebar.image("https://cdn-icons-png.flaticon.com/512/3448/3448339.png", width=100)
    st.sidebar.title("Menú Principal")
    st.sidebar.markdown("---")
    
    choice = st.sidebar.radio("Selecciona un Módulo:", [
        "🏠 Inicio",
        "📈 Mod 1: Predicción de Demanda",
        "📸 Mod 2: Conducción Distractiva",
        "🗺️ Mod 3: Recomendación de Destinos"
    ])
    
    st.sidebar.markdown("---")
    st.sidebar.info("Proyecto de Redes Neuronales y Algoritmos Bioinspirados - Trabajo 3")

    if choice == "🏠 Inicio":
        st.title("Sistema Inteligente Integrado para Transporte")
        st.markdown("""
        Bienvenido a la herramienta web integral de la Empresa de Transporte. 
        Este sistema utiliza modelos de **Aprendizaje Profundo (Deep Learning)** para:
        
        1. **Anticipar la demanda** de transporte en rutas clave.
        2. **Mejorar la seguridad vial** clasificando el comportamiento del conductor mediante visión por computadora.
        3. **Recomendar destinos** de viaje personalizados a nuestros usuarios.
        
         *Utiliza el menú lateral para navegar entre los módulos.*
        """)
        
        cols = st.columns(3)
        with cols[0]:
            st.markdown("""
            <div class='metric-card'>
                <h3>📈 Predicción</h3>
                <p>Redes Neuronales Recurrentes (LSTM/GRU) para análisis de series de tiempo de demanda.</p>
            </div>
            """, unsafe_allow_html=True)
        with cols[1]:
            st.markdown("""
            <div class='metric-card'>
                <h3>📸 Visión</h3>
                <p>Transfer Learning con ResNet18 en PyTorch para detección de distracciones en tiempo real.</p>
            </div>
            """, unsafe_allow_html=True)
        with cols[2]:
            st.markdown("""
            <div class='metric-card'>
                <h3>🗺️ Recomendación</h3>
                <p>NeuMF-H (Neural Collaborative Filtering Híbrido) en Keras para sugerencias precisas.</p>
            </div>
            """, unsafe_allow_html=True)

    elif choice == "📈 Mod 1: Predicción de Demanda":
        import modules.mod1_demand as mod1
        mod1.app()
        
    elif choice == "📸 Mod 2: Conducción Distractiva":
        import modules.mod2_vision as mod2
        mod2.app()
        
    elif choice == "🗺️ Mod 3: Recomendación de Destinos":
        import modules.mod3_recommend as mod3
        mod3.app()

if __name__ == '__main__':
    main()
