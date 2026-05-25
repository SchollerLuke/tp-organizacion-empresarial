import csv
from itertools import islice
import pandas as pd
import matplotlib.pyplot as plt
# Librerías importadas para lectura de archivos csv, para acortar lectura de archivos y para generar gráfico

nombre_meses = (
    "Enero",
    "Febrero",
    "Marzo",
    "Abril",
    "Mayo",
    "Junio",
    "Julio",
    "Agosto",
    "Septiembre",
    "Octubre",
    "Noviembre",
    "Diciembre"
)

def lectura_inicial():
    meses=[]
    mes_anterior=0
    pos=0
    try:
        with open("datos/sales_sample.csv", "r", newline="", encoding="utf-8") as dataset:
            lector = csv.DictReader(dataset)
            for fila in lector:
                mes = int(fila["sales_date"][5:7])
                # La variable "mes" toma el valor ej. "04" de "2024-04-01"
                if mes != mes_anterior:
                    meses.append(pos)
                    mes_anterior = mes
                pos+=1  
                # La posición suma uno en cada iteración
                # Cuando cambia el mes se agrega a la lista "meses" la posición
        meses.append(pos)           

        # Con esta función inicia el programa, sirve para conocer la existencia del archivo
        # y leer en que días empieza y termina el mes para no analizar el archivo entero luego.

    except FileNotFoundError:
        print("\nError: el archivo no existe")
    except PermissionError:
        print("\nError: otro programa puede tener abierto el archivo")
    except IndexError:
        print("\nError: índice fuera de rango, pueden faltar datos en el archivo")
    except ValueError:
        print("\nError: valor inválido en el archivo")
    except Exception as e:
            print(f"\nError inesperado: {e}")
    else: return meses

def leer_archivo(desde, hasta, date=""):
    ventas=0
    try:
        with open("datos/sales_sample.csv", "r", newline="", encoding="utf-8") as dataset:
            lector = csv.DictReader(dataset)
            for fila in islice(lector, desde, hasta):
                # El archivo se analiza solo desde que empieza hasta que termina el mes
                if date == "": ventas += int(fila["sales_amount"])
                # Si no hay día cargado entonces suma todas las ventas de los días del mes en la variable "ventas"
                else: 
                    if fila["sales_date"] == date: 
                        ventas = fila["sales_amount"]
                        break
                    # Si hay día lo busca y agrega las ventas a la variable "ventas"

        # Esta función analiza el archivo por posiciones
        # Permite contar ventas por meses o buscar las ventas de un día específico
                         
    except FileNotFoundError:
        print("\nError: el archivo no existe")
    except PermissionError:
        print("\nError: otro programa puede tener abierto el archivo")
    except IndexError:
        print("\nError: índice fuera de rango, pueden faltar datos en el archivo")
    except ValueError:
        print("\nError: valor inválido en el archivo")
    except Exception as e:
            print(f"\nError inesperado: {e}")
    else: return ventas

def comprobar(texto):
    while True:
        try:
            ingreso = int(input(texto))
            break

        except ValueError:
            print("Error: valor inválido")
        except Exception as e:
            print(f"Error inesperado: {e}")
            
    return ingreso
# Función que comprueba validez de datos ingresados

def imprimir_menu():
    print("\n" + "=" * 30)
    print("MENU PRINCIPAL".center(30))
    print("=" * 30)
    print("1) Lista de ventas mensuales")
    print("2) Buscar ventas en un dia")
    print("3) Promedio de ventas")
    print("4) Generar gráfico")
    print("5) Salir")
    print("=" * 30)
    while True:
        opcion = comprobar("Seleccione una opción: ")
        if opcion in range(1, 6): break
        else: print("Error: opción ingresada inválida")
    return opcion
# Definición de función que imprime el menú de opciones y comprueba la validez de la opción ingresada

