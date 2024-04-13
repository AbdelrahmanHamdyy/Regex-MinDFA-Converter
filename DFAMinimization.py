import json
import copy
import graphviz




# Open the JSON file
with open('DFA_result.json', 'r') as file:
    # Load the JSON data into a Python object
    data = json.load(file)

# Firstly we need to make an array of arrays
# and each small array will be considered as a group
#then we will keep splitting until convergence

#Firstly initialize the first basic groups where they are goals and normal nodes

charRegex =['a','b']
nonTerminatingGroup =[]
terminatingGroup =[]
groups =[nonTerminatingGroup,terminatingGroup]
numberOfStates=0
stateToNumberMap ={}
#make map for each state and its number
for key,value in data.items():
    if "isTerminatingState" in value:
        numberOfStates+=1
        stateToNumberMap[key] = int(key.split('S')[1])
        if value["isTerminatingState"]:
            terminatingGroup.append(key)
        else:
            nonTerminatingGroup.append(key)

isThereAChange = True

def getGroupOfOutput(groups,point):
    for i,group in enumerate(groups):
        if point in group:
            return i

while(isThereAChange):
    isThereAChange=False
    newGroups=[]
    for group in groups:
        #print("I'm group ",group , " And i have length ",len(group))
        if len(group) == 1:
            continue
        #Dlw2te ana 3ayz en l kul group ashuf hwa hytl3 mnu kam group mn l akher
        #ha7tag agrb kul charachter fa hena hgrb char el a 3ala el non terminal
        for char in charRegex:
            #da 3shan ashuf ana htl3 kam array fl akher mn l group da
            values = set()
            for element in group:
                previousArraySize = len(values)
                value = getGroupOfOutput(groups,data[element][char])
                #print("element ",element ," using char ",char," is going to group ",value)
                values.add(value)
                #Then We need to add a new array
                if len(values) > previousArraySize:
                    newGroups.append([element])
                #else Then we need to go and find which is my group
                else :
                    for newGroup in newGroups:
                        for newElement in newGroup:
                            if(newElement in group):
                                if(getGroupOfOutput(groups,data[element][char]) == getGroupOfOutput(groups,data[newElement][char])):
                                    newGroup.append(element)
                                    break
            #print("for char ",char, "we will need ", len(values), " array")
            if(len(values) != 1):
                isThereAChange = True
                break
    if(isThereAChange):
        groups=newGroups



newStates= copy.copy(data)
#Merge Nodes
#loop over all the groups and check if the size of the group is greater than one then it needs a merge
for group in groups:
    if len(group) > 1:
        #Then we will need to merge these two into one element
        #I will consider the first node of the group as the name of the resulting node
        nameOfTheGroup = group[0]
        #Looping over all the nodes and it we found anything in that group then change its name to the new name of the group
        #and if we found an element that exists in the group and doesn't have the name of the group then we should delete it
        for key,value in data.items():
            #delete the other nodes in the group
            if key in group and key != nameOfTheGroup:
                del newStates[key]
                continue
            #Get the nodes that will be changed
            if "isTerminatingState" in value:
                #Then this means it's not the starting state
                #looping over all possible transitions we have
                for char in value:
                    if char in charRegex:                        
                        #print(newStates[key])
                        #print("We Are in State ",key," and we are looking for Char ",char, " Then we will move to ",newStates[key][char])
                        #Then this means it's a transition
                        if newStates[key][char] in group:
                            newStates[key][char]=nameOfTheGroup

