#!/bin/python3

import pickle
import os
import subprocess
images={
    "ubuntu":"kasmweb/core-ubuntu-focal:1.11.0-rolling",
    "parrot":"kasmweb/parrotos-5-desktop:develop-rolling",
    "fedora":"kasmweb/fedora-37-desktop:develop",
    "kali":"kasmweb/core-kali-rolling:1.12.0-rolling"
    }
def errorMessage():
    print("there are no containers created")
def createContainer(name, passd,root,disposable,port,image,discription,status):
    match typeOfContainer(root,disposable):
        case 0:
            os.system(f"docker run -itd --name {name} --shm-size=512m -p {port}:6901 -e VNC_PW={passd} {image}")
            pass
        case 1:
            os.system(f"docker run -itd --rm --name {name} --shm-size=512m -p {port}:6901 -e VNC_PW={passd} {image}")
            pass
        case 2:
            os.system(f"docker run -itd --user root --name {name} --shm-size=512m -p {port}:6901 -e VNC_PW={passd} {image}")
            pass
        case 3:
            os.system(f"docker run -itd --user root --rm --name {name} --shm-size=512m -p {port}:6901 -e VNC_PW={passd} {image}")
            pass
    displayInfo(name,passd,port,root,disposable,discription,status)
    preContent={}
    try:
        file = open("/etc/fisher/.container","rb")
        preContent=pickle.load(file)
        file.close()
    except:
        pass
    file=open("/etc/fisher/.container","wb")
    containerInfo={
        "password":passd,
        "port":port,
        "root":root,
        "disposable":disposable,
        "description":discription,
        "status":status
    }
    preContent.update({name:containerInfo})
    pickle.dump(preContent,file)
    file.close()
    pass
def displayInfo(name,passd,port,root,disposable,discription,status):
    print(f"Container Name: {name}")
    ipaddress = subprocess.getoutput("ip addr | grep inet | grep eth0 | awk '{print $2}' | cut -f 1 -d \"/\"")
    print(f"website: https://{ipaddress}:{port}")
    print(f"username: kasm_user")
    print(f"password: {passd}")
    if(root=="y"):
        print(f"root privilege\tstatus: {status}")
    else:
        print(f"user privilege\tstatus: {status}")
    if(disposable=="y"):
        print("disposable container")
    else:
        print("NON disposable container")
    print(f"Discription: {discription}\n")
    pass
def listImages():
    imageList=images.keys()
    for i in imageList:
        print("\t"+i+"\n")
    pass
def listContainer():
    try:
        file = open("/etc/fisher/.container","rb")
        content=pickle.load(file)
        listOfContainers = content.keys()
        i=1
        for c in listOfContainers:
            temp=content.get(c)
            status = temp.get("status")
            print(str(i)+"  "+c+"    status: "+status)
            i+=1
        file.close()
    except:
        errorMessage()
    pass
def loadContainer(name):
    try:
        file=open("/etc/fisher/.container","rb")
        dictCont=pickle.load(file)
        presentContainers=dictCont.keys()
        if (name not in presentContainers):
            print("container not found!")
            file.close()
            return
        os.system(f"docker start {name}")
        cInfo=dictCont.get(name)
        displayInfo(name,cInfo.get("password"),cInfo.get("port"),cInfo.get("root"),cInfo.get("disposable"),cInfo.get("description"),"running")
        file.close()
        file=open("/etc/fisher/.container","wb")
        dictCont.get(name).update(status="running")
        pickle.dump(dictCont,file)
        file.close()
    except:
        errorMessage()
    pass
def deleteContainer(name,delete='n'):
    flag = 0
    try:
        file=open("/etc/fisher/.container","rb")
        dictCont=dict(pickle.load(file))
        presentContainers=dictCont.keys()
        st = dictCont.get(name).get("disposable")
        if(st == "y"):
            flag = 1
        file.close()
    except:
        errorMessage()
    if name not in presentContainers:
        print("container not found!")
        return
    if(flag == 1):
        file = open("/etc/fisher/.container","wb")
        dictCont.pop(name)
        pickle.dump(dictCont,file)
        file.close()
        os.system(f"docker stop {name}")
        print("container deleted")
    if(flag == 0):
        while True:
            file = open("/etc/fisher/.container","wb")
            match delete:
                case "y":
                    dictCont.pop(name)
                    pickle.dump(dictCont,file)
                    os.system(f"docker stop {name}")
                    os.system(f"docker rm {name}")
                    print("container deleted")
                    break
                case "n":
                    dictCont.get(name).update(status="stopped")
                    pickle.dump(dictCont,file)
                    os.system(f"docker stop {name}")
                    print("container is stoped")
                    break
                case _:
                    print("invalid input!")
                    pass
        file.close()
    pass
def typeOfContainer(root,disp):
    tp=0
    if(root=="y"):
        tp+=2
    if(disp=="y"):
        tp+=1
    return tp
os.system("clear")
while True:
    flag = 0
    delete=False
    commandInput = input(">>> ")
    command = commandInput.split(" ")
    if(command[0] == "info" or command[0] == "start"):
        command[0] = "load"
    if(command[0] == "rm" or command[0] == "del"):
        delete = True
        command[0] = "stop"  
    match command[0]:
        case "create":
            if(len(command) <= 1 or command[1] == ""):
                print("syntax error\nsyntax:\n\tcreate [image name]")
            elif(command[1] not in images.keys()):
                print("image not found")
            else:
                try:
                    name=input("Name: ")
                    if(len(name) <= 1):
                        print("name has to be minimum of 2 characters")
                        raise "exp"
                    passd=input("Password: ")
                    root=input("root? (y/n): ")
                    if (root != "y" and root != "n"):
                        print("invalid input")
                        raise "exp"
                    disp=input("disposable? (y/n): ")
                    if (disp != "y" and disp != "n"):
                        print("invalid input")
                        raise "exp"
                    discription = input("Discription of container: ")
                    p=input("container number (only 2 digits): ")
                    try:
                        port= "60"+p
                    except:
                        print("container number has to be a numarical value!")
                        flag = 1
                except:
                    flag = 1
                if(flag == 0):
                    createContainer(name,passd,root,disp,port,images.get(command[1]),discription,"running")
                pass
        case "list":
            if(len(command) > 1 and command[1] == "images"):
                listImages()
                pass
            elif(len(command) == 1):
                listContainer()
                pass
            else:
                print("""

    invalid command!

    list
        => to show the list of containers
    list images
        => to show the list of available images

                """)
                pass
            pass
        case "load":
            if(len(command) > 1 and command[1] != " "):
                name = command[1]
            else:
                name = input("Container name: ")
            try:
                file = open("/etc/fisher/.container","rb")
                readc = pickle.load(file)
                file.close()
            except:
                errorMessage()
            if(name not in readc.keys()):
                print("container not found!")
                pass
            else:
                loadContainer(name)
            pass
        case "stop":
            if(len(command) > 1 and command[1] != " "):
                name = command[1]
            else:
                name = input("Container name: ")
            try:
                file = open("/etc/fisher/.container","rb")
                readc = pickle.load(file)
                file.close()
            except:
                errorMessage()
            if(name not in readc.keys()):
                print("container not found!")
                pass
            else:
                if(delete):
                    deleteContainer(name,"y")
                else:
                    deleteContainer(name)
            pass
        case "clear":
            os.system("clear")
            pass
        case "help":
            print("""
    create
        => to create a new container
        syntax: create [image name]
    list
        => to list images and containers
        list => to list containers
        list images => to list all images
    load
        => load / start containers
        syntax: load [container name]
    stop
        => to remove a container
        syntax: del [container name]
    clear
        => clear screen
    help
        => to view this message
    exit
        => to exit the program
            """)
            pass
        case "exit":
            exit()
        case _:
            print("invalid command")
            pass
