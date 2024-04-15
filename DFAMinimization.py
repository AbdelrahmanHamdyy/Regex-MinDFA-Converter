import json
import copy
import graphviz
import time

class MinimizedDFA:
    def __init__(self,path,char_regex):
        self.load(path)
        self.char_regex = char_regex

    def load(self, file_path):
        with open(file_path, 'r') as file:
            self.data = json.load(file)

    def initialize_groups(self):
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
        #Keep looping as we have change in the groups
        while is_there_a_change:
            #Initialize there is a change as false and if we found a change we will set it as true
            is_there_a_change = False
            #Here we will have the array that contains the new groups of this iteration
            new_groups = []
            print(groups)
            #looping over all the groups existing with us, if they are with length 1 then we need not to see where they are going to
            #As we can't split it more
            for idx,group in enumerate(groups):
                #check law l group da 1 fa khlas d5lu w skip
                if len(group) == 1:
                    new_groups.append([group[0]])
                    continue
                #tab law hwa fady zy mslan gatlk case n kolhum terminal states f sa3tha khlas skip l group da
                if len(group)==0:
                    continue
                #Now We will take each character that may cause a transition to see how this will affect the group we are taking in consideration right now
                #dlw2te ana mask l group l awl wl nftrd feh [s0,s1,s2,s3,s4,s5,s6]
                #hena na hmsk 7rf el a mslan w b3den alf beh 3la kul l states de w ashuf eh ely hy7sal b2a hal haynfslu 3an ba3d wala la2
                for char in self.char_regex:
                    #khlas dlw2te ehna fe edena 7arf mu3yn w hnbus eh ely hy7sl
                    #fa ha7ut ll 7rf da set w law l size bta3 l set de zad 3an el 1 fa ma3na kda en fe kaza element byru7u l hagat mu5tlfa
                    values = set()
                    for element in group:
    
                        #print("Ana dlw2te bdwr fe group",group, "best5dam letter ",char , "w mask element ",element,"wl values heya ",values)
                        #esmk b2a l group ely ehna feh da w lef 3ala element element gwah
                        #print("Ana dlw2te bdwr fe group",group, "best5dam letter ",char , "w mask element ",element)
                        previous_array_size = len(values)
                        value = "NotFound"
                        if char in self.data[element]:
                            value = self.get_group_of_output(groups, self.data[element][char])
                        values.add(value)
                        
                        #print("Ana dlw2te bdwr fe group",group, " b3d m 3mlt add value best5dam letter ",char , "w mask element ",element,"wl values heya ",values , "is there a change?",is_there_a_change)
                        if len(values) > previous_array_size:
                            new_groups.append([element])
                        else:
                            for new_group in new_groups:
                                for new_element in new_group:
                                    if new_element in group:
                                        elementValue = "NotFound"
                                        newElementValue = "NotFound"
                                        if char in self.data[element]:
                                            elementValue = self.get_group_of_output(groups, self.data[element][char])
                                        if char in self.data[new_element]:
                                            newElementValue = self.get_group_of_output(groups, self.data[new_element][char])
                                        if  elementValue == newElementValue:
                                            new_group.append(element)
                                            break
                    if len(values) != 1:
                        is_there_a_change = True
                        break
                    else:
                        new_groups.pop(-1)
                if(not is_there_a_change):
                    new_groups.append(groups[idx])
            #Before Assigning new groups to groups we just want to make sure that all the elements exists here
            emptyArray =[]
            for element in self.data:
                if element != "startingState":
                    elementExisting = False
                    #Now We are looking for each state in data we have to make sure it exists and we haven't drop it down
                    for group in new_groups:
                        if element in group:
                            elementExisting = True
                            break
                    if(not elementExisting):
                       emptyArray.append(element)
            if(len(emptyArray)!=0):
                new_groups.append(emptyArray)
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
                            if char in self.char_regex and key in new_states:
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
        dot.render('output/min_dfa.gv', view=True)

    def minimize(self):
        groups = self.initialize_groups()
        groups = self.get_groups_after_splitting(groups)
        new_states = self.merge_nodes(groups)
        finalized_states = self.rename_nodes(new_states)
        self.write_data('output/minimized_DFA.json', finalized_states)
        print("Minimized Successfully")

if __name__ == "__main__":
    minDfa = MinimizedDFA('output/dfa.json',['a','b'])
    minDfa.minimize()
    MinimizedDFA.visualize('output/minimized_DFA.json')