print("\nIniciando programa de análisis de ventas...")
meses = lectura_inicial()
if meses == None: print("Solucione el error detectado en el archivo y vuelva a ejecutar el programa")
# Se realiza la lectura inicial y si el archivo no existe, lo indica y termina el programa

while meses != None: 
    opcion = imprimir_menu()
    match opcion:
        # Inicio de bucle que mantiene el programa en funcionamiento

        case 1:
            print("\n"+"-"*30)
            print("Lista de Ventas por Mes".center(30))
            print("-"*30)
            for i in range(12):
                # Bucle que muestra las ventas de todos los meses
                ventas = leer_archivo( meses[i], meses[i+1] )
                print(f"{nombre_meses[i]}" + "|".rjust(15-len(nombre_meses[i])) + f"{ventas}".rjust(15))
            print("-"*30)
            input("Presione enter para continuar...")
            # Caso 1: Realiza la lista de ventas mensuales

        case 2:
            while True:
                mes = str(comprobar("Ingrese el número del mes a buscar: "))
                if 1 <= int(mes) <= 12:
                    if int(mes) < 10: mes = "0"+ mes
                    break              
                else: print("Ingrese un mes válido\n")
                # Comprobación de mes válido

            while True:
                dia = str(comprobar("Ingrese el día a buscar: "))
                if 1 <= int(dia) <= ( meses[int(mes)] - meses[int(mes)-1] ): 
                    if int(dia) < 10: dia = "0"+ dia
                    break
                else: print("Ingrese un día válido\n")
                # Comprobación de día válido
                
            ventas = leer_archivo(meses[int(mes)-1], meses[int(mes)], "2024-" + mes + "-" + dia)
            if ventas == 0: print(f"\nNo se ha encontrado ventas el {dia} de {nombre_meses[int(mes)-1]} del 2024")
            else: print(f"\nEl {dia} de {nombre_meses[int(mes)-1]} del 2024 se registraron {ventas} ventas")
            # Muestra las ventas del día y sino indica que no hubo ventas
            input("Presione enter para continuar...")
            # Caso 2: Búsqueda de ventas de un día específico

        case 3:
            ventas_totales = 0
            print("\n"+"-"*30)
            print("Lista de Promedio de Ventas".center(30))
            print("-"*30)
            print("Promedio diario por mes")
            print("-"*30)
            for i in range(12):
                # Bucle que recorre todos los meses y toma el promedio de ventas diarios
                ventas = leer_archivo( meses[i], meses[i+1] )
                ventas_totales += ventas
                print(f"{nombre_meses[i]}" + "|".rjust(15-len(nombre_meses[i])) + f"{( ventas / ( meses[i+1] - meses[i] ) ):.2f}".rjust(15))
            print("-"*30)
            print("Promedio diario total")
            print( f"{( ventas_totales / (meses[-1] - meses[0]) ):.2f}" )
            # Se muestra el promedio diario de todo el año
            print("-"*30)
            print("Promedio mensual")
            print(f"{(ventas_totales / 12):.2f}")
            # Se muestra el promedio mensual de todo el año
            print("-"*30)
            print("Ventas totales")
            print(ventas_totales)
            # Se muestran las ventas totales en el año
            print("-"*30)
            input("Presione enter para continuar...")
            # Caso 3: Muestra promedios de ventas

        case 4:
            ventas = []
            for i in range(12):
                ventas.append(leer_archivo( meses[i], meses[i+1] ))
                # Se agregan las ventas mensuales a una lista de ventas
            plt.figure(figsize=(12, 5))
            # Se establece un tamaño óptimo para el gráfico
            plt.plot(nombre_meses, ventas)
            plt.title("Ventas mensuales")
            # Se indica título de gráfico y las listas que ocupan los ejes cartesianos
            plt.savefig("resultados/grafico_ventas.png")
            # Caso 4: Generación de gráfico de ventas

        case 5: break
        # Caso 5: Cierre del programa

print("Programa de análisis de ventas finalizado.")
