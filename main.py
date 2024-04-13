from Preprocessing import RegexToPostfix
from NFA import NFA, get_main_chars
from NFAToDFA import DFA
from DFAMinimization import MinimizedDFA

if __name__ == '__main__':
    regex = "(a|b)*abb"
    tokens = get_main_chars(regex)
    print("Main Tokens:", tokens)
    
    r2p = RegexToPostfix(regex)
    print(r2p)
    
    nfa = NFA(postfix=r2p.postfix)
    nfa.execute('nfa.json')
    NFA.visualize('nfa.json')
    
    dfa = DFA('nfa.json', tokens)
    dfa.execute('dfa.json')
    DFA.visualize_dfa('dfa.json')
    
    minimized_dfa = MinimizedDFA('dfa.json', tokens)
    minimized_dfa.minimize()
    MinimizedDFA.visualize('minimized_dfa.json')
    