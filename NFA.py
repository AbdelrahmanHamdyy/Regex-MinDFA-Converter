from enum import Enum
import json

class StateType(Enum):
    START = 1
    ACCEPT = 2

class State:
    def __init__(self, name, type: StateType):
        self.name = name
        self.type = type
        self.is_terminating = True
        self.transitions = []

    def add_transition(self, symbol, state):
        self.transitions.append((symbol, state))
        self.is_terminating = False

    def get_transitions(self, symbol):
        if symbol in self.transitions:
            return self.transitions[symbol]
        else:
            return set()

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
                nfa1.accept.type = StateType.START
                nfa1.accept.add_transition('', nfa2.start)
                stack.append(NFA(nfa1.start, nfa2.accept))
            elif token == '|':
                nfa2 = stack.pop()
                nfa1 = stack.pop()
                start = State(f'S{i}', StateType.START)
                start.add_transition('', nfa1.start)
                start.add_transition('', nfa2.start)
                accept = State(f'S{i + 1}', StateType.ACCEPT)
                nfa1.accept.add_transition('', accept)
                nfa2.accept.add_transition('', accept)
                stack.append(NFA(start, accept))
            elif token == '*':
                nfa = stack.pop()
                start = State(f'S{i}', StateType.START)
                accept = State(f'S{i + 1}', StateType.ACCEPT)
                start.add_transition('', nfa.start)
                start.add_transition('', accept)
                nfa.accept.add_transition('', start)
                nfa.accept.add_transition('', accept)
                stack.append(NFA(start, accept))
            elif token == '+':
                nfa = stack.pop()
                start = State(f'S{i}', StateType.START)
                accept = State(f'S{i + 1}', StateType.ACCEPT)
                start.add_transition('', nfa.start)
                nfa.accept.add_transition('', start)
                nfa.accept.add_transition('', accept)
                stack.append(NFA(start, accept))
            elif token == '?':
                nfa = stack.pop()
                start = State(f'S{i}', StateType.START)
                accept = State(f'S{i + 1}', StateType.ACCEPT)
                start.add_transition('', nfa.start)
                start.add_transition('', accept)
                nfa.accept.add_transition('', accept)
                stack.append(NFA(start, accept))
            else:
                start = State(f'S{i}', StateType.START)
                accept = State(f'S{i + 1}', StateType.ACCEPT)
                start.add_transition(token, accept)
                stack.append(NFA(start, accept))
        
            i += 2 if token != '.' else 0
            
        return stack.pop()
    
    def execute(self, postix):
        nfa = self.build_nfa(postix)
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
    
if __name__ == '__main__':
    nfa = NFA(None, None)
    nfa.execute('ab*|c.')
    print("NFA generated successfully!")
    