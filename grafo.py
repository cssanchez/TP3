visitar_nulo = lambda a,b,c,d: True
heuristica_nula = lambda actual,destino: 0
import heapq

class Grafo(object):
    '''Clase que representa un grafo. El grafo puede ser dirigido, o no, y puede no indicarsele peso a las aristas
    (se comportara como peso = 1). Implementado como "diccionario de diccionarios"'''

    
    def __init__(self, es_dirigido = False):
        '''Crea el grafo. El parametro 'es_dirigido' indica si sera dirigido, o no.'''
        self.es_dirigido = es_dirigido
        self.grafo = {}


    def __len__(self):
        '''Devuelve la cantidad de vertices del grafo'''
        return len(self.grafo)


    def __iter__(self):
        '''Devuelve un iterador de vertices, sin ningun tipo de relacion entre los consecutivos'''
        return iter(self.grafo)


    def keys(self):
        '''Devuelve una lista de identificadores de vertices. Iterar sobre ellos es equivalente a iterar sobre el grafo.'''
        return list(self.grafo)


    def __getitem__(self, id):
        '''Devuelve el valor del vertice asociado, del identificador indicado. Si no existe el identificador en el grafo, lanzara KeyError.'''
        try:
            return self.grafo[id]["value"]
        except ValueError:
            raise


    def __setitem__(self, id, valor):
        '''Agrega un nuevo vertice con el par <id, valor> indicado. ID debe ser de identificador unico del vertice.
        En caso que el identificador ya se encuentre asociado a un vertice, se actualizara el valor.
        '''
        if id not in self.grafo:
            self.grafo[id] = {"value": valor}
        else:
            self.grafo[id]["value"] = valor


    def __delitem__(self, id):
        '''Elimina el vertice del grafo, y devuelve el valor asociado. Si no existe el identificador en el grafo, lanzara KeyError.
        Borra tambien todas las aristas que salian y entraban al vertice en cuestion.
        '''
        try:
            d = self.grafo.pop(id)
            for k in self.grafo:
                try:
                    self.grafo[k].pop(id)
                except KeyError:
                    pass
            return d["value"]
        except KeyError:
            raise


    def __contains__(self, id):
        ''' Determina si el grafo contiene un vertice con el identificador indicado.'''
        return id in self.grafo


    def agregar_arista(self, desde, hasta, peso = 1):
        '''Agrega una arista que conecta los vertices indicados. Parametros:
            - desde y hasta: identificadores de vertices dentro del grafo. Si alguno de estos no existe dentro del grafo, lanzara KeyError.
            - Peso: valor de peso que toma la conexion. Si no se indica, valdra 1.
            Si el grafo es no-dirigido, tambien agregara la arista reciproca.
        '''
        if not desde in self.grafo or not hasta in self.grafo:
            raise KeyError()
        self.grafo[desde][hasta] = peso
        if not self.es_dirigido:
            self.grafo[hasta][desde] = peso


    def borrar_arista(self, desde, hasta):
        '''Borra una arista que conecta los vertices indicados. Parametros:
            - desde y hasta: identificadores de vertices dentro del grafo. Si alguno de estos no existe dentro del grafo, lanzara KeyError.
           En caso de no existir la arista, se lanzara ValueError.
        '''
        if not desde in self.grafo or not hasta in self.grafo:
            raise KeyError()
        try:
            del self.grafo[desde][hasta]
            if not self.es_dirigido:
                del self.grafo[hasta][desde]
        except KeyError:
            raise ValueError()


    def obtener_peso_arista(self, desde, hasta):
        '''Obtiene el peso de la arista que va desde el vertice 'desde', hasta el vertice 'hasta'. Parametros:
            - desde y hasta: identificadores de vertices dentro del grafo. Si alguno de estos no existe dentro del grafo, lanzara KeyError.
            En caso de no existir la union consultada, se devuelve None.
        '''
        if not desde in self.grafo or not hasta in self.grafo:
            raise KeyError()
        if not hasta in self.grafo[desde]:
            return None
        else:
            return self.grafo[desde][hasta]


    def adyacentes(self, id):
        '''Devuelve una lista con los vertices (identificadores) adyacentes al indicado. Si no existe el vertice, se lanzara KeyError'''
        try: 
            lista = list(self.grafo[id])
            lista.remove("value")
            return lista
        except KeyError:
            raise


    def bfs(self, visitar = visitar_nulo, extra = None, inicio=None):
        '''Realiza un recorrido BFS dentro del grafo, aplicando la funcion pasada por parametro en cada vertice visitado.
        Parametros:
            - visitar: una funcion cuya firma sea del tipo: 
                    visitar(v, padre, orden, extra) -> Boolean
                    Donde 'v' es el identificador del vertice actual, 
                    'padre' el diccionario de padres actualizado hasta el momento,
                    'orden' el diccionario de ordenes del recorrido actualizado hasta el momento, y 
                    'extra' un parametro extra que puede utilizar la funcion (cualquier elemento adicional que pueda servirle a la funcion a aplicar). 
                    La funcion aplicar devuelve True si se quiere continuar iterando, False en caso contrario.
            - extra: el parametro extra que se le pasara a la funcion 'visitar'
            - inicio: identificador del vertice que se usa como inicio. Si se indica un vertice, el recorrido se comenzara en dicho vertice, 
            y solo se seguira hasta donde se pueda (no se seguira con los vertices que falten visitar)
        Salida:
            Tupla (padre, orden), donde :
                - 'padre' es un diccionario que indica para un identificador, cual es el identificador del vertice padre en el recorrido BFS (None si es el inicio)
                - 'orden' es un diccionario que indica para un identificador, cual es su orden en el recorrido BFS
        '''
        visitados = []
        padre = {}
        orden = {}
        cola = []

        salida = []

        cola.append(inicio)
        visitados.append(inicio)
        padre[inicio] = None
        orden[inicio] = 0
        while len(cola) != 0:
            v = cola.pop(0)
            print(v)
            visitar(v, padre, orden, extra)
            for w in self.adyacentes(v):
                if w not in visitados:
                    visitados.append(w)
                    padre[w] = v
                    orden[w] = orden[v] + 1
                    cola.append(w)
            salida.append(v)        
        return (padre,orden,salida)


    def dfs(self, visitar = visitar_nulo, extra = None, inicio=None):
        '''Realiza un recorrido DFS dentro del grafo, aplicando la funcion pasada por parametro en cada vertice visitado.
        - visitar: una funcion cuya firma sea del tipo: 
                    visitar(v, padre, orden, extra) -> Boolean
                    Donde 'v' es el identificador del vertice actual, 
                    'padre' el diccionario de padres actualizado hasta el momento,
                    'orden' el diccionario de ordenes del recorrido actualizado hasta el momento, y 
                    'extra' un parametro extra que puede utilizar la funcion (cualquier elemento adicional que pueda servirle a la funcion a aplicar). 
                    La funcion aplicar devuelve True si se quiere continuar iterando, False en caso contrario.
            - extra: el parametro extra que se le pasara a la funcion 'visitar'
            - inicio: identificador del vertice que se usa como inicio. Si se indica un vertice, el recorrido se comenzara en dicho vertice, 
            y solo se seguira hasta donde se pueda (no se seguira con los vertices que falten visitar)
        Salida:
            Tupla (padre, orden), donde :
                - 'padre' es un diccionario que indica para un identificador, cual es el identificador del vertice padre en el recorrido DFS (None si es el inicio)
                - 'orden' es un diccionario que indica para un identificador, cual es su orden en el recorrido DFS
        '''
        visitados = []
        padre = {}
        orden = {}
        pila = []
        salida = []
        pila.append(inicio)
        visitados.append(inicio)
        padre[inicio] = None
        orden[inicio] = 0
        while len(pila) != 0:
            v = pila.pop()
            print(v)
            visitar(v, padre, orden, extra)
            for w in self.adyacentes(v):
                if w not in visitados:
                    visitados.append(w)
                    padre[w] = v
                    orden[w] = orden[v] + 1
                    pila.append(w)
            salida.append(v)
        return (padre,orden, salida)    

    def componentes_conexas(self):
        '''Devuelve una lista de listas con componentes conexas. Cada componente conexa es representada con una lista, con los identificadores de sus vertices.
        Solamente tiene sentido de aplicar en grafos no dirigidos, por lo que
        en caso de aplicarse a un grafo dirigido se lanzara TypeError'''
        if self.es_dirigido: raise TypeError()
        lista_conjuntos = []
        lista_conexas = []
        for k in self.grafo:
            conjunto = set(self.adyacentes(k))
            conjunto.add(k)
            disjunto = True
            for c in lista_conjuntos:
                if conjunto.issuperset(c) or len(conjunto.intersection(c)) > 0:
                    disjunto = False
                    lista_conexas.remove(list(c))
                    c.update(conjunto)
                    lista_conexas.append(list(c))
                    break
                elif conjunto.issubset(c):
                    disjunto = False
                    break
                else:
                    disjunto = True
            if disjunto == True: 
                lista_conjuntos.append(conjunto)
                lista_conexas.append(list(conjunto))
        return lista_conexas

        
    def camino_minimo(self, origen, destino, heuristica=heuristica_nula):
        '''Devuelve el recorrido minimo desde el origen hasta el destino, aplicando el algoritmo de Dijkstra, o bien
        A* en caso que la heuristica no sea nula. Parametros:
            - origen y destino: identificadores de vertices dentro del grafo. Si alguno de estos no existe dentro del grafo, lanzara KeyError.
            - heuristica: funcion que recibe dos parametros (un vertice y el destino) y nos devuelve la 'distancia' a tener en cuenta para ajustar los resultados y converger mas rapido.
            Por defecto, la funcion nula (devuelve 0 siempre)
        Devuelve:
            - Listado de vertices (identificadores) ordenado con el recorrido, incluyendo a los vertices de origen y destino. 
            En caso que no exista camino entre el origen y el destino, se devuelve None. 
        '''
        q = []
        heap = heapq
        heap.heappush(q, (origen, 0))
        vuelta = {}
        vuelta[origen] = None
        costos = {}
        costos[origen] = 0
        while len(q) != 0:
            actual = heap.heappop(q)
            for v in self.adyacentes(actual[0]):
                nuevo_costo = costos[actual[0]] + self.grafo[actual[0]][v]
                if not v in costos or nuevo_costo < costos[v]:
                    costos[v] = nuevo_costo
                    heap.heappush(q, (v, nuevo_costo + heuristica(actual[0], v)))
                    vuelta[v] = actual[0]
        recorrido = []
        recorrido.append(destino)
        anterior = destino
        while recorrido[0] != origen:
            recorrido.insert(0, vuelta[anterior])
            anterior = vuelta[anterior]
        return recorrido


    def mst(self):
        '''Calcula el Arbol de Tendido Minimo (MST) para un grafo no dirigido. En caso de ser dirigido, lanza una excepcion.
        Devuelve: un nuevo grafo, con los mismos vertices que el original, pero en forma de MST.'''
        if self.es_dirigido: raise TypeError()
        if len(self.componentes_conexas()) > 1: 
            raise TypeError()
        nuevo_grafo = Grafo()
        lista_novisitados = self.keys()
        visitados = []
        q = []
        pesos = heapq
        actual = lista_novisitados[0]
        print("actual")
        print (actual)
        nuevo_grafo[actual] = self.grafo[actual]["value"]
        lista_novisitados.remove(actual)
        while len(lista_novisitados) > 0:
            for adyacente in self.adyacentes(actual):
                if adyacente in lista_novisitados:
                    p = self.obtener_peso_arista(actual, adyacente)
                    pesos.heappush(q, (p, (actual, adyacente)))
            minimo = pesos.heappop(q)
            actual = minimo[1][0]
            proximo = minimo[1][1]
            while proximo not in lista_novisitados:
                minimo = pesos.heappop(q)
                actual = minimo[1][0]
                proximo = minimo[1][1]
            nuevo_grafo[proximo] = self.grafo[proximo]["value"]
            nuevo_grafo.agregar_arista(actual, proximo, minimo[0])
            actual = proximo
            lista_novisitados.remove(proximo)
        return nuevo_grafo


