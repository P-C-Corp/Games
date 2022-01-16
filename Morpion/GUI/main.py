# ___                                 _
#|_ _| _ __ ___   _ __    ___   _ __ | |_  ___
# | | | '_ ` _ \ | '_ \  / _ \ | '__|| __|/ __|
# | | | | | | | || |_) || (_) || |   | |_ \__ \
#|___||_| |_| |_|| .__/  \___/ |_|    \__||___/
#                |_|
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import QCoreApplication, QThread, pyqtSignal
import sys
import os
import traceback
import platform
import getpass
from PyQt5.QtGui import QMovie, QPixmap
import time
import json
import random
from functools import partial
import uuid
import logging
import shutil


# ____         _
#/ ___|   ___ | |_    _   _  _ __
#\___ \  / _ \| __|  | | | || '_ \
# ___) ||  __/| |_   | |_| || |_) |
#|____/  \___| \__|   \__,_|| .__/
#                           |_|


#get the path to the script's file
user = str(getpass.getuser())
user = user[:5]
path = (fr"C:\Users\{user}\AppData\Local\Programs\PetchouDev-Morpion")

#Get the path to the UI files (GUI ressources and  images)
def pathToUi()->str:
    global path
    if platform.system() == 'Windows':
        thePath = path+"/"  
        print(path, thePath)
        return thePath
    else:
        return path+"/ui/" 




#get the path to the save file
def pathToSave()->str:
    if platform.system() == 'Windows':
        usr = str(getpass.getuser())
        usr = usr[:5]
        path = str("c:/Users/{}/PetchouDev/Morpion".format(usr))
        return path
    else:
        return f"/Users/{getpass.getuser()}/PetchouDev/Morpion"

global save
save = {}


#gérer la langue
global lang
lang = {"fr":None, "en":None}
#créer les variables joueurs
global p1 
p1= ""
global p2 
p2 = ""
global currentPlayer
currentPlayer = None


#créer la grille
grid = {1:None, 2:None, 3:None, 4:None, 5:None, 6:None, 7:None, 8:None, 9:None}
global turn
turn = 1
global winner
winner = None






#    _                   _  _               _    _
#   / \    _ __   _ __  | |(_)  ___   __ _ | |_ (_)  ___   _ __
#  / _ \  | '_ \ | '_ \ | || | / __| / _` || __|| | / _ \ | '_ \
# / ___ \ | |_) || |_) || || || (__ | (_| || |_ | || (_) || | | |
#/_/   \_\| .__/ | .__/ |_||_| \___| \__,_| \__||_| \___/ |_| |_|
#         |_|    |_|


#Barre de chargement et tâches de démarrage

class Task(QThread):
    #créer les variables d'interraction avec le GUI
    changeValue = pyqtSignal(int)
    nextScreen = pyqtSignal(str)
    isFirst = pyqtSignal()
    loader = pyqtSignal()
    is_paused = False
    #barre de chargement
    def run(self):

        for i in range(1, 101):
            self.changeValue.emit(i)
            if i == 40:
                self.isFirst.emit()
            elif i == 80:
                self.loader.emit()
            
            elif  i == 101:
                print("Load reached 100% triggering next step")
            time.sleep(0.04)
            while self.is_paused:
                time.sleep(0)
        print('Load Complete')
        self.nextScreen.emit("Loading succesful !")

    def pause(self):
        self.is_paused = True
    def resume(self):
        self.is_paused = False



