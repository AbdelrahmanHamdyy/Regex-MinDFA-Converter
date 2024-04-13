from Preprocessing import RegexToPostfix
from NFA import NFA, get_main_chars
from NFAToDFA import DFA
from DFAMinimization import MinimizedDFA

if __name__ == '__main__':
    regex = "(a|b)*abb[a-z]c?"
    
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
    