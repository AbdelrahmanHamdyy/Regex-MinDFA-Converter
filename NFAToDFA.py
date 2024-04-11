import json
import time

def getAllNeededStates(data,startingState,incomingLetter):
    finalStates=[]
    if (incomingLetter in data[startingState]):
        states = data[startingState][incomingLetter]
        newStates = states.split(',')
        for state in newStates:
            finalStates.append(state)

    result = set()
    for state in finalStates:
        returnedSet = getEpsilons(data, state, set())
        if isinstance(returnedSet, str):
            value = returnedSet
            returnedSet = set()  # Initialize as empty set
            returnedSet.add(value)  # Add the string value
        result |= returnedSet  # Perform set union
    
    return result
#---------------------------------------------------------------------------------------------------------------------------
def getEpsilons(data,startingState,lettersSet):
    resultState=lettersSet
    if('epsilon' in data[startingState]):
        epsilons = data[startingState]['epsilon']
        newStates = epsilons.split(',')
        for state in newStates:
            if(state in resultState):
                break
            returnedVal = getEpsilons(data,state,resultState)
            if isinstance(returnedVal, str):
                resultState.add(returnedVal)
        resultState.add(startingState)
    else:
        return startingState
    return resultState

# Open the JSON file
with open('nu3man1.json', 'r') as file:
    # Load the JSON data into a Python object
    data = json.load(file)

#Hena kul lchars bta3ty ely ha3uz adwr 3leha
#wb3den lama ag alf 3l states fa ana ha7tag en le kol state gdeda half 3l combinations bta3tha de 
# ely hwa mslan l state de lazm agrb alf 3l a bta3tha wl b bta3tha w ashuf htl3ly state gdeda wala la2
regexChars= ['a','b']
#Hena b2a ana 3ayz a3ml object b7es en l object da tb2a feh l letters on interest as keys w odamha array feha anhy states htb2a mohema bensbalii 3shan abos 3leha
#3shan a2dr a generate b2a
charsOfInterest ={}
for char in regexChars:
    charsOfInterest[char]=[]

charValues ={}

#Dlw2te geh el dor eny amla b2a el states el muhema bensbali
# hamla b2a 7arf 7arf mn l regex chars ely 3andy

for char in regexChars:
    for key,value in data.items():
        if char in value:
            charsOfInterest[char].append(key)
            #charValues[key] = getAllNeededStates()

#Dlw2te ana m3aya kul el 7ruf el muhema bensbali w ely menha ana ha3ml generation ll new states wl new states htb2a b esmhum w best5damha ha2dr a2ul heya el state de gdeda wala la

#FirstLoop we will start from start Node
print(getAllNeededStates(data,'L','a'))


