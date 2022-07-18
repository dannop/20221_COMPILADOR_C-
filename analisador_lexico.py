f = open('main.c','r')

operadores = { 
    '=': 'Operador de atribuicao',
    '+': 'Operador de adicao', 
    '-' : 'Operador de subtracao', 
    '/' : 'Operador de divisao', 
    '*': 'Operador de multiplicacao', 
    '<': 'Operador logico (menor que)', 
    '>': 'Operador logico (maior que)', 
    '<=': 'Operador logico (menor ou igual)', 
    '>=': 'Operador logico (maior ou igual)', 
    '==': 'Operador logico (igualdade)', 
    '!=': 'Operador logico (desigualdade)'
}
operadores_chave = operadores.keys()

comentarios = {
    r'//' : 'Comentário de uma linha',
    r'/*' : 'Inicio de um comentário com várias linhas', 
    r'*/' : 'Fim de um comentário com várias linhas', 
    '/**/' : 'Comentário vazio'
}
comentario_chave = comentarios.keys()

macros = {
    r'#\w+' : 'macro'
}
macros_keys = macros.keys()

tipo = {
    'int': 'Inteiro',
    'float' : 'Ponto flutuante', 
    'char': 'Char',
}
tipo_chaves = tipo.keys()

palavra_chave = {
    'return' : 'palavra_chave que indica o resultado gerado de um bloco',
    'if': 'instrucao que indica que vamos testar uma condicao',
    'else': 'istrucao que indica o contraponto do que foi testado no if',
    'while': 'instrucao de execucao de um bloco n vezes',
}
palavra_chave_chaves = palavra_chave.keys()

delimitador = {
    ';':'ponto e virgula indica que aquela acao terminou (;)'
}
delimitador_chave = delimitador.keys()

bloco = {
    '{' : 'Abrindo um bloco de código', 
    '}':'Encerrando um bloco de código'
}
bloco_chaves = bloco.keys()

funcoes_de_construcao = {'printf':'printf coloca na tela o que desejamos'}

nao_sao_identificadores = ['_','-','+','/','*','`','~','!','@','#','$','%','^','&','*','(',')','=','|','"',':',';','{','}','[',']','<','>','?','/']

numerais = ['0','1','2','3','4','5','6','7','8','9','10']

# Flags
dataFlag = False


i = f.read()

count = 0
program =  i.split('\n')

for line in program:
    count = count+1
    print ("Linha #", count,"\n", line)
    
     
    tokens = line.split(' ')
    print ("Os Tokens sao",tokens)
    print ("Linha #",count,'propriedades \n')
    for token in tokens:
        
        if '\r' in token:
            position = token.find('\r')
            token=token[:position]
        # print 1
        
        if token in bloco_chaves:
            print (bloco[token])
        if token in operadores_chave:
            print ("O operador aqui eh: ", operadores[token])
        if token in comentario_chave:
            print ("O tipo de comentário aqui eh: ", comentarios[token])
        if token in macros_keys:
            print ("O macro eh: ", macros[token])
        if '()' in token:
            print ("Aqui temos uma funcao chamada", token)
        
        if dataFlag == True and (token not in nao_sao_identificadores) and ('()' not in token):
            print ("Identificador: ",token)
        if token in tipo_chaves:
            print ("O tipo usado eh: ", tipo[token])
            dataFlag = True
        
        if token in palavra_chave_chaves:
            print (palavra_chave[token])
            
        if token in delimitador:
            print ("delimitador" , delimitador[token])
        if token in numerais:
            print (token,type(int(token)))
            
    dataFlag = False   
            
    
    print ("________________________")
    

f.close()