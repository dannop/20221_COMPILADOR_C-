class Node:
  def __init__(self, token = None, tipo = None, fihos = []):
    self.token = token
    self.tipo = tipo
    self.filhos = fihos
    
  def __str__(self):
    return f'{self.tipo}'