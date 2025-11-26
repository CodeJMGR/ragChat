import streamlit as st
import requests

# URL de tu servicio en AWS (API Gateway, ALB, etc.)
AWS_CHAT_URL = "https://d62dyx3bi7.execute-api.us-east-1.amazonaws.com/default/funcChatQA"

st.set_page_config(page_title="Chat AWS", page_icon="🤖")
st.title("🤖 Chatbot con backend en AWS")

# Inicializar historial de mensajes en la sesión
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar historial de conversación
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Entrada del usuario
prompt = st.chat_input("Escribe tu pregunta...")

if prompt:
    # 1. Agregar mensaje del usuario al historial
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. Llamar a tu servicio en AWS
    try:
        # Ajusta el payload a lo que reciba tu API
        payload = {
            "message": prompt,
            "history": [
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
                if m["role"] in ("user", "assistant")
            ]
        }

        # Si tu API necesita headers (API Key, JWT, etc.), agrégalos aquí
        headers = {
            # "x-api-key": "TU_API_KEY",
            "Content-Type": "application/json"
        }

        response = requests.post(
            AWS_CHAT_URL,
            json=payload,
            headers=headers,
            timeout=30
        )
        response.raise_for_status()
        data = response.json()

        # Supongamos que tu API responde algo como:
        # { "reply": "texto de la respuesta del modelo" }
        bot_reply = data.get("reply", "No se recibió respuesta del backend.")

    except Exception as e:
        bot_reply = f"Error al llamar al servicio de AWS: {e}"

    # 3. Mostrar respuesta del bot y guardarla
    with st.chat_message("assistant"):
        st.markdown(bot_reply)

    st.session_state.messages.append(
        {"role": "assistant", "content": bot_reply}
    )
