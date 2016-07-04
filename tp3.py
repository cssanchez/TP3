import grafo
import sys
import heapq


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
		grafo_wiki = grafo.Grafo(True)
		archivo.readline()
		for n in range (CANTIDAD_ARTICULOS):
			linea = archivo.readline()
			header, resto = linea.split('>')
			grafo_wiki[header] = None
		archivo.seek(0)
		archivo.readline()
		for n in range (CANTIDAD_ARTICULOS):
			linea = archivo.readline()
			header, resto = linea.split('>')
			lista_links = resto.split('<')
			for link in lista_links:
				if link in grafo_wiki:
					grafo_wiki.agregar_arista(header, link)
		archivo.close()
		return grafo_wiki
	except FileNotFoundError:
		raise


def calcular_pagerank(grafo_wiki, cant_articulos, k): 
	d = 0.85
	dic_pr = {}
	for v in grafo_wiki:
		dic_pr[v] = (1-d)/cant_articulos
	for i in range(k):
		dic_aux = {}
		for v in grafo_wiki:
			dic_aux[v] = (1-d)/cant_articulos
		for v in grafo_wiki:
			for ady in grafo_wiki.adyacentes(v):
				dic_aux[ady] += ((d * dic_pr[v]) / len(grafo_wiki.adyacentes(v)))
		dic_pr = dic_aux
	return dic_pr


def mostrar_pagerank(dic_pr, articulo):
	return dic_pr[articulo]


def aux_mostrar_top_k_diccionarios(dic, k):
	q = []
	heap = heapq
	cont = k
	for v in dic:
		if k > 0:
			heap.heappush(q, (dic[v], v))
			k -= 1
			continue
		if dic[v] > q[0][0]:
			heap.heappop(q)
			heap.heappush(q, (dic[v], v))
	lista_top = []
	while len(q) > 0:
		lista_top.append(heap.heappop(q))
	return lista_top


def mostrar_top_pagerank (dic_pr, k):
	lista_top = aux_mostrar_top_k_diccionarios(dic_pr, k)
	for i in range(1, len(lista_top)+1):
		mayor = lista_top.pop()
		print("%i.%s: %f" % (i, mayor[1], mayor[0]))


def camino_mas_corto(grafo_wiki, articulo1, articulo2):
	camino = grafo_wiki.camino_minimo(articulo1, articulo2)
	if camino == None : 
		print ("No hay camino")
		return
	print(" -> ".join(camino))


def centralidad(grafo_wiki, k): 
	dic_cent = {}
	for v in grafo_wiki:
		dic_cent[v] = 0
	for v in grafo_wiki:
		for w in grafo_wiki:
			camino = grafo_wiki.camino_minimo(v, w)
			if camino == None: continue
			for x in camino: dic_cent[x] += 1
	lista_top = aux_mostrar_top_k_diccionarios(dic_cent, k)
	for i in range(1, len(lista_top)+1):
		mayor = lista_top.pop()
		print("%i.%s: %i" % (i, mayor[1], mayor[0]))


def diametro(grafo_wiki):
	res_diam = [0,[]]
	for v in grafo_wiki:
		for w in grafo_wiki:
			camino = grafo_wiki.camino_minimo(v, w)
			if camino == None: continue
			if len(camino) > res_diam[0]:
				res_diam[0] = len(camino)
				res_diam[1] = camino
	print("Diametro: %i" % res_diam[0])
	print("Camino:"," -> ".join(res_diam[1]))


def distancias(grafo_wiki, articulo):
 	'''Todos los vertices a las distintas distancias. Esta operación debe realizarse en O(V + E).'''
 	dic_dist = {}
 	(padre, orden) = grafo_wiki.bfs(inicio = articulo)
 	for k in orden:
 		if not orden[k] in dic_dist:
 			dic_dist[orden[k]] = [k]
 		else:
 			dic_dist[orden[k]].append(k)
 	dic_dist.pop(0)
 	for i in range(1, len(dic_dist)+1):
 		lista_links = dic_dist.pop(i)
 		print("    Distancia %i: %s" % (i, ", ".join(lista_links)))


def main(argv):
	NOMBRE_ARCHIVO, CANTIDAD_ARTICULOS = validar_entrada(argv)
	grafo_wiki = cargar_grafo(NOMBRE_ARCHIVO, CANTIDAD_ARTICULOS)

	comandos = {"calcular_pagerank": 0, "mostrar_top_pagerank": 1, "mostrar_pagerank": 2, 
	"camino_mas_corto": 3, "centralidad": 4, "diametro": 5, "distancias": 6}
	ingreso = input("Ingrese un comando: ").split(' ')
	while ingreso[0] != 'exit':
		try:
			if not ingreso[0] in comandos:
				print("No es un comando valido.")
			if len(ingreso) != 2 and comandos[ingreso[0]] != 5:
				print("El numero de valores no es valido para el comando requerido.")
			elif comandos[ingreso[0]] == 0:
				dic_pr = calcular_pagerank(grafo_wiki, CANTIDAD_ARTICULOS, int(ingreso[1]))
			elif comandos[ingreso[0]] == 1:
				mostrar_top_pagerank(dic_pr, int(ingreso[1]))
			elif comandos[ingreso[0]] == 2:
				print(mostrar_pagerank(dic_pr, ingreso[1]))
			elif comandos[ingreso[0]] == 3:
				articulos = ingreso[1].split(',')
				camino_mas_corto(grafo_wiki, articulos[0], articulos[1])
			elif comandos[ingreso[0]] == 4:
				centralidad(grafo_wiki, int(ingreso[1]))
			elif comandos[ingreso[0]] == 5:
				diametro(grafo_wiki)
			elif comandos[ingreso[0]] == 6:
				distancias(grafo_wiki, ingreso[1])
		except ValueError:
			print("El valor ingresado no es valido para el comando requerido.")
		ingreso = input("Ingrese un comando: ").split(' ')
	return
main(sys.argv)