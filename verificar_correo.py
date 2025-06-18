import os
from dotenv import load_dotenv
from email.message import EmailMessage
import ssl
import smtplib
import random

# Carga las variables de entorno desde el archivo .env
load_dotenv()

# Obtiene el correo y la contraseña del archivo .env
email_sender = os.getenv("CORREO")       # Dirección de correo del remitente
password = os.getenv("PASSWORD")         # Contraseña o clave de aplicación del remitente

# Lista de destinatarios (debe rellenarse con los correos reales)
email_receiver = ['']  # Lista de correos electrónicos de los destinatarios

# Genera un número aleatorio de 8 dígitos
codigo_verificacion = str(random.randint(10**7, 10**8 - 1))

# Asunto y cuerpo del mensaje de verificación
subject = 'Mensaje de verificación de correo'
body = f"""
¡Ya casi has terminado de registrarte en Espanyola Viajes!

Tu código de verificación es: {codigo_verificacion}
"""

# Crea el mensaje de correo electrónico
em = EmailMessage()
em['From'] = email_sender
em['To'] = ', '.join(email_receiver)
em['Subject'] = subject
em.set_content(body)

# Crea un contexto SSL seguro para la conexión
context = ssl.create_default_context()

# Envía el correo usando el servidor SMTP de Gmail
with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
    smtp.login(email_sender, password)  # Inicia sesión con las credenciales
    smtp.sendmail(email_sender, email_receiver, em.as_string())  # Envía el correo
