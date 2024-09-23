import ply.lex as lex
from grammar import Grammar
from predict import predict_algorithm
from token_sequence import token_sequence
from ll1_check import is_ll1
import write_ll1_parser
import sys

# LEXER

tokens = ('TipoDado', 'Number', 'Add', 'Sub', 'Mul', 'Div', 'AbreChave',
          'FechaChave', 'AbreParenteses', 'FechaParenteses', 'AbreColchete',
          'FechaColchete', 'Ponto', 'PontoVirgula', 'Virgula', 'DoisPontos',
          'IgualAtribuidor', 'And', 'Or', 'Not', 'Maior', 'Menor',
          'MaiorIgual', 'MenorIgual', 'Igual', 'Diferente', 'While', 'If',
          'Else', 'Endif', 'Printf', 'Variavel', 'Void', 'Main', 'QuebraLinha')

t_Number = r'-?\d+(\.\d+)?'
t_Add = r'\+'
t_Sub = r'-'
t_Mul = r'\*'
t_Div = r'/'
t_AbreChave = r'\{'
t_FechaChave = r'\}'
t_AbreParenteses = r'\('
t_FechaParenteses = r'\)'
t_AbreColchete = r'\['
t_FechaColchete = r'\]'
t_PontoVirgula = r';'
t_Virgula = r','
t_DoisPontos = r':'
t_IgualAtribuidor = r'='
t_And = r'&&'
t_Or = r'\|\|'
t_Not = r'!'
t_Maior = r'>'
t_Menor = r'<'
t_MaiorIgual = r'>='
t_MenorIgual = r'<='
t_Igual = r'=='
t_Diferente = r'!='
t_Ponto = r'\.'

def t_TipoDado(t):
    r'int|float'
    return t
   
def t_While(t):
    r'while'
    return t
   
def t_If(t):
    r'if'
    return t
   
def t_Endif(t):
    r'endif'
    return t

def t_Else(t):
    r'else'
    return t

def t_Printf(t):
    r'printf'
    return t

def t_Main(t):
    r'main'
    return t

