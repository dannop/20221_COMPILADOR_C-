from node import Node
from token_type import TokenType
from bnf_type import BNFType

class Parser:
  def __init__(self, tokens):
    self.tokens = tokens
    self.token_anterior = [None, None, None]
    self.ids_declarados = []

  def validaToken(self, token_esperado):
    if self.tokens[0].tipo == token_esperado:
      self.tokens = self.tokens.pop(0)
    else:
      print("Houve um problema na linha {} na posicao {}: Deveria ter um {} no lugar de {}.".format(self.tokens[2].linha, self.tokens[2].pos, token_esperado, self.tokens[1].tipo))
      exit(1)  

  def exe(self):
    return self.programa()

  def programa(self):
    return self.declaracaoLista()

  def declaracaoLista(self):
    no = self.declaracao()
    
    p = no
    while self.tokens[0].tipo == TokenType.INT or self.tokens[0].tipo == TokenType.VOID:
      q = self.declaracao()
      p.sibling = q
      p = q

    return no

  def declaracao(self):
    no = Node()
    no.filhos.append(self.tipoEspecificador())
    id_node = Node(self.tokens[1], 'ID')
    id_line = self.tokens[2]
    self.validaToken(TokenType.ID)
    no.filhos.append(id_node)
    
    if self.tokens[0].tipo == TokenType.PARENTESE_ABRE:  
      self.ids_declarados.append([])
      self.validaToken(TokenType.PARENTESE_ABRE)
      p = self.params()
      params = []
      for param in p.filhos:
        params.append(param.filhos[1].token)
      self.validaToken(TokenType.PARENTESE_FECHA)
      no.filhos.append(p)
      self.ids_declarados[-1] += params
      no.filhos.append(self.compostoDecl())
      no.tipo = BNFType.FUN_DECLARACAO
      self.ids_declarados.pop()
    else: 
      if self.tokens[0].tipo == TokenType.COLCHETE_ABRE:
        self.validaToken(TokenType.COLCHETE_ABRE)
        self.validaToken(TokenType.NUM)
        self.validaToken(TokenType.COLCHETE_FECHA)
      self.validaToken(TokenType.PONTO_VIRGULA)
      no.tipo = BNFType.VAR_DECLARACAO

      if self.verificaDeclaracao(id_node.token):
        print(f'Erro na linha {id_line}: Variável {id_node.token} não pode ser declarada novamente')
        exit(1)
      self.ids_declarados[-1].append(id_node.token)

    return no

  def tipoEspecificador(self):
    no = Node()
    no.tipo = BNFType.TIPO_ESPECIFICADOR

    if self.tokens[0].tipo == TokenType.INT:
      self.validaToken(TokenType.INT)
      no.token = 'int'
    elif self.tokens[0].tipo == TokenType.VOID:
      self.validaToken(TokenType.VOID)
      no.token = 'void'
    return no

  def params(self):
    no = Node()
    no.tipo = BNFType.PARAMS
    if self.tokens[0].tipo == TokenType.VOID:
      self.validaToken(TokenType.VOID)
    else:
      no.filhos += self.paramLista()
    return no

  def paramLista(self):
    params = []
    no = self.param()
    params.append(no)
    while self.tokens[0].tipo == TokenType.VIRGULA:
      self.validaToken(TokenType.VIRGULA)
      q = self.param()
      params.append(q)
    return params

  def param(self):
    no = Node()
    no.filhos.append(self.tipoEspecificador())
    id_node = Node()
    id_node.tipo = 'ID'
    id_node.token = self.tokens[1]
    self.validaToken(TokenType.ID)
    no.filhos.append(id_node)
    no.token = self.tokens[1]
    if self.tokens[0].tipo == TokenType.COLCHETE_ABRE:
      self.validaToken(TokenType.COLCHETE_ABRE)
      self.validaToken(TokenType.COLCHETE_FECHA)
    no.tipo = BNFType.PARAM
    return no

  def compostoDecl(self):
    no = Node()
    no.tipo = BNFType.COMPOSTO_DECL
    self.validaToken(TokenType.CHAVE_ABRE)
    self.ids_declarados.append([])
    no.filhos += self.localDeclaracoes()
    no.filhos += self.statement_list()
    self.validaToken(TokenType.CHAVE_FECHA)
    self.ids_declarados.pop()
    return no

  def localDeclaracoes(self):
    declarations = []
    while self.tokens[0].tipo == TokenType.INT or self.tokens[0].tipo == TokenType.VOID:
      no = Node()
      no.tipo = BNFType.VAR_DECLARACAO
      no.filhos.append(self.tipoEspecificador())
      id_node = Node()
      id_node.tipo = 'ID'
      id_node.token = self.tokens[1]
      id_line = self.tokens[2]
      self.validaToken(TokenType.ID)
      no.filhos.append(id_node)
      
      if self.verificaDeclaracao(id_node.token):
        print(f'Erro na linha {id_line}: Variável {id_node.token} não pode ser declarada novamente')
        exit(1)
      self.ids_declarados[-1].append(id_node.token)
      
      if self.tokens[0].tipo == TokenType.COLCHETE_ABRE:
        self.validaToken(TokenType.COLCHETE_ABRE)
        self.validaToken(TokenType.NUM)
        self.validaToken(TokenType.COLCHETE_FECHA)
      self.validaToken(TokenType.PONTO_VIRGULA)
      declarations.append(no)
    return declarations

  def statement_list(self):
    statements = []
    while (self.tokens[0].tipo == TokenType.PONTO_VIRGULA or self.tokens[0].tipo == TokenType.ID or
        self.tokens[0].tipo == TokenType.PARENTESE_ABRE or self.tokens[0].tipo == TokenType.NUM or
        self.tokens[0].tipo == TokenType.RETURN or self.tokens[0].tipo == TokenType.CHAVE_ABRE or
        self.tokens[0].tipo == TokenType.IF or self.tokens[0].tipo == TokenType.WHILE):
      statements.append(self.statement())
    
    return statements

  def statement(self):
    if self.tokens[0].tipo == TokenType.RETURN:
      return self.retornoDecl()
    elif self.tokens[0].tipo == TokenType.CHAVE_ABRE:
      self.compostoDecl()
    elif self.tokens[0].tipo == TokenType.IF:
      return self.selecaoDecl()
    elif self.tokens[0].tipo == TokenType.WHILE:
      return self.iteracaoDecl()
    else:
      return self.expressaoDecl()

  def selecaoDecl(self):
    no = Node()
    no.tipo = BNFType.SELECAO_DECL
    self.validaToken(TokenType.IF)
    self.validaToken(TokenType.PARENTESE_ABRE)
    no.filhos.append(self.expressao())
    self.validaToken(TokenType.PARENTESE_FECHA)
    no.filhos.append(self.statement())
    if self.tokens[0].tipo == TokenType.ELSE:
      self.validaToken(TokenType.ELSE)
      no.filhos.append(self.statement())
    return no

  def iteracaoDecl(self):
    no = Node()
    no.tipo = BNFType.ITERACAO_DECL
    self.validaToken(TokenType.WHILE)
    self.validaToken(TokenType.PARENTESE_ABRE)
    no.filhos.append(self.expressao())
    self.validaToken(TokenType.PARENTESE_FECHA)
    no.filhos.append(self.statement())
    return no

  def retornoDecl(self):
    no = Node()
    no.tipo = BNFType.RETORNO_DECL
    self.validaToken(TokenType.RETURN)
    if (self.tokens[0].tipo == TokenType.PONTO_VIRGULA or self.tokens[0].tipo == TokenType.ID or
          self.tokens[0].tipo == TokenType.PARENTESE_ABRE or self.tokens[0].tipo == TokenType.NUM):
      no.filhos.append(self.expressao())
    self.validaToken(TokenType.PONTO_VIRGULA)
    return no

  def expressaoDecl(self):
    no = Node()
    no.tipo = BNFType.EXPRESSAO_DECL
    if (self.tokens[0].tipo == TokenType.PONTO_VIRGULA or self.tokens[0].tipo == TokenType.ID or
          self.tokens[0].tipo == TokenType.PARENTESE_ABRE or self.tokens[0].tipo == TokenType.NUM):
      no.filhos.append(self.expressao())
    self.validaToken(TokenType.PONTO_VIRGULA)
    return no

  def expressao(self):
    no = Node()
    no.tipo = BNFType.EXPRESSAO
    p = no
    while self.tokens[0].tipo == TokenType.ID:
      q = Node()
      q.token = self.tokens[1]
      token_anterior = self.token
      id_line = self.tokens[2]
      self.validaToken(TokenType.ID)
      if self.tokens[0].tipo == TokenType.COLCHETE_ABRE:
        self.validaToken(TokenType.COLCHETE_ABRE)
        q.filhos.append(self.expressao())
        self.validaToken(TokenType.COLCHETE_FECHA)
        if self.tokens[0].tipo == TokenType.token:
          self.validaToken(TokenType.token)
      else:
        if self.tokens[0].tipo == TokenType.token:
          self.validaToken(TokenType.token)
        else:
          self.token_anterior = token_anterior
          break
      q.tipo = 'ASSIGN'
      p.filhos.append(q)
      p = q
      if not self.verificaDeclaracao(p.token):
        print(f'Erro na linha {id_line}: Variável {p.token} sendo utilizada antes de sua declaração')
        exit(1)
    p.filhos.append(self.simplesExpressao())
    return no

  def simplesExpressao(self):
    no = Node()
    no.tipo = BNFType.SIMPLES_EXPRESSAO
    no.filhos.append(self.somaExpressao())
    if (self.tokens[0].tipo == TokenType.MAIOR or self.tokens[0].tipo == TokenType.MAIOR_IGUAL or
        self.tokens[0].tipo == TokenType.IGUAL or self.tokens[0].tipo == TokenType.MENOR or
        self.tokens[0].tipo == TokenType.MENOR_IGUAL or self.tokens[0].tipo == TokenType.DIF):
      no.filhos.append(self.relacional())
      no.filhos.append(self.somaExpressao())
    return no

  def relacional(self):
    no = Node()
    no.tipo = BNFType.RELACIONAL
    if self.tokens[0].tipo == TokenType.MAIOR:
      no.token = '>'
      self.validaToken(TokenType.MAIOR)
    elif self.tokens[0].tipo == TokenType.MAIOR_IGUAL:
      no.token = '>='
      self.validaToken(TokenType.MAIOR_IGUAL)
    elif self.tokens[0].tipo == TokenType.IGUAL:
      no.token = '=='
      self.validaToken(TokenType.IGUAL)
    elif self.tokens[0].tipo == TokenType.MENOR:
      no.token = '<'
      self.validaToken(TokenType.MENOR)
    elif self.tokens[0].tipo == TokenType.MENOR_IGUAL:
      no.token = '<='
      self.validaToken(TokenType.MENOR_IGUAL)
    elif self.tokens[0].tipo == TokenType.DIF:
      no.token = '!='
      self.validaToken(TokenType.DIF)
    return no

  def somaExpressao(self):
    no = Node()
    no.tipo = BNFType.SOMA_EXPRESSAO
    no.filhos.append(self.termo())
    if self.tokens[0].tipo == TokenType.MAIS or self.tokens[0].tipo == TokenType.MENOS:
      no.filhos.append(self.soma())
      no.filhos.append(self.termo())
    return no

  def soma(self):
    no = Node()
    no.tipo = BNFType.SOMA
    if self.tokens[0].tipo == TokenType.MAIS:
      no.token = '+'
      self.validaToken(TokenType.MAIS)
    elif self.tokens[0].tipo == TokenType.MENOS:
      no.token = '-'
      self.validaToken(TokenType.MENOS)
    return no

  def termo(self):
    no = Node()
    no.tipo = BNFType.TERMO 
    no.filhos.append(self.fator())
    while self.tokens[0].tipo == TokenType.MULT or self.tokens[0].tipo == TokenType.DIV:
      no.filhos.append(self.mult())
      no.filhos.append(self.fator())
    return no

  def mult(self):
    no = Node()
    no.tipo = BNFType.MULT
    if self.tokens[0].tipo == TokenType.MULT:
      no.token = '*'
      self.validaToken(TokenType.MULT)
    elif self.tokens[0].tipo == TokenType.DIV:
      no.token = '/'
      self.validaToken(TokenType.DIV)
    return no

  def fator(self):
    no = Node()
    no.tipo = BNFType.FATOR
    if self.tokens[0].tipo == TokenType.ID or self.token_anterior[0].tipo == TokenType.ID:
      p = Node()
      p.token = self.token_anterior[1]
      if not self.token_anterior[0] == TokenType.ID:
        p.token = self.tokens[1]
        self.validaToken(TokenType.ID)
      self.token_anterior = [None, None, None]
      if self.tokens[0].tipo == TokenType.PARENTESE_ABRE:  # call
        p.tipo = BNFType.ATIVACAO
        self.validaToken(TokenType.PARENTESE_ABRE)
        p.filhos.append(self.args())
        self.validaToken(TokenType.PARENTESE_FECHA)
      else: 
        p.tipo = BNFType.VAR
        if self.tokens[0].tipo == TokenType.COLCHETE_ABRE:
          self.validaToken(TokenType.COLCHETE_ABRE)
          p.filhos.append(self.expressao())
          self.validaToken(TokenType.COLCHETE_FECHA)
      no.filhos.append(p)
    elif self.tokens[0].tipo == TokenType.PARENTESE_ABRE:
      self.validaToken(TokenType.PARENTESE_ABRE)
      no.filhos.append(self.expressao())
      self.validaToken(TokenType.PARENTESE_FECHA)
    elif self.tokens[0].tipo == TokenType.NUM:
      p = Node()
      p.tipo = 'NUM'
      p.token = self.tokens[1]
      no.filhos.append(p)
      self.validaToken(TokenType.NUM)
    return no

  def args(self):
    no = Node()
    no.tipo = BNFType.ARGS
    no.filhos.append(self.expressao())
    while self.tokens[0].tipo == TokenType.VIRGULA:
      self.validaToken(TokenType.VIRGULA)
      no.filhos.append(self.expressao())
    return no

  def verificaDeclaracao(self, valor):
    return valor in [x for scope in self.ids_declarados for x in scope]

  