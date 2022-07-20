class Node:
  def __init__(self):
    self.filhos = None
    self.sibling = None
    self.token = None
    self.tipo = None
    
  def __str__(self):
    return f'{self.tipo}'