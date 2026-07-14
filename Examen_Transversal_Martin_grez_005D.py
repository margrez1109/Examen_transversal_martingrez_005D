def buscar_codigo(codigo, cartelera):
    """
    Recorre el diccionario y retorna True si el código existe,
    o False si no existe (no distingue mayúsculas/minúsculas).
    """
    return codigo.upper() in [k.upper() for k in cartelera.keys()]



def validar_codigo(codigo, cartelera):
    if not codigo.strip():
        return False
    
    if buscar_codigo(codigo, cartelera):
        return False
    return True

def validar_titulo(titulo):
    return bool(titulo.strip())

def validar_genero(genero):
    return bool(genero.strip())

def validar_duracion(duracion_str):
    try:
        duracion = int(duracion_str)
        return duracion > 0
    except ValueError:
        return False

def validar_clasificacion(clasificacion):
    return clasificacion in ['A', 'B', 'C']

def validar_idioma(idioma):
    return bool(idioma.strip())

def validar_es_3d(es_3d_str):
    return es_3d_str.lower() in ['s', 'n']

def validar_precio(precio_str):
    try:
        precio = int(precio_str)
        return precio > 0
    except ValueError:
        return False

def validar_cupos(cupos_str):
    try:
        cupos = int(cupos_str)
        return cupos >= 0
    except ValueError:
        return False




def leer_opcion():
    """
    Solicita una opción, valida que sea entero entre 1 y 6.
    Maneja excepciones en caso de ingresos no enteros.
    """
    while True:
        try:
            opcion = int(input("Ingrese opción: "))
            if 1 <= opcion <= 6:
                return opcion
            else:
                print("Debe seleccionar una opción válida")
        except ValueError:
            print("Debe seleccionar una opción válida")


def cupos_genero(genero, peliculas, cartelera):
    """
    Suma y muestra el total de cupos para un género específico.
    La búsqueda no distingue mayúsculas/minúsculas.
    """
    total_cupos = 0
    genero_busqueda = genero.lower().strip()
    
    for cod_pelicula, datos in peliculas.items():
        genero_pelicula = datos[1].lower()  # El género está en el índice 1
        if genero_pelicula == genero_busqueda:
            
            if cod_pelicula in cartelera:
                total_cupos += cartelera[cod_pelicula][1]
                
    print(f"El total de cupos disponibles es: {total_cupos}")


def busqueda_precio(p_min, p_max, peliculas, cartelera):
    """
    Busca películas dentro de un rango de precio y con cupos disponibles.
    Muestra los resultados ordenados alfabéticamente por título.
    """
    resultados = []
    for cod_pelicula, datos_cartelera in cartelera.items():
        precio = datos_cartelera[0]
        cupos = datos_cartelera[1]
        
        if p_min <= precio <= p_max and cupos > 0:
           
            if cod_pelicula in peliculas:
                titulo = peliculas[cod_pelicula][0]
                resultados.append(f"{titulo}--{cod_pelicula}")
    
    if resultados:
        
        resultados.sort()
        print(f"Las películas encontradas son: {resultados}")
    else:
        print("No hay películas en ese rango de precios.")


def actualizar_precio(codigo, nuevo_precio, cartelera):
    """
    Verifica existencia y actualiza el precio en el diccionario cartelera.
    """
    codigo_up = codigo.upper()
    if buscar_codigo(codigo_up, cartelera):
        
        for k in cartelera.keys():
            if k.upper() == codigo_up:
                cartelera[k][0] = nuevo_precio
                return True
    return False


def agregar_pelicula(codigo, titulo, genero, duracion, clasificacion, idioma, es_3d, precio, cupos, peliculas, cartelera):
    """
    Agrega la nueva película a ambos diccionarios tras confirmar que el código no exista.
    """
    codigo_up = codigo.upper()
    if buscar_codigo(codigo_up, cartelera):
        return False
    
    
    es_3d_bool = True if es_3d.lower() == 's' else False
    
    
    peliculas[codigo_up] = [titulo, genero, int(duracion), clasificacion, idioma, es_3d_bool]
    
    cartelera[codigo_up] = [int(precio), int(cupos)]
    return True


def eliminar_pelicula(codigo, peliculas, cartelera):
    """
    Elimina los registros asociados al código en ambos diccionarios.
    """
    codigo_up = codigo.upper()
    if buscar_codigo(codigo_up, cartelera):
        
        clave_p = next((k for k in peliculas.keys() if k.upper() == codigo_up), None)
        clave_c = next((k for k in cartelera.keys() if k.upper() == codigo_up), None)
        
        if clave_p:
            del peliculas[clave_p]
        if clave_c:
            del cartelera[clave_c]
        return True
    return False




