from node import Node
from token_type import TokenType
from bnf_type import BNFType

class Parser:
  def __init__(self, tokens):
    self.tokens = tokens
    self.token = None
    self.prevToken = [None, None, None]
    self.ids_declarados = []

  def match(self, expectedToken):
    if self.token[0] == expectedToken:
      self.token = self.scanner.getToken()
    else:
      self.error(expectedToken)

  def error(self, expectedToken):
    print(f'Erro na linha {self.token[2]} : Esperando token {expectedToken.valor} no lugar de {self.token[1]}')
    exit(1)

  def program(self):
    return self.declaration_list()

  def declaration_list(self):
    t = self.declaracao()
    p = t
    while self.token[0] == TokenType.INT or self.token[0] == TokenType.VOID:
      q = self.declaracao()
      p.sibling = q
      p = q
    return t

  def declaracao(self):
    t = Node()
    t.filhos.append(self.tipoEspecificador())
    id_node = Node()
    id_node.tipo = 'ID'
    id_node.token = self.token[1]
    id_line = self.token[2]
    self.match(TokenType.ID)
    t.filhos.append(id_node)
    
    if self.token[0] == TokenType.PARENTESE_ABRE:  
      self.ids_declarados.append([])
      self.match(TokenType.PARENTESE_ABRE)
      p = self.params()
      params = []
      for param in p.filhos:
          params.append(param.filhos[1].token)
      self.match(TokenType.PARENTESE_FECHA)
      t.filhos.append(p)
      self.ids_declarados[-1] += params
      t.filhos.append(self.compound_stmt())
      t.tipo = BNFType.FUN_DECLARACAO
      self.ids_declarados.pop()
    else: 
      if self.token[0] == TokenType.COLCHETE_ABRE:
        self.match(TokenType.COLCHETE_ABRE)
        self.match(TokenType.NUM)
        self.match(TokenType.COLCHETE_FECHA)
      self.match(TokenType.PONTO_VIRGULA)
      t.tipo = BNFType.VAR_DECLARACAO
      if self.verificaDeclaracao(id_node.token):
        print(f'Erro na linha {id_line}: Variável {id_node.token} não pode ser declarada novamente')
        exit(1)
      self.ids_declarados[-1].append(id_node.token)
    return t

  def tipoEspecificador(self):
    t = Node()
    t.tipo = BNFType.TIPO_ESPECIFICADOR
    if self.token[0] == TokenType.INT:
      self.match(TokenType.INT)
      t.token = 'int'
    elif self.token[0] == TokenType.VOID:
      self.match(TokenType.VOID)
      t.token = 'void'
    return t

  def params(self):
    t = Node()
    t.tipo = BNFType.PARAMS
    if self.token[0] == TokenType.VOID:
      self.match(TokenType.VOID)
    else:
      t.filhos += self.param_list()
    return t

  def param_list(self):
    params = []
    t = self.param()
    params.append(t)
    while self.token[0] == TokenType.VIRGULA:
      self.match(TokenType.VIRGULA)
      q = self.param()
      params.append(q)
    return params

  def param(self):
    t = Node()
    t.filhos.append(self.tipoEspecificador())
    id_node = Node()
    id_node.tipo = 'ID'
    id_node.token = self.token[1]
    self.match(TokenType.ID)
    t.filhos.append(id_node)
    t.token = self.token[1]
    if self.token[0] == TokenType.COLCHETE_ABRE:
      self.match(TokenType.COLCHETE_ABRE)
      self.match(TokenType.COLCHETE_FECHA)
    t.tipo = BNFType.PARAM
    return t

  def compound_stmt(self):
    t = Node()
    t.tipo = BNFType.COMPOSTO_DECL
    self.match(TokenType.CHAVE_ABRE)
    self.ids_declarados.append([])
    t.filhos += self.local_declarations()
    t.filhos += self.statement_list()
    self.match(TokenType.CHAVE_FECHA)
    self.ids_declarados.pop()
    return t

  def local_declarations(self):
    declarations = []
    while self.token[0] == TokenType.INT or self.token[0] == TokenType.VOID:
      t = Node()
      t.tipo = BNFType.VAR_DECLARACAO
      t.filhos.append(self.tipoEspecificador())
      id_node = Node()
      id_node.tipo = 'ID'
      id_node.token = self.token[1]
      id_line = self.token[2]
      self.match(TokenType.ID)
      t.filhos.append(id_node)
      if self.verificaDeclaracao(id_node.token):
        print(f'Erro na linha {id_line}: Variável {id_node.token} não pode ser declarada novamente')
        exit(1)
      self.ids_declarados[-1].append(id_node.token)
      if self.token[0] == TokenType.COLCHETE_ABRE:
        self.match(TokenType.COLCHETE_ABRE)
        self.match(TokenType.NUM)
        self.match(TokenType.COLCHETE_FECHA)
      self.match(TokenType.PONTO_VIRGULA)
      declarations.append(t)
    return declarations

  def statement_list(self):
    statements = []
    while (self.token[0] == TokenType.PONTO_VIRGULA or self.token[0] == TokenType.ID or
        self.token[0] == TokenType.PARENTESE_ABRE or self.token[0] == TokenType.NUM or
        self.token[0] == TokenType.RETURN or self.token[0] == TokenType.CHAVE_ABRE or
        self.token[0] == TokenType.IF or self.token[0] == TokenType.WHILE):
      statements.append(self.statement())
    return statements

  def statement(self):
    if self.token[0] == TokenType.RETURN:
      return self.return_stmt()
    elif self.token[0] == TokenType.CHAVE_ABRE:
      self.compound_stmt()
    elif self.token[0] == TokenType.IF:
      return self.selection_stmt()
    elif self.token[0] == TokenType.WHILE:
      return self.iteration_stmt()
    else:
      return self.expression_stmt()

  def selection_stmt(self):
    t = Node()
    t.tipo = BNFType.SELECAO_DECL
    self.match(TokenType.IF)
    self.match(TokenType.PARENTESE_ABRE)
    t.filhos.append(self.expression())
    self.match(TokenType.PARENTESE_FECHA)
    t.filhos.append(self.statement())
    if self.token[0] == TokenType.ELSE:
      self.match(TokenType.ELSE)
      t.filhos.append(self.statement())
    return t

  def iteration_stmt(self):
    t = Node()
    t.tipo = BNFType.ITERACAO_DECL
    self.match(TokenType.WHILE)
    self.match(TokenType.PARENTESE_ABRE)
    t.filhos.append(self.expression())
    self.match(TokenType.PARENTESE_FECHA)
    t.filhos.append(self.statement())
    return t

  def return_stmt(self):
    t = Node()
    t.tipo = BNFType.RETORNO_DECL
    self.match(TokenType.RETURN)
    if (self.token[0] == TokenType.PONTO_VIRGULA or self.token[0] == TokenType.ID or
          self.token[0] == TokenType.PARENTESE_ABRE or self.token[0] == TokenType.NUM):
      t.filhos.append(self.expression())
    self.match(TokenType.PONTO_VIRGULA)
    return t

  def expression_stmt(self):
    t = Node()
    t.tipo = BNFType.EXPRESSAO_DECL
    if (self.token[0] == TokenType.PONTO_VIRGULA or self.token[0] == TokenType.ID or
          self.token[0] == TokenType.PARENTESE_ABRE or self.token[0] == TokenType.NUM):
      t.filhos.append(self.expression())
    self.match(TokenType.PONTO_VIRGULA)
    return t

  def expression(self):
    t = Node()
    t.tipo = BNFType.EXPRESSAO
    p = t
    while self.token[0] == TokenType.ID:
      q = Node()
      q.token = self.token[1]
      prev_token = self.token
      id_line = self.token[2]
      self.match(TokenType.ID)
      if self.token[0] == TokenType.COLCHETE_ABRE:
        self.match(TokenType.COLCHETE_ABRE)
        q.filhos.append(self.expression())
        self.match(TokenType.COLCHETE_FECHA)
        if self.token[0] == TokenType.token:
          self.match(TokenType.token)
      else:
        if self.token[0] == TokenType.token:
          self.match(TokenType.token)
        else:
          self.prevToken = prev_token
          break
      q.tipo = 'ASSIGN'
      p.filhos.append(q)
      p = q
      if not self.verificaDeclaracao(p.token):
        print(f'Erro na linha {id_line}: Variável {p.token} sendo utilizada antes de sua declaração')
        exit(1)
    p.filhos.append(self.simple_expression())
    return t

  def simple_expression(self):
    t = Node()
    t.tipo = BNFType.SIMPLES_EXPRESSAO
    t.filhos.append(self.additive_expression())
    if (self.token[0] == TokenType.MAIOR or self.token[0] == TokenType.MAIOR_IGUAL or
        self.token[0] == TokenType.IGUAL or self.token[0] == TokenType.MENOR or
        self.token[0] == TokenType.MENOR_IGUAL or self.token[0] == TokenType.DIF):
      t.filhos.append(self.relop())
      t.filhos.append(self.additive_expression())
    return t

  def relop(self):
    t = Node()
    t.tipo = BNFType.RELACIONAL
    if self.token[0] == TokenType.MAIOR:
      t.token = '>'
      self.match(TokenType.MAIOR)
    elif self.token[0] == TokenType.MAIOR_IGUAL:
      t.token = '>='
      self.match(TokenType.MAIOR_IGUAL)
    elif self.token[0] == TokenType.IGUAL:
      t.token = '=='
      self.match(TokenType.IGUAL)
    elif self.token[0] == TokenType.MENOR:
      t.token = '<'
      self.match(TokenType.MENOR)
    elif self.token[0] == TokenType.MENOR_IGUAL:
      t.token = '<='
      self.match(TokenType.MENOR_IGUAL)
    elif self.token[0] == TokenType.DIF:
      t.token = '!='
      self.match(TokenType.DIF)
    return t

  def additive_expression(self):
    t = Node()
    t.tipo = BNFType.SOMA_EXPRESSAO
    t.filhos.append(self.term())
    if self.token[0] == TokenType.MAIS or self.token[0] == TokenType.MENOS:
      t.filhos.append(self.addop())
      t.filhos.append(self.term())
    return t

  def addop(self):
    t = Node()
    t.tipo = BNFType.SOMA
    if self.token[0] == TokenType.MAIS:
      t.token = '+'
      self.match(TokenType.MAIS)
    elif self.token[0] == TokenType.MENOS:
      t.token = '-'
      self.match(TokenType.MENOS)
    return t

  def term(self):
    t = Node()
    t.tipo = BNFType.TERMO 
    t.filhos.append(self.factor())
    while self.token[0] == TokenType.MULT or self.token[0] == TokenType.DIV:
      t.filhos.append(self.mulop())
      t.filhos.append(self.factor())
    return t

  def mulop(self):
    t = Node()
    t.tipo = BNFType.MULT
    if self.token[0] == TokenType.MULT:
      t.token = '*'
      self.match(TokenType.MULT)
    elif self.token[0] == TokenType.DIV:
      t.token = '/'
      self.match(TokenType.DIV)
    return t

  def factor(self):
    t = Node()
    t.tipo = BNFType.FATOR
    if self.token[0] == TokenType.ID or self.prevToken[0] == TokenType.ID:
      p = Node()
      p.token = self.prevToken[1]
      if not self.prevToken[0] == TokenType.ID:
        p.token = self.token[1]
        self.match(TokenType.ID)
      self.prevToken = [None, None, None]
      if self.token[0] == TokenType.PARENTESE_ABRE:  # call
        p.tipo = BNFType.ATIVACAO
        self.match(TokenType.PARENTESE_ABRE)
        p.filhos.append(self.args())
        self.match(TokenType.PARENTESE_FECHA)
      else: 
        p.tipo = BNFType.VAR
        if self.token[0] == TokenType.COLCHETE_ABRE:
          self.match(TokenType.COLCHETE_ABRE)
          p.filhos.append(self.expression())
          self.match(TokenType.COLCHETE_FECHA)
      t.filhos.append(p)
    elif self.token[0] == TokenType.PARENTESE_ABRE:
      self.match(TokenType.PARENTESE_ABRE)
      t.filhos.append(self.expression())
      self.match(TokenType.PARENTESE_FECHA)
    elif self.token[0] == TokenType.NUM:
      p = Node()
      p.tipo = 'NUM'
      p.token = self.token[1]
      t.filhos.append(p)
      self.match(TokenType.NUM)
    return t

  def args(self):
    t = Node()
    t.tipo = BNFType.ARGS
    t.filhos.append(self.expression())
    while self.token[0] == TokenType.VIRGULA:
      self.match(TokenType.VIRGULA)
      t.filhos.append(self.expression())
    return t

  def verificaDeclaracao(self, valor):
    return valor in [x for scope in self.ids_declarados for x in scope]

  def exe(self):
    return self.program()