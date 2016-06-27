"""l.remove(x)
l.find(x)
l.pop(i)
l.insert(x, i)"""

class AristaDirigida(object):
	'''Representa una arista dirigida'''

	def __init__(self, peso, origen, destino):
		self.peso = peso
		self.origenes = {origen:[destino]}

	def get_peso(self):
		'''Devuelve el peso de la arista'''
		return self.peso
