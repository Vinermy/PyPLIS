from tkinter import *
import os

#Период обновления логики в секундах
sleeptime = 0.5

inputsDict = {}

def setChildrenPadding(object, vpad, hpad):
    for child in object.winfo_children():
        child.grid_configure(padx=hpad, pady=vpad)

#FILE LOADER
def loadfile(pathToFile):
    fileContents = []
    try:
        with open(pathToFile) as f:   
            for i in f.readlines():
                fileContents.append(i.replace('\n', ''))
     
    except FileNotFoundError:
        return "File not found"
    finally:
        return fileContents
    


#INTERAFCE FOR PC ONLY WINDOW MODE (FILE SELECTOR)
def initPcOnlyWindowMode():
    root_selectfile = Tk()
    root_selectfile.title("PyPLIS - File selection")
    filepath = StringVar()
    lbl = Label(root_selectfile, text="Select a file:")
    filepath_entry = Entry(root_selectfile, textvariable=filepath, width=50)
    run_button = Button(root_selectfile, text="Run this file", command=lambda: runPCOWM(loadfile(filepath.get()), os.path.basename(filepath.get())))

    lbl.grid(column=0, row=0)
    filepath_entry.grid(column= 0, row=1)
    run_button.grid(column=0, row=2)

    setChildrenPadding(root_selectfile, 10 , 10)

    root_selectfile.mainloop()

#INTERAFCE FOR PC ONLY WINDOW MODE (MAIN PyPLIS WINDOW)
def  runPCOWM(fileContents, fileName):
    global runLogicLoop
    inputsArray = []
    print(fileContents)

    for i in range(len(fileContents)):
        if fileContents[i] == "IN":
            inputsArray.append(i)
    
    root = Tk()
    root.title("PyPLIS - "+fileName)

    inputs_frame = Frame(root, relief='sunken', borderwidth=2)
    inputs_frame.grid(row=0, column=0, rowspan=2)
    input_checkboxes = {}
    inputVarsDict = {}

    for i in range(len(inputsArray)):
        inputVarsDict[inputsArray[i]] = BooleanVar(value=False)
        input_checkboxes[inputsArray[i]] = Checkbutton(inputs_frame, 
                                                       variable=inputVarsDict[inputsArray[i]],
                                                       onvalue=True,
                                                       offvalue=False,
                                                       command=isChecked(inputVarsDict[inputsArray[i]].get(), inputsArray[i]),
                                                       text = 'Input at line ' + str(inputsArray[i]+1) + ':')

        input_checkboxes[inputsArray[i]].grid(row=i, column=1)
    setChildrenPadding(inputs_frame, 3, 3)
    setChildrenPadding(root, 5, 5)

    out_lbl = Label(root, text = 'Result:')
    out_lbl.grid(column = 0, row=len(inputsArray)+1)
    run_but = Button(root, text = 'Run logic', command = lambda: initLogicLoop(fileContents, out_lbl))
    run_but.grid(column = 0, row = len(inputsArray)+2)


    root.mainloop()

def isChecked(value, key):
    global inputsDict
    inputsDict[key] = value
    print(inputsDict)



def initLogicLoop(fileContents, out_lbl):
    out_lbl.configure(text = 'Result:'+logicLoop(fileContents))

def logicLoop(fileContent):
    global inputsDict
    
    lineToValue = inputsDict

    for i in range(len(fileContent)):
        line = fileContent[i]
        output = ''
        words = line.split()
        #try:
        print(lineToValue)
        print(i)
        if words[0] == 'AND':
            lineToValue[i] = lineToValue[int(words[1])-1] and lineToValue[int(words[2])-1]
        if words[0] == 'OR':
            lineToValue[i] = lineToValue[int(words[1])-1] or lineToValue[int(words[2])-1]
        if words[0] == 'NOT':
            lineToValue[i] = not lineToValue[int(words[1])-1]
        if words[0] == 'XOR':
            lineToValue[i] = lineToValue[int(words[1])-1] != lineToValue[int(words[2])-1]
        if words[0] == 'NAND':
            lineToValue[i] = not (lineToValue[int(words[1])-1] and lineToValue[int(words[2])-1])
        if words[0] == 'NOR':
            lineToValue[i] = not (lineToValue[int(words[1])-1] or lineToValue[int(words[2])-1])
        if words[0] == 'OUT':
            for i in words[1::]:
                if lineToValue[int(i)-1]:
                    output += '1'
                else:
                    output += '0'
            return output
        #except KeyError:
            #print('Key error')

#mode = input()
mode = 'PCOWM'
if mode == 'PCOWM':
    initPcOnlyWindowMode()
