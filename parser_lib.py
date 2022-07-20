from node import Node
from token_type import TokenType, OPERADORES
from bnf_type import BNFType

SEQUENCIA_DECLARACAO = [TokenType.PONTO_VIRGULA, TokenType.ID, TokenType.PARENTESE_ABRE, TokenType.NUM]
SEQUENCIA_STATEMENT = [TokenType.PONTO_VIRGULA, TokenType.ID, TokenType.PARENTESE_ABRE, TokenType.NUM, 
  TokenType.RETURN, TokenType.CHAVE_ABRE, TokenType.IF, TokenType.WHILE]

class Parser:
  def __init__(self, tokens):
    self.tokens = [token for token in tokens if token.tipo != TokenType.COMENTARIO]
    self.token_index = 0
    self.token_atual = self.tokens[self.token_index]
    self.ids_declarados = []
    self.houve_erro = False
    
  def avancaToken(self):
    novo_index = self.token_index + 1
    self.token_index = novo_index
    self.token_atual = self.tokens[novo_index]

  def validaToken(self, token_tipo_esperado):
    # print("Token Atual", self.token_atual)
    if self.token_atual.tipo == token_tipo_esperado:
      if self.token_atual.tipo == TokenType.ID:
        self.ids_declarados.append(self.token_atual.valor)
      token = self.token_atual
      self.avancaToken()

      return token
    else:
      self.erroValidacao(token_tipo_esperado, self.token_atual)

  def erroValidacao(self, tipo_esperado, token_atual):
    print("Houve um problema na linha {} na posicao {}: Deveria ter um {} no lugar de {}.".format(token_atual.linha, token_atual.pos, tipo_esperado, token_atual.tipo))
    self.houve_erro = True
    # exit(1) 

  def erroDuplicado(self, token_atual):
    print("Houve um problema na linha {} na posicao {}: {} não pode ser declarado novamente.".format(token_atual.linha, token_atual.pos, token_atual.valor))
    self.houve_erro = True
    # exit(1) 
  
  def verificaDeclaracao(self, token):
    return token.valor in self.ids_declarados
  
  def programa(self):
    return self.declaracaoLista()

  def declaracaoLista(self):
    no = self.declaracao()
    
    while self.token_atual.tipo == TokenType.INT or self.token_atual.tipo == TokenType.VOID:
      no = self.declaracao()
      
    if not self.houve_erro:
      print("Compilado com sucesso!")
    return no

  def declaracao(self):
    no = Node()
    no.add(self.tipoEspecificador())
    
    no_id = Node(self.tokens[self.token_index+1], TokenType.ID)
    self.validaToken(TokenType.ID)
    no.add(no_id)

    if self.token_atual.tipo == TokenType.PARENTESE_ABRE: 
      no.tipo = BNFType.FUN_DECLARACAO 
      self.funDeclaracao(no)
    else: 
      no.tipo = BNFType.VAR_DECLARACAO
      self.varDeclaracao(no_id)
      
    return no

  def varDeclaracao(self, no):
    if self.token_atual.tipo == TokenType.COLCHETE_ABRE:
      self.validaToken(TokenType.COLCHETE_ABRE)
      self.validaToken(TokenType.NUM)
      self.validaToken(TokenType.COLCHETE_FECHA)
    self.validaToken(TokenType.PONTO_VIRGULA)
    
    if self.verificaDeclaracao(no.token):
      self.erroDuplicado(no.token)

  def tipoEspecificador(self):
    no = Node(self.token_atual, BNFType.TIPO_ESPECIFICADOR)
    self.validaToken(self.token_atual.tipo)
    return no

  def funDeclaracao(self, no):
    self.validaToken(TokenType.PARENTESE_ABRE)
    no_aux = self.params()

    params = []
    for param in no_aux.filhos:
      params.append(param.filhos[1].token)

    self.validaToken(TokenType.PARENTESE_FECHA)
    no.add(no_aux)
    no.add(self.compostoDecl())

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

    no_id = Node(self.tokens[self.token_index+1], TokenType.ID)
    self.validaToken(TokenType.ID)
    no.add(no_id)
    no.token = self.tokens[self.token_index+1]
    
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
    delclaracoes = []

    while self.token_atual.tipo == TokenType.INT or self.token_atual.tipo == TokenType.VOID:
      no = Node(None, BNFType.VAR_DECLARACAO)
      no.add(self.tipoEspecificador())

      no_id = Node(self.tokens[self.token_index+1], TokenType.ID)
      self.validaToken(TokenType.ID)
      no.add(no_id)
      
      if self.verificaDeclaracao(no_id.token):
        self.erroDuplicado(no_id.token)
      
      if self.token_atual.tipo == TokenType.COLCHETE_ABRE:
        self.validaToken(TokenType.COLCHETE_ABRE)
        self.validaToken(TokenType.NUM)
        self.validaToken(TokenType.COLCHETE_FECHA)

      self.validaToken(TokenType.PONTO_VIRGULA)
      delclaracoes.append(no)

    return delclaracoes

  def statementLista(self):
    statements = []
    while (self.token_atual.tipo in SEQUENCIA_STATEMENT):
      statements.append(self.statement())
    
    return statements

  def statement(self):
    if self.token_atual.tipo == TokenType.RETURN:
      return self.retornoDecl()
    elif self.token_atual.tipo == TokenType.CHAVE_ABRE:
      return self.compostoDecl()
    elif self.token_atual.tipo == TokenType.IF:
      return self.selecaoDecl()
    elif self.token_atual.tipo == TokenType.WHILE:
      return self.iteracaoDecl()
    else:
      return self.expressaoDecl()

  def expressaoDecl(self):
    no = Node(None, BNFType.EXPRESSAO_DECL)
    
    if (self.token_atual.tipo in SEQUENCIA_DECLARACAO):
      no.add(self.expressao())
    self.validaToken(TokenType.PONTO_VIRGULA)
    
    return no

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
    
    if (self.token_atual.tipo in SEQUENCIA_DECLARACAO):
      no.add(self.expressao())
    self.validaToken(TokenType.PONTO_VIRGULA)
    
    return no

  def expressao(self):
    no = Node(None, BNFType.EXPRESSAO)
    no_aux = no

    while self.token_atual.tipo == TokenType.ID:
      no_temp = Node(self.tokens[self.token_index+1])
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
          break

      no_temp.tipo = TokenType.ATRIBUI
      no_aux.add(no_temp)
      no_aux = no_temp

      if not self.verificaDeclaracao(no_aux.token):
        self.erroDuplicado(no_aux.token)
    
    no_aux.add(self.simplesExpressao())
    return no

  def var(self, no):
    if self.token_atual.tipo == TokenType.COLCHETE_ABRE:
      self.validaToken(TokenType.COLCHETE_ABRE)
      no.add(self.expressao())
      self.validaToken(TokenType.COLCHETE_FECHA)

  def simplesExpressao(self):
    no = Node(None, BNFType.SIMPLES_EXPRESSAO)
    no.add(self.somaExpressao())

    if (self.token_atual.tipo in list(OPERADORES.values())):
      no.add(self.relacional())
      no.add(self.somaExpressao())

    return no

  def relacional(self):
    no = Node(self.token_atual, BNFType.RELACIONAL)
    self.validaToken(self.token_atual.tipo)

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
    
    if self.token_atual.tipo == TokenType.ID:
      no_aux = Node(self.tokens[self.token_index+1])
      self.validaToken(TokenType.ID)
      
      if self.token_atual.tipo == TokenType.PARENTESE_ABRE:
        no_aux.tipo = BNFType.ATIVACAO
        self.ativacao(no_aux)
      else: 
        no_aux.tipo = BNFType.VAR
        self.var(no_aux)
      no.add(no_aux)
    elif self.token_atual.tipo == TokenType.PARENTESE_ABRE:
      self.validaToken(TokenType.PARENTESE_ABRE)
      no.add(self.expressao())
      self.validaToken(TokenType.PARENTESE_FECHA)
    elif self.token_atual.tipo == TokenType.NUM:
      no.add(Node(self.tokens[self.token_index+1], TokenType.NUM))
      self.validaToken(TokenType.NUM)

    return no

  def ativacao(self, no):
    self.validaToken(TokenType.PARENTESE_ABRE)
    no.add(self.args())
    self.validaToken(TokenType.PARENTESE_FECHA)

  def args(self):
    no = Node(None, BNFType.ARGS)
    no.add(self.expressao())

    while self.token_atual.tipo == TokenType.VIRGULA:
      self.validaToken(TokenType.VIRGULA)
      no.add(self.expressao())

    return no