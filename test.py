images = {
    "ubuntu":"kasmweb/core-ubuntu-bionic:1.13.0-rolling",
    "desktop":"kasmweb/ubuntu-bionic-desktop:1.10.0-rolling"
}


name = input("containers naem: ")
print(name)
name = images.get(name)
print(name)