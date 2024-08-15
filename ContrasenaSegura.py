import customtkinter as ctk
import random
import string
import unicodedata


def limpiar_acentos(frase):
    # Normalizar la frase para separar los acentos de las letras
    nfkd_form = unicodedata.normalize('NFKD', frase)
    return ''.join([c for c in nfkd_form if not unicodedata.combining(c)])


def transformar_caracter(caracter):
    vocales = {'a': '@', 'e': '3', 'i': '1', 'o': '0', 'u': 'u'}
    if caracter.lower() in vocales:
        return vocales[caracter.lower()].upper() if random.choice([True, False]) else vocales[caracter.lower()]
    elif caracter.isalpha():
        # Alternar aleatoriamente entre mayúsculas y minúsculas
        return caracter.upper() if random.choice([True, False]) else caracter.lower()
    elif caracter == ' ':
        return '-'
    return caracter


def verificar_contrasena(contrasena):
    # Verificar que hay al menos una mayúscula y una minúscula
    tiene_mayuscula = any(c.isupper() for c in contrasena if c.isalpha())
    tiene_minuscula = any(c.islower() for c in contrasena if c.isalpha())
    return tiene_mayuscula and tiene_minuscula


def generar_contrasenas(frase):
    simbolos = "!@#$%^&*"
    numeros = "0123456789"

    while True:
        # Transformar la frase
        frase_transformada = ''.join(transformar_caracter(c) for c in frase)
        # Añadir un símbolo al inicio y al final
        frase_transformada = random.choice(simbolos) + frase_transformada + random.choice(simbolos)

        # Asegurarnos de que la contraseña tenga al menos 12 caracteres
        while len(frase_transformada) < 12:
            frase_transformada += random.choice(simbolos + numeros)

        # Asegurarnos de que la contraseña tenga al menos una letra mayúscula y una minúscula
        if not any(c.isupper() for c in frase_transformada):
            frase_transformada += random.choice(string.ascii_uppercase)
        if not any(c.islower() for c in frase_transformada):
            frase_transformada += random.choice(string.ascii_lowercase)

        if verificar_contrasena(frase_transformada):
            return frase_transformada


def generar(event=None):
    frase = limpiar_acentos(entrada.get())
    contrasenas = [generar_contrasenas(frase) for _ in range(4)]
    # Actualizar cada campo de contraseña con las contraseñas generadas
    for i in range(4):
        entradas_resultado[i].delete(0, ctk.END)  # Limpiar el campo anterior
        entradas_resultado[i].insert(0, contrasenas[i])  # Insertar nueva contraseña


def limpiar():
    entrada.delete(0, ctk.END)
    for i in range(4):
        entradas_resultado[i].delete(0, ctk.END)  # Limpiar el campo de contraseña


def copiar_al_portapapeles(indice):
    root.clipboard_clear()
    root.clipboard_append(entradas_resultado[indice].get())


# Configuración de la ventana
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.geometry("500x500")
root.title("Generador de Contraseñas")

titulo_principal = ctk.CTkLabel(root, text="Generador de Contraseñas", font=("Arial", 20, "bold"))

etiqueta = ctk.CTkLabel(root, text="Ingresa una frase:", font=("Arial", 16))
entrada = ctk.CTkEntry(root, width=400)

frame_botones = ctk.CTkFrame(root)
boton_generar = ctk.CTkButton(frame_botones, text="Generar Contraseñas", command=generar)
boton_limpiar = ctk.CTkButton(frame_botones, text="Limpiar", command=limpiar)

titulo_contrasenas = ctk.CTkLabel(root, text="Contraseñas sugeridas:", font=("Arial", 16))

frames_resultado = [ctk.CTkFrame(root) for _ in range(4)]
entradas_resultado = [ctk.CTkEntry(frames_resultado[i], width=300) for i in range(4)]
botones_copiar = [ctk.CTkButton(frames_resultado[i], text="Copiar", command=lambda i=i: copiar_al_portapapeles(i)) for i
                  in range(4)]

titulo_principal.pack(pady=20)
etiqueta.pack(pady=10, padx=20)
entrada.pack(pady=10, padx=20)
frame_botones.pack(pady=10, padx=20)
boton_generar.pack(side=ctk.LEFT, padx=5)
boton_limpiar.pack(side=ctk.LEFT, padx=5)
titulo_contrasenas.pack(pady=20, padx=20)
for i in range(4):
    entradas_resultado[i].pack(side=ctk.LEFT, padx=5, pady=5)
    botones_copiar[i].pack(side=ctk.LEFT, padx=5, pady=5)
    frames_resultado[i].pack(pady=5, padx=20)

root.bind('<Return>', generar)

root.mainloop()