#fenêtre de chargement
class Startup(QtWidgets.QMainWindow):
    window_closed = pyqtSignal()
    def __init__(self):
        
        super(Startup, self).__init__() # Call the inherited classes __init__ method
        path = pathToUi()
        uic.loadUi(path+"/Load.ui", self) # Load the .ui file
        print('UI file loaded')

        #self.Form.setStyleSheet('background-color:white;')
        self.setFixedWidth(850)
        self.setFixedHeight(330)

        self.logo = QMovie(f"{pathToUi()}/Morpion.gif")
        self.label_3.setMovie(self.logo)
        self.logo.start()
        
        self.progressBar.setValue(0)
        
        self.show()

        self.startProgressBar()



    def loadFiles(self):
        #charger le fichier de sauvegarde
        global save 
        save = {}
        with open(f'{pathToSave()}/save.json', 'r', encoding='utf-8') as saveFile:
            save = json.load(saveFile)
            print(save)

        logging.basicConfig(filename=pathToSave()+"/logs.txt", level=logging.DEBUG)

        logging.debug('initializing logs session')


    def getLang(self):
        self.thread.is_paused = True
        global lang
        items = ("English", "Français")
		
        item, ok = QtWidgets.QInputDialog.getItem(self, "select input dialog", 
        "list of languages", items, 0, False)
			
        if ok and item:
            lang = str(item)
            with open(pathToSave()+"/language.txt", "w") as output:
                output.write("fr" if lang == "Français"  else "en" )
        self.thread.is_paused = False



    def isFirst(self):

        global lang
        try:
            with open(pathToSave()+"/language.txt", "r"):
                pass
            
        except FileNotFoundError:
            print('First use, initializing filesystem...')
            try:
                os.mkdir(pathToSave())
            except FileExistsError:
                pass
            try:
                os.mkdir(pathToSave()+"/logs")
            except FileExistsError:
                pass
            save = open(pathToSave()+'/save.json', "w")
            debugDatas = {}
            json.dump(debugDatas, save)
            save.close()

            langage = open(pathToSave()+"/language.txt", "w")
            langage.write('en')
            langage.close()
            
            logs = open(pathToSave()+"/logs/logs.txt", "w")
            logs.write("Initialized logs file")
            logs.close()

            self.getLang()

    def startProgressBar(self):
        
        self.thread = Task()
        self.thread.changeValue.connect(self.progressBar.setValue)
        self.thread.nextScreen.connect(self.nextStep)
        self.thread.isFirst.connect(self.isFirst)
        self.thread.loader.connect(self.loadFiles)
        self.thread.start()

    def nextStep(self, log):
        print('Loading next step')
        print(log)
        self.win = SetPlayers()
        
        self.win.show()
        self.close()

    
    def closeWindow(self, event):
        print('Closed')
        self.window_closed.emit()
        event.accept()

#tache de gestion de la liste de joueurs
class PlayerUpdater(QThread):
    updater = pyqtSignal()
    L1Deleted = None
    L2Deleted = None

    def run(self):
        while True:
            self.updater.emit()
            time.sleep(0.3)
        



#Gérer les joueurs
class SetPlayers(QtWidgets.QMainWindow):
    def __init__(self) -> None:
        super(SetPlayers, self).__init__()
        uic.loadUi(f'{pathToUi()}/Players.ui', self)

        self.PlayersList()
        self.L1DEL = None
        self.L2DEL = None

        self.pushButton.clicked.connect(self.NewPlayer)
        self.pushButton_2.clicked.connect(self.NewPlayer)
        self.pushButton_3.clicked.connect(self.nextStep)

        self.thread = PlayerUpdater()
        self.thread.updater.connect(self.UpdatePlayers)
        self.thread.start()

        self.show()

    #Lister les joueurs enregistrés
    def PlayersList(self):
        global save
        self.comboBox.addItem("Select Player")
        self.comboBox_2.addItem("Select Player")
        for player in save.keys():
            if player != 'currentPlayers':
                self.comboBox.addItem(player)
                self.comboBox_2.addItem(player)

    def UpdatePlayers(self):

        #Gérer les noms dans les listes

        L1Items = [self.comboBox.itemText(i) for i in range(self.comboBox.count())]
        
        L2Items = [self.comboBox_2.itemText(i) for i in range(self.comboBox_2.count())]

        
        #liste 2 en focntion de liste 1
        if self.comboBox.currentText() in L2Items :
            if self.comboBox.currentText() != "Select Player":
                if self.L2DEL != None:
                    self.comboBox_2.addItem(self.L2DEL)
                    
                self.L2DEL = self.comboBox.currentText()
                self.comboBox_2.removeItem(self.comboBox_2.findText(self.comboBox.currentText()))
            elif self.comboBox.currentText() == "Select Player" and self.L2DEL not in L2Items and self.L2DEL != None:
                self.comboBox_2.addItem(self.L2DEL)


        #liste 1 en focntion de liste 2
        if self.comboBox_2.currentText() in L1Items :
            if self.comboBox_2.currentText() != "Select Player":
                if self.L1DEL != None:
                    self.comboBox.addItem(self.L1DEL)
                    
                self.L1DEL = self.comboBox_2.currentText()
                self.comboBox.removeItem(self.comboBox.findText(self.comboBox_2.currentText()))
            elif self.comboBox_2.currentText() == "Select Player" and self.L1DEL not in L1Items and self.L1DEL != None:
                self.comboBox.addItem(self.L1DEL)


        #gérer le  bouton play
        if "Select Player" == (self.comboBox_2.currentText() or self.comboBox.currentText()):
            self.pushButton_3.setEnabled(False)
        else:
            self.pushButton_3.setEnabled(True)

    def NewPlayer(self):
        text, ok = QtWidgets.QInputDialog.getText(self, 'Create new player', "New player's name :")
		
        if ok and text != "":
            global save
            if str(text) not in save.keys():
                save[str(text)] = [0, 0, 0]
                self.comboBox.addItem(str(text))
                self.comboBox_2.addItem(str(text))
            if self.comboBox.currentText() == "Select Player":
                self.comboBox.setCurrentIndex(self.comboBox.findText(str(text)))
            else:
                if self.comboBox_2.currentText() == "Select Player":
                    self.comboBox_2.setCurrentIndex(self.comboBox_2.findText(str(text)))

    def nextStep(self):
        global p1
        global p2
        p1 = self.comboBox.currentText()
        p2 = self.comboBox_2.currentText()
        print('Loading next step')
        self.win = Game()
        self.win.show()
        self.close()

    def closeWindow(self, event):
        print('Closed')
        self.window_closed.emit()
        event.accept()