def t_Variavel(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    return t

t_ignore = ' \t'

def t_QuebraLinha(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
    pass

def t_error(t):
    print(f"Caractere ilegal '{t.value[0]}'")
    t.lexer.skip(1)

lexer = lex.lex()

arquivo_c = 'codigo.c'
with open(arquivo_c, 'r') as file:
    data = file.read()

lexer.input(data)

endereco = 0
tokens_list = []
tipodado_enc = 0
var_enc = 0
modo_atribuicao = 0
modo_if = 0
modo_while = 0
end_while = 0
end_aux = 0
print_aux = 0
op_aux = 'None'
comp_aux = 'None'
neg = 0
var_dict = {}
sint_err = 0

#criacao da lista de tokens e verificacao de dupla-atribuicao
for tok in lexer:
    tokens_list.append(tok.type)
    if tok.type == 'TipoDado':
       tipodado_enc = 1
    if tok.type == 'Variavel' and tipodado_enc == 1 and tok.value not in var_dict:
       var_dict[tok.value] = endereco   
       endereco = endereco + 1
       tipodado_enc = 0
    elif tok.type == 'Variavel' and tipodado_enc == 1 and tok.value in var_dict:
       print('')
       print(f'Lexical error: a variavel {tok.value} foi declarada mais de uma vez.')
       exit(0)

print('')
print('Tabela de Variaveis')
print('--------------------')
for var in var_dict:
    print(f'{var} : {var_dict[var]}')
print('')

# PARSER

def print_grammar(G: Grammar) -> None:
    print('Terminais:', ' '.join([x for x in G.terminals()]))
    print('Não-terminais:', ' '.join([X for X in G.nonterminals()]))
    # print(G.productions())
    print(
        'Produções:', ' '.join([
            'id: ' + str(p) + ' ' + str(G.lhs(p)) + '->' + str(G.rhs(p))
            for p in G.productions()
        ]))


def my_grammar() -> Grammar:
  G = Grammar()
  G.add_nonterminal('program')  
  G.add_nonterminal('main') 
  G.add_nonterminal('listaDeclarations')  
  G.add_nonterminal('declaration') 
  G.add_nonterminal('listaStatements')  
  G.add_nonterminal('statement')  
  G.add_nonterminal('else') 
  G.add_nonterminal('expr')
  G.add_nonterminal('moreExpr')
  G.add_nonterminal('logOp')
  G.add_nonterminal('relational_op')
  G.add_nonterminal('expression')
  G.add_nonterminal('logExpr') 
  G.add_nonterminal('expressionTail')
  G.add_nonterminal('termTail')
  G.add_nonterminal('term')  
  G.add_nonterminal('factor')  
  G.add_nonterminal('end')  
  G.add_terminal('TipoDado')  
  G.add_terminal('Number')  
  G.add_terminal('Add')  
  G.add_terminal('Sub')
  G.add_terminal('Mul') 
  G.add_terminal('Div')  
  G.add_terminal('AbreChave')  
  G.add_terminal('FechaChave')  
  G.add_terminal('AbreParenteses')  
  G.add_terminal('FechaParenteses')  
  G.add_terminal('AbreColchete')  
  G.add_terminal('FechaColchete')  
  G.add_terminal('Ponto')  
  G.add_terminal('PontoVirgula')  
  G.add_terminal('Virgula')  
  G.add_terminal('DoisPontos')  
  G.add_terminal('IgualAtribuidor')  
  G.add_terminal('And')  
  G.add_terminal('Or')  
  G.add_terminal('Not')  
  G.add_terminal('Maior')  
  G.add_terminal('Menor')  
  G.add_terminal('MaiorIgual')  
  G.add_terminal('MenorIgual')  
  G.add_terminal('Igual')  
  G.add_terminal('Diferente')  
  G.add_terminal('While')  
  G.add_terminal('If')  
  G.add_terminal('Else')  
  G.add_terminal('Endif')  
  G.add_terminal('Printf')  
  G.add_terminal('Variavel')  
  G.add_terminal('Void')  
  G.add_terminal('Main')  
  G.add_terminal('QuebraLinha')  
  G.add_production('program',['main', 'listaDeclarations', 'listaStatements', 'end'])
  G.add_production('main',['TipoDado', 'Main', 'AbreParenteses', 'FechaParenteses', 'AbreChave'])  
  G.add_production('listaDeclarations',['declaration', 'listaDeclarations'])  
  G.add_production('listaDeclarations', [])  
  G.add_production('declaration',['TipoDado', 'Variavel', 'PontoVirgula'])  
  G.add_production('listaStatements',['statement', 'listaStatements'])  
  G.add_production('listaStatements', [])  
  G.add_production('statement',['Variavel', 'IgualAtribuidor', 'expression', 'PontoVirgula'])  
  G.add_production('statement', ['While', 'logExpr', 'AbreChave', 'listaStatements', 'FechaChave']) 
  G.add_production('statement', ['If', 'logExpr', 'AbreChave', 'listaStatements', 'FechaChave','else', 'Endif'])
  G.add_production('else', ['Else', 'AbreChave', 'listaStatements', 'FechaChave', 'else']) 
  G.add_production('else', []) 
  G.add_production('statement', ['Printf', 'AbreParenteses', 'Variavel', 'FechaParenteses','PontoVirgula'])  
  G.add_production('expr', ['AbreParenteses', 'expression', 'relational_op', 'expression', 'FechaParenteses'])
  G.add_production('logExpr', ['expr', 'moreExpr'])
  G.add_production('moreExpr', ['logOp', 'expr'])
  G.add_production('moreExpr', [])
  G.add_production('logOp', ['And'])
  G.add_production('logOp', ['Or'])
  G.add_production('relational_op', ['Maior'])  
  G.add_production('relational_op', ['Menor']) 
  G.add_production('relational_op', ['MaiorIgual']) 
  G.add_production('relational_op', ['MenorIgual']) 
  G.add_production('relational_op', ['Igual']) 
  G.add_production('relational_op', ['Diferente']) 
  G.add_production('expression', ['term', 'expressionTail'])  
  G.add_production('expressionTail', ['Add', 'term', 'expressionTail'])
  G.add_production('expressionTail', ['Sub', 'term', 'expressionTail'])  
  G.add_production('expressionTail', [])
  G.add_production('term', ['factor', 'termTail'])  
  G.add_production('termTail', ['Mul', 'factor', 'termTail'])
  G.add_production('termTail', ['Div', 'factor', 'termTail']) 
  G.add_production('termTail', [])   
  G.add_production('factor',['AbreParenteses', 'expression', 'FechaParenteses'])  
  G.add_production('factor', ['Number'])  
  G.add_production('factor', ['Variavel'])  
  G.add_production('end', ['FechaChave'])  
  return G

def program(ts,p):
     if ts.peek() in p.predict(53):
        main(ts,p)
        listaDeclarations(ts,p)
        listaStatements(ts,p)
        end(ts,p)
     else:
        print("Syntax error in program")
        global sint_err
        sint_err = 1

def main(ts,p):
     if ts.peek() in p.predict(54):
        ts.match("TipoDado")
        ts.match("Main")
        ts.match("AbreParenteses")
        ts.match("FechaParenteses")
        ts.match("AbreChave")
     else:
        print("Syntax error in main")
        global sint_err
        sint_err = 1

def listaDeclarations(ts,p):
     if ts.peek() in p.predict(55):
        declaration(ts,p)
        listaDeclarations(ts,p)
     elif ts.peek() in p.predict(56):
        return
     else:
        print("Syntax error in listaDeclarations")
        global sint_err
        sint_err = 1

def declaration(ts,p):
     if ts.peek() in p.predict(57):
        ts.match("TipoDado")
        ts.match("Variavel")
        ts.match("PontoVirgula")
     else:
        print("Syntax error in declaration")
        global sint_err
        sint_err = 1

def listaStatements(ts,p):
     if ts.peek() in p.predict(58):
        statement(ts,p)
        listaStatements(ts,p)
     elif ts.peek() in p.predict(59):
        return
     else:
        print("Syntax error in listaStatements")
        global sint_err
        sint_err = 1

def statement(ts,p):
     if ts.peek() in p.predict(60):
        ts.match("Variavel")
        ts.match("IgualAtribuidor")
        expression(ts,p)
        ts.match("PontoVirgula")
     elif ts.peek() in p.predict(61):
        ts.match("While")
        logExpr(ts,p)
        ts.match("AbreChave")
        listaStatements(ts,p)
        ts.match("FechaChave")
     elif ts.peek() in p.predict(62):
        ts.match("If")
        logExpr(ts,p)
        ts.match("AbreChave")
        listaStatements(ts,p)
        ts.match("FechaChave")
        else_(ts,p)
        ts.match("Endif")
     elif ts.peek() in p.predict(65):
        ts.match("Printf")
        ts.match("AbreParenteses")
        ts.match("Variavel")
        ts.match("FechaParenteses")
        ts.match("PontoVirgula")
     else:
        print("Syntax error in statement")
        global sint_err
        sint_err = 1

def else_(ts,p):
     if ts.peek() in p.predict(63):
        ts.match("Else")
        ts.match("AbreChave")
        listaStatements(ts,p)
        ts.match("FechaChave")
        else_(ts,p)
     elif ts.peek() in p.predict(64):
        return
     else:
        print("Syntax error in else")
        global sint_err
        sint_err = 1

def expr(ts,p):
     if ts.peek() in p.predict(66):
        ts.match("AbreParenteses")
        expression(ts,p)
        relational_op(ts,p)
        expression(ts,p)
        ts.match("FechaParenteses")
     else:
        print("Syntax error in expr")
        global sint_err
        sint_err = 1

def moreExpr(ts,p):
     if ts.peek() in p.predict(68):
        logOp(ts,p)
        expr(ts,p)
     elif ts.peek() in p.predict(69):
        return
     else:
        print("Syntax error in moreExpr")
        global sint_err
        sint_err = 1

def logOp(ts,p):
     if ts.peek() in p.predict(70):
        ts.match("And")
     elif ts.peek() in p.predict(71):
        ts.match("Or")
     else:
        print("Syntax error in logOp")
        global sint_err
        sint_err = 1

def relational_op(ts,p):
     if ts.peek() in p.predict(72):
        ts.match("Maior")
     elif ts.peek() in p.predict(73):
        ts.match("Menor")
     elif ts.peek() in p.predict(74):
        ts.match("MaiorIgual")
     elif ts.peek() in p.predict(75):
        ts.match("MenorIgual")
     elif ts.peek() in p.predict(76):
        ts.match("Igual")
     elif ts.peek() in p.predict(77):
        ts.match("Diferente")
     else:
        print("Syntax error in relational_op")
        global sint_err
        sint_err = 1

def expression(ts,p):
     if ts.peek() in p.predict(78):
        term(ts,p)
        expressionTail(ts,p)
     else:
        print("Syntax error in expression")
        global sint_err
        sint_err = 1

def logExpr(ts,p):
     if ts.peek() in p.predict(67):
        expr(ts,p)
        moreExpr(ts,p)
     else:
        print("Syntax error in logExpr")
        global sint_err
        sint_err = 1

def expressionTail(ts,p):
     if ts.peek() in p.predict(79):
        ts.match("Add")
        term(ts,p)
        expressionTail(ts,p)
     elif ts.peek() in p.predict(80):
        ts.match("Sub")
        term(ts,p)
        expressionTail(ts,p)
     elif ts.peek() in p.predict(81):
        return
     else:
        print("Syntax error in expressionTail")
        global sint_err
        sint_err = 1

def termTail(ts,p):
     if ts.peek() in p.predict(83):
        ts.match("Mul")
        factor(ts,p)
        termTail(ts,p)
     elif ts.peek() in p.predict(84):
        ts.match("Div")
        factor(ts,p)
        termTail(ts,p)
     elif ts.peek() in p.predict(85):
        return
     else:
        print("Syntax error in termTail")
        global sint_err
        sint_err = 1

def term(ts,p):
     if ts.peek() in p.predict(82):
        factor(ts,p)
        termTail(ts,p)
     else:
        print("Syntax error in term")
        global sint_err
        sint_err = 1

def factor(ts,p):
     if ts.peek() in p.predict(86):
        ts.match("AbreParenteses")
        expression(ts,p)
        ts.match("FechaParenteses")
     elif ts.peek() in p.predict(87):
        ts.match("Number")
     elif ts.peek() in p.predict(88):
        ts.match("Variavel")
     else:
        print("Syntax error in factor")
        global sint_err
        sint_err = 1

def end(ts,p):
     if ts.peek() in p.predict(89):
        ts.match("FechaChave")
     else:
        print("Syntax error in end")
        global sint_err
        sint_err = 1

def PrintGrammar(G: Grammar) -> None:
    for x in G.productions():
        print(x, G.lhs(x), '->', G.rhs(x))

if __name__ == '__main__':
    ts = token_sequence(tokens_list)
    G = my_grammar()
    predict_alg = predict_algorithm(G)
    #print('LL(1) ? ', is_ll1(G, predict_alg))
    #write_ll1_parser.write_ll1_parser(G)
    #PrintGrammar(G)
    program(ts, predict_alg)
    if sint_err == 1:
      print('')
      print('Geracao do arquivo SAM cancelada.')
      exit(0)
    else:
      print(f'O arquivo "{arquivo_c}" nao possui erros de sintaxe.')
    print('')

# GERAÇÃO DO ARQUIVO EM ASSEMBLY SAM

sam_filename = "output.sam"
sam_file = open(sam_filename, "w")
sys.stdout = sam_file

print(f'ADDSP {len(var_dict)}')
lexer.input(data)
for tok in lexer:
   if tok.type == 'Variavel' and modo_atribuicao == 0:
      var_enc = 1
      end_aux = var_dict[tok.value]
      if print_aux == 2 and end_aux != 0:
         print(f'PUSHABS {end_aux}')
         print('STOREABS 0')
         print(f'ADDSP -{len(var_dict)-1}')
         print('STOP')
         print_aux = 0
      if print_aux == 2 and end_aux == 0:
         print(f'ADDSP -{len(var_dict)-1}')
         print('STOP')
         print_aux = 0
   if tok.type == 'Variavel' and modo_atribuicao == 1:
      print(f'PUSHABS {var_dict[tok.value]}')
      if op_aux != 'None':
         print(f'{op_aux}')
         op_aux = 'None'
   if tok.type == 'Variavel' and modo_if == 1:
      print(f'PUSHABS {var_dict[tok.value]}')
      if comp_aux != 'None':
         print(f'{comp_aux}')
         if neg == 1:
            print('NOT')
            neg = 0
         print('JUMPC ELSE')
         modo_if = 0
         comp_aux = 'None'
   if tok.type == 'Variavel' and modo_while == 1:
      print(f'PUSHABS {var_dict[tok.value]}')
      if comp_aux != 'None':
         print(f'{comp_aux}')
         if neg == 1:
            print('NOT')
            neg = 0
         print('JUMPC ENDWHILE')
         modo_while = 0
         comp_aux = 'None'
   if tok.type == 'Number' and modo_atribuicao == 1: 
      print(f'PUSHIMM {tok.value}')
      if op_aux != 'None':
         print(f'{op_aux}')
         op_aux = 'None'
   if tok.type == 'Number' and modo_if == 1:
      print(f'PUSHIMM {tok.value}')
      if comp_aux != 'None':
         print(f'{comp_aux}')
         if neg == 1:
            print('NOT')
            neg = 0
         print('JUMPC ELSE')
         modo_if = 0
         comp_aux = 'None'
   if tok.type == 'Number' and modo_while == 1:
      print(f'PUSHIMM {tok.value}')
      if comp_aux != 'None':
         print(f'{comp_aux}')
         if neg == 1:
            print('NOT')
            neg = 0
         print('JUMPC ENDWHILE')
         modo_while = 0
         comp_aux = 'None'
   if tok.type == 'IgualAtribuidor' and var_enc == 1:
      modo_atribuicao = 1
      var_enc = 0
   if tok.type == 'Add':
      op_aux = 'ADD'
   if tok.type == 'Sub':
      op_aux = 'SUB'
   if tok.type == 'Mul':
      op_aux = 'TIMES'
   if tok.type == 'Div':
      op_aux = 'DIV'
   if tok.type == 'If':
      modo_if = 1
   if tok.type == 'Else':
      print('ELSE')
   if tok.type == 'Maior':
      comp_aux = 'GREATER'
      neg = 1
   if tok.type == 'Menor':
      comp_aux = 'LESS'
      neg = 1
   if tok.type == 'MaiorIgual':
      comp_aux = 'LESS'
   if tok.type == 'MenorIgual':
      comp_aux = 'GREATER'
   if tok.type == 'Igual':
      comp_aux = 'EQUAL'
      neg = 1
   if tok.type == 'Diferente':
      comp_aux = 'EQUAL'
   if tok.type == 'While':
      print('WHILE')
      modo_while = 1
      end_while = 1
   if tok.type == 'FechaChave' and end_while == 1:
      print('JUMP WHILE')
      print('ENDWHILE')
      end_while = 0
   if tok.type == 'Printf':
      print_aux = 1
   if tok.type == 'AbreParenteses' and print_aux == 1:
      print_aux = 2
   if tok.type == 'PontoVirgula' and modo_atribuicao == 1:
      print(f'STOREABS {end_aux}')
      end_aux = 0
      modo_atribuicao = 0

sam_file.close()
sys.stdout = sys.__stdout__
print('Novo arquivo gerado: output.sam')
print('')

with open("output.sam") as arquivo:
  linhas = arquivo.readlines()
pilha = []
pos = len(pilha)
ignorar = 0
loop = 1
chave = 'x'

print('Execucao do arquivo SAM')
print('--------------------------')
print('')
while loop == 1:
  for item in linhas:
    if ignorar == 1 and chave in item:
      ignorar = 0
      continue
    if ignorar == 0:
      print(pilha)
      if 'PUSHIMM' in item:
          pilha.append(int(item[8:]))
      elif 'ADDSP' in item:
        mod = int(item[6:])
        i = 0
        if mod > 0:
          while(i<mod):
              pilha.append(' ')
              i+=1
        elif mod < 0:
          mod = abs(mod)
          while(i<mod):
            pilha.pop(pos-1)
            i+=1
      elif 'ADD' in item:
          pilha[pos-2] = pilha[pos-2] + pilha[pos-1]
          pilha.pop(pos-1)
      elif 'SUB' in item:
          pilha[pos-2] = pilha[pos-2] - pilha[pos-1]
          pilha.pop(pos-1)
      elif 'TIMES' in item:
          pilha[pos-2] = pilha[pos-2] * pilha[pos-1]
          pilha.pop(pos-1)
      elif 'DIV' in item:
          pilha[pos-2] = pilha[pos-2] / pilha[pos-1]
          pilha.pop(pos-1)
      elif 'STOP' in item:
          loop = 0
          break
      elif 'NOT' in item:
          pilha[pos-1] = pilha[pos-1]*(-1) 
      elif 'GREATER' in item:
          a = pilha[pos-1]
          b = pilha[pos-2]
          if (b>a):
            pilha[pos-2] = 1
            pilha.pop(pos-1)
          else:
            pilha[pos-2] = 0
            pilha.pop(pos-1)
      elif 'LESS' in item:
          a = pilha[pos-1]
          b = pilha[pos-2]
          if (b<a):
            pilha[pos-2] = 1
            pilha.pop(pos-1)
          else:
            pilha[pos-2] = 0
            pilha.pop(pos-1)
      elif 'EQUAL' in item:
          a = pilha[pos-1]
          b = pilha[pos-2]
          if (a==b):
            pilha[pos-2] = 1
            pilha.pop(pos-1)
          else:
            pilha[pos-2] = 0
            pilha.pop(pos-1)
      elif 'STOREABS' in item:
        valor = int(item[9:])
        pilha[valor] = pilha[pos-1]
        pilha.pop(pos-1)
      elif 'PUSHABS' in item:
        valor = int(item[8:])
        pilha.append(pilha[valor])
      elif 'JUMPC' in item:
        chave = item[6:]
        if pilha[pos-1] == 1:
          ignorar = 1
        pilha.pop(pos-1)
      elif 'JUMP' in item:
        chave = item[5:]
        ignorar = 1
        break
      elif 'ISNIL' in item:
        if pilha[pos-1] == 0:
          pilha[pos-1] = 1
        elif pilha[pos-1] == 1:
          pilha[pos-1] = 0

print(f'Exit Code: {pilha}')
