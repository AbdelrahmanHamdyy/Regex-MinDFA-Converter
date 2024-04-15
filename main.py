from Preprocessing import RegexToPostfix
from NFA import NFA, get_main_chars
from NFAToDFA import DFA
from DFAMinimization import MinimizedDFA

test_cases = {0: '(a*?)*', 1: '(a*)*', 2: '(a*b)(b?a+)', 3: '(a*b*)([a-b]*)', 4: '(a+?a+?)+?b', 5: '(a+a+)+b', 6: '(a|b)*a[ab]?', 7: '[a-c]*', 8: '[A-Ea-c]+1|2[0-9]*K?[ABC](ABC)', 9: 'Aym[o+o+]na?', 10: '[a-f0-9]32', 11: '[a-fA-C]', 12: '[abc](d|e|f)', 13: '[bc]*(cd)+', 14: 'a * b+ [a-z](c?)', 15: 'a*|b*', 16: 'a*b*ca', 17: 'a+|b+', 18: 'a+b', 19: 'a+b*a', 20: 'ab(b|c)*d+', 21: 'employ(er|ee|ment|ing|able)', 22: 'Kam*(o|ou)la'} 

if __name__ == '__main__':
    regex = test_cases[22]
    
    r2p = RegexToPostfix(regex)
    print(r2p)
    
    tokens = get_main_chars(r2p.postfix)
    print("Main Tokens:", tokens)
    
    nfa = NFA(postfix=r2p.postfix)
    nfa.execute()
    NFA.visualize()
    
    dfa = DFA('output/nfa.json', tokens)
    dfa.execute('output/dfa.json')
    DFA.visualize_dfa('output/dfa.json')
    
    minimized_dfa = MinimizedDFA('output/dfa.json', tokens)
    minimized_dfa.minimize()
    MinimizedDFA.visualize('output/minimized_dfa.json')
    