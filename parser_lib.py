from node import Node
from token_type import TokenType
from bnf_type import BNFType

class Parser:
  def __init__(self, tokens):
    self.tokens = tokens
    self.token_index = 0
    self.token_atual = self.tokens[self.token_index]
    self.tokens_sequencia = []
    self.ids_declarados = []
    
  def avancaToken(self):
    novo_index = self.token_index + 1
    self.token_index = novo_index
    self.token_atual = self.tokens[novo_index]

    return self.token_atual

  def validaToken(self, token_tipo_esperado):
    # print("Token Atual", self.token_atual)
    if self.token_atual.tipo == token_tipo_esperado:
      if token_tipo_esperado == TokenType.ID:
        self.ids_declarados.append(self.token_atual.valor)
      token = self.token_atual
      self.avancaToken()

      return token
    else:
      self.erroValidacao(token_tipo_esperado, self.token_atual)

  def erroValidacao(self, tipo_esperado, token_atual):
    print("Houve um problema na linha {} na posicao {}: Deveria ter um {} no lugar de {}.".format(token_atual.linha, token_atual.pos, tipo_esperado, token_atual.tipo))
    exit(1) 

  def erroDuplicado(self, token_atual):
    print("Houve um problema na linha {} na posicao {}: ID não pode ser declarado novamente.".format(token_atual.linha, token_atual.pos))
    exit(1) 

  def programa(self):
    self.removeComentarios()
    return self.declaracaoLista()

  def declaracaoLista(self):
    no = self.declaracao()
    
    no_aux = no
    while self.token_atual.tipo == TokenType.INT or self.token_atual.tipo == TokenType.VOID:
      no_temp = self.declaracao()
      no_aux.sibling = no_temp
      no_aux = no_temp

    print("Compilado com sucesso!")

  def declaracao(self):
    no = Node()
    no.add(self.tipoEspecificador())
    
    id_node = Node(self.tokens[1], TokenType.ID)
    self.validaToken(TokenType.ID)
    no.add(id_node)

    if self.token_atual.tipo == TokenType.PARENTESE_ABRE:  
      self.validaToken(TokenType.PARENTESE_ABRE)
      no_aux = self.params()
      params = []
      for param in no_aux.filhos:
        params.append(param.filhos[1].token)
      self.validaToken(TokenType.PARENTESE_FECHA)
      no.add(no_aux)
      no.add(self.compostoDecl())
      no.tipo = BNFType.FUN_DECLARACAO
    else: 
      if self.token_atual.tipo == TokenType.COLCHETE_ABRE:
        self.validaToken(TokenType.COLCHETE_ABRE)
        self.validaToken(TokenType.NUM)
        self.validaToken(TokenType.COLCHETE_FECHA)
      self.validaToken(TokenType.PONTO_VIRGULA)
      no.tipo = BNFType.VAR_DECLARACAO

      if self.verificaDeclaracao(id_node.token).valor:
        self.erroDuplicado(id_node.token)

    return no

  def tipoEspecificador(self):
    no = Node(self.token_atual, BNFType.TIPO_ESPECIFICADOR)
    self.validaToken(self.token_atual.tipo)
    return no

  def params(self):
    no = Node(None, BNFType.PARAMS)
    
    if self.token_atual.tipo == TokenType.VOID:
      self.validaToken(TokenType.VOID)
    else:
      no.filhos += self.paramLista()
    
    return no

  def paramLista(self):
    no = self.param()
    params = []
    params.append(no)
    
    while self.token_atual.tipo == TokenType.VIRGULA:
      self.validaToken(TokenType.VIRGULA)
      no_temp = self.param()
      params.append(no_temp)

    return params

  def param(self):
    no = Node()
    no.add(self.tipoEspecificador())
    id_node = Node(self.tokens[1], TokenType.ID)
    self.validaToken(TokenType.ID)
    no.add(id_node)
    no.token = self.tokens[1]
    
    if self.token_atual.tipo == TokenType.COLCHETE_ABRE:
      self.validaToken(TokenType.COLCHETE_ABRE)
      self.validaToken(TokenType.COLCHETE_FECHA)
    no.tipo = BNFType.PARAM
    
    return no

  def compostoDecl(self):
    no = Node(None, BNFType.COMPOSTO_DECL)
    self.validaToken(TokenType.CHAVE_ABRE)
    no.filhos += self.localDeclaracoes()
    no.filhos += self.statementLista()
    self.validaToken(TokenType.CHAVE_FECHA)
    
    return no

  def localDeclaracoes(self):
    declarations = []

    while self.token_atual.tipo == TokenType.INT or self.token_atual.tipo == TokenType.VOID:
      no = Node(None, BNFType.VAR_DECLARACAO)
      no.add(self.tipoEspecificador())
      id_node = Node(self.tokens[1], TokenType.ID)
      self.validaToken(TokenType.ID)
      no.add(id_node)
      
      if self.verificaDeclaracao(id_node.token.valor):
        self.erroDuplicado(id_node.token)
      
      if self.token_atual.tipo == TokenType.COLCHETE_ABRE:
        self.validaToken(TokenType.COLCHETE_ABRE)
        self.validaToken(TokenType.NUM)
        self.validaToken(TokenType.COLCHETE_FECHA)

      self.validaToken(TokenType.PONTO_VIRGULA)
      declarations.append(no)

    return declarations

  def statementLista(self):
    statements = []
    while (self.token_atual.tipo == TokenType.PONTO_VIRGULA or self.token_atual.tipo == TokenType.ID or
        self.token_atual.tipo == TokenType.PARENTESE_ABRE or self.token_atual.tipo == TokenType.NUM or
        self.token_atual.tipo == TokenType.RETURN or self.token_atual.tipo == TokenType.CHAVE_ABRE or
        self.token_atual.tipo == TokenType.IF or self.token_atual.tipo == TokenType.WHILE):
      statements.append(self.statement())
    
    return statements

  def statement(self):
    if self.token_atual.tipo == TokenType.RETURN:
      return self.retornoDecl()
    elif self.token_atual.tipo == TokenType.CHAVE_ABRE:
      self.compostoDecl()
    elif self.token_atual.tipo == TokenType.IF:
      return self.selecaoDecl()
    elif self.token_atual.tipo == TokenType.WHILE:
      return self.iteracaoDecl()
    else:
      return self.expressaoDecl()

  def selecaoDecl(self):
    no = Node(None, BNFType.SELECAO_DECL)
    self.validaToken(TokenType.IF)
    self.validaToken(TokenType.PARENTESE_ABRE)
    no.add(self.expressao())
    self.validaToken(TokenType.PARENTESE_FECHA)
    no.add(self.statement())
    
    if self.token_atual.tipo == TokenType.ELSE:
      self.validaToken(TokenType.ELSE)
      no.add(self.statement())
    
    return no

  def iteracaoDecl(self):
    no = Node(None, BNFType.ITERACAO_DECL)
    self.validaToken(TokenType.WHILE)
    self.validaToken(TokenType.PARENTESE_ABRE)
    no.add(self.expressao())
    self.validaToken(TokenType.PARENTESE_FECHA)
    no.add(self.statement())
    
    return no

  def retornoDecl(self):
    no = Node(None, BNFType.RETORNO_DECL)
    self.validaToken(TokenType.RETURN)
    
    if (self.token_atual.tipo == TokenType.PONTO_VIRGULA or self.token_atual.tipo == TokenType.ID or
        self.token_atual.tipo == TokenType.PARENTESE_ABRE or self.token_atual.tipo == TokenType.NUM):
      no.add(self.expressao())
    self.validaToken(TokenType.PONTO_VIRGULA)
    
    return no

  def expressaoDecl(self):
    no = Node(None, BNFType.EXPRESSAO_DECL)
    
    if (self.token_atual.tipo == TokenType.PONTO_VIRGULA or self.token_atual.tipo == TokenType.ID or
        self.token_atual.tipo == TokenType.PARENTESE_ABRE or self.token_atual.tipo == TokenType.NUM):
      no.add(self.expressao())
    self.validaToken(TokenType.PONTO_VIRGULA)
    
    return no

  def expressao(self):
    no = Node(None, BNFType.EXPRESSAO)
    no_aux = no

    while self.token_atual.tipo == TokenType.ID:
      no_temp = Node()
      no_temp.token = self.tokens[1]
      tokens_sequencia = self.tokens
      self.validaToken(TokenType.ID)
      
      if self.token_atual.tipo == TokenType.COLCHETE_ABRE:
        self.validaToken(TokenType.COLCHETE_ABRE)
        no_temp.add(self.expressao())
        self.validaToken(TokenType.COLCHETE_FECHA)
        if self.token_atual.tipo == TokenType.ATRIBUI:
          self.validaToken(TokenType.ATRIBUI)
      else:
        if self.token_atual.tipo == TokenType.ATRIBUI:
          self.validaToken(TokenType.ATRIBUI)
        else:
          self.tokens_sequencia = tokens_sequencia
          break

      no_temp.tipo = TokenType.ATRIBUI
      no_aux.add(no_temp)
      no_aux = no_temp

      if not self.verificaDeclaracao(no_aux.token.valor):
        self.erroDuplicado(no_aux.token)
    
    no_aux.add(self.simplesExpressao())
    return no

  def simplesExpressao(self):
    no = Node(None, BNFType.SIMPLES_EXPRESSAO)
    no.add(self.somaExpressao())
    if (self.token_atual.tipo == TokenType.MAIOR or self.token_atual.tipo == TokenType.MAIOR_IGUAL or
        self.token_atual.tipo == TokenType.IGUAL or self.token_atual.tipo == TokenType.MENOR or
        self.token_atual.tipo == TokenType.MENOR_IGUAL or self.token_atual.tipo == TokenType.DIF):
      no.add(self.relacional())
      no.add(self.somaExpressao())

    return no

  def relacional(self):
    no = Node(None, BNFType.RELACIONAL)
    if self.token_atual.tipo == TokenType.MAIOR:
      no.token = TokenType.MAIOR
      self.validaToken(TokenType.MAIOR)
    elif self.token_atual.tipo == TokenType.MAIOR_IGUAL:
      no.token = TokenType.MAIOR_IGUAL
      self.validaToken(TokenType.MAIOR_IGUAL)
    elif self.token_atual.tipo == TokenType.IGUAL:
      no.token = TokenType.IGUAL
      self.validaToken(TokenType.IGUAL)
    elif self.token_atual.tipo == TokenType.MENOR:
      no.token = TokenType.MENOR
      self.validaToken(TokenType.MENOR)
    elif self.token_atual.tipo == TokenType.MENOR_IGUAL:
      no.token = TokenType.MENOR_IGUAL
      self.validaToken(TokenType.MENOR_IGUAL)
    elif self.token_atual.tipo == TokenType.DIF:
      no.token = TokenType.DIF
      self.validaToken(TokenType.DIF)

    return no

  def somaExpressao(self):
    no = Node(None, BNFType.SOMA_EXPRESSAO)
    no.add(self.termo())
    if self.token_atual.tipo == TokenType.MAIS or self.token_atual.tipo == TokenType.MENOS:
      no.add(self.soma())
      no.add(self.termo())

    return no

  def soma(self):
    no = Node(self.token_atual, BNFType.SOMA)
    self.validaToken(self.token_atual.tipo)

    return no

  def termo(self):
    no = Node(None, BNFType.TERMO)
    no.add(self.fator()) 
    while self.token_atual.tipo == TokenType.MULT or self.token_atual.tipo == TokenType.DIV:
      no.add(self.mult())
      no.add(self.fator())

    return no

  def mult(self):
    no = Node(self.token_atual, BNFType.MULT)
    self.validaToken(self.token_atual.tipo)

    return no

  def fator(self):
    no = Node(None, BNFType.FATOR)
    
    if self.token_atual.tipo == TokenType.ID or self.tokens_sequencia[0].tipo == TokenType.ID:
      no_aux = Node(self.tokens_sequencia[1])

      if not self.tokens_sequencia[0].tipo == TokenType.ID:
        no_aux.token = self.tokens[1]
        self.validaToken(TokenType.ID)
      self.tokens_sequencia = []
      
      if self.token_atual.tipo == TokenType.PARENTESE_ABRE:
        no_aux.tipo = BNFType.ATIVACAO
        self.validaToken(TokenType.PARENTESE_ABRE)
        no_aux.add(self.args())
        self.validaToken(TokenType.PARENTESE_FECHA)
      else: 
        no_aux.tipo = BNFType.VAR
        if self.token_atual.tipo == TokenType.COLCHETE_ABRE:
          self.validaToken(TokenType.COLCHETE_ABRE)
          no_aux.add(self.expressao())
          self.validaToken(TokenType.COLCHETE_FECHA)
      no.add(no_aux)
    elif self.token_atual.tipo == TokenType.PARENTESE_ABRE:
      self.validaToken(TokenType.PARENTESE_ABRE)
      no.add(self.expressao())
      self.validaToken(TokenType.PARENTESE_FECHA)
    elif self.token_atual.tipo == TokenType.NUM:
      no.add(Node(self.tokens[1], TokenType.NUM))
      self.validaToken(TokenType.NUM)

    return no

  def args(self):
    no = Node(None, BNFType.ARGS)
    no.add(self.expressao())

    while self.token_atual.tipo == TokenType.VIRGULA:
      self.validaToken(TokenType.VIRGULA)
      no.add(self.expressao())

    return no

  def verificaDeclaracao(self, valor):
    return valor in self.ids_declarados

  def removeComentarios(self):
    tokens_validos = [token for token in self.tokens if token.tipo != TokenType.COMENTARIO]
    self.tokens = tokens_validos
  