if __name__ == '__main__':
    g = Grafo()
    g["a"] = "a"
    g["b"] = "b"
    g["c"] = "c"
    g["d"] = "d"
    g["e"] = "e"
    g["f"] = "f"
    g["g"] = "g"

    g.agregar_arista("a", "d",5)
    g.agregar_arista('a', 'b',7)
    g.agregar_arista('b', 'c',8)
    g.agregar_arista('b', 'd',9)
    g.agregar_arista('b', 'e',7)
    g.agregar_arista('c','e',5)
    g.agregar_arista('d','e',15)
    g.agregar_arista('d','f',6)
    g.agregar_arista('f','e',8)
    g.agregar_arista('g','e',9)
    g.agregar_arista('g','f',11)


    print(g.grafo)
    print("cconexas:")
    print(g.componentes_conexas())
    print("prim:")
    print(g.mst().grafo)
    '''g = Grafo()
    g[1] = 1
    g[2] = 2
    g[3] = 3
    g[4] = 4
    g[5] = 5
    g[6] = 6
    g[7] = 7
    g[8] = 8
    g[9] = 9
    g[10] = 10
    g[11] = 11
    g.agregar_arista(1,2)
    g.agregar_arista(1,3)
    g.agregar_arista(1,4)
    g.agregar_arista(2,5)
    g.agregar_arista(2,6)
    g.agregar_arista(3,7)
    g.agregar_arista(3,8)
    g.agregar_arista(3,9)
    g.agregar_arista(4,10)  
    g.agregar_arista(4,11)
    print(g.grafo)
    print("DFS:")
    print(g.dfs(inicio = 1))'''
    #print("minimo:")
    #print(g.camino_minimo(3,1))
    #print("BFS:")
    #print(g.bfs(inicio = 3))
    #print("DFS:")
    #print(g.dfs(inicio = 3))
