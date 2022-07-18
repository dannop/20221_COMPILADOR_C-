class Node:
  def __init__(self, token, filhos):
    self.filhos = filhos
    self.token = token
    self.tipo = ''
    
  def __str__(self):
    return f'{self.tipo}'