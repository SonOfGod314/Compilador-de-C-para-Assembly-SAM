from grammar import Grammar

def write_ll1_parser(G:Grammar):
    for X in G.nonterminals():
        print('')
        print(f'def {X}(ts,p):')
        first = True
        nt = X
        for rule in G.productions_for(X):
            rhs = G.rhs(rule)
            if first:
                first = False
                print('\t if',end=' ')
            else:
                print('\t elif',end=' ')
            print(f'ts.peek() in p.predict({rule}):')
            for X in rhs:
                if G.is_terminal(X):
                    print(f'\t\tts.match("{X}")')
                else:
                    print(f'\t\t{X}(ts,p)')
        print('\t else:')
        print(f'\t\tprint("Syntax error in {nt}")')
