import streamlit as st
import pandas as pd
import numpy as np
from tensorflow.keras.models import load_model

# Cargar el modelo entrenado

model = load_model('C:\\Users\\billt\\OneDrive\\Pictures\\Project\\Neural_Networks_Solution\\models\\locksmith_nn_model.h5')

# Título de la aplicación
st.title('Key Duplication Service Price Prediction / Predicción del precio del servicio de copia de llaves')

# Entradas del usuario
key_type = st.selectbox('Select Key Type / Selecciona el tipo de llave:', ['Llave 1 - sin botones', 'Llave 2 - con botones', 'Llave 3 - push button'])
distance = st.number_input('Enter the distance (in meters) / Ingrese la distancia (en metros):', 0)  # Distancia en metros
service_type = st.selectbox('Select Service Type / Selecciona el tipo de servicio:', ['Store', 'Customer'])

# Mapeo de valores de entrada
key_type_map = {
    'Llave 1 - sin botones': 1,
    'Llave 2 - con botones': 2,
    'Llave 3 - push button': 3
}

service_type_map = {
    'Customer': 1,
    'Store': 2
}

# Convertir las entradas del usuario a números
key_type_num = key_type_map[key_type]
service_type_num = service_type_map[service_type]

# Verificar si alguno de los valores es 0 y mostrar un mensaje de error
if service_type == 'Customer' and distance <= 0:
    st.error("Error: The distance must be greater than 0 when the service type is 'Customer'. Please provide a valid value.")  # Display error message
else:
    # Si el servicio es 'Store', la distancia no se toma en cuenta
    if service_type == 'Store':
        distance = 0

    # Crear un DataFrame con los datos proporcionados por el usuario
    input_data = np.array([[key_type_num, distance, service_type_num]])

    # Hacer la predicción usando el modelo cargado
    prediction = model.predict(input_data)

    # Establecer los precios mínimos según el tipo de llave
    if key_type == 'Llave 1 - sin botones':
        prediction[0][0] = max(prediction[0][0], 50)  # Asegurarse que no sea menor a 50
    elif key_type == 'Llave 2 - con botones':
        prediction[0][0] = max(prediction[0][0], 100)  # Asegurarse que no sea menor a 100
    elif key_type == 'Llave 3 - push button':
        prediction[0][0] = max(prediction[0][0], 180)  # Asegurarse que no sea menor a 180

    # Mostrar el resultado de la predicción
    st.write(f'The predicted price for the key duplication service is: ${prediction[0][0]:,.2f} / El precio previsto para el servicio de copia de llaves es: ${prediction[0][0]:,.2f}')
