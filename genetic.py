import main

def run_game(chrome_val):
    get_high = (main.main(chrome_val))
    print('Current Max: '+ str(get_high))
    print('Current Ruleset: '+ str(chrome_val))
    return get_high

run_game('1000')

# gonna be return type
# print(max_chrome)
    # try:
    #     print(main.main())
    # except:
    #     print('something')