def main():

    peliculas = {
        'P101': ['Luz de Otoño', 'drama', 110, 'B', 'Español', False],
        'P102': ['Noche Neón', 'acción', 125, 'C', 'Ingles', True],
        'P103': ['Planeta Agua', 'documental', 90, 'A', 'Español', False],
        'P104': ['Risa Total', 'comedia', 105, 'A', 'Español', True],
        'P105': ['Código Zero', 'thriller', 118, 'C', 'Ingles', True],
        'P106': ['Viaje Lunar', 'ciencia ficción', 132, 'B', 'Ingles', False]
    }

    cartelera = {
        'P101': [5990, 40],
        'P102': [7990, 0],
        'P103': [4990, 25],
        'P104': [6990, 12],
        'P105': [8990, 8],
        'P106': [7490, 3]
    }

    while True:
        print("\n========== MENÚ PRINCIPAL ==========")
        print("1. Cupos por género")
        print("2. Búsqueda de películas por rango de precio")
        print("3. Actualizar precio de película")
        print("4. Agregar película")
        print("5. Eliminar película")
        print("6. Salir")
        print("=====================================")
        
        opcion = leer_opcion()
        
        
        if opcion == 1:
            genero = input("Ingrese género a consultar: ")
            cupos_genero(genero, peliculas, cartelera)
            
        
        elif opcion == 2:
            while True:
                try:
                    p_min_str = input("Ingrese precio mínimo: ")
                    p_min = int(p_min_str)
                    p_max_str = input("Ingrese precio máximo: ")
                    p_max = int(p_max_str)
                    
                    if p_min >= 0 and p_max >= 0 and p_min <= p_max:
                        busqueda_precio(p_min, p_max, peliculas, cartelera)
                        break
                    else:
                        print("Debe ingresar valores enteros válidos (mínimo menor o igual al máximo y mayores a cero).")
                except ValueError:
                    print("Debe ingresar valores enteros")
                    
        
        elif opcion == 3:
            procesando = True
            while procesando:
                codigo = input("Ingrese código de película: ")
                nuevo_precio_str = input("Ingrese nuevo precio: ")
                
                
                if nuevo_precio_str.isdigit() and int(nuevo_precio_str) > 0:
                    nuevo_precio = int(nuevo_precio_str)
                    
                    
                    exito = actualizar_precio(codigo, nuevo_precio, cartelera)
                    if exito:
                        print("Precio actualizado")
                    else:
                        print("El código no existe")
                else:
                    print("El precio debe ser un valor entero positivo.")
                
                
                while True:
                    continuar = input("¿Desea actualizar otro precio (s/n)?: ").lower().strip()
                    if continuar == 's':
                        break
                    elif continuar == 'n':
                        procesando = False
                        break
                        
        
        elif opcion == 4:
            codigo = input("Ingrese código de película: ")
            titulo = input("Ingrese título: ")
            genero = input("Ingrese género: ")
            duracion = input("Ingrese duración (minutos): ")
            clasificacion = input("Ingrese clasificación: ")
            idioma = input("Ingrese idioma: ")
            es_3d = input("¿Es 3D? (s/n): ")
            precio = input("Ingrese precio: ")
            cupos = input("Ingrese cupos: ")
            
            
            if not validar_codigo(codigo, cartelera):
                print("Error: Código inválido o ya registrado.")
            elif not validar_titulo(titulo):
                print("Error: El título no puede estar vacío.")
            elif not validar_genero(genero):
                print("Error: El género no puede estar vacío.")
            elif not validar_duracion(duracion):
                print("Error: La duración debe ser un número entero mayor que cero.")
            elif not validar_clasificacion(clasificacion):
                print("Error: La clasificación debe ser exactamente 'A', 'B' o 'C'.")
            elif not validar_idioma(idioma):
                print("Error: El idioma no puede estar vacío.")
            elif not validar_es_3d(es_3d):
                print("Error: En '¿Es 3D?' debe ingresar exactamente 's' o 'n'.")
            elif not validar_precio(precio):
                print("Error: El precio debe ser un número entero mayor que cero.")
            elif not validar_cupos(cupos):
                print("Error: Los cupos deben ser un número entero mayor o igual a cero.")
            else:
                
                agregado = agregar_pelicula(codigo, titulo, genero, duracion, clasificacion, idioma, es_3d, precio, cupos, peliculas, cartelera)
                if agregado:
                    print("Película agregada")
                else:
                    print("El código ya existe")
                    
        
        elif opcion == 5:
            codigo = input("Ingrese código de película: ")
            eliminado = eliminar_pelicula(codigo, peliculas, cartelera)
            if eliminado:
                print("Película eliminada")
            else:
                print("El código no existe")
                
        
        elif opcion == 6:
            print("Programa finalizado.")
            break

if __name__ == "__main__":
    main()