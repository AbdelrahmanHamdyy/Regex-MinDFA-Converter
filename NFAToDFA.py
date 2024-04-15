import json
import graphviz

class DFA:
    def __init__(self, path,regex_chars):
        self.data = self.load_data(path)
        self.regex_chars = regex_chars
        self.result_states = None

    @staticmethod
    def load_data(path):
        with open(path, 'r') as file:
            data = json.load(file)
        return data

    @staticmethod
    def get_target_chars(regex_chars):
        return {char: [] for char in regex_chars}

    @staticmethod
    def get_all_needed_states(data, starting_state, incoming_letter, is_start_state=False):
        final_states = {starting_state} if is_start_state else set()
        if incoming_letter in data[starting_state]:
            new_states = data[starting_state][incoming_letter].split(',')
            final_states |= set(new_states)
        result = set()
        for state in final_states:
            result |= DFA.get_epsilons(data, state)
        return result

    @staticmethod
    def get_epsilons(data, starting_state):
        stack = [starting_state]
        result_state = set()
        while stack:
            state = stack.pop()
            if state not in result_state:
                result_state.add(state)
                if 'epsilon' in data[state]:
                    epsilons = data[state]['epsilon'].split(',')
                    stack.extend(epsilons)
        return result_state

    def get_required_data(self, regex_chars):
        terminal_states = {key for key, value in self.data.items() if "isTerminatingState" in value and value["isTerminatingState"]}
        target_chars = self.get_target_chars(regex_chars)
        values_generated_from_taking_char = {}

        for char in regex_chars:
            for key, value in self.data.items():
                if char in value and key != "startingState":
                    target_chars[char].append(key)
                    values_generated_from_taking_char[key] = self.get_all_needed_states(self.data, key, char)

        return terminal_states, target_chars, values_generated_from_taking_char

    def create_dfa(self, terminal_states, regex_chars, char_values, target_chars):
        current_state_num = 0
        states_increment_num = 1
        starting_state = sorted(self.get_all_needed_states(self.data, self.data['startingState'], '', True))
        is_terminal_state = any(letter in terminal_states for letter in starting_state)

        starting_state_object = {
            "value": starting_state,
            "isTerminatingState": is_terminal_state,
        }
        result_states = {
            "startingState": "S0",
            "S0": starting_state_object,
        }

        while current_state_num != states_increment_num:
            current_state_idx = 'S' + str(current_state_num)
            current_state = result_states[current_state_idx]

            for char in regex_chars:
                result = set()
                for letter in current_state["value"]:
                    if letter in char_values and letter in target_chars[char]:
                        result |= char_values[letter]
                if not result:
                    continue
                result = sorted(result)
                is_terminal_state = any(letter in terminal_states for letter in result)

                referenced_state = "NotFound"
                for key, value in result_states.items():
                    if "value" in value:
                        if value["value"] == result:
                            referenced_state = key
                            break

                if referenced_state == "NotFound":
                    new_state_idx = 'S' + str(states_increment_num)
                    states_increment_num += 1
                    new_state_obj = {
                        "value": result,
                        "isTerminatingState": is_terminal_state
                    }
                    result_states[new_state_idx] = new_state_obj
                    referenced_state = new_state_idx
                current_state[char] = referenced_state
            current_state_num += 1
        self.result_states = result_states

    @staticmethod
    def write_data(result_states, output_path):
        for key, value in result_states.items():
            if "value" in value:
                del value['value']

        with open(output_path, "w") as json_file:
            json.dump(result_states, json_file)

    @staticmethod
    def visualize_dfa(path):
        dot = graphviz.Digraph(comment='DFA Visualization')
        states_json = None
        with open(path, 'r') as f:
            states_json = json.load(f)

        starting_state_name = states_json.pop('startingState')

        for state_name, state_data in states_json.items():
            shape = 'doublecircle' if state_data['isTerminatingState'] else 'circle'
            dot.node(state_name, label=state_name, shape=shape)

        for state_name, transitions in states_json.items():
            for symbol, next_state in transitions.items():
                if symbol == 'isTerminatingState':
                    continue
                dot.edge(state_name, next_state, label=symbol if symbol != '\u03b5' else 'ε')
        dot.render('output/dfa.gv', view=False)

    def execute(self, output_path):
        terminal_states, target_chars, values_generated_from_taking_char = self.get_required_data(self.regex_chars)
        self.create_dfa(terminal_states, self.regex_chars, values_generated_from_taking_char, target_chars)
        self.write_data(self.result_states, output_path)

if __name__ == "__main__":
    dfa = DFA('nu3man6.json',['a','b'])
    dfa.execute( 'DFA.json')
    DFA.visualize_dfa('DFA.json')
