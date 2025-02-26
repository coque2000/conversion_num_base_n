import re

# "A" equivalente a 11 base 11, "B" equivalente a 12 base 12, ... "Z" equivalente a 37 base 37
PRIMER_CARACTER: int = 55
CARACTER_ENIE: int = 14

def pedir_entrada_str(mensaje: str):
    entrada: str
    return input(mensaje)

def pedir_numero_base():
    numero = ""
    base = 0
    print("Ejemplo de entrada (binario): \"10111011 2\"")
    while True:
        entrada = input("Ingresa el número que quieras convertir y su base: ")
        n_entrada = eliminar_espacios_blanco_repetidos(entrada)
        numero, base = n_entrada.split(' ')
        if not base.isnumeric():  # Comprueba si la base es un numero
            print(f"La base \"{base}\" no es válida\n")
            continue
        base_num = int(base)
        if base_num <= 1 or base_num > 36:  # Si la base se encuentra dentro de la base
            print(f"La base \"{base}\" no es válida. Solo base (2-36).\n")
            continue
        if not comprobar_numero_base(numero, int(base)):  # Comprueba si el numero pertenece a la base
            print(f"El número \"{numero}\" en base \"{base}\" no es válido\n")
        else:
            break
    return {"numero": numero, "base": int(base)}

def pedir_base_destino():
    base = 0
    while True:
        entrada = input("Ingresa base a la que quieras convertir: ")
        b_entrada = eliminar_espacios_blanco_repetidos(entrada)
        if not b_entrada.isnumeric():  # Comprueba si la base es un numero
            print(f"La base \"{b_entrada}\" no es válida\n")
            continue
        base = int(b_entrada)
        if base <= 1 or base > 36:  # Si la base se encuentra dentro de la base
            print(f"La base \"{base}\" no es válida. Solo base (2-36).\n")
            continue
        else:
            break
    return base

def eliminar_espacios_blanco_repetidos(cadena: str):
    return re.sub(r"\s+", " ", cadena)

def comprobar_numero_base(numero: str, base: int):
    if  numero is None or numero == "" or base is None:
        return False
    if numero.count(".") > 1:  # Si hay mas de un punto es un numero invalido
        return False
    numero = numero.upper()
    for caracter in numero:
        if caracter == ".":
            continue
        if caracter.isdigit():
            numero = int(caracter)
            if numero >= base:
                return False
        elif caracter.isalpha():  # Es cualquier cosa
            num_ascii = ord(caracter) - PRIMER_CARACTER
            if num_ascii >= base and num_ascii <= PRIMER_CARACTER:
                return False
        else:  # No es un numero, caracter o unico punto
            return False
    return True

def numero_equivalente_base_10(caracter: str):
    if len(caracter) > 1:
        return None
    if caracter.isdigit():
        return int(caracter)
    caracter = caracter.upper()
    if caracter.isalpha():
        if caracter == "Ñ":
            return CARACTER_ENIE + 10
        num_ascii = ord(caracter) - PRIMER_CARACTER
        if num_ascii < CARACTER_ENIE + 10:
            return num_ascii
        else:
            return num_ascii + 1
    return None

def caracter_equivalente_numero(numero: int):
    if numero < 0 or numero > 36:
        return None
    if 0 <= numero < 10:
        return str(numero)
    if numero == 24:
        return "Ñ"
    num_caracter = PRIMER_CARACTER + numero
    if numero > 24:
        num_caracter -= 1
    return chr(num_caracter)

def convertir_a_base10(numero_origen: str, base_origen: int):
    longitud_entera = 0
    if "." in numero_origen:
        parte_entera, _ = numero_origen.split(".")
        longitud_entera = len(parte_entera) - 1
    else:
        longitud_entera = len(numero_origen)
    base_pos = longitud_entera
    numero_destino = 0.0

    for caracter in numero_origen:
        if caracter == ".":
            base_pos = -1
            continue
        caracter_num = numero_equivalente_base_10(caracter)
        numero_destino += caracter_num * pow(base_origen, base_pos)
        base_pos -= 1
    return numero_destino

def convertir_base_10_a_base_n(numero_origen: float, base_destino: int, precision: int = 5):
    numero_str = str(numero_origen)
    entero = fraccion = ""
    if "." in numero_str:
        entero, fraccion = numero_str.split(".")
    else:
        entero = numero_str
        fraccion = "0"  # Se asume que la parte fraccionaria es 0 si no existe

    # Parte entera
    entero = int(entero)
    numero_entero_destino = ""
    while True:
        residuo = entero % base_destino
        entero = int(entero / base_destino)
        numero_entero_destino += caracter_equivalente_numero(residuo)  # Apendiza el residuo
        if entero < base_destino:  # El ultimo caracter ya no puede ser operado
            numero_entero_destino += caracter_equivalente_numero(entero)
            break
    numero_entero_destino = numero_entero_destino[::-1]  # Se invierten las posiciones

    # Parte fraccionaria
    numero_fracc_destino = ""
    fraccion = float("0." + fraccion)  # Se convierte a numero y agrega "0."
    i = 0
    while fraccion > 0 and i < precision:
        fraccion *= base_destino
        entero = int(fraccion)
        fraccion -= entero
        numero_fracc_destino += str(entero)
        i += 1
        if fraccion in (0.0, 1.0):  # Si se llega a 0 o 1 se detiene
            break
    if numero_fracc_destino == "":
        numero_fracc_destino = "0"
    return numero_entero_destino + "." + numero_fracc_destino

def convertir_base_n_a_base_n(numero_origen: str, base_origen: int, base_destino: int) -> str:
    if base_origen == base_destino:  # Si las bases son iguales retorna el mismo numero
        return numero_origen
    numero_b_10 = 0
    if base_origen == 10:  # Si la base origen es 10 ya no convierte a base 10
        numero_b_10 = int(numero_origen)
    else:  # Si la base es diferente a 10, lo convierte a base 10
        numero_b_10 = convertir_a_base10(numero_origen, base_origen)
    if base_destino == 10:  # Se retorna el numero sin convertir de nuevo
        return str(numero_b_10)
    else:  # Retorna el numero a la nueva base
        return convertir_base_10_a_base_n(float(numero_b_10), base_destino)



if __name__ == "__main__":

    # print(comprobarNumeroBase("123.12321", 4))
    # print(convertir_a_base10("666.66", 8))
    # print(convertir_base_10_a_base_n(4566.12, 7))

    numero_base = pedir_numero_base()
    base_destino = pedir_base_destino()
    numero_destino = convertir_base_n_a_base_n(numero_base["numero"], numero_base["base"], base_destino)
    print(f"El número:\n\"{numero_base['numero']}\" base: \"{numero_base['base']}\" -> \"{numero_destino}\" base: \"{base_destino}\" ")
