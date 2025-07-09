import base64
from cryptography.fernet import Fernet
from hashlib import sha256
import getpass
import sys
import time

def decrypt_key():
    print("Iniciando el proceso de desencriptación de tu clave privada XLM...")
    print("Asegúrate de que estás en un entorno seguro y, si es posible, DESCONECTADO de INTERNET.")

    # Solicita la clave privada encriptada al usuario
    print("\n--- PASO 1: INTRODUCE TU CLAVE ENCRIPTADA ---")
    encrypted_key_str = getpass.getpass("Pega o escribe tu CLAVE PRIVADA ENCRIPTADA (la que empieza por 'gAAAAAB'): ")
    encrypted_key_str = encrypted_key_str.strip() # Limpia posibles espacios en blanco

    if not encrypted_key_str.startswith("gAAAAAB"):
        print("\n¡Error! La clave encriptada no parece tener el formato correcto de Fernet.")
        print("Asegúrate de que copiaste la clave completa y sin errores.")
        return

    # Solicita la contraseña para desencriptar
    print("\n--- PASO 2: INTRODUCE TU CONTRASEÑA ---")
    password = getpass.getpass("Introduce la CONTRASEÑA que usaste para encriptar tu clave privada: ")

    try:
        # Recrea la clave Fernet usando el hash SHA256 de la contraseña (misma lógica que en la encriptación)
        # ADVERTENCIA: Esta derivación es SIMPLIFICADA para este script.
        # Para producción, usar un KDF (PBKDF2HMAC, Scrypt) con salt guardado.
        key_for_fernet = Fernet(base64.urlsafe_b64encode(sha256(password.encode()).digest()))

        # Intenta desencriptar la clave
        decrypted_key = key_for_fernet.decrypt(encrypted_key_str.encode()).decode()

        # Verifica que la clave desencriptada tiene el formato de Stellar (empieza por 'S' y tiene 56 caracteres)
        if not (decrypted_key.startswith("S") and len(decrypted_key) == 56):
            print("\n¡ADVERTENCIA! La clave desencriptada no tiene el formato esperado de una clave privada Stellar.")
            print("Esto podría indicar un error en la contraseña o en la clave encriptada copiada.")
            print("Continúa con precaución.")

        print("\n--- ¡DESENCRIPTACIÓN EXITOSA! ---")
        print("------------------------------------------------------------------------------------------------")
        print("                 *** TU CLAVE PRIVADA DESENCRIPTADA (¡SECRETO TOTAL!) ***")
        print("------------------------------------------------------------------------------------------------")
        print("\n", decrypted_key)
        print("\n------------------------------------------------------------------------------------------------")
        print("\n*** INSTRUCCIONES IMPORTANTES: ***")
        print("1. USA ESTA CLAVE AHORA PARA IMPORTARLA A UNA BILLETERA DE SOFTWARE O HARDWARE.")
        print("2. UNA VEZ USADA, CIERRA ESTA VENTANA INMEDIATAMENTE.")
        print("3. NUNCA GUARDES ESTA CLAVE SIN ENCRIPTAR EN TU ORDENADOR.")
        print("4. NO LA COMPARTAS CON NADIE.")
        print("5. Cuando hayas terminado de usar la clave, presiona Enter para cerrar el script.")

        input("\nPresiona ENTER para cerrar el script y borrar la clave de la memoria.")
        print("\nProceso finalizado. Cerrando...")
        time.sleep(2) # Pequeña pausa antes de salir

    except Exception as e:
        print(f"\n¡ERROR AL DESENCRIPTAR! Asegúrate de que la CLAVE ENCRIPTADA y la CONTRASEÑA son correctas.")
        print(f"Mensaje de error: {e}")
        print("Verifica cuidadosamente cada carácter.")

if __name__ == "__main__":
    decrypt_key()
