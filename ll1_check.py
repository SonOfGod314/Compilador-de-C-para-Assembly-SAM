from grammar import Grammar
from predict import predict_algorithm


def is_ll1(G: Grammar, pred_alg: predict_algorithm) -> bool:
    for A in G.nonterminals():
        print(f'************* Checking LL1 for non-terminal {A}')
        pred_set = set()
        for p in G.productions_for(A):
            print(f'Rule {G.lhs(p)} -> {G.rhs(p)}')
            pred = pred_alg.predict(p)
            print(f'{pred} and {pred_set}')
            if not pred_set.isdisjoint(pred):
                print('!!!!!!!!!!!!!!! NOT LL1')
                return False
            pred_set.update(pred)
    return True
