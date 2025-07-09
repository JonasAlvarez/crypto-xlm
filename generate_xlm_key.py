import os
import sys
from stellar_sdk import Keypair
from cryptography.fernet import Fernet
import getpass
import time
import base64

# Importación condicional de qrcode para impresión en terminal
try:
    import qrcode
    from qrcode.image.svg import SvgImage
    # No se usa en este caso, se imprime directamente el string
    # import qrcode.console # Para imprimir en terminal como caracteres
except ImportError:
    print("La librería 'qrcode' no está instalada o 'qrcode.console' no está disponible.")
    print("No se podrán generar los códigos QR en la terminal.")
    print("Asegúrate de que 'pip install qrcode' se ejecutó correctamente en el contenedor.")
    sys.exit(1)

def generate_and_encrypt_key():
    print("Iniciando la generación de claves XLM...")

    # Genera un par de claves aleatorio y seguro
    keypair = Keypair.random()
    public_key = keypair.public_key
    private_key = keypair.secret

    print("\n--- PASO 1: ENCRIPTACIÓN DE LA CLAVE PRIVADA ---")
    password = getpass.getpass("Introduce una contraseña robusta para encriptar tu clave privada: ")
    password_confirm = getpass.getpass("Confirma la contraseña: ")

    if password != password_confirm:
        print("\n¡Error! Las contraseñas no coinciden. Saliendo.")
        return

    # Usando Fernet con una derivación simple de clave desde el password.
    # ADVERTENCIA: Esta derivación es SIMPLIFICADA para este script EFÍMERO.
    # Para producción a largo plazo, usar un KDF (PBKDF2HMAC, Scrypt) con salt.
    try:
        # Crea una clave Fernet de 32 bytes (256 bits) usando SHA256 de la contraseña, luego Base64 urlsafe
        key_for_fernet = Fernet(base64.urlsafe_b64encode(sha256(password.encode()).digest()))
        encrypted_private_key = key_for_fernet.encrypt(private_key.encode()).decode()
    except Exception as e:
        print(f"Error al encriptar: {e}")
        print("Asegúrate de que la contraseña sea lo suficientemente larga y compleja.")
        return

    print("\n--- PASO 2: GENERACIÓN DE CÓDIGOS QR Y DATOS (COPIA ESTO EN PAPEL) ---")
    print("------------------------------------------------------------------------------------------------")
    print("                 *** WALLET XLM ENCRIPTADA PARA ALMACENAMIENTO EN FRÍO ***")
    print("------------------------------------------------------------------------------------------------")

    print("\n--- CÓDIGO QR DE TU CLAVE PÚBLICA (PUBLIC KEY / DIRECCIÓN XLM): ---")
    print("Puedes escanear este QR para enviar XLM a tu wallet.\n")
    qr_public = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=1, # Tamaño de los bloques para que quepa en terminal
        border=1,   # Borde pequeño
    )
    qr_public.add_data(public_key)
    qr_public.make(fit=True)
    qr_public.print_ascii(out=sys.stdout, tty=True, invert=True) # Imprime con caracteres ASCII

    print(f"\nTU CLAVE PÚBLICA (TEXTO CLARO): {public_key}")
    print("------------------------------------------------------------------------------------------------")

    print("\n--- CÓDIGO QR DE TU CLAVE PRIVADA ENCRIPTADA (SECRET KEY - ¡SÚPER SECRETA!): ---")
    print("NECESITARÁS LA CONTRASEÑA QUE PUSISTE PARA DESENCRIPTARLA.\n")
    qr_private_encrypted = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=1,
        border=1,
    )
    qr_private_encrypted.add_data(encrypted_private_key)
    qr_private_encrypted.make(fit=True)
    qr_private_encrypted.print_ascii(out=sys.stdout, tty=True, invert=True) # Imprime con caracteres ASCII

    print(f"\nTU CLAVE PRIVADA ENCRIPTADA (TEXTO CLARO): {encrypted_private_key}")
    print("\n------------------------------------------------------------------------------------------------")

    print("\n*** INSTRUCCIONES IMPORTANTES: ***")
    print("1. IMPRIME O COPIA AMBOS CÓDIGOS QR Y SUS TEXTOS EN UN PAPEL AHORA MISMO.")
    print("2. ASEGÚRATE DE COPIAR LA CONTRASEÑA EN UN LUGAR SEGURO Y SEPARADO DE ESTE PAPEL.")
    print("3. VERIFICA LA COPIA/IMPRESIÓN VARIAS VECES. Escanea los QR para confirmarlos.")
    print("4. NO PIERDAS LA CONTRASEÑA O LA CLAVE ENCRIPTADA. AMBAS SON NECESARIAS PARA RECUPERAR LOS XLM.")
    print("5. Cuando hayas terminado de imprimir y verificar, presiona Enter para destruir el contenedor.")

    input("\nPresiona ENTER para continuar y finalizar el proceso (esto borrará toda la información).")
    print("\nProceso finalizado. El contenedor se cerrará y se borrará.")
    time.sleep(2) # Pequeña pausa antes de salir para asegurar que el usuario vea el mensaje

if __name__ == "__main__":
    from hashlib import sha256 # Importa aquí para asegurar que solo se use si se ejecuta el script
    generate_and_encrypt_key()
