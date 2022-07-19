from token import Token
from token_type import TokenType

class Scanner:
  def __init__(self, arquivo):
    self.arquivo = arquivo
    # String da linha atual
    self.linha_atual = arquivo[0]
    # Posicao da analise da linha atual
    self.linha_pos = -1
    # Contador de linhas verificadas
    self.linha_cont = -1

  def pegaProxValor(self):
    if not self.linha_atual or self.linha_pos >= len(self.linha_atual):
      raise Exception("Houve um problema ao ler o próximo valor de uma linha.")
    return self.linha_atual[self.linha_pos]

  def avancaLinha(self):
    nova_pos = self.linha_cont+1
    self.linha_atual = self.arquivo[nova_pos]
    self.linha_pos = -1
    self.linha_cont = nova_pos
    print("{}: {}".format(self.linha_cont, self.linha_atual))

  def avancaPos(self): 
    try:
      self.linha_pos += 1
      return self.linha_atual[self.linha_pos]
    except: 
      try: 
        self.avancaLinha()
      except:
        return 'EOF'

      return self.avancaLinha()
  
  def completaInt(self, valor):
    c = self.avancaPos()
    while c.isnumeric():
      valor += c
      c = self.avancaPos()

    return valor

  def completaID(self, valor):
    c = self.avancaPos()
    print("valor")
    print(valor)
    while c != "\"":
      valor += c
      c = self.avancaPos()
    valor += c

    return valor 

  def analisaToken(self): 
    c = self.avancaPos()
    
    if c == '\n' or c == ' ' or c == '\t' or c == 'FIM':
      return None

    tipo = None 
    valor = c
    if c.isalpha():
      tipo = TokenType.ID
      valor = self.completaID(c)
    elif c.isnumeric():
      tipo = TokenType.INT
      valor = self.completaInt(c)
    elif c == '>':
      c += self.avancaPos()
      if c == '=':
        tipo = TokenType.GREAT_EQUAL
      else:
        tipo = TokenType.GREAT
    elif c == '<':
      c += self.avancaPos()
      if c == '=':
        tipo = TokenType.LESS_EQUAL
      else:
        tipo = TokenType.LESS
    elif c == '=':
      c += self.avancaPos()
      if c == '=':
        tipo = TokenType.EQUAL
      else:
        tipo = TokenType.ATTR
    elif c == '!':
      c += self.avancaPos()
      if c == '=':
        tipo = TokenType.DIF
      else:
        tipo = TokenType.ERROR
    elif c == '/':
      if c == '*':
        pass
        # if c == '*':
        #   if c == '/':
        #     token_string = ''
        #   elif c == 'EOF':
        #     tipo = TokenType.EOF
        #   else:
        #     state = StateType.COMMENT
        # elif c == 'EOF':
        #   tipo = TokenType.EOF
      else:
        self.avancaPos()
        tipo = TokenType.DIV
    elif c == '+':
      tipo = TokenType.MAIS
    elif c == '-':
      tipo = TokenType.MENOS
    elif c == '*':
      tipo = TokenType.MULT
    elif c == ';':
      tipo = TokenType.PONTO_VIRGULA
    elif c == ',':
      tipo = TokenType.VIRGULA
    elif c == '(':
      tipo = TokenType.PARENT_OP
    elif c == ')':
      tipo = TokenType.PARENT_ED
    elif c == '[':
      tipo = TokenType.COLCH_OP
    elif c == ']':
      tipo = TokenType.COLCH_ED
    elif c == '{':
      tipo = TokenType.CHAVES_OP
    elif c == '}':
      tipo = TokenType.CHAVES_ED
    elif c == 'EOF':
      tipo = TokenType.EOF

    return Token(valor, tipo, self.linha_cont, self.linha_pos)

  def geraTokens(self):
    tokens = []
    while self.linha_atual:
      print("Dentro do while")
      token = self.analisaToken()
      if token is not None:
        tokens.append(token)
    
    return tokens