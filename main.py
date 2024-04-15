from Preprocessing import RegexToPostfix
from NFA import NFA, get_main_chars
from NFAToDFA import DFA
from DFAMinimization import MinimizedDFA

test_cases = ['(a*?)*','(a*)*','(a*b)(b?a+)','(a*b*)([a-b]*)','(a+?a+?)+?b','(a+a+)+b','(a|b)*a[ab]?','[a-c]*','[A-Ea-c]+1|2[0-9]*K?[ABC](ABC)','Aym[o+o+]na?']

if __name__ == '__main__':
    regex = test_cases[9]
    
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
    