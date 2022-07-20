# Compilador em Python para C-

## Analisador Léxico
Scanner para gerar Tokens válidos para serem analisados. 

## Analisador Sintático
- Analisador sintático via gramátca LL1 ou como parser descendente recursivo. 
- O parser deve considerar também o tratamento de erros, indicando para o usuário em que linha do código fonte de entrada o erro ocorreu. 
- Implementação de uma tabela de símbolos e verificando caso um identificador seja usado sem ter sido declarado.

## Compilador Final
- Analisador léxico
- Analisador sintático
- Tratamento de erros léxicos e sintáticos
- Códigos fonte da linguagem escolhida para realizar a análise léxica e sintática

## Como rodar

Para executar o programa, coloque o nome do arquivo em txt logo apos o comando, exemplo:

```
python3 main.py main.txt
```