import streamlit as st
import torch
from torchvision import models, transforms
from PIL import Image
import io

# Clases en orden alfabético según el notebook
CLASS_NAMES = ['other_activities', 'safe_driving', 'talking_phone', 'texting_phone', 'turning']
CLASS_LABELS = {
    'safe_driving': '✅ Conducción Segura',
    'turning': '⚠️ Girando / Mirando Atrás',
    'texting_phone': '📱 Escribiendo en el Celular',
    'talking_phone': '📞 Hablando por Celular',
    'other_activities': '🥤 Otras Distracciones (Bebiendo/Comiendo)'
}

@st.cache_resource
def load_vision_model():
    try:
        # Cargar ResNet18
        model = models.resnet18(pretrained=False)
        num_ftrs = model.fc.in_features
        model.fc = torch.nn.Sequential(
            torch.nn.Dropout(0.5),
            torch.nn.Linear(num_ftrs, 5)
        )
        
        # Cargar Pesos (Se asume CPU para inferencia web estándar)
        checkpoint = torch.load("para_web_modulo_2.pth", map_location=torch.device('cpu'))
        # Dependiendo de cómo se guardó (state_dict directo o diccionario con 'model_state_dict')
        if 'model_state_dict' in checkpoint:
            model.load_state_dict(checkpoint['model_state_dict'])
        else:
            model.load_state_dict(checkpoint)
            
        model.eval()
        return model, True
    except Exception as e:
        return str(e), False

def preprocess_image(image):
    transform = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])
    return transform(image).unsqueeze(0)

def app():
    st.title("📸 Módulo 2: Detección de Conducción Distractiva")
    st.markdown("Clasifica automáticamente imágenes de conductores para mejorar la seguridad vial.")
    
    model, is_loaded = load_vision_model()
    
    if not is_loaded:
        st.warning(f"⚠️ Hubo un problema cargando el modelo ResNet18. Detalles: {model}")
        return
        
    st.success("✅ Modelo ResNet18 cargado correctamente.")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### Sube una imagen del conductor")
        uploaded_file = st.file_uploader("Elige una imagen (JPG, PNG)", type=["jpg", "jpeg", "png"])
        
        if uploaded_file is not None:
            image = Image.open(uploaded_file).convert('RGB')
            st.image(image, caption="Imagen Subida", use_container_width=True)
            
    with col2:
        if uploaded_file is not None:
            st.markdown("### Resultados del Análisis")
            with st.spinner("Analizando la imagen con ResNet18..."):
                input_tensor = preprocess_image(image)
                
                with torch.no_grad():
                    outputs = model(input_tensor)
                    probabilities = torch.nn.functional.softmax(outputs[0], dim=0)
                    
                # Obtener Top predicciones
                top_prob, top_catid = torch.topk(probabilities, 5)
                
                best_class = CLASS_NAMES[top_catid[0]]
                best_prob = top_prob[0].item() * 100
                
                if best_class == 'safe_driving':
                    st.success(f"**{CLASS_LABELS[best_class]}** ({best_prob:.2f}%)")
                else:
                    st.error(f"**{CLASS_LABELS[best_class]}** ({best_prob:.2f}%)")
                    
                st.markdown("#### Confianza por Categoría:")
                for i in range(5):
                    cat_name = CLASS_NAMES[top_catid[i]]
                    prob = top_prob[i].item() * 100
                    st.progress(int(prob))
                    st.caption(f"{CLASS_LABELS[cat_name]}: {prob:.2f}%")
