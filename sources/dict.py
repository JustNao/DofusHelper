import os, sys 

if getattr(sys, 'frozen', False):
    # If the application is run as a bundle, the PyInstaller bootloader
    # extends the sys module by a flag frozen=True and sets the app 
    # path into variable _MEIPASS'.
    application_path = sys._MEIPASS
else:
    application_path = os.path.dirname(os.path.abspath(__file__))

def Ids(path= application_path + 'sources\\scripts\\com\\ankamagames\\dofus\\network\\messages'):
    fichiers=[os.path.join(path, f) for f in os.listdir(path) if os.path.isfile(os.path.join(path, f)) and f != '.DS_Store' and f != 'Ids.py']
    dossiers=[os.path.join(path, f) for f in os.listdir(path) if os.path.isdir(os.path.join(path, f))]
    for f in fichiers:
        o=open(f)
        r=o.read()
        o.close()
        find=r.find('protocolId:uint =')
        if find != -1:
            find+=17
            find2=r.find(';',find)
            indice=int(r[find:find2])
            nom=os.path.basename(f)[:-3]
            dictIds[indice]=nom
    for d in dossiers:
        Ids(d)

def createIds(path='sources\\scripts\\com\\ankamagames\\dofus\\network\\messages'):
    ### crée le dictionnaire dictIds et le remplit
    global dictIds
    dictIds = dict()
    Ids(path)
    print('Terminé '+str(len(dictIds)))

import pickle

def dumpIds(path='./Ids'):
    ### crée le dictionnaire dictIds, le remplit et le sauvegarde
    createIds()
    f = open(path, 'wb')
    pickle.dump(dictIds, f)
    f.close()
    
def loadIds():
    ### charge le dictionnaire dictIds depuis le fichier
    f = open('./Ids', 'rb') #'/Users/louisabraham/Documents/Projet bot/Programme/Ids
    global dictIds
    dictIds = pickle.load(f)
    f.close()
