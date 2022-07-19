class Token:
  def __init__(self, valor, tipo, linha, pos):
    self.valor = valor
    self.tipo = tipo
    self.linha = linha+1
    self.pos = pos

  def __str__(self, level):
    return "\t" * level + self.valor + "\n"