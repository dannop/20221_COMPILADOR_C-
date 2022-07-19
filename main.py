import sys

from scanner import Scanner

def leArquivo(nome):
  try:
    arquivo = open(nome, 'r')
    resultado = arquivo.read().splitlines()
    arquivo.close()
    return resultado
  except FileNotFoundError:
    raise FileNotFoundError('Arquivo não encontrado.')

def main():
  if len(sys.argv) == 2:
    nome_arquivo = sys.argv[1]
    programa = leArquivo(nome_arquivo)
    tokens = Scanner(programa).geraTokens()
    print("Tokens", tokens)
    print("Numero de tokens: {}".format(len(tokens)))
  else:
    print('Não foi passado arquivo de entrada.')

if __name__ == "__main__":
  main()
