#!/usr/bin/python
import Configurator
configurator = Configurator.Configurator('../webarticleparser.ini')
options = configurator.getDefauls()

print 'Default values:'
for (key,value) in options.items():
    print str(key) + " = " + str(value)

options = configurator.getConfig()

print 'Read from config file:'
for (key,value) in options.items():
    print str(key) + " = " + str(value)


configurator_def = Configurator.Configurator()
options = configurator_def.getConfig()

print 'Only defaults:'
for (key,value) in options.items():
    print str(key) + " = " + str(value)
