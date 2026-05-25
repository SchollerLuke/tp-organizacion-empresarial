import csv
from itertools import islice
import pandas as pd
import matplotlib.pyplot as plt

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
                if mes != mes_anterior:
                    meses.append(pos)
                    mes_anterior = mes
                pos+=1  
        meses.append(pos)               

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
# Definición de función que lee el archivo

def leer_archivo(desde, hasta, date=""):
    ventas=0
    try:
        with open("datos/sales_sample.csv", "r", newline="", encoding="utf-8") as dataset:
            lector = csv.DictReader(dataset)
            for fila in islice(lector, desde, hasta):
                if date == "": ventas += int(fila["sales_amount"])
                else: 
                    if fila["sales_date"] == date: 
                        ventas = fila["sales_amount"]
                        break
                         
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
# Definición de función que comprueba validez de datos ingresados
# Puede comprobar string, int o float dependiendo los argumentos ingresados

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
# Definición de función que imprime el menú de opciones

print("\nIniciando programa de análisis de ventas...")
meses = lectura_inicial()
if meses == None: print("Solucione el error detectado en el archivo y vuelva a ejecutar el programa")

while meses != None: 
    opcion = imprimir_menu()
    match opcion:

        case 1:
            print("\n"+"-"*30)
            print("Lista de Ventas por Mes".center(30))
            print("-"*30)
            for i in range(12):
                ventas = leer_archivo( meses[i], meses[i+1] )
                print(f"{nombre_meses[i]}" + "|".rjust(15-len(nombre_meses[i])) + f"{ventas}".rjust(15))
            print("-"*30)
            input("Presione enter para continuar...")

        case 2:
            while True:
                mes = str(comprobar("Ingrese el número del mes a buscar: "))
                if 1 <= int(mes) <= 12:
                    if int(mes) < 10: mes = "0"+ mes
                    break              
                else: print("Ingrese un mes válido\n")

            while True:
                dia = str(comprobar("Ingrese el día a buscar: "))
                if 1 <= int(dia) <= ( meses[int(mes)] - meses[int(mes)-1] ): 
                    if int(dia) < 10: dia = "0"+ dia
                    break
                else: print("Ingrese un día válido\n")
                
            ventas = leer_archivo(meses[int(mes)-1], meses[int(mes)], "2024-" + mes + "-" + dia)
            if ventas == 0: print(f"\nNo se ha encontrado ventas el {dia} de {nombre_meses[int(mes)-1]} del 2024")
            else: print(f"\nEl {dia} de {nombre_meses[int(mes)-1]} del 2024 se registraron {ventas} ventas")
            input("Presione enter para continuar...")

        case 3:
            ventas_totales = 0
            print("\n"+"-"*30)
            print("Lista de Promedio de Ventas".center(30))
            print("-"*30)
            print("Promedio diario por mes")
            print("-"*30)
            for i in range(12):
                ventas = leer_archivo( meses[i], meses[i+1] )
                ventas_totales += ventas
                print(f"{nombre_meses[i]}" + "|".rjust(15-len(nombre_meses[i])) + f"{( ventas / ( meses[i+1] - meses[i] ) ):.2f}".rjust(15))
            print("-"*30)
            print("Promedio diario total")
            print( f"{( ventas_totales / (meses[-1] - meses[0]) ):.2f}" )
            print("-"*30)
            print("Promedio mensual")
            print(f"{(ventas_totales / 12):.2f}")
            print("-"*30)
            print("Ventas totales")
            print(ventas_totales)
            print("-"*30)
            input("Presione enter para continuar...")

        case 4:
            ventas = []
            for i in range(12):
                ventas.append(leer_archivo( meses[i], meses[i+1] ))
            plt.figure(figsize=(12, 5))
            plt.plot(nombre_meses, ventas)
            plt.title("Ventas mensuales")
            plt.savefig("resultados/grafico_ventas.png")

        case 5: break

print("Programa de análisis de ventas finalizado.")