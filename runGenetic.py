import geneticAlgo

# 1st stringLength (do not change)
# 2nd population size (can change if needed, probably not likely)
# 3rd number of generations (can change, leave low to test performance first. Likely will need to be higher for final run
# 4th probability of mutation (can change but likely not needed)
# 5th probability of crossover (can change slightly, might be worth experimenting with)
ga = geneticAlgo.sga(4, 1, 0, .001, .4)

ga.runGA()

