import json
from collections import defaultdict
import graphviz

class State:
    def __init__(self, name):
        # State label
        self.name = name
        # Flag to indicate if the state is a terminating state
        self.is_terminating = True
        # Initialize transitions to an empty dictionary of lists
        self.transitions = defaultdict(list)

    def add_transition(self, symbol, state):
        '''
        Add a transition from the current state to the next state
        '''
        # Add the next state to the list of states reachable by the given symbol
        self.transitions[symbol].append(state)
        # If a transition is added, we now know that the current state is not a terminating state
        self.is_terminating = False

'''
Reference: https://medium.com/swlh/visualizing-thompsons-construction-algorithm-for-nfas-step-by-step-f92ef378581b
'''

class NFA:
    def __init__(self, start: State = None, accept: State = None, postfix: str = None):
        # Starting state of the NFA
        self.start = start
        # Accepting state of the NFA
        self.accept = accept
        # Postfix expression
        self.postfix = postfix
        
    def build_nfa(self):
        '''
        Thomspon's construction algorithm
        '''
        # Initialize an empty stack to store NFAs during construction
        stack = []
        # Counter to keep track of the state names
        i = 0
        for token in self.postfix:
            if token == '.': # Concatenation operator
                '''
                - Pop two NFAs from the stack, connect the accept state of the first NFA to the start state of the second NFA which accounts for the concatenation of the two NFAs
                - Push the new NFA back to the stack
                '''
                nfa2 = stack.pop()
                nfa1 = stack.pop()
                nfa1.accept.add_transition('ε', nfa2.start)
                stack.append(NFA(nfa1.start, nfa2.accept))
            elif token == '|': # OR operator
                '''
                - Pop two NFAs from the stack, create a new start state and connect it to the start states of the two NFAs, this new start state represents the option of choosing either of the two NFAs
                - Connect the accept states of the two NFAs to a new accept state and push the new NFA back to the stack
                '''
                nfa2 = stack.pop()
                nfa1 = stack.pop()
                start = State(f'S{i}')
                start.add_transition('ε', nfa1.start)
                start.add_transition('ε', nfa2.start)
                accept = State(f'S{i + 1}')
                nfa1.accept.add_transition('ε', accept)
                nfa2.accept.add_transition('ε', accept)
                stack.append(NFA(start, accept))
            elif token == '*': # Kleene star operator
                '''
                - Pop an NFA from the stack, create a new start state and a new accept state
                - Connect the new start state to the start state of the NFA and to the new accept state which represents the option of not consuming the NFA at all
                - Connect the accept state of the NFA to the start state of the NFA for looping and to the new accept state for exiting the loop
                '''
                nfa = stack.pop()
                start = State(f'S{i}')
                accept = State(f'S{i + 1}')
                start.add_transition('ε', nfa.start)
                start.add_transition('ε', accept)
                nfa.accept.add_transition('ε', start)
                nfa.accept.add_transition('ε', accept)
                stack.append(NFA(start, accept))
            elif token == '+': # One or more operator
                '''
                - Pop an NFA from the stack, create a new start state and a new accept state
                - Connect the new start state to the start state of the NFA which means the NFA must be consumed at least once
                - Connect the accept state of the NFA to the start state of the NFA for looping and to the new accept state for ending it
                '''
                nfa = stack.pop()
                start = State(f'S{i}')
                accept = State(f'S{i + 1}')
                start.add_transition('ε', nfa.start)
                nfa.accept.add_transition('ε', start)
                nfa.accept.add_transition('ε', accept)
                stack.append(NFA(start, accept))
            elif token == '?': # Zero or one operator
                '''
                - Pop an NFA from the stack, create a new start state and a new accept state
                - Connect the new start state to the start state of the NFA and to the new accept state which means the NFA can be consumed or not
                - Connect the accept state of the NFA to the new accept state
                '''
                nfa = stack.pop()
                start = State(f'S{i}')
                accept = State(f'S{i + 1}')
                start.add_transition('ε', nfa.start)
                start.add_transition('ε', accept)
                nfa.accept.add_transition('ε', accept)
                stack.append(NFA(start, accept))
            else: # Operand
                '''
                - Simply create a new NFA with a start state and an accept state and connect them with the token
                '''
                start = State(f'S{i}')
                accept = State(f'S{i + 1}')
                start.add_transition(token, accept)
                stack.append(NFA(start, accept))
        
            # Increment the counter by 2 if the token is not a concatenation operator since it doesn't consume a state name
            i += 2 if token != '.' else 0
            
        return stack.pop()
    
    def gather_states(self, nfa, visited, states):
        '''
        Gather all states reachable from the starting state
        '''
        # Add the current state to the list of visited states
        visited.add(nfa.start)
        states.append(nfa.start)
        # Iterate over the transitions from the current state
        for _, next_states in nfa.start.transitions.items():
            for state in next_states:
                # If the next state has not been visited, recursively gather states from that state
                if state not in visited:
                    self.gather_states(NFA(start=state), visited, states)
    
    def execute(self, path):
        # Build the NFA and set the starting and accepting states of the final NFA
        nfa = self.build_nfa()
        self.start = nfa.start
        self.accept = nfa.accept
        
        # Get all states reachable from the starting state
        states = []
        visited = set()
        self.gather_states(nfa, visited, states)
        
        # Get the JSON representation of the NFA
        result = self.get_json(states)
        # Dump to JSON file
        with open(path, 'w') as f:
            json.dump(result, f, indent=4)
    
    def get_json(self, states):
        '''
        Convert the NFA to a JSON object
        '''
        # Initialize the result dictionary with the starting state
        result = {'startingState': self.start.name}
        # Loop through each state and add its transitions to the result dictionary
        for state in states:
            # Initialize the state dictionary with the terminating state flag
            result[state.name] = {
                'isTerminatingState': state.is_terminating,
            }
            # Add the transitions to the state dictionary as string separated by commas
            for symbol, next_states in state.transitions.items():
                result[state.name][symbol] = ','.join([next_state.name for next_state in next_states])
        return result
    
    @staticmethod
    def visualize(path):
        # Initialize the graph
        dot = graphviz.Digraph(comment='NFA Visualization')
        
        # Load the JSON representation of the NFA
        states_json = None
        with open(path, 'r') as f:
            states_json = json.load(f)

        # Pop the starting state from the JSON object
        start_state_name = states_json.pop('startingState')
        
        # Add a starting point to the graph
        dot.node('', label='', shape='point')
        
        # Explicitly add the starting state to the graph
        shape = 'doublecircle' if states_json[start_state_name]['isTerminatingState'] else 'circle'
        dot.node(start_state_name, label=start_state_name, shape=shape)
        
        # Connect the starting point to the starting state
        dot.edge('', start_state_name)

        # Add states to the graph
        for state_name, state_data in states_json.items():
            if state_name == start_state_name:
                continue
            shape = 'doublecircle' if state_data['isTerminatingState'] else 'circle'
            dot.node(state_name, label=state_name, shape=shape)

        # Add transitions
        for state_name, transitions in states_json.items():
            for symbol, next_states in transitions.items():
                # Skip the terminating state flag
                if symbol == 'isTerminatingState':
                    continue
                for next_state in next_states:
                    dot.edge(state_name, next_state, label=symbol if symbol != '\u03b5' else 'ε')

        # Save the graph to a file and optionally view it
        dot.render('nfa.gv', view=False)
    
def get_main_chars(regex):
    '''
    Get the main characters of interest in the regular expression that would form new states
    '''
    chars_of_interest = []
    for token in regex:
        if token not in chars_of_interest and token.isalnum():
            chars_of_interest.append(token)
    return chars_of_interest
    
if __name__ == '__main__':
    nfa = NFA(postfix='AB.AB|*.AB..')
    nfa.execute('nfa.json')
    NFA.visualize('nfa.json')
    print("NFA generated successfully!")
    