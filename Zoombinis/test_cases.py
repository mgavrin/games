import mirror_machine_analyzer
from mirror_machine_analyzer import *

###Note: all test cases in this file are actual instances
###I found while playing Mirror Machine (Mac OS version).

##################### Test case 1: Solvable#####################
zoombini1=zFilter("pony","specs","red","skates")
zoombini2=zFilter("fluff","shades","yellow","prop")
goal1=zFilter("pony","specs","pink","spring")
goal2=zFilter("fluff","sleepy","green","skates")
filters=[]
filters.append(zFilter("blank","rotator","blank","wheels"))
filters.append(zFilter("blank","blank","yellow","blank"))
filters.append(zFilter("blank","blank","blank","wheels"))
filters.append(zFilter("tuft","blank","blank","blank"))
filters.append(zFilter("blank","shades","yellow","blank"))
filters.append(zFilter("tuft","shades","blank","blank"))
print "Running test case 1"
checkForSolutions(zoombini1,zoombini2,goal1,goal2,filters)
print "\n\n"

##################### Test case 2: Solvable#####################
zoombini1=zFilter("cap","shades","green","wheels")
zoombini2=zFilter("tuft","sleepy","red","prop")
goal1=zFilter("fluff","specs","yellow","prop")
goal2=zFilter("tuft","shades","yellow","prop")
filters=[]
filters.append(zFilter("pony","blank","blank","blank"))
filters.append(zFilter("blank","rotator","blank","spring"))
filters.append(zFilter("blank","blank","blue","blank"))
filters.append(zFilter("blank","blank","pink","blank"))
filters.append(zFilter("blank","blank","rotator","blank"))
filters.append(zFilter("pony","blank","blank","rotator"))
print "Running test case 2"
checkForSolutions(zoombini1,zoombini2,goal1,goal2,filters)
print "\n\n"



##################### Test case 3: Unsolvable ###################
zoombini1=zFilter("cap","shades","green","wheels")
zoombini2=zFilter("tuft","sleepy","red","prop")
goal1=zFilter("fluff","specs","yellow","prop")
goal2=zFilter("tuft","shades","yellow","prop")
filters=[]
filters.append(zFilter("pony","blank","blank","blank"))
filters.append(zFilter("blank","blank","blank","spring"))
filters.append(zFilter("blank","blank","blue","blank"))
filters.append(zFilter("blank","blank","pink","blank"))
filters.append(zFilter("blank","blank","rotator","blank"))
filters.append(zFilter("pony","blank","blank","rotator"))
print "Running test case 3"
checkForSolutions(zoombini1,zoombini2,goal1,goal2,filters)
print "\n\n"


##################### Test case 4: Unsolvable ###################
zoombini1=zFilter("cap","shades","yellow","shoes")
zoombini2=zFilter("pony","shades","red","prop")
goal1=zFilter("cap","cyclops","green","wheels")
goal2=zFilter("pony","shades","yellow","spring")
filters=[]
filters.append(zFilter("fluff","blank","blank","blank"))
filters.append(zFilter("blank","blank","blank","spring"))
filters.append(zFilter("blank","blank","blue","blank"))
filters.append(zFilter("blank","specs","blue","blank"))
filters.append(zFilter("blank","specs","blank","skates"))
filters.append(zFilter("blank","cyclops","blank","rotator"))
print "Running test case 4"
checkForSolutions(zoombini1,zoombini2,goal1,goal2,filters)
print "\n\n"


##################### Test case 5: Unsolvable ###################
zoombini1=zFilter("cap","dot","yellow","prop")
zoombini2=zFilter("tuft","cyclops","yellow","skates")
goal1=zFilter("tuft","sleepy","yellow","wheels")
goal2=zFilter("cap","dot","pink","wheels")
filters=[]
filters.append(zFilter("blank","rotator","blank","blank"))
filters.append(zFilter("flat","blank","blue","blank"))
filters.append(zFilter("tuft","blank","blank","blank"))
filters.append(zFilter("rotator","blank","green","blank"))
filters.append(zFilter("fluff","blank","green","blank"))
filters.append(zFilter("blank","blank","blank","wheels"))
print "Running test case 5"
checkForSolutions(zoombini1,zoombini2,goal1,goal2,filters)
