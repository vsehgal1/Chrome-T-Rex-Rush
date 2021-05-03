import main

max_chrome = (0,'')

chromes = ['1010', '1000']

def run_game(chrome_val):
    get_high = (main.main(chrome_val))
    print('Current Max: '+ str(get_high))
    print('Current Ruleset: '+ str(chrome_val))
    return get_high

# gonna be return type
# print(max_chrome)
    # try:
    #     print(main.main())
    # except:
    #     print('something')