import json
import time

def getAllNeededStates(data,startingState,incomingLetter,isStartState=False):
    finalStates=[]
    if(isStartState):
        finalStates=[startingState]
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
terminalStates=set()
#Hena b2a ana 3ayz a3ml object b7es en l object da tb2a feh l letters on interest as keys w odamha array feha anhy states htb2a mohema bensbalii 3shan abos 3leha
#3shan a2dr a generate b2a

targetChars ={}
for char in regexChars:
    targetChars[char]=[]

#Dlw2te geh el dor eny amla b2a el states el muhema bensbali
# hamla b2a 7arf 7arf mn l regex chars ely 3andy

charValues ={}
wantedValues ={}
for char in regexChars:
    for key,value in data.items():
        if "isTerminatingState" in value and value["isTerminatingState"]==True:
            terminalStates.add(key)
        if char in value:
            targetChars[char].append(key)
            charValues[key] = getAllNeededStates(data,key,char)

currentStateNum =0
statesIncrementNum =1
startingState = "".join(sorted(getAllNeededStates(data,data['startingState'],'a',True)))
startingStateObject = {
    "value": startingState,
    "isTerminalState": False,
}
resultStates ={
    "S0":startingStateObject
}

# regexChars -> All Chars that will move us from a state to another
# resultStates -> contains all the states that we will add to the json in the end
# 

while(currentStateNum!=statesIncrementNum):
    #We need to select the currentState Number to select which stated we will working on
    #Select the current State to work on
    currentStateIdx = 'S'+str(currentStateNum)
    # w de el current State ely ana hshtghl 3leha dlw2ty wl mfrud en fe awl khatwa khals b3mlha access mn bara l2nha mawguda f3lan
    currentState = resultStates[currentStateIdx]
    #Shuf l state ely ana wa2f feha dlw2ty de htt7rk ezay lma ygelha ay char mn l possible chars ely bt7rk
    for char in regexChars:
        #da ely hyshel el output ely hyegy mn l char bta3 dlw2te da
        result = set()
        #Loop for each letter in the currentStateLetters
        # w law fe wahd mnhum mn l chars l muhema ely bntklm 3anha fo2 fa sa3tha bus 3l map bta3tu
        for letter in currentState["value"]:
            if(letter in charValues and letter in targetChars[char]):
                result |= charValues[letter]
        result = "".join(sorted(result))
        isTerminalState=False
        for letter in result:
            if letter in terminalStates:
                isTerminalState=True
                break
        #dlw2te ana tl3t el result ely m3aya w 3ayz ashuf hal ha3ml state gdeda wala mogrd hshawr 3la wahda mawguda 3ndy f3lan
        referencedState = "NotFound"
        for key,value in resultStates.items():
            #dlw2ty hlf 3la kol el existing states ely mawguda blf3l 3ndy
            #law l current state de mawguda yb2a mugrd ha reference
            #law msh mawguda fa ha3ml reference we kman h create wahda gdeda
            if value["value"]==result:
                #w da m3nah enna l2enaha f3lan
                referencedState = key
                break
        
        if(referencedState == "NotFound"):
            #yb2a kda ml2enahash
            newStateIdx = 'S'+str(statesIncrementNum)
            statesIncrementNum +=1
            newStateObj = {
                "value":result,
                "isTerminalState":isTerminalState
            }
            resultStates[newStateIdx] = newStateObj
            referencedState = newStateIdx
        currentState[char]=referencedState
    currentStateNum+=1



file_path = "DFA_result.json"
with open(file_path, "w") as json_file:
    json.dump(resultStates, json_file)