#Jouer au jeu
class Game(QtWidgets.QMainWindow):
    window_closed = pyqtSignal()
    def __init__(self):
        
        super(Game, self).__init__() # Call the inherited classes __init__ method
        uic.loadUi(f'{pathToUi()}/Game.ui', self) # Load the .ui file
        print('UI file loaded')


        #récupérer les joueurs et décider qui commence
        global p1icon
        p1icon = QPixmap(f'{pathToUi()}/cross.png')
        global p2icon
        p2icon = QPixmap(f'{pathToUi()}/circle.png')
        
        global p1
        global p2
        
        self.currentPlayer = random.choice([p1, p2])

        #mettre  en place le GUI
        global cases
        self. cases = [self.L1, self.L2, self.L3, self.L4, self.L5, self.L6, self.L7, self.L8, self.L9]
        for case in self.cases:
            case.setPixmap(QPixmap(f'{pathToUi()}/empty.png'))
            case.mousePressEvent = partial(self.play, case)
        self.grid.setPixmap(QPixmap(f'{pathToUi()}/grid.png'))

        self.PlayerTurn.setText(f"It's {self.currentPlayer}'s trun !")
        

        if self.currentPlayer == p1:
            self.Icon.setPixmap(p1icon)
        else: 
            self.Icon.setPixmap(p2icon)

        self.TurnCounter.setText("Trun 1")

        self.show()


    def play(self, case, event):

        global grid
        global p1
        global p2
        global p1icon
        global p2icon
        global turn
        global winner 
        #récupérer les cases
        case = str(case.objectName())
        case = int(case[-1])

        print(self.currentPlayer, p1, p2)
        #si c'est p1 qui joue
        if self.currentPlayer == p1 and grid[case] == None:
            print('P1 played')
            grid[case] = p1
            self.cases[case -1].setPixmap(QPixmap(f'{pathToUi()}/cross.png'))
            self.currentPlayer = p2
            self.PlayerTurn.setText(f"It's {self.currentPlayer}'s trun !")
            self.Icon.setPixmap(p1icon if self.currentPlayer == p1 else p2icon)
            text = str(self.TurnCounter.text())
            self.TurnCounter.setText(f"Turn {int(text[-1])+1}")
            turn = int(text[-1])+1

        #si c'est p2 qui joue
        elif self.currentPlayer == p2 and grid[case] == None:
            print('P2 played')
            grid[case] = p2
            self.cases[case -1].setPixmap( QPixmap(f'{pathToUi()}/circle.png'))
            self.currentPlayer = p1
            self.PlayerTurn.setText(f"It's {self.currentPlayer}'s trun !")
            self.Icon.setPixmap(p1icon if self.currentPlayer == p1 else p2icon)
            text = str(self.TurnCounter.text())
            self.TurnCounter.setText(f"Turn {int(text[-1])+1}")
            turn = int(text[-1])+1


        #savoir si c'est terminé
        isEnded = self.isEnded()
        if  isEnded != True and isEnded == 10 : #not car True et false sont inversés... --,
            winner = None
            self.nextStep("Game ended on draw")
            

        elif isEnded != True and isEnded != 10:
            winner = isEnded
            self.nextStep(f"{isEnded} won the game")


        #si le jeu est fini
    def isEnded(self):
        global grid
        global turn
        if grid[1] == grid[2] == grid[3] != None:
            return grid[1]
        elif grid[4] == grid[5] == grid[6] != None:
            return grid[4]
        elif grid[7] == grid[8] == grid[9] != None:
            return grid[7]
        elif grid[1] == grid[4] == grid[7] != None:
            return grid[1]
        elif grid[2] == grid[5] == grid[8] != None:
            return grid[2]
        elif grid[3] == grid[6] == grid[9] != None:
            return grid[3]
        elif grid[1] == grid[5] == grid[9] != None:
            return grid[1]
        elif grid[3] == grid[5] == grid[7] != None:
            return grid[3]
        elif turn == 10:
            return 10
        else:
            return True


    def nextStep(self, log):
        print('Loading next step')
        print(log)
        self.win = EndScreen()
        
        self.win.show()
        self.close()

    
    def closeWindow(self, event):
        print('Closed')
        self.window_closed.emit()
        event.accept()



#afficher les résultats
class EndScreen(QtWidgets.QMainWindow):
    window_closed = pyqtSignal()
    def __init__(self):
        
        super(EndScreen, self).__init__() # Call the inherited classes __init__ method
        uic.loadUi(f'{pathToUi()}/EndScreen.ui', self) # Load the .ui file
        
        global winner
        global p1
        global p2
        global save
        if winner == None:
            self.Notif.setText("That's a draw...")
            self.Comment.setText("Well done to the both of you")
            save[p1][2] += 1
            save[p2][2] += 1

        
        else:
            self.Notif.setText(f"Congratz {winner} !")
            self.Comment.setText("You won the game")
            if winner == p1:
                save[p1][0] += 1
                save[p2][1] += 1
            else:
                save[p1][1] += 1
                save[p2][0] += 1
            
        with open(f'{pathToSave()}/save.json', 'w', encoding='utf-8') as saveFile:
            json.dump(save, saveFile)

        print(save)
        
        self.ps1.setText(f"{p1} : {save[p1][0]} wins, {save[p1][1]} defeats and {save[p1][2]} draw")
        self.ps2.setText(f"{p2} : {save[p2][0]} wins, {save[p2][1]} defeats and {save[p2][2]} draw")

        self.Replay.clicked.connect(self.ReplayNow)
        self.Leave.clicked.connect(self.LeaveGame)
        self.Change.clicked.connect(self.ChangePlayers)
        self.Settings.clicked.connect(self.SettingsPannel)

        self.show()

    def SettingsPannel(self):
        self.settingsWindow = SettingsWindow(self)
        self.settingsWindow.show()


    def ReplayNow(self):
        global grid
        grid = {1:None, 2:None, 3:None, 4:None, 5:None, 6:None, 7:None, 8:None, 9:None}
        self.nextStep(Game())

    def ChangePlayers(self):
        global grid
        grid = {1:None, 2:None, 3:None, 4:None, 5:None, 6:None, 7:None, 8:None, 9:None}
        self.nextStep(SetPlayers())

    def LeaveGame(self):
        self.close()
        QCoreApplication.instance().quit()

    def nextStep(self, screen):
        self.win = screen
        self.win.show()
        self.close()

    
    def closeWindow(self, event):
        print('Closed')
        self.window_closed.emit()
        event.accept()

