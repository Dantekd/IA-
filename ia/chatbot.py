import streamlit as st
import groq

modelos=['llama3-8b-8192','llama3-70b-8192']
#configurar la pagina
def configurar_pagina():
    st.set_page_config(page_title=" Bienvenidos a tu IA",page_icon="😋")#cambia el nombre de la ventana
    st.title("Bienvenidos a tu IA")
def mostrar_sidebar():
    st.sidebar.title("Elegi tu modelo de IA favorito")
    modelo= st.sidebar.selectbox("¿Cual elejís?", modelos,index=0)
    st.write(f"**ELEJISTE EL MODELO** : {modelo}")
    return modelo
def crear_cliente_groq():
    groq_api_key= st.secrets['GROQ_API_KEY']#Almacena la apikey de gorq
    return groq.Groq(api_key=groq_api_key)
#inicializar el estado de los mensajes.
def inicializacion_estado_chat():
    if "mensajes" not in st.session_state:
        st.session_state.mensajes=[]
#histotial del chat 
def mostrar_historial_chat():
    for mensaje in st.session_state.mensajes:
        with st.chat_message(mensaje["role"]): #context manager
            st.markdown(mensaje["content"])
def obtener_mensaje_usuario():
    return st.chat_input("Envia un mensaje")
#agregar los mensaje al estado 
def agregar_mensaje_al_historial(role, content):
    st.session_state.mensajes.append({"role":role,"content":content})
#mostar mensaje en la pantalla
def mostrar_mensaje(role, content):
    with st.chat_message(role):
        st.markdown(content)
#llamar al modelo groq
def obtener_respuesta_modelo(cliente, modelo, mensajes):
    respuesta=cliente.chat.completions.create(
        model=modelo,
        messages=mensajes,
        stream= False
    )
    return respuesta.choices[0].message.content

#Flujo de la app
def ejecutar_app():
    configurar_pagina()
    modelo=mostrar_sidebar()
    cliente=crear_cliente_groq()
    inicializacion_estado_chat()
    mostrar_historial_chat()
    mensaje_usuario=obtener_mensaje_usuario()
    

    if mensaje_usuario:
        agregar_mensaje_al_historial("user",mensaje_usuario)
        mostrar_mensaje("user",mensaje_usuario)
        mensaje_modelo=obtener_respuesta_modelo(cliente,modelo,st.session_state.mensajes)
        agregar_mensaje_al_historial("assistant",mensaje_modelo)
        mostrar_mensaje("assistant",mensaje_modelo)
        

if __name__ =='__main__':#si este archivo es el archivo principal, entonces EJECUTÁ
    ejecutar_app()