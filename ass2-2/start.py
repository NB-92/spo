
import sys
from machine import Machine

m = Machine()

fileName = sys.argv[1]
m.readObjCode(fileName)
