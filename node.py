class Node:
  def __init__(self, token = None, tipo = None, filhos = None):
    if filhos is None:
        filhos = []
    self.token = token
    self.tipo = tipo
    self.filhos = filhos
  
  def __repr__(self):
    return "{}: {} - Filhos {} \n".format(self.token, self.tipo, len(self.filhos))

  def __str__(self):
    return "{}: {} - Filhos {} \n".format(self.token, self.tipo, len(self.filhos))

  def add(self, valor):
    self.filhos.append(valor)