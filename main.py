from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from PyPDF2 import PdfReader
import pandas as pd

# read pdf
caminho = "atprank.pdf"
reader = PdfReader(caminho)
number_of_pages = len(reader.pages)
jogadores = pd.DataFrame(columns=["Rank", "Player", "Natl.", "Total Points", "Grand Slam Points", "Master 1000 Points", "Other Points", "Tourns. Played", "Points Dropping", "Next Best"])
for pag in range(1,number_of_pages):
    page = reader.pages[pag]
    text = page.extract_text().split() # text is the variable with full text of the page

    # managing the text
    data = text[5:8] # date
    jogadores_junto = text[25:-15] #info of the players together
    
    cont = cont2 = ajuste = 0
    j = {}
    duplo =False

    # itterating the jogadores junto to create each row of of DataFrame jogadores
    for p in range(len(jogadores_junto)):
        # fail safe if ajuste goes over the length
        if p+ajuste>len(jogadores_junto)-1:
            break
        palavra = jogadores_junto[p+ajuste]
        if cont == 0: 
            j["Rank"] = palavra
        elif cont==1:
            j["Player"] = palavra
            while "," not in palavra: # in case the player has more than one name
                index = p+ajuste
                j["Player"]+= " "+ jogadores_junto[index+1]
                ajuste += 1
                palavra = jogadores_junto[index+1]
            
            print("-="*24)
            print(f"jogador: {palavra}")
        elif cont ==2:
            ajuste-=1
            while True: # in case the player has more than one name
                if "(" in palavra:
                    break
                if palavra.isnumeric():
                    break 
                j["Player"] += " "+palavra
                ajuste +=1
                index = p+ajuste
                palavra = jogadores_junto[index+1]

        elif cont == 3:
            if not(palavra.isnumeric()):
                j["Natl."] = palavra
            else:
                ajuste -=1
        elif cont == 4:
            j["Total Points"] = palavra
        elif cont == 5:
            j["Grand Slam Points"] = palavra
        elif cont == 6: # for some reason the program (pypdf2) jumps over masters points to points dropping
            j["Points Dropping"] = palavra
        elif cont == 7:
            j["Next Best"] = palavra
        elif cont== 8:
            j["Tourns. Played"] = palavra
        elif cont == 9:
            j["Master 1000 Points"] = palavra
        elif cont == 10:
            j["Other Points"] = palavra
            cont = -1
            # add a row in jogadores (data frame)
            jogadores = jogadores._append(j.copy(), ignore_index=True)
            j.clear()
        cont+=1


print(data)
print('-='*24)
print(jogadores.head(2055))
jogadores.to_excel("tabela.xlsx") # saves an excel sheet of the ranking
