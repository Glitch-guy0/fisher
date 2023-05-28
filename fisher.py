#!/bin/python3

#! json format
# "name":{
#     "url":"",
#     "status":"",
#     "description":"",
#     "root":bool,
#     "password":""
# }


#* modules
import pickle
import platform
import os
import subprocess
import docker
import random
from sys import exit

#! update here
#* images section
images = {
    "ubuntu":"kasmweb/core-ubuntu-focal:1.13.0-rolling",
    "desktop":"kasmweb/ubuntu-bionic-desktop:1.10.0-rolling"
}
ip = subprocess.getoutput("ip a | grep \"eth0\" | grep \"inet\" | awk \'{print $2}\' | cut -d \"/\" -f 1")
#* path creating section
#! use platform.system() => import platform
PATH = platform.system()
username = subprocess.getoutput("powershell $env:username")
#?  windows / linux / macos
if(PATH == "Windows"):
    PATH = "C:/Users/"+username+"/Fisher"
elif(PATH == "Linux"):
    PATH = "/etc/Fisher"
else: #! update here
    #todo print error message with changes to work on
    pass
#? creating folder
# check if already exists else it will throw error
if(not os.path.isdir(PATH)):
    print("not exists")
    os.makedirs(PATH)
    portpath = PATH + "/Ports"
    filepath = PATH + "/Containers"
    with open(portpath,"wb") as tempp:
        pass
    with open(filepath,"wb") as temp:
        pass

#* file initialization
portpath = PATH+"/Ports"
PATH = PATH+"/Containers"
#* json file
containerinfo = {}
portinfo = {"ports":[]}

# todo: open file in write binary mode
def write():
    filewrite = open(PATH,"wb")
    portwrite = open(portpath,"wb")
    pickle.dump(containerinfo,filewrite) # because pickle uses binary to read & write json
    pickle.dump(portinfo,portwrite)
    filewrite.close()
    portwrite.close()
#? use pickle load and dump methods => import pickle
#todo: open file in read binary mode
fileread = open(PATH,"rb")
portread = open(portpath,"rb")
try:
    containerinfo = pickle.load(fileread)
    portinfo = pickle.load(portread)
except:
    pass
fileread.close()
portread.close()

#* checking for updates due to restart / from external command
#? if docker is not running
try:
    client = docker.from_env()
except:
    print("docker is not running")
    exit()
# todo cmd: docker ps -a => split get fields (name, status) and update accordingly

#todo get container id
containerlist = client.containers.list(all=True)
for parse in containerlist:
    #todo parse containers ids
    container = client.containers.get(str(parse).split(' ')[1].split(">")[0])
    #todo look for kasm images only
    if(container.name in containerinfo.keys()):
    #todo match names and update
        info = containerinfo.get(container.name)
        info.update(status=container.status)
        pass
#todo update file
write()

#* clear functionality
def clear():
    if(platform.system() == "Windows"):
        os.system("cls")
    else:
        os.system("clear")

#* creating container
# todo 
    #* get name, port, user type, password, description
def createContainer(image,name,root,password,description):
    #todo check for image
    if(image not in images):
        print("image not found\ninvalid image name")
        return
    image = images.get(image)
    #! port info updater
    temp = portinfo.get("ports")
    while True:
        randport = random.randint(10,99)
        port = "60"+str(randport)
        if(port not in temp):
            break
    #* add to json file

    temp.append(port)
    #todo check for root and deploy
    if(root == True):
        os.system(f"docker run --user 0 -itd --name {name} --shm-size=512m -p {port}:6901/tcp -e VNC_PW={password} {image}")
    else:
        os.system(f"docker run -itd --name {name} --shm-size=512m -p {port}:6901/tcp -e VNC_PW={password} {image}")
#* make url
    link = "https://"+ip+":"+port
#* update attributes
    attributes = {
        "status":"running",
        "url": link,
        "port":port,
        "password":password,
        "root":root,
        "description":description
    }
    #? update file using "pickle"
    containerinfo.update({name:attributes})
    write()

