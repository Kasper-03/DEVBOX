from functions import joke_generator, currency_conventer, info, country_get_info, SpaceX

while True:
    print("=== MENU GŁÓWNE ===")
    print("1: Generator żartów") 
    print("2: Konwenter walut")
    print("3: Informacje o położeniu")
    print("4: Informacje o kraju")
    print("5: Informacje o misji SpaceX")
    print("===================")
    decision = input("\nKtórego programu chcesz użyć? wpisz odpowiednia cyfre na klawaiturze, by wyjsc wpisz (q): ").strip()
    
    if decision == "1":
        print("Witaj w prostym generatorze żartów!")
        joke_generator()               

    elif decision =="2":
        print("Witaj w konwenterze walut!")
        currency_conventer()
    elif decision == "3":
        print("Witaj w informacjach o położeniu!")
        info()
    elif decision == "4":
        print("Witaj w informacjach o danym kraju!")
        country_get_info()
    elif decision == "5":
        print("Witaj w informacji o misji SpaceX!")
        SpaceX()
        
    elif decision == "q":
        print("Papa!")
        break
    else:
        print(f"Nie ma programu o numerze: {decision}")

