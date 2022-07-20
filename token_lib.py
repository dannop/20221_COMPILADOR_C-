class Token:
  def __init__(self, valor, tipo, linha, pos):
    self.valor = valor
    self.tipo = tipo
    self.linha = linha
    self.pos = pos

  def __repr__(self):
    return "{}: {} \n".format(self.valor, self.tipo)

  def __str__(self):
    return "{}: {} \n".format(self.valor, self.tipo)