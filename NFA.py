import json
from collections import defaultdict
import graphviz

class State:
    def __init__(self, name):
        self.name = name
        self.is_terminating = True
        self.transitions = defaultdict(list)

    def add_transition(self, symbol, state):
        self.transitions[symbol].append(state)
        self.is_terminating = False

class NFA:
    def __init__(self, start: State = None, accept: State = None):
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
                nfa1.accept.add_transition('ε', nfa2.start)
                stack.append(NFA(nfa1.start, nfa2.accept))
            elif token == '|':
                nfa2 = stack.pop()
                nfa1 = stack.pop()
                start = State(f'S{i}')
                start.add_transition('ε', nfa1.start)
                start.add_transition('ε', nfa2.start)
                accept = State(f'S{i + 1}')
                nfa1.accept.add_transition('ε', accept)
                nfa2.accept.add_transition('ε', accept)
                stack.append(NFA(start, accept))
            elif token == '*':
                nfa = stack.pop()
                start = State(f'S{i}')
                accept = State(f'S{i + 1}')
                start.add_transition('ε', nfa.start)
                start.add_transition('ε', accept)
                nfa.accept.add_transition('ε', start)
                nfa.accept.add_transition('ε', accept)
                stack.append(NFA(start, accept))
            elif token == '+':
                nfa = stack.pop()
                start = State(f'S{i}')
                accept = State(f'S{i + 1}')
                start.add_transition('ε', nfa.start)
                nfa.accept.add_transition('ε', start)
                nfa.accept.add_transition('ε', accept)
                stack.append(NFA(start, accept))
            elif token == '?':
                nfa = stack.pop()
                start = State(f'S{i}')
                accept = State(f'S{i + 1}')
                start.add_transition('ε', nfa.start)
                start.add_transition('ε', accept)
                nfa.accept.add_transition('ε', accept)
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
            for _, next_states in state.transitions.items():
                for transition in next_states:
                    if transition not in visited:
                        visited.add(transition)
                        queue.append(transition)
        
        result = self.get_json(states)
        # Dump to JSON
        with open('nfa.json', 'w') as f:
            json.dump(result, f, indent=4)
            
        # Visualize the NFA
        self.visualize()
    
    def get_json(self, states):
        '''
        Convert the NFA to a JSON object
        '''
        result = {'startingState': self.start.name}
        for state in states:
            result[state.name] = {
                'isTerminatingState': state.is_terminating,
            }
            for symbol, next_states in state.transitions.items():
                result[state.name].setdefault(symbol, []).extend([transition.name for transition in next_states])
        return result
    
    def visualize(self):
        dot = graphviz.Digraph(comment='NFA Visualization')
        states_json = None
        with open('nfa.json', 'r') as f:
            states_json = json.load(f)

        # Handle starting state separately
        starting_state_name = states_json.pop('startingState')

        # Add states to the graph
        for state_name, state_data in states_json.items():
            shape = 'doublecircle' if state_data['isTerminatingState'] else 'circle'
            dot.node(state_name, label=state_name, shape=shape)

        # Add starting state explicitly
        dot.node(starting_state_name, label=starting_state_name, shape='circle')

        # Add transitions
        for state_name, transitions in states_json.items():
            for symbol, next_states in transitions.items():
                # Skip the terminating state flag
                if symbol == 'isTerminatingState':
                    continue
                for next_state in next_states:
                        dot.edge(state_name, next_state, label=symbol if symbol != '\u03b5' else 'ε')

        dot.render('nfa.gv', view=True)
    
def get_main_chars(regex):
    chars_of_interest = set()
    for token in regex:
        chars_of_interest.add(token)
    return chars_of_interest
    
if __name__ == '__main__':
    nfa = NFA()
    nfa.execute('ab*|c.')
    print("NFA generated successfully!")
    