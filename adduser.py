import os
import re

# Jared Marcuccilli
# NSSA-221 Script 02

def read_data(_fName):
    linearray = []
    print("Reading data...")
    f = open(_fName, 'r')
    line = f.readline().strip()
    linearray.append(line)
    
    while line:
        #print(line)
        line = f.readline().strip()
        linearray.append(line)

    return linearray

# linesplit[0] EmployeeID (XXXXXXX)
# linesplit[1] LastName (Letters, ', -)
# linesplit[2] FirstName (Letters, ', -)
# linesplit[3] Office (XX-XXXX)
# linesplit[4] Phone (XXX-XXXX OR "unlisted")
# linesplit[5] Department (all letters, numbers, and -)
# linesplit[6] Group (all letters, numbers, and -)

def add_users(_Array):
    global DEFAULT_SHELL
    usernames = []
    finalusernames = []
    finalusername = ""
    print("Adding users...")

    for line in _Array:
        linesplit = line.split(",")
        #print(linesplit[0])
        if re.match(r"\d{7}", linesplit[0]): # Valid 7-digit Employee ID
            #print("EmployeeID OK")
            if re.match(r"[a-zA-Z'-]+", linesplit[1]): # Valid LastName
                #print("LastName OK")
                if re.match(r"[a-zA-Z'-]+", linesplit[2]): # Valid FirstName
                    #print("FirstName OK")
                    if re.match(r"\d\d-\d\d\d\d", linesplit[3]): # Valid Office
                        #print("Office OK")
                        #if re.match(r"\d\d\d-\d\d\d\d|unlisted", linesplit[4]): # Valid Phone
                            #print("Phone OK")
                            if re.match(r"^[a-zA-Z0-9-]+$", linesplit[5]): # Valid Department
                                os.system("mkdir /home/" + linesplit[5])
                                #print("Department OK")
                                if re.match(r"^[a-zA-Z0-9-]+$", linesplit[6]): # Valid Group
                                    #print("Group OK")
                                    os.system("groupadd -f " + linesplit[6])
                                    username = linesplit[2][0].lower() + linesplit[1].lower().replace("'", "").replace("-", "")
                                    if username in usernames:
                                        print("Repeat username")
                                        tempusername = finalusernames[-1]
                                        temp = ""
                                        for char in tempusername:
                                            if not char.isdigit():
                                                temp = temp + char
                                        x = len(finalusername) - len(temp)
                                        if x == 0:
                                            number = 0
                                        else:
                                            number = int(tempusername[-x:])
                                        y = int(number) + 1
                                        finalusername = username + str(y)
                                    else:
                                        finalusername = username
                                    finalusernames.append(finalusername)
                                    print("***Adding user: " + finalusername)
                                    usernames.append(username)

                                    if linesplit[5] == "ceo":
                                        DEFAULT_SHELL = "csh"
                                    else:
                                        DEFAULT_SHELL = "bash"
                                        
                                    os.system("groupadd -f " + linesplit[6])
                                    os.system("sudo useradd -m -d /home/" + linesplit[5].lower() + "/" + finalusername + " -s /bin/" + DEFAULT_SHELL + " -g " + linesplit[6].lower() + ' -c "' + linesplit[2] + ' ' + linesplit[1] + '" ' + finalusername)
                                    password = finalusername[::-1]
                                    os.system("echo " + password + " | passwd " + finalusername + " --stdin")
                                    os.system("passwd -e " + finalusername)
                                else:
                                    print("Invalid group for ID: " + linesplit[0])
                            else:
                                print("Invalid department for ID: " + linesplit[0])
                        #else:
                            #print("Invalid phone for ID: " + linesplit[0])
                    else:
                        print("Invalid office for ID: " + linesplit[0])
                else:
                    print("Invalid first name for ID: " + linesplit[0])
            else:
                print("Invalid last name for ID: " + linesplit[0])
        elif linesplit[0] == "":
            break
        else:
            print("Invalid employee ID encountered.")
# --- Main Program ---
fName = "Lab02_Users.csv"
add_users(read_data(fName))