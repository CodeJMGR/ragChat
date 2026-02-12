import streamlit as st
import requests
import json

AWS_CHAT_URL = "https://odmnxemt26.execute-api.us-east-1.amazonaws.com/default/rag-lambda-fn"

st.set_page_config(page_title="Chat QA Marítimo", page_icon="⚓")
st.title("⚓ Chatbot Jurídico Costero y Playas (AWS RAG)")


# --------------------------
# Inicializar historial
# --------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []


# --------------------------
# Mostrar historial
# --------------------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])


# --------------------------
# Input del usuario
# --------------------------
prompt = st.chat_input("Escribe tu pregunta jurídica sobre normativa marítima...")

if prompt:

    # 1. Mostrar mensaje del usuario
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. Crear payload EXACTO que espera el backend
    payload = {
        "question": prompt,
        "ground_truth": ""
    }

    try:
        headers = {"Content-Type": "application/json"}

        response = requests.post(
            AWS_CHAT_URL,
            json=payload,
            headers=headers,
            timeout=60
        )
        response.raise_for_status()

        # ✔️ Tu backend retorna JSON directo (NO tiene body)
        data = response.json()

        # ✔️ Extraer el campo correcto
        bot_reply = data.get("answer", "No se encontró 'answer' en la respuesta.")

        # (Opcional) Mostrar detalles crudos
        with st.expander("Ver JSON completo devuelto por AWS"):
            st.json(data)

    except Exception as e:
        bot_reply = f"❌ Error al llamar al servicio de AWS: {e}"

    # 3. Respuesta del bot
    with st.chat_message("assistant"):
        st.markdown(bot_reply)

    # Guardar en historial
    st.session_state.messages.append(
        {"role": "assistant", "content": bot_reply}
    )
