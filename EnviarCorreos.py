import os
import smtplib
from email.message import EmailMessage

REMITENTE = "proyectostec736@gmail.com"
CONTRASENA_APLICACION = "tzbu fvsx erxh kzsp"
#DESTINATARIO = "angiecolochos@gmail.com"
SERVIDOR_SMTP = "smtp.gmail.com"
PUERTO_SMTP = 587


def validar_archivo(ruta_pdf):
    return os.path.exists(ruta_pdf)


def crearMensaje(remitente, destinatario, asunto, cuerpo):
    mensaje = EmailMessage()
    mensaje["From"] = remitente
    mensaje["To"] = destinatario
    mensaje["Subject"] = asunto
    mensaje.set_content(cuerpo)
    return mensaje


def adjuntarPdf(mensaje, ruta_pdf):
    with open(ruta_pdf, "rb") as archivo:
        mensaje.add_attachment(
            archivo.read(),
            maintype="application",
            subtype="pdf",
            filename=os.path.basename(ruta_pdf)
        )


def enviarMensajeSMTP(mensaje, remitente, contrasena):
    with smtplib.SMTP(SERVIDOR_SMTP, PUERTO_SMTP) as servidor:
        servidor.starttls()
        servidor.login(remitente, contrasena)
        servidor.send_message(mensaje)


def enviarReporteCorreo(ruta_pdf, destinatario):
    if not validar_archivo(ruta_pdf):
        print(f"Error: no se encontró el archivo '{ruta_pdf}'.")
        return False

    asunto = "Reporte generado por el sistema"
    cuerpo = (
        "Estimado/a usuario/a,\n\n"
        "Se ha generado correctamente el reporte solicitado en el sistema ATI Logística Aduanera.\n\n"
        "En el archivo adjunto encontrará el reporte de productos ordenados por costo total "
        "según el país seleccionado, incluyendo la información de precios e impuestos "
        "correspondientes.\n\n"
        "Este documento ha sido generado automáticamente por el sistema para facilitar "
        "la consulta y análisis de los datos registrados.\n\n"
        "Saludos cordiales,\n\n"
        "Sistema ATI Logística Aduanera"
    )

    try:
        mensaje = crearMensaje(REMITENTE, destinatario, asunto, cuerpo)
        adjuntarPdf(mensaje, ruta_pdf)
        enviarMensajeSMTP(mensaje, REMITENTE, CONTRASENA_APLICACION)

        print(f"Correo enviado correctamente a {destinatario}.")
        return True

    except Exception as e:
        print(f"Ocurrió un error al enviar el correo: {e}")
        return False


if __name__ == "__main__":
    enviarReporteCorreo("reporte_ATI_logistica.pdf", "angiecolochos@gmail.com")