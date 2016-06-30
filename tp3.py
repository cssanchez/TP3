import grafo
import sys


def validar_entrada(argv):
	if len(argv) != 3:
		raise ValueError("La cantidad de elementos es incorrecta.")
	try:
		int(argv[2])
	except ValueError:
		raise TypeError("El argumento 2 debe ser un entero")
	return argv[1], int(argv[2])


def cargar_grafo(NOMBRE_ARCHIVO, CANTIDAD_ARTICULOS):
	try:
		archivo = open(NOMBRE_ARCHIVO, 'r')
		grafo_wiki = grafo.Grafo()
		archivo.readline()                        #Para saltearnos el primero, que no sirve
		for n in range (CANTIDAD_ARTICULOS):
			linea = archivo.readline()
			header, resto = linea.split('>')
			grafo_wiki[header] = None             #No se me ocurre algo util para poner de 'valor'
		archivo.seek(0)                           #Reinicio el buffer de readline al principio del archivo
		archivo.readline()
		for n in range (CANTIDAD_ARTICULOS):
			linea = archivo.readline()
			header, resto = linea.split('>')
			lista_links = resto.split('<')
			for link in lista_links:
				if link in grafo_wiki:
					grafo_wiki.agregar_arista(header, link)
		archivo.close()

		#pruebas:
		#print (grafo_wiki.grafo)                 
		#print (len(grafo_wiki.componentes_conexas()))

		return grafo_wiki
	except FileNotFoundError:
		raise


def camino_mas_corto(grafo_wiki, articulo1, articulo2):
	print(" -> ".join(grafo_wiki.camino_minimo(articulo1, articulo2)))


def main(argv):
	NOMBRE_ARCHIVO, CANTIDAD_ARTICULOS = validar_entrada(argv)
	grafo_wiki = cargar_grafo(NOMBRE_ARCHIVO, CANTIDAD_ARTICULOS)
	camino_mas_corto(grafo_wiki, "Club Atlético Independiente", "Pirineos")  #Prueba
main(sys.argv)