from token_lib import Token
from token_type import PALAVRAS_RESERVADAS, TokenType
from string import ascii_letters

class Scanner:
  def __init__(self, arquivo):
    self.arquivo = arquivo
    self.arquivo_linhas = sum(1 for linha in arquivo)
    self.tokens = []
    # String da linha atual
    self.linha_atual = arquivo[0]
    # Posicao da analise da linha atual
    self.linha_pos = -1
    # Contador de linhas verificadas
    self.linha_cont = 0

  def avancaLinha(self):
    # if self.linha_cont+1 > 0:
    #   print("{}: {}".format(self.linha_cont+1, self.arquivo[self.linha_cont]))
    
    try:
      nova_linha = self.linha_cont+1
      self.linha_cont = nova_linha
      self.linha_atual = self.arquivo[nova_linha]
      self.linha_pos = 0
      return self.linha_atual[self.linha_pos]
    except:
      return 'EOF'
      
  def avancaPos(self): 
    try:
      nova_pos = self.linha_pos + 1
      # print("linha atual {} // posicao atual {} // char atual ->{}<- \n".format(self.linha_cont, self.linha_pos, self.linha_atual[nova_pos]))
      self.linha_pos = nova_pos
      return self.linha_atual[nova_pos]
    except: 
      return self.avancaLinha()

  def voltaPos(self):
    self.linha_pos -= 1

  def completaInt(self, valor):
    c = self.avancaPos()
    while c.isnumeric():
      valor += str(c)
      c = self.avancaPos()
  
    self.voltaPos()
    return valor

  def completaID(self, valor):
    c = self.avancaPos()
    while c in ascii_letters:
      valor += c
      c = self.avancaPos()
      if c.isnumeric():
        print("Houve um problema na linha {} na posicao {}: Sua declaração não pode conter números.".format(self.linha_cont+1, self.linha_pos+1))
        exit(1)
    
    self.voltaPos()
    return valor 

  def completaComentario(self, valor):
    c = self.avancaPos()
    while valor[-2:] != '*/':
      valor += c
      c = self.avancaPos()

    self.voltaPos()
    return valor

  def analisaToken(self): 
    c = self.avancaPos()
    if c == ' ' or c == '\n' or c == '\t' or c == None or c == 'EOF':
      return None

    tipo = None 
    valor = c
    
    if c == '>':
      c = self.avancaPos()
      if c == '=':
        valor += c
        tipo = TokenType.MAIOR_IGUAL
      else:
        self.voltaPos()
        tipo = TokenType.MAIOR
    elif c == '<':
      c = self.avancaPos()
      if c == '=':
        valor += c
        tipo = TokenType.MENOR_IGUAL
      else:
        self.voltaPos()
        tipo = TokenType.MENOR
    elif c == '=':
      c = self.avancaPos()
      if c == '=':
        valor += c
        tipo = TokenType.IGUAL
      else:
        self.voltaPos()
        tipo = TokenType.ATRIBUI
    elif c == '!':
      c = self.avancaPos()
      if c == '=':
        valor += c
        tipo = TokenType.DIF
      else:
        self.voltaPos()
        tipo = TokenType.ERROR
    elif c == '/':
      tipo = TokenType.DIV
      c = self.avancaPos()
      if c == '*':
        tipo = TokenType.COMENTARIO
        valor = self.completaComentario(valor+c)
      else: 
        self.voltaPos()
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
      tipo = TokenType.PARENTESE_ABRE
    elif c == ')':
      tipo = TokenType.PARENTESE_FECHA
    elif c == '[':
      tipo = TokenType.COLCHETE_ABRE
    elif c == ']':
      tipo = TokenType.COLCHETE_FECHA
    elif c == '{':
      tipo = TokenType.CHAVE_ABRE
    elif c == '}':
      tipo = TokenType.CHAVE_FECHA
    elif c == 'EOF':
      tipo = TokenType.EOF
    elif c.isnumeric():
      tipo = TokenType.INT
      valor = self.completaInt(c)
    elif c in ascii_letters:
      tipo = TokenType.ID
      valor = self.completaID(c)
      if valor in list(PALAVRAS_RESERVADAS.keys()):
        tipo = PALAVRAS_RESERVADAS[valor]

    return Token(valor, tipo, self.linha_cont, self.linha_pos)

  def geraTokens(self):
    while self.linha_cont < self.arquivo_linhas:
      token = self.analisaToken()
      if token is not None:
        self.tokens.append(token)
    
    return self.tokens