#* check for container
def check(name):
    if(name not in containerinfo.keys()):
        print("container not found\n")
        return True
    
#* displaying container
def display(name):
    #? get info from the file
    # check for container name
    if(check(name)):
        return
    print("\n\n")
    #* show url username, password, and status, description
    info = containerinfo.get(name)
    status = info.get("status")
    url = info.get("url")
    password = info.get("password")
    root = info.get("root")
    description = info.get("description")
    print(f"name: {name}")
    print(f"status: {status}")
    if(root):
        print("running in root privilege")
    print(f"url: {url}")
    print(f"username: kasm-user")
    print(f"password: {password}")
    print(f"description: {description}\n")


#* deleting container
def delete( name, delete = False):
    # check for image
    if(check(name)):
        return
    # todo " stop " method
    #* this method only stops
    if(not delete):
        subprocess.getoutput(f"docker stop {name}")
        print(f"{name} stopped")
        #update
        info = containerinfo.get(name)
        info.update(status="exited")
    else:
    #* this method stops and deletes container
        subprocess.getoutput(f"docker stop {name}")
        subprocess.getoutput(f"docker rm {name}")
        print(f"{name} deleted")
        #update
        temp = portinfo.get("ports")
        tempcontainer = containerinfo.get(name)
        temp.remove(tempcontainer.get("port"))
        containerinfo.pop(name)
    #! update file
    write()

#* listing container and images
def listContainer(container = True):
    #? two methods "images":"" => "": containers
    if(container):
        for containers in containerinfo.keys():
            print(f"\n{containers}")
    else:
        for image in images:
            print(f"\n{image}")
    print()

#* load container
def loadContainer(name):
    # check for container
    subprocess.getoutput(f"docker start {name}")
    info = containerinfo.get(name)
    info.update(status="running")
    write()
    display(name)


while True:
    cmd = input(">>> ").split(" ")
    #! command updates / changes
    if(cmd[0] == "ls"):
        cmd[0] = "list"
        pass
    #!end
    match(cmd[0]):
        case "create":
            try:
                image = cmd[1]
                if(image not in images.keys()):
                    print("image not found")
                    continue
            except:
                print("syntax: create image_name")
                continue
            name = input("container name: ")
            root = False
            if("y" == input("root?(y/n)(defalut 'n')")):
                root = True
            password = input("password: ")
            description = input("description: ")
            createContainer(image,name,root,password,description)
            print("container created")
            display(name)
            pass
        case "info":
            try:
                name = cmd[1]
            except:
                print("syntax: info container_name")
                continue
            if(check(name)):
                print("container not found")
            else:
                display(name)
            pass
        case "start":
            try:
                name = cmd[1]
            except:
                print("syntax: start container_name")
                continue
            if(check(name)):
                print("container not found")
                continue
            else:
                loadContainer(name)
            pass
        case "stop":
            try:
                name = cmd[1]
            except:
                print("syntax: stop container_name")
                continue
            if(check(name)):
                print("container not found")
                continue
            else:
                delete(name)
            pass
        case "rm":
            try:
                name = cmd[1]
            except:
                print("syntax: rm container_name")
                continue
            if(name == "a" or name == "all"):
                conts = containerinfo.copy().keys()
                for c in conts:
                    delete(c,True)
                continue
            if(check(name)):
                print("container not found")
                continue
            else:
                delete(name,True)
            pass
        case "list":
            try:
                if(cmd[1] == "images"):
                    listContainer(False)
                else:
                    print('invalid arguments')
                    continue
            except:
                listContainer()
            pass
        case "help":
            print("""
create image_name
    to create a new container

list [images]
    to list containers or images

info container_name
    to get container information

start container_name
    to start container

stop conteiner_name
    to stop container

rm container_name
    to delete container

rm all 
    to delete all containers

help
    to display this

exit
    to exit the program
            """)
        case "clear":
            clear()
            pass
        case "exit":
            exit()
        case _:
            print("invalid command")
            pass
