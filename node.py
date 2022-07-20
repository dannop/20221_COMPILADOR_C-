class Node:
  def __init__(self, token = None, tipo = None, fihos = None):
    if fihos is None:
        fihos = []
    self.token = token
    self.tipo = tipo
    self.filhos = fihos
  
  def __repr__(self):
    return "{}: {} - Filhos {} \n".format(self.token, self.tipo, len(self.filhos))

  def __str__(self):
    return "{}: {} - Filhos {} \n".format(self.token, self.tipo, len(self.filhos))

  def add(self, valor):
    self.filhos.append(valor)