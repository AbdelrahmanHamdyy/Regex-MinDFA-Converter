import json
import copy
import graphviz

class MinimizedDFA:
    def __init__(self,path,char_regex):
        self.load(path)
        self.char_regex = char_regex

    def load(self, file_path):
        with open(file_path, 'r') as file:
            self.data = json.load(file)

    def initialize_groups(self):
        print(self.data)
        non_terminating_group = []
        terminating_group = []
        groups = [non_terminating_group, terminating_group]
        number_of_states = 0
        state_to_number_map = {}
        for key, value in self.data.items():
            if "isTerminatingState" in value:
                number_of_states += 1
                state_to_number_map[key] = int(key.split('S')[1])
                if value["isTerminatingState"]:
                    terminating_group.append(key)
                else:
                    non_terminating_group.append(key)
        return groups

    def get_group_of_output(self, groups, point):
        for i, group in enumerate(groups):
            if point in group:
                return i

    def get_groups_after_splitting(self, groups):
        is_there_a_change = True
        while is_there_a_change:
            is_there_a_change = False
            new_groups = []
            for group in groups:
                if len(group) == 1:
                    continue
                for char in self.char_regex:
                    values = set()
                    for element in group:
                        previous_array_size = len(values)
                        value = "NotFound"
                        if char in self.data[element]:
                            value = self.get_group_of_output(groups, self.data[element][char])
                        values.add(value)
                        if len(values) > previous_array_size:
                            new_groups.append([element])
                        else:
                            for new_group in new_groups:
                                for new_element in new_group:
                                    if new_element in group:
                                        if char in self.data[element] and char in self.data[new_element]:
                                            if self.get_group_of_output(groups, self.data[element][char]) == \
                                                    self.get_group_of_output(groups, self.data[new_element][char]):
                                                new_group.append(element)
                                                break
                    if len(values) != 1:
                        is_there_a_change = True
                        break
            if is_there_a_change:
                groups = new_groups
        return groups

    def merge_nodes(self, groups):
        new_states = copy.copy(self.data)
        for group in groups:
            if len(group) > 1:
                name_of_the_group = group[0]
                for key, value in self.data.items():
                    if key in group and key != name_of_the_group:
                        del new_states[key]
                        continue
                    if "isTerminatingState" in value:
                        for char in value:
                            if char in self.char_regex:
                                if new_states[key][char] in group:
                                    new_states[key][char] = name_of_the_group
        return new_states

    def rename_nodes(self, new_states):
        number_of_states = 0
        for key, value in new_states.items():
            if isinstance(value, str):
                continue
            number_of_states += 1

        current_state_idx = 0
        real_states_idx = 0
        stringify_object = str(new_states)
        while current_state_idx < number_of_states:
            state_we_will_have = 'S' + str(current_state_idx)
            state_existing = 'S' + str(real_states_idx)
            if state_we_will_have not in stringify_object:
                while state_existing not in stringify_object:
                    real_states_idx += 1
                    state_existing = 'S' + str(real_states_idx)
                stringify_object = stringify_object.replace(state_existing, state_we_will_have)
            real_states_idx += 1
            current_state_idx += 1

        return eval(stringify_object)

    def write_data(self, write_path, finalized_states):
        with open(write_path, "w") as json_file:
            json.dump(finalized_states, json_file)

    @staticmethod
    def visualize(path):
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
        dot.render('nfa.gv', view=True)

    def minimize(self):
        groups = self.initialize_groups()
        groups = self.get_groups_after_splitting(groups)
        new_states = self.merge_nodes(groups)
        finalized_states = self.rename_nodes(new_states)
        self.write_data('minimized_DFA.json', finalized_states)

if __name__ == "__main__":
    minDfa = MinimizedDFA('DFA.json',['A','B'])
    minDfa.minimize()
    MinimizedDFA.visualize('minimized_DFA.json')