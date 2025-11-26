import streamlit as st
import requests
import json

# Endpoint AWS
AWS_CHAT_URL = "https://d62dyx3bi7.execute-api.us-east-1.amazonaws.com/default/funcChatQA"

st.set_page_config(page_title="Chat QA Marítimo", page_icon="⚓")
st.title("⚓ Chatbot Jurídico Costero (AWS RAG)")


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

    # 2. Crear payload EXACTO que espera tu Lambda
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

        # Lanza error si el código no es 200
        response.raise_for_status()

        # Tu Lambda devuelve algo como:
        # {
        #   "statusCode": 200,
        #   "body": "{\"question\": ..., \"answer\": ..., ...}"
        # }
        outer_json = response.json()

        # Body viene como STRING → convertirlo a JSON
        body_raw = outer_json.get("body", "{}")
        body = json.loads(body_raw)

        # Extraemos la respuesta de RAG
        bot_reply = body.get("answer", "No se recibió 'answer' desde el backend.")

        # (Opcional) Mostrar detalles completos en un expander
        with st.expander("Ver JSON completo devuelto por AWS"):
            st.json(outer_json)
            st.json(body)

    except Exception as e:
        bot_reply = f"❌ Error al llamar al servicio de AWS: {e}"

    # 3. Mostrar respuesta del chatbot
    with st.chat_message("assistant"):
        st.markdown(bot_reply)

    # Guardar en historial
    st.session_state.messages.append(
        {"role": "assistant", "content": bot_reply}
    )
