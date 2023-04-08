# fisher
This is a python code for kasm desktop setup just for temp desktop setup **without any volumes**

>[!tip]
>use vscode with docker extension to download file from the container

>[!problems]
> 1. The Program is not optimized (I just did it on the go)
> 2. It has a lot of repeated code blocks
> 3. you have to add the images manually

# Images to download
## ubuntu
```bash
sudo docker pull kasmweb/core-ubuntu-focal:1.11.0-rolling
```
## parrot
```bash
sudo docker pull kasmweb/parrotos-5-desktop:develop-rolling
```
## fedora
```bash
sudo docker pull kasmweb/fedora-37-desktop:develop
```
### kali
```bash
sudo docker pull kasmweb/core-kali-rolling:1.12.0-rolling
```

>[!warning]
> You will see all these images by default; even if you didn't download
