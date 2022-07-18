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

if __name__ == "__main__":
  if len(sys.argv) == 2:
    nome_arquivo = sys.argv[1]
    programa = leArquivo(nome_arquivo)
    Scanner(programa).analisar()
  else:
    print('Não foi passado arquivo de entrada.')