#réglages 
class SettingsWindow(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(SettingsWindow, self).__init__(parent)
        uic.loadUi(f'{pathToUi()}/Settings.ui', self)
        
        self.btn.clicked.connect(self.getItem)
        
        
        self.eraseDatas.clicked.connect(self.gettext)
        
        with open(pathToSave()+"/language.txt","r") as language:
            self.currentLanguage = language.read()

        self.le.setText(self.currentLanguage)

        self.Save.clicked.connect(self.QuitAndApply)
        self.Cancel.clicked.connect(self.QuitWithoutApply)


    def getItem(self):
            items = ("English - en", "French - fr")
            
            item, ok = QtWidgets.QInputDialog.getItem(self, "Select your language", 
            "list of languages", items, 0, False)
                
            if ok and item:
                
                self.le.setText(item)

    def gettext(self):
            captcha = str(uuid.uuid4())
            captcha = captcha[:6]
            text, ok = QtWidgets.QInputDialog.getText(self, 'Erase datas', f"Recopy the following text to proceed \n{captcha}\nPlease note that the game will  restart after deleting datas")
                
            if ok and str(text) == captcha:
                global save
                save = {}
                with open(pathToSave()+"/save.json", "w", encoding="utf-8") as newSave:
                    json.dump(save, newSave)
                time.sleep(2)
                self.close()
                QCoreApplication.instance().quit()

    def QuitWithoutApply(self):
        self.close()

    def QuitAndApply(self):
        global lang
        item = str(self.le.text())
        item = str(item)
        item = item[:-2]
        if  item in lang.keys():
            newlang = item
            with open(pathToSave()+"/language.txt" ,"w") as output:
                output.write(newlang)

        else:
            pass
        self.close()


# _____  ____   ____    ___   ____   ____
#| ____||  _ \ |  _ \  / _ \ |  _ \ / ___|
#|  _|  | |_) || |_) || | | || |_) |\___ \
#| |___ |  _ < |  _ < | |_| ||  _ <  ___) |
#|_____||_| \_\|_| \_\ \___/ |_| \_\|____/

class ReportError(QtWidgets.QMainWindow):
    def __init__(self):
        super(ReportError, self).__init__() # Call the inherited classes __init__ method
        uic.loadUi(f'{pathToUi()}/Error.ui', self)

        self.logView = 322
        self.setFixedHeight(130)

        with open(pathToSave()+"/logs/logs.txt") as logs:
            self.traceback = logs.read()  
        self.logText.setText(self.traceback)
        self.here.setText('<a href=\"https://github.com/P-C-Corp/Games/issues/new">here</a>')
        self.View.clicked.connect(partial(self.Show, self.View))
        self.cancel.clicked.connect(self.exitApp)
        self.ResetFiles.clicked.connect(self.Reset)

    def Show(self, btn):
        self.setFixedHeight(self.logView)
        btn.setEnabled(False)

    def Reset(self):
            
            
            shutil.rmtree(pathToSave(), ignore_errors=True)

            
            self.close()
            QCoreApplication.instance().quit()

    def exitApp(self):
        self.close()
        QCoreApplication.instance().quit()


# ____
#|  _ \   ___  _ __ ___    __ _  _ __  _ __   __ _   __ _   ___
#| | | | / _ \| '_ ` _ \  / _` || '__|| '__| / _` | / _` | / _ \
#| |_| ||  __/| | | | | || (_| || |   | |   | (_| || (_| ||  __/
#|____/  \___||_| |_| |_| \__,_||_|   |_|    \__,_| \__, | \___|
#                                                   |___/
try:
    
    if __name__ == "__main__":
        try:
            pathToFolder = str(pathToSave())
            pathToFolder = pathToFolder.replace("/Morpion", "")
            os.mkdir(pathToFolder)
        except FileExistsError:
            print(pathToSave())
            pass

        try:
            os.mkdir(pathToSave())
        except FileExistsError:
            print(pathToSave())
            pass

        try:
            os.mkdir(pathToSave()+"/logs")
        except FileExistsError:
            pass

        logfile = open(pathToSave()+"/logs/logs.txt", "w")
        logfile.write("Log file initialized\n")
        logfile.close()


        logging.basicConfig(filename=pathToSave()+"/logs/logs.txt", level=logging.DEBUG)

        logging.debug('initializing logs session')

        application = QtWidgets.QApplication(sys.argv)
        window = Startup()
        window.show()
        currentExitCode = application.exec_()
        application = None 
        
except  :

    exc_type, exc_value, exc_traceback = sys.exc_info()
    traceback.print_exception(exc_type, exc_value, exc_traceback)
    logging.exception('Application went into an error')
    try:
        QCoreApplication.instance().quit()
    except:
        pass
    application = QtWidgets.QApplication(sys.argv)
    window = ReportError()
    window.show()
    currentExitCode = application.exec_()
    application = None 




