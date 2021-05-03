import main

max_chrome = (0,'')

chromes = ['1010', '1000']

for i in chromes:
    get_high = (main.main(i))
    if get_high > max_chrome[0]:
        max_chrome = (get_high, i)
    print('Current Max: '+ str(max_chrome[0]))
    print('Current Ruleset: '+ max_chrome[1])

# gonna be return type
print(max_chrome)
    # try:
    #     print(main.main())
    # except:
    #     print('something')