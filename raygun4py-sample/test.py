import sys
from provider import raygunprovider

cl = raygunprovider.RaygunSender("etc")

cl.send("fake exception")
