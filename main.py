import sys
from parser_lib import Parser

from scanner import Scanner
from token_type import TokenType

def leArquivo(nome):
  try:
    arquivo = open(nome, 'r')
    resultado = arquivo.read().splitlines()
    arquivo.close()
    return resultado
  except FileNotFoundError:
    raise FileNotFoundError('Arquivo não encontrado.')

def main():
  nome_arquivo = 'main.txt'

  if len(sys.argv) == 2:
    if sys.argv[1] != "":
      nome_arquivo = sys.argv[1]
  
  programa = leArquivo(nome_arquivo)
  tokens = Scanner(programa).geraTokens()
  # print("Tokens", tokens)
  print("Numero de tokens: {}".format(len(tokens)))
  parser = Parser(tokens)
  parser.programa()

if __name__ == "__main__":
  main()
