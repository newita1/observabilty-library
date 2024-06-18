from cryptography.fernet import Fernet
import sys

def encrypt_password(password, name):
    #Intentamos obtener la clave privada, si no existe, generamos una nueva
    try:
    #Obtenemos la calve de cifrado.
        with open("key.fernet", "rb") as f:
            key = f.read()
            f.close()
    #Cargamos la key para usarla de encoder.
    except:
        #Si no existe el fichero key.fernet o esta corrompido, generamos una nueva Key y sobreescribimos el file.
        key = Fernet.generate_key()
        with("key.fernet","a") as file:
            file.write(key)
            file.close()
    fernet = Fernet(key)
    #Encriptamos la password
    encrypted_password = fernet.encrypt(password.encode())
    #Guardamos la contraseña cifrada en la misma ruta de ejecucion en la carpeta passwords.
    with open(f".\passwords\{name}.fernet", 'a') as file:
        file.write(encrypted_password.decode())
        file.close()

if __name__ == "__main__":
    encrypt_password(sys.argv[1], sys.argv[2])