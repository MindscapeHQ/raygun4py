import sys
from provider import raygunprovider

cl = raygunprovider.RaygunSender("onPbQXtZKqJX38IuN4AQKA==")

print cl.send("fake exception")
