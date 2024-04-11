from enum import Enum
import json

class State:
    def __init__(self, name):
        self.name = name
        self.is_terminating = True
        self.transitions = []

    def add_transition(self, symbol, state):
        self.transitions.append((symbol, state))
        self.is_terminating = False

class NFA:
    def __init__(self, start: State, accept: State):
        self.start = start
        self.accept = accept
        
    def build_nfa(self, postfix):
        '''
        Thomspon's construction algorithm
        '''
        stack = []
        i = 0
        for token in postfix:
            if token == '.':
                nfa2 = stack.pop()
                nfa1 = stack.pop()
                nfa1.accept.add_transition('', nfa2.start)
                stack.append(NFA(nfa1.start, nfa2.accept))
            elif token == '|':
                nfa2 = stack.pop()
                nfa1 = stack.pop()
                start = State(f'S{i}')
                start.add_transition('', nfa1.start)
                start.add_transition('', nfa2.start)
                accept = State(f'S{i + 1}')
                nfa1.accept.add_transition('', accept)
                nfa2.accept.add_transition('', accept)
                stack.append(NFA(start, accept))
            elif token == '*':
                nfa = stack.pop()
                start = State(f'S{i}')
                accept = State(f'S{i + 1}')
                start.add_transition('', nfa.start)
                start.add_transition('', accept)
                nfa.accept.add_transition('', start)
                nfa.accept.add_transition('', accept)
                stack.append(NFA(start, accept))
            elif token == '+':
                nfa = stack.pop()
                start = State(f'S{i}')
                accept = State(f'S{i + 1}')
                start.add_transition('', nfa.start)
                nfa.accept.add_transition('', start)
                nfa.accept.add_transition('', accept)
                stack.append(NFA(start, accept))
            elif token == '?':
                nfa = stack.pop()
                start = State(f'S{i}')
                accept = State(f'S{i + 1}')
                start.add_transition('', nfa.start)
                start.add_transition('', accept)
                nfa.accept.add_transition('', accept)
                stack.append(NFA(start, accept))
            else:
                start = State(f'S{i}')
                accept = State(f'S{i + 1}')
                start.add_transition(token, accept)
                stack.append(NFA(start, accept))
        
            i += 2 if token != '.' else 0
            
        return stack.pop()
    
    def execute(self, postfix):
        nfa = self.build_nfa(postfix)
        self.start = nfa.start
        self.accept = nfa.accept
        
        # Get states
        visited = set()
        states = []
        queue = [self.start]
        visited.add(self.start)
        while queue:
            state = queue.pop(0)
            states.append(state)
            for transition in state.transitions:
                if transition[1] not in visited:
                    visited.add(transition[1])
                    queue.append(transition[1])
        
        result = self.get_json(states)
        # Dump to JSON
        with open('nfa.json', 'w') as f:
            json.dump(result, f, indent=4)
    
    def get_json(self, states):
        '''
        Convert the NFA to a JSON object
        '''
        result = {'startingState': self.start.name}
        for state in states:
            result[state.name] = {
                'isTerminatingState': state.is_terminating,
            }
            for symbol, transition in state.transitions:
                if symbol == '':
                    symbol = 'ε'
                result[state.name][symbol] = transition.name if symbol not in result[state.name] else result[state.name][symbol] + ',' + transition.name
        return result
    
    def visualize(self):
        pass
    
def get_main_chars(regex):
    chars_of_interest = set()
    for token in regex:
        chars_of_interest.add(token)
    return chars_of_interest
    
if __name__ == '__main__':
    nfa = NFA(None, None)
    nfa.execute('ab*|c.')
    print("NFA generated successfully!")
    