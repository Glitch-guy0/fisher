port = {
    "ports":[43,34,33]
}

print(port.get("ports"))
up = port.get("ports")
up.pop(0)
print(up)
print(port.get("ports"))