'''
MIT License

Copyright (c) 2024 Jacob Smithmyer, Pennsylvania College of Technology

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

__all__: 'PCTspice'


#TO-DO LIST:
# Add EXPORT feature

try:
    from sympy import Matrix
except ModuleNotFoundError:
    print("\033[1;31;40m" + "ERROR: SymPy python module required for PCTspice calculations.\nPlease install SymPy to proceed.\n\nUse the terminal command \"pip install sympy\" to install using the Python package manager." + "\033[0m")
    print("\n\033[1;37;40mPress [ENTER] to close terminal.\033[38;5;0m\033[?25l")
    input()
    print("\033[0m\033[?25h")
    exit()

#__________________________________________________________________________________________________________________________________________
#OBJECT DEFS

class Branch: # Stores entered branches by recording start node, end node, component name, and component value.
    def __init__(self, startNode, endNode, compVal, compName):
        self.startNode = startNode.upper()
        self.endNode = endNode.upper()
        self.compVal = int(compVal)
        self.compName = compName.upper()
    #END def __init__()


    def printBranch(branch): # Prints branch in a readable format.
        if branch.compVal:
            compValStr = engNot(branch.compVal, "to", short= True)
            return str('{: ^5}'.format(branch.startNode) + ' ' + '{: ^4}'.format(branch.compName) + " = " + '{: <6}'.format(compValStr) + ' ' + '{: ^5}'.format(branch.endNode))
        else:
            return str('{: ^5}'.format(branch.startNode) + ' ' + '{: ^4}'.format(branch.compName) + ' ' + '{: ^5}'.format(branch.endNode))
    #END def printBranch()

    
    def validComp(branch):
        
        validComps = ['R', 'V', 'I']
        
        compType = ""

        for char in branch.compName:
            if char.isalpha():
                compType = compType + char.upper()

        if compType in validComps:
            return True
        else:
            return False
    #END def validComp()

#END class Branch



#__________________________________________________________________________________________________________________________________________
# HELP FUNCTIONS

def helpprint(): # Prints general help statement, including syntax guide and keyword list.
    print("\033[1;32;40m\n────────────────────────────────────────────────────────────────────────────────")
    print("PCTspice help:\n")
    print("PCTspice is an application for solving and analyzing DC circuits.\nCircuit branches are input, containing node names, component names and values, and various parameters can be returned.")
    print("Enter each command on a new line.\n\n")

# Syntax description:
    print("Input syntax:\n")
    print("\033[1;33;40m\t[START NODE NAME] [COMPONENT][#]=[VALUE] [END NODE NAME]\033[1;32;40m\n\n\tExample: \033[1;34;40mA R1=10k B\033[1;32;40m")
    print("\n\tOR\n")
    print("\033[1;33;40m\t[START NODE NAME] [COMPONENT][#] [END NODE NAME]\n\t[COMPONENT][#]=[VALUE]\033[1;32;40m\n\n\tExample: \033[1;34;40mA R1 B\n\t         R1=10k\033[1;32;40m")
    print("\n\t\t> \033[1;34;40m" + "[START NODE NAME]" + "\033[1;32;40m" + ":\tAny valid alphanumeric character, not case sensitive.\n")
    print("\t\t> \033[1;34;40m" + "[COMPONENT]" + "\033[1;32;40m" + ":\tValid component type followed by a number so different components can be differentiated.\n")
    print("\t\t> \033[1;34;40m" + "[VALUE]" + "\033[1;32;40m" + ":\tValue of the compent.\n\t\t\t\tEngineering notation suffixes can be used without a space between them and the number.\n")
    print("\t\t> \033[1;34;40m" + "[END NODE NAME]" + "\033[1;32;40m" + ":\tAny valid alphanumeric character, not case sensitive.\n")
    input("\033[1;37;40m--- Press [ENTER] to continue ---\033[38;5;0m\033[?25l")
    print("\33[2K\33[A\33[2K\33[A\r\033[0m\033[?25h")


    print("\n\n\t\033[1;32;40mUse node name \033[1;33;40mGND\033[1;32;40m for reference ground (0V).\n\tAny values returned will be given in reference to that node.")
    print("\n\tComponent values can be entered seperately at any point.\n\tTo change the value of a component, see the EDIT command.")
    print("\n\n")

# List of valid component types
    print("\n\033[1;33;40m" + "Valid component list:" + "\033[1;32;40m\n")
    print("> " + "\033[1;33;40m" + "Resistor" + "\033[1;32;40m" + "\t\tDC non-reactive resistance.\n\t\t\tUnit: Ohms\n\t\033[1;37;40m╱╲╱╲╱╲╱\033[1;32;40m\t\tFormat: R[#]=[value]\n")
    print("\n> " + "\033[1;33;40m" + "DC Voltage Source" + "\033[1;32;40m" + "\tIdeal DC voltage source.\n\t\033[1;37;40m ┌───┐ \033[1;32;40m\t\tThe start node is the positive terminal, the end node is the negative terminal.\n\t\033[1;37;40m─┤+ -├─\033[1;32;40m\t\tUnit: Volts\n\t\033[1;37;40m └───┘ \033[1;32;40m\t\tFormat: V[#]=[value]\n")
    print("\n> " + "\033[1;33;40m" + "DC Current Source" + "\033[1;32;40m" + "\tIdeal DC current source.\n\t\033[1;37;40m ┌───┐ \033[1;32;40m\t\tThe start node is the positive terminal, the end node is the negative terminal.\n\t\033[1;37;40m─┤◄──├─\033[1;32;40m\t\tUnit: Amperes\n\t\033[1;37;40m └───┘ \033[1;32;40m\t\tFormat: I[#]=[value]\n")
    print("\n")
    input("\033[1;37;40m--- Press [ENTER] to continue ---\033[38;5;0m\033[?25l")
    print("\33[2K\33[A\33[2K\33[A\r\033[0m\033[?25h")

# List of reserved keywords
    print("\033[1;34;40m" + "Keyword and command list:" + "\033[1;32;40m\n")
    print("> " + "\033[1;34;40m" + "CLEAR" + "\033[1;32;40m" + "\t\tClear terminal window.\n\t\tFormat: CLEAR\n")
    print("> " + "\033[1;34;40m" + "CLS" + "\033[1;32;40m" + "\t\tSynonym of CLEAR\n\t\tFormat: CLS\n")
    print("> " + "\033[1;34;40m" + "EDIT" + "\033[1;32;40m" + "\t\tEdits given parameter.\n\t\tFormat: EDIT [PARAMETER]\n")
        # Continuation of EDIT
    print("\t\t> " + "\033[1;34;40m" + "[COMPONENT]" + "\033[1;32;40m" + "\tEdits given component value.\n\t\t\t\tFormat:  EDIT [COMPONENT][#]=[NEW VALUE]\n")
    print("\t\t> " + "\033[1;34;40m" + "BRANCH" + "\033[1;32;40m" + "\tEdits specified branch by prompting the user for the replacement branch description.\n\t\t\t\tBranch numbers are shown using the 'PRINT BRANCHES' command.\n\t\t\t\tEither syntax for branch descriptions may be used.\n\t\t\t\tFormat:  EDIT BRANCH [BRANCH NUMBER]\n\t\t\t\t         > [START NODE NAME] [COMPONENT][#]=[VALUE] [END NODE NAME]\n")
        # End of EDIT
    print("> " + "\033[1;34;40m" + "END" + "\033[1;32;40m\t\tExit and stop running PCTspice.\n\t\tFormat: END\n")
    print("> " + "\033[1;34;40m" + "EXIT" + "\033[1;32;40m" + "\t\tSynonym of END.\n\t\tFormat: EXIT\n")
    print("> " + "\033[1;34;40m" + "HELP" + "\033[1;32;40m" + "\t\tPrint out help message.\n\t\tFormat: HELP\n")

    input("\033[1;37;40m--- Press [ENTER] to continue ---\033[38;5;0m\033[?25l")
    print("\33[2K\33[A\33[2K\33[A\r\033[0m\033[?25h\033[1;32;40m")

    print("> " + "\033[1;34;40m" + "IMPORT" + "\033[1;32;40m" + "\tImport text file (.txt) as parameter input.\n\t\tFormat: IMPORT fileName.txt\n")
    print("> " + "\033[1;34;40m" + "NEW" + "\033[1;32;40m" + "\t\tClears current workspace and deletes all branches, nodes, and components from memory.\n\t\tFormat: NEW\n")
   
    print("> " + "\033[1;34;40m" + "PRINT" + "\033[1;32;40m" + "\t\tPrint various variables or parameters.\n\t\tFormat: PRINT [PARAMETER]\n")
        # Continuation of PRINT
    print("\t\t> " + "\033[1;34;40m" + "BRANCHES" + "\033[1;32;40m" + "\tPrints a list of entered branches with starting node, component, and end node.\n\t\t\t\tFormat: PRINT BRANCHES\n")
    print("\t\t> " + "\033[1;34;40m" + "COMPONENTS" + "\033[1;32;40m" + "\tPrints a list of entered compnents and values, even if not yet assigned to a node.\n\t\t\t\tFormat: PRINT COMPONENTS\n")
        #End of PRINT
    print("> " + "\033[1;34;40m" + "RETURN" + "\033[1;32;40m" + "\tPrints calculated values of entered parameter to the screen.\n\t\tFormat: RETURN [PARAMETER]\n")
        # Continuation of RETURN
    print("\t\t> " + "\033[1;34;40m" + "V()" + "\033[1;32;40m" + "\tVoltage of entered node, or voltage drop across component.\n\t\t\tV(ALL) returns voltage of all nodes.\n\t\t\tFormat: RETURN V([node or component])\n")
    print("\t\t> " + "\033[1;34;40m" + "I()" + "\033[1;32;40m" + "\tCurrent through component.\n\t\t\tI(ALL) returns current through all components.\n\t\t\tFormat: RETURN I([component])\n")
        # End of RETURN
    print("\n")
# end
    print("────────────────────────────────────────────────────────────────────────────────\033[0m")
#END def helpprint()



#__________________________________________________________________________________________________________________________________________
#LINE INTERPRETING FUNCTIONS

def importFromLine(line): # Opens text file called by user input.
    fileName = line[len("IMPORT")+1:]
    returnArray = []
    lineList = []
    compDict = {}
    try:
        file = open(fileName, "rt")
        print("\n\033[1;34;40mContents of %s:\n┌──────────────────────────────────────────────────────────────────────────────┐" %fileName)
        for fileLine in file:
            if fileLine[-1] == '\n':
                fileLine = fileLine[0:-1]
            print("│" + fileLine.ljust(78, ' ') + "│")
            lineList.append(fileLine)
        print("└──────────────────────────────────────────────────────────────────────────────┘\033[0m")
        file.close()

        for l in lineList:
            returnArray.append(nodeAssign(l))

        num = len(returnArray)
        if num == 1:
            print("\033[1;34;40mImported %d branch.\033[0m\n" %num)
        else:
            print("\033[1;34;40mImported %d branches.\033[0m\n" %num)

        return returnArray

    except FileNotFoundError:
        print("\n\033[1;31;40m" + "ERROR:  File '%s' not found." %fileName + "\033[0m\n")
    except OSError:
        print("\n\033[1;31;40m" + "ERROR:  Invalid file name or path." + "\033[0m\n")
#END def importFromLine()


def nodeAssign(line):  #Extract node and component names and value from line of entered text
    try: 
        line = line.upper()
        newBranch = Branch('', '', 0.0, '')
        i = 0
        while line[i] != ' ':
            newBranch.startNode = newBranch.startNode + line[i]
            i += 1


        i = -1
        while line[i] != ' ':
            newBranch.endNode = line[i] + newBranch.endNode
            i -= 1

        i = len(newBranch.startNode)+1
        while line[i] != " " and line[i] != "=":
            newBranch.compName = newBranch.compName + line[i]
            i += 1

        if line[i] == "=":
            i += 1
            compValTemp = ""
            while line[i] != " ":
                compValTemp = compValTemp + line[i]
                i += 1
            newBranch.compVal = engNot(compValTemp, 'from')

        if newBranch and newBranch.validComp():
            return newBranch
        else:
            return None
        
    except:
        return None
#END def nodeAssign()





#__________________________________________________________________________________________________________________________________________
#MATH FUNCTIONS


def engNot(Value, toOrFromStr, short = False):  # Converts to and from engineering notation.  Enter string "from" or "to" along with value to convert.
    if toOrFromStr.lower() == "from":
        suffix = ""
        for c in Value:
            if c.isalpha():
                suffix += c

        match suffix:
            case 'T':
                returnVal = float(Value[0:-len(suffix)]) * 10**12
            case 'G':
                returnVal = float(Value[0:-len(suffix)]) * 10**9
            case 'M':
                returnVal = float(Value[0:-len(suffix)]) * 10**6
            case 'Meg':
                returnVal = float(Value[0:-len(suffix)]) * 10**6
            case 'MEG':
                returnVal = float(Value[0:-len(suffix)]) * 10**6
            case 'K':
                returnVal = float(Value[0:-len(suffix)]) * 10**3
            case 'k':
                returnVal = float(Value[0:-len(suffix)]) * 10**3
            case 'm':
                returnVal = float(Value[0:-len(suffix)]) * 10**-3
            case 'u':
                returnVal = float(Value[0:-len(suffix)]) * 10**-6
            case 'n':
                returnVal = float(Value[0:-len(suffix)]) * 10**-9
            case 'p':
                returnVal = float(Value[0:-len(suffix)]) * 10**-12
            case _:
                returnVal = float(Value)

    elif toOrFromStr.lower() == "to":
        exponent = 0
        newVal = float(Value)
        while (newVal >= 1000 or newVal <= -1000) and exponent < 12:
            exponent += 3
            newVal = Value / 10**exponent
        while ((newVal < 1.0 and newVal > 0.0) or (newVal > -1.0 and newVal < 0.0)) and exponent > -12:
            exponent -= 3
            newVal = Value / 10**exponent

        if short:
            returnVal = returnVal = '{:0<5.4}'.format(newVal)
        else:
            returnVal = '{:.6f}'.format(newVal)
    
        match exponent:
            case 12: 
                returnVal += 'T'
            case 9: 
                returnVal += 'G'
            case 6: 
                returnVal += 'M'
            case 3:
                returnVal += 'k'
            case -3:
                returnVal += 'm'
            case -6:
                returnVal += 'u'
            case -9:
                returnVal += 'n'
            case -12:
                returnVal += 'p'
            case _:
                pass

    else:
        returnVal = Value      
    return returnVal
#END def engNot()



def nodalAnalysis(branchArray, nodeDict):  # Solves for nodal voltages based on array of branches and dictionary object containing node names as keys and index of branches that refer to them
    nodeList = list(nodeDict.keys())
    nodeMat = [[0.0] * (len(nodeList)+1) for n in range(len(nodeList))]
    for i in range(len(nodeMat)):
        node = nodeList[i]
        voltageNode=False

        for n in nodeDict[node][0]:
            branch = branchArray[n]
            if not voltageNode:
                if branch.compName[0] == 'R':
                    comp = 1/branch.compVal
                    if branch.startNode != "GND":
                        nodeMat[i][nodeList.index(branch.startNode)] += comp
                    
                    if branch.endNode != "GND":
                        nodeMat[i][nodeList.index(branch.endNode)] -= comp

                elif branch.compName[0] == 'V':
                    nodeMat[i] = [0.0] * (len(nodeList)+1)
                    if branch.startNode != "GND":
                        nodeMat[i][nodeList.index(branch.startNode)] = 1
                    if branch.endNode != "GND":
                        nodeMat[i][nodeList.index(branch.endNode)] = -1
                    voltageNode = True
                    
                    nodeMat[i][-1] = branch.compVal

                elif branch.compName[0] == 'I':
                    nodeMat[i][-1] += branch.compVal

        for n in nodeDict[node][1]:
            if not voltageNode:
                branch = branchArray[n]
                if branch.compName[0] == 'R':
                    comp = 1/branch.compVal
                    if branch.startNode != "GND":
                        nodeMat[i][nodeList.index(branch.startNode)] -= comp
                    
                    if branch.endNode != "GND":
                        nodeMat[i][nodeList.index(branch.endNode)] += comp

                elif branch.compName[0] == 'V':
                    nodeMat[i] = [0.0] * (len(nodeList)+1)
                
                    if branch.startNode == "GND":
                        nodeMat[i][nodeList.index(branch.endNode)] = -1
                        nodeMat[i][-1] = branch.compVal
                        voltageNode = True
                    else:
                        otherNodes = superNode(branchArray, nodeDict, branch.startNode)
                        for l in range(len(otherNodes[0])):
                            if otherNodes[0][l] == "ENDOFMAT":
                                nodeMat[i][-1] += otherNodes[1][l]
                            else:
                                nodeMat[i][nodeList.index(otherNodes[0][l])] += otherNodes[1][l]
                        voltageNode = True

                elif branch.compName[0] == 'I':
                    nodeMat[i][-1] -= branch.compVal

    #print(nodeList)
    #print(Matrix(nodeMat))
    nodeVoltages = Matrix(nodeMat).rref()[0].col(-1)
    solutionMat = [nodeList,[]]
    for i in range(len(nodeList)):
        solutionMat[1].append(nodeVoltages[i])

    return solutionMat
#END def nodalAnalysis()



def superNode(branchArray, nodeDict, nodeName, branchToExclude = None):  # Assigns KCL equations if the node needs to become supernode, calls itself recursively for each voltage source encountered.
    superNodeList = [[],[]]

    for i in nodeDict[nodeName][0]:
        branch = branchArray[i]

        if branch != branchToExclude:
            if branch.compName[0] == 'R':
                if branch.startNode not in superNodeList[0]:
                    superNodeList[0].append(branch.startNode)
                    superNodeList[1].append(0)
                if branch.endNode not in superNodeList[0] and branch.endNode != "GND":
                    superNodeList[0].append(branch.endNode)
                    superNodeList[1].append(0)

                superNodeList[1][superNodeList[0].index(branch.startNode)] += 1/branch.compVal
                if branch.endNode != "GND":
                    superNodeList[1][superNodeList[0].index(branch.endNode)] -= 1/branch.compVal

            if branch.compName[0] == 'V':
                temp = superNode(branchArray, nodeDict, branch.endNode, branchToExclude=branch)
                for t in range(len(temp[0])):
                    if temp[0][t] not in superNodeList[0]:
                        superNodeList[0].append(temp[0][t])
                        superNodeList[1].append(0)

                    superNodeList[1][superNodeList[0].index(temp[0][t])] += temp[1][t]
            
            if branch.compName[0] == 'I':
                    if "ENDOFMAT" not in superNodeList[0]:
                        superNodeList[0].append(branch.endNode)
                        superNodeList[1].append(0)
                    superNodeList[0][superNodeList[0].index("ENDOFMAT")] -= branch.compVal

    for i in nodeDict[nodeName][1]:
        branch = branchArray[i]
        if branch != branchToExclude:
            if branch.compName[0] == 'R':
                if branch.startNode not in superNodeList[0]:
                    superNodeList[0].append(branch.startNode)
                    superNodeList[1].append(0)
                if branch.endNode not in superNodeList[0] and branch.startNode != "GND":
                    superNodeList[0].append(branch.endNode)
                    superNodeList[1].append(0)

                if branch.startNode != "GND":
                    superNodeList[1][superNodeList[0].index(branch.startNode)] -= 1/branch.compVal
                superNodeList[1][superNodeList[0].index(branch.endNode)] += 1/branch.compVal

            if branch.compName[0] == 'V':
                temp = superNode(branchArray, nodeDict, branch.startNode, branchToExclude=branch)
                for t in range(len(temp[0])):
                    if temp[0][t] not in superNodeList[0]:
                        superNodeList[0].append(temp[0][t])
                        superNodeList[1].append(0)

                    superNodeList[1][superNodeList[0].index(temp[0][t])] += temp[1][t]

            if branch.compName[0] == 'I':
                    if "ENDOFMAT" not in superNodeList[0]:
                        superNodeList[0].append(branch.endNode)
                        superNodeList[1].append(0)
                    superNodeList[0][superNodeList[0].index("ENDOFMAT")] += branch.compVal

    return superNodeList
# END def superNode()



def currentCalc(branchArray, results, nodeDict, compName):
    if compName[0] == 'R':
        for branch in branchArray:
            if branch.compName == compName:
                start = branch.startNode
                end = branch.endNode
                compVal = branch.compVal

        if start == "GND":
            current = (-results[1][results[0].index(end)])/compVal
        elif end == "GND":
            current = (results[1][results[0].index(start)])/compVal
        else:
            current = (results[1][results[0].index(start)]-results[1][results[0].index(end)])/compVal
        
        return current
    
    elif compName[0] == 'V':
        current = 0
        for branch in branchArray:
            if branch.compName == compName:
                if branch.startNode != 'GND':
                    testNode = branch.startNode
                else:
                    testNode = branch.endNode

        for i in nodeDict[testNode][0]:
            if branchArray[i].compName != compName:
                current += currentCalc(branchArray, results, nodeDict, branchArray[i].compName)
        
        for i in nodeDict[testNode][1]:
            if branchArray[i].compName != compName:
                current -= currentCalc(branchArray, results, nodeDict, branchArray[i].compName)

        return -current
    
    elif compName[0] == 'I':
        for branch in branchArray:
            if branch.compName == compName:
                return branch.compVal

    else:
        return False
# END def currentCalc()



#__________________________________________________________________________________________________________________________________________
#MAIN FUNCTION

def PCTspice():
    run = True
    print("\033[1;32;40m\nRunning PCTspice circuit analysis!\033[0;32;40m\n\nEnter data below or import text file.\nAll data will be lost when ending the PCTspice session.\nSome commands may not work correctly if not running directly in Python terminal.\n\n\033[1;32;40mType \033[1;33;40mHELP\033[1;32;40m for help.\n\n────────────────────────────────────────────────────────────────────────────────\033[0m\n")

    branchArray = []
    compnentDict = {}
    nodeIndexDict = {}
    results = []

    while run:
        line = input()

        match line.upper():
            case "":
                pass
            case "=":
                pass
            case "END":
                print("\033[0m")
                exit()
            case "EXIT":
                print("\033[0m")
                exit()
            case "HELP":
                helpprint()
            case "NEW":
                branchArray = []
                compnentDict = {}
                nodeIndexDict = {}
                results = []
                print("\n\033[1;32;40mMemory cleared.\nRunning PCTspice circuit analysis!  \033[1;32;40mType \033[1;33;40mHELP\033[1;32;40m for help./n────────────────────────────────────────────────────────────────────────────────\033[0m\n")
            case "CLEAR":
                print('\033c', end='')
                print("\033[1;32;40m\nRunning PCTspice circuit analysis!  \033[1;32;40mType \033[1;33;40mHELP\033[1;32;40m for help.\n\n────────────────────────────────────────────────────────────────────────────────\033[0m\n\n")
            case "CLS":
                print('\033c', end='')
                print("\033[1;32;40m\nRunning PCTspice circuit analysis!  \033[1;32;40mType \033[1;33;40mHELP\033[1;32;40m for help.\n\n────────────────────────────────────────────────────────────────────────────────\033[0m\n\n")
            case "PCTSPICE":
                print("\n\033[1;32;40mPCTspice is already running!\033[0m\n")
            case _:

     # RETURN command
                if line[0:len("RETURN")].upper() == "RETURN":
                    i = len("RETURN")+1
                    cmd = ""
                    operand = ""
                    while line[i] != '(' and line[i] != '\n':
                        cmd = cmd + line[i].upper()
                        i += 1

                #Put things like Rth here

                    i += 1
                    while line[i] != ')':
                        operand = operand + line[i].upper()
                        i += 1

                    if not results:
                        tempBranchArray = []
                        for branch in branchArray:
                            branch.compVal = compnentDict[branch.compName]
                            tempBranchArray.append(branch)
                        results = nodalAnalysis(tempBranchArray, nodeIndexDict)

                # Returning VOLTAGE
                    if cmd == 'V':
                        if operand == 'ALL':
                            for i in range(len(results[0])):
                                print("\033[1;36;40m" + "V(" + results[0][i] + ")\t = " + engNot(results[1][i], "to") + "\tVOLTS\033[0m")
                        
                        elif operand in results[0]:
                            index = results[0].index(operand)
                            print("\033[1;36;40m" + "V(" + results[0][index] + ")\t = " + engNot(results[1][index], "to") + "\tVOLTS\033[0m")
                        
                        elif operand in list(compnentDict.keys()):
                            for branch in branchArray:
                                if branch.compName == operand:
                                    start = branch.startNode
                                    end = branch.endNode
                            
                            if start and end:
                                if start == "GND":
                                    print("\033[1;36;40m" + "V(" + operand + ")\t = " + engNot(-results[1][results[0].index(end)], "to") + "\tVOLTS\033[0m")
                                elif end == "GND":
                                    print("\033[1;36;40m" + "V(" + operand + ")\t = " + engNot(results[1][results[0].index(start)], "to") + "\tVOLTS\033[0m")
                                else:
                                    print("\033[1;36;40m" + "V(" + operand + ")\t = " + engNot(results[1][results[0].index(start)]-results[1][results[0].index(end)], "to") + "\tVOLTS\033[0m")
                        else:
                            print("\033[1;31;40m" + "ERROR: Invalid node or component value in RETURN command." + "\033[0m")
                    
                # Returning CURRENT
                    elif cmd == 'I':
                        testBranchArray = []
                        for branch in branchArray:
                            testBranchArray.append(branch)
                            testBranchArray[-1].compVal = compnentDict[branch.compName]

                        currentCalc(branchArray, results, nodeIndexDict, operand)    
                        if operand == "ALL":
                            for comp in list(compnentDict.keys()):
                                print("\033[1;36;40m" + "I(" + comp + ")\t = " + engNot(currentCalc(testBranchArray, results, nodeIndexDict, comp), 'to') + "\tAMPERES\033[0m")

                        elif operand in list(compnentDict.keys()):
                            print("\033[1;36;40m" + "I(" + operand + ")\t = " + engNot(currentCalc(testBranchArray, results, nodeIndexDict, operand), 'to') + "\tAMPERES\033[0m")

                        else:
                            print("\033[1;31;40m" + "ERROR: Invalid component value in RETURN command." + "\033[0m")
                        

     # IMPORT command
                if line[0:len("IMPORT")].upper() == "IMPORT":
                    branchesToAdd = importFromLine(line)
                    try:
                        if branchesToAdd:
                            for branchVal in branchesToAdd:
                                if branchVal:
                                    compnentDict[branchVal.compName] = branchVal.compVal
                                    branchVal.compVal = 0
                                    branchArray.append(branchVal)
                                    try:
                                        nodeIndexDict[branchVal.startNode][0].append(branchArray.index(branchVal))
                                    except KeyError:
                                        if branchVal.startNode != "GND":
                                            nodeIndexDict[branchVal.startNode] = [[branchArray.index(branchVal)],[]]
                                    try:
                                        nodeIndexDict[branchVal.endNode][1].append(branchArray.index(branchVal))
                                    except KeyError:
                                        if branchVal.endNode != "GND":
                                            nodeIndexDict[branchVal.endNode] = [[],[branchArray.index(branchVal)]]
                    except TypeError:
                        print("\033[1;31;40m" + "ERROR: Unable to read net description in file." + "\033[0m")

         # PRINT command 
                elif line[0:len("PRINT")].upper() == "PRINT":
                 # PRINT BRANCHES
                    if line[len("PRINT")+1:].upper() == "BRANCH" or line[len("PRINT")+1:].upper() == "BRANCHES" or line[len("PRINT")+1:].upper() == "BRANCHS":
                        print("\033[1;34;40m┌─────┬──────────────────────────────────┐\n│ NUM │ BRANCHES                         │\n├─────┼──────────────────────────────────┤")
                        for branch in branchArray:
                            if branch:
                                if branch.compName in list(compnentDict.keys()):
                                    branch.compVal = compnentDict[branch.compName]
                                branchStr = branch.printBranch()
                                print("│"+ "{: <40}".format("{: >4}".format(branchArray.index(branch)+1) +" ┼ " + branchStr) + '│')
                                print("│     │                                  │")
                        print("└─────┴──────────────────────────────────┘\033[0m\n")

                 # PRINT COMPONENTS
                    elif line[len("PRINT")+1:].upper() == "COMPONENT" or line[len("PRINT")+1:].upper() == "COMPONENTS" or line[len("PRINT")+1:].upper() == "COMPS" or line[len("PRINT")+1:].upper() == "COMP":
                        print("\033[1;34;40m")
                        for name, val in compnentDict.items():
                            if val:
                                engVal = engNot(val,"to", short=True)
                                print(name + "=" + engVal)
                            else:
                                print(name)
                        print("\033[0m\n")

                    else:
                        print("\033[1;31;40m" + "ERROR: Invalid or incomplete command." + "\033[0m")
        
         # EDIT command 
                elif line[0:len("EDIT")].upper() == "EDIT":
                    line = line.upper()
                
                # EDIT COMPONENTS
                    if "=" in line[len("EDIT")+1:] and " " not in line[len("EDIT")+1:]:
                        name = ""
                        val = ""
                        i = len("EDIT") + 1
                        while line[i] != '=':
                            name = name + line[i]
                            i += 1
                        for i in line[len("EDIT") + len(name) + 2 :]:
                            val = val + i
                        val = engNot(val, toOrFromStr="from")
                        psuedoBranch = Branch('', '', 0.0, '')
                        psuedoBranch.compName = name
                        if psuedoBranch.validComp():
                            compnentDict[name.upper()] = val

                # EDIT BRANCHES
                    elif line[len("EDIT "):len("EDIT BRANCH")] == "BRANCH":
                        index = int(line[len("EDIT BRANCH "):])-1
                        newBranch = input("> ")
                        print("\033[0m")

                        branchVal = nodeAssign(newBranch)
                        

                        if branchVal:

                            tempBranch = branchArray[index]
                            if tempBranch.startNode != 'GND':
                                nodeIndexDict[tempBranch.startNode][0].remove(index)
                            if tempBranch.endNode != 'GND':
                                nodeIndexDict[tempBranch.endNode][1].remove(index)

                            branchArray[index] = branchVal
                            print("\33[2A\r\033[2K\r" + "> \033[1;33;40m" + newBranch + "\033[0m")

                            try:
                                if branchVal.compVal and compnentDict[branchVal.compName]:
                                    compnentDict[branchVal.compName] = branchVal.compVal
                            except KeyError:
                                if branchVal.compVal:
                                    compnentDict[branchVal.compName] = branchVal.compVal
                            branchVal.compVal = 0

                            try:
                                if branchVal.startNode != "GND":
                                    nodeIndexDict[branchVal.startNode][0].append(branchArray.index(branchVal))
                            except KeyError:
                                if branchVal.startNode != "GND":
                                    nodeIndexDict[branchVal.startNode] = [[branchArray.index(branchVal)],[]]
                            try:
                                if branchVal.endNode != "GND":
                                    nodeIndexDict[branchVal.endNode][1].append(branchArray.index(branchVal))
                            except KeyError:
                                if branchVal.endNode != "GND":
                                    nodeIndexDict[branchVal.endNode] = [[],[branchArray.index(branchVal)]]



                    else:
                        print("\033[1;31;40m" + "ERROR: Invalid or incomplete command." + "\033[0m")
               
               
         # Assigning components outside of branch description
                elif '=' in line and ' ' not in line:
                    try:
                        name = ""
                        val = ""
                        i = 0
                        while line[i] != '=':
                            name = name + line[i]
                            i += 1
                        for i in line[len(name)+1:]:
                            val = val + i
                        val = engNot(val, toOrFromStr="from")
                        psuedoBranch = Branch('', '', 0.0, '')
                        psuedoBranch.compName = name
                        if compnentDict[name.upper()] != 0:
                            print("\033[1;31;40m" + "Component %s already exists." %name.upper() + "\033[0m")
                        else:
                            if psuedoBranch.validComp():
                                print("\33[2K\33[A\r\033[1;33;40m" + line + "\033[0m")
                                compnentDict[name.upper()] = val
                    except KeyError:
                        if psuedoBranch.validComp():
                            print("\33[2K\33[A\r\033[1;33;40m" + line + "\033[0m")
                            compnentDict[name.upper()] = val
               

         # Handling branch descriptions
                else:
                    branchVal = nodeAssign(line)
                    if branchVal:
                        if branchVal.compName in list(compnentDict.keys()):
                            print("\033[1;31;40m" + "Component %s already exists." %branchVal.compName + "\033[0m")
                        else:
                            print("\33[2K\33[A\r\033[1;33;40m" + line + "\033[0m")
                        
                            compnentDict[branchVal.compName] = branchVal.compVal
                            branchVal.compVal = 0
                            branchArray.append(branchVal)
                            try:
                                nodeIndexDict[branchVal.startNode][0].append(branchArray.index(branchVal))
                            except KeyError:
                                if branchVal.startNode != "GND":
                                    nodeIndexDict[branchVal.startNode] = [[branchArray.index(branchVal)],[]]
                            try:
                                nodeIndexDict[branchVal.endNode][1].append(branchArray.index(branchVal))
                            except KeyError:
                                if branchVal.endNode != "GND":
                                    nodeIndexDict[branchVal.endNode] = [[],[branchArray.index(branchVal)]]
                        
#END def PCTspice()



#__________________________________________________________________________________________________________________________________________
#CODE TO EXECUTE
if __name__ == '__main__':
    try:
        PCTspice()
    except Exception as error:
        print("\n\n\033[1;31;40mPYTHON ERROR:  " +  str(error) + "\033[0m")
        print("\033[1;37;40m\nPress [ENTER] to close terminal.\033[38;5;0m\033[?25l")
        input()
        print("\033[0m\033[?25h")