# Rename Node
currentIncrement = 0
#Now I will capture each node existing in our json file
#and we should sort them by their order
#So they should go like S0 S1 S2 S3 and keep going like that
#so i wil have current increment value that monitors now we should be in the state S(increment)
#and if there is a change due to deleting some nodes in minimization
#Then we shall change this
# finalizedStates ={}
# for key,value in newStates.items():
#     if isinstance(value, str):
#         finalizedStates[key]=value
#         continue
#     newIdx = 'S'+str(currentIncrement)
#     print("Now we are in state ",key, "And we want to be in state ",newIdx)
#     if(newIdx != key):
#         for stateName,stateValue in newStates.items():
#             if isinstance(stateValue, str):
#                 continue
#             else:
#                 newStates[newIdx]= newStates.pop(key)
#                 for char,transitionState in stateValue.items():
#                     if char!="isTerminatingState":
#                         if transitionState == key:
#                             newStates[stateName][char] = newIdx
#     currentIncrement+=1

# print(newStates)

# Serialize the object to a string
numberOfStates = 0
for key,value in newStates.items():
    if isinstance(value, str):
        continue
    numberOfStates+=1

currentStateIdx = 0
realStatesIdx = 0
stringifyObject = str(newStates)
while(currentStateIdx < numberOfStates):
    stateWeWillHave = 'S'+str(currentStateIdx)
    stateExisting = 'S'+str(realStatesIdx)
    if stateWeWillHave not in stringifyObject:
        while(stateExisting not in stringifyObject):
            realStatesIdx+=1
            stateExisting = 'S'+str(realStatesIdx)
        stringifyObject = stringifyObject.replace(stateExisting, stateWeWillHave)
    realStatesIdx +=1
    currentStateIdx+=1

finalizedStates = eval(stringifyObject)


file_path ="minimized_DFA.json"
with open(file_path, "w") as json_file:
    json.dump(finalizedStates, json_file)


    
def visualize():
    dot = graphviz.Digraph(comment='DFA Visualization')
    states_json = None
    with open('minimized_DFA.json', 'r') as f:
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
        for symbol, nextState in transitions.items():
            # Skip the terminating state flag
            if symbol == 'isTerminatingState':
                continue
            dot.edge(state_name, nextState, label=symbol if symbol != '\u03b5' else 'ε')
    dot.render('nfa.gv', view=True)

visualize()







    
    

# matrixOfDistinguishStates = []
# for i in range(numberOfStates):
#     matrixOfDistinguishStates.append([True for _ in range(i+1)])
#     matrixOfDistinguishStates[i][-1]=False

# #Mark Difference between goals and normal states as False
# for row in range(numberOfStates):
#     for column in range(numberOfStates):
#         if(column > row):
#             break
#         rowState = 'S'+str(row)
#         columnState = 'S'+str(column)
#         if(data[rowState]["isTerminatingState"] != data[columnState]["isTerminatingState"]):
#             matrixOfDistinguishStates[row][column]=False

# print(matrixOfDistinguishStates)

# #Now We will keep looping until we won't find any change happened then we will be done and the spaces which will be true should be merged together
# isThereAChange = True
# while(isThereAChange):
#     isThereAChange=False
#     #Now We will take each single point in row and column and compare all the possible directions of them
#     for row in range(numberOfStates):
#         for column in range(numberOfStates):
#             if(column > row):
#                 break
#             if(matrixOfDistinguishStates[row][column]==False):
#                 continue   
#             rowData = data['S'+str(row)]
#             columnDate = data['S'+str(column)]
#             #Here we should loop over all available chars that will move us from a state to another
#             for char in charRegex:
#                 rowShouldGoTo = stateToNumberMap[rowData[char]]
#                 columnShouldGoTo = stateToNumberMap[columnDate[char]]
#                 minVal=columnShouldGoTo
#                 maxVal=rowShouldGoTo
#                 if minVal > maxVal :
#                     maxVal=columnShouldGoTo
#                     minVal=rowShouldGoTo
#                 if minVal == maxVal:
#                     continue
#                 if(matrixOfDistinguishStates[maxVal][minVal]==False):
#                     isThereAChange=True
#                     matrixOfDistinguishStates[row][column] = False
#             if(isThereAChange==True):
#                 break
#         if(isThereAChange==True):
#             break

# print(matrixOfDistinguishStates)



