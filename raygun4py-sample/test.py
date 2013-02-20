import sys
from provider import raygunprovider

cl = raygunprovider.RaygunSender("onPbQXtZKqJX38IuN4AQKA==")
cl.set_version("1.2")
print cl.send(Exception("python borked"))
