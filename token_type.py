from enum import Enum

class TokenType(Enum):
  ID = 1
  NUM = 2
  ATRIBUI = 3
  MAIS = 4
  MENOS = 5
  MULT = 6
  DIV = 7
  DIF = 8
  IGUAL = 9
  MAIOR = 10
  MAIOR_IGUAL = 11
  MENOR = 12
  MENOR_IGUAL = 13
  COLCHETE_ABRE = 14
  COLCHETE_FECHA = 15
  PARENTESE_ABRE = 16
  PARENTESE_FECHA = 17
  CHAVE_ABRE = 18
  CHAVE_FECHA = 19
  PONTO_VIRGULA = 20
  VIRGULA = 21
  EOF = 23
  IF = 24
  ELSE = 25
  INT = 26
  RETURN = 27
  VOID = 28
  WHILE = 29
  COMENTARIO = 30

PALAVRAS_RESERVADAS = {
  "if": TokenType.IF, 
  "else": TokenType.ELSE, 
  "while": TokenType.WHILE, 
  "void": TokenType.VOID, 
  "int": TokenType.INT, 
  "return": TokenType.RETURN
}

OPERADORES = {
  ">": TokenType.MAIOR,
  ">=": TokenType.MAIOR_IGUAL,
  "==": TokenType.IGUAL,
  "<": TokenType.MENOR,
  "<=": TokenType.MENOR_IGUAL,
  "!=": TokenType.DIF,
}