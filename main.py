import os
from strings import greetingString, menuString, inputErrorString, menuStringEnd
from utils import mkdir


def main():  
    mkdir()  
    from log import authLog
    from fileHandler import chooseCSV, chooseDocx_vEdge, modNDLMvEdge, modNDLM2vEdge, cEdgeTemplatevEdge
    from functions import checkIsDigit
    while True:
        os.system("CLS")
        greetingString()
        menuString()
        selection = input("Please choose the option that you want: ")
        if checkIsDigit(selection):
            if selection == "1":
                csvValues = chooseCSV()
                docxValues = chooseDocx_vEdge(csvValues)
                rowText = docxValues['rowText']
                rowText1 = docxValues['rowText1']
                modNDLMvEdge(rowText, rowText1)
                modNDLM2vEdge(rowText, rowText1)
                cEdgeTemplatevEdge(rowText, rowText1)
                break

            if selection == "2":
                print(f"There are no Tier 4 using ISR platform, try again. :)")
                os.system("PAUSE")
                break

        else:
            authLog.error(f"Wrong option chosen {selection}")
            inputErrorString()
            os.system("PAUSE")
    while True:
        os.system("CLS")
        menuStringEnd()
        mkdir()
        selection = input("Please choose the option that you want: ")
        if checkIsDigit(selection):
            if selection == "1":
                csvValues = chooseCSV()
                docxValues = chooseDocx_vEdge(csvValues)
                rowText = docxValues['rowText']
                rowText1 = docxValues['rowText1']
                modNDLMvEdge(rowText, rowText1)
                modNDLM2vEdge(rowText, rowText1)
                cEdgeTemplatevEdge(rowText, rowText1)

            if selection == "2":
                print(f"There are no Tier 4 using ISR platform, try again. :)")
                os.system("PAUSE")

            if selection == "3":
                break
    
        else:
            authLog.error(f"Wrong option chosen {selection}")
            inputErrorString()
            os.system("PAUSE")

if __name__ == "__main__":
    main()