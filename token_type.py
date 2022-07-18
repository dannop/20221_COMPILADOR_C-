from enum import Enum

class TokenType(Enum):
  ID = 1
  NUM = 2
  ATTR = 3
  MAIS = 4
  MENOS = 5
  MULT = 6
  DIV = 7
  DIF = 8
  EQUAL = 9
  GREAT = 10
  GREAT_EQUAL = 11
  LESS = 12
  LESS_EQUAL = 13
  COLCH_OP = 14
  COLCH_ED = 15
  PARENT_OP = 16
  PARENT_ED = 17
  CHAVES_OP = 18
  CHAVES_ED = 19
  PONTO_VIRGULA = 20
  VIRGULA = 21
  EOF = 23
  IF = 24
  ELSE = 25
  INT = 26
  RETURN = 27
  VOID = 28
  WHILE = 29
  ERROR = 30