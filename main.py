import sys
from parserx import Parser

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
    nome_arquivo = sys.argv[1]
  programa = leArquivo(nome_arquivo)
  tokens = Scanner(programa).geraTokens()
  tokens_validos = [token for token in tokens if token.tipo != TokenType.COMENTARIO]
  parser = Parser(tokens_validos)
  parser.exe()
  print("Tokens", tokens)
  print("Numero de tokens: {}".format(len(tokens)))

if __name__ == "__main__":
  main()
