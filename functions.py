import requests, time

def server_response(url):
    try:
        response = requests.get(url, timeout=5)
        if response.ok:
            return response.json()
        else:
            print(f"Problem z serwerem. Kod:{response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
            print(f"Błąd połączenia: {e}")
            return None               

def joke_generator():
    while True:
            joke_decision = input("(y) by usłyszeć żart, (q) powrót do menu: ").strip().lower()
            if joke_decision =="y":
                data = server_response("https://official-joke-api.appspot.com/random_joke")
                if data:
                    print("-----------------------------------------------------")
                    print(f"{data['setup']}")
                    time.sleep(2)
                    print(f"{data['punchline']}")
            elif joke_decision =="q":
                break
            else:
                print("To nie może byc takie trudne, wpisz (y) albo (q)") 

def currency_conventer():
    data = server_response("https://open.er-api.com/v6/latest")
    if not data:
         print("Nie udało sie pobrać danych o walutach.")
         return
    while True:
        currency_1 = input("Podaj walute do konwersji. (np. PLN, USD): ").strip().upper()
        if currency_1 not in data["rates"]:
            print(f"Nie znaleziono waluty : {currency_1}")
            continue
        try:
            amount = float(input("Podaj ilość waluty: "))
        except ValueError:
            print("Niepoprawna liczba! spróbuj ponownie.")
            continue    
        currency_2 = input("Podaj walute docelowa (np. PLN, USD): ").strip().upper()

        if currency_2 not in data["rates"]:
            print(f"Nie znaleziono waluty : {currency_2}")
            continue

        currency_1_rate = float(data["rates"][f"{currency_1}"])
        currency_2_rate = float(data["rates"][f"{currency_2}"])

        converted = float((amount / currency_1_rate) * currency_2_rate)
        print(f"\n{amount:.2f} {currency_1} = {converted:.2f} {currency_2}")
        
        again = input("\nChcesz zrobić kolejną konwersję? (y) tak / (q) powrót do menu: ").strip().lower()
        if again == "q":
            break
        
def info():
    ip = requests.get("https://api.ipify.org", timeout=5).text
    city = server_response(f"http://ip-api.com/json/{ip}")
    lat = float(city['lat'])
    lon = float(city['lon'])
    info = server_response(f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m") 

    print("===Informacje o twoim położeniu===")
    print(f"IP: {ip}")
    print(f"Kraj: {city['country']}")
    print(f"Miasto: {city['city']}")
    print(f"Strefa czasowa: {city['timezone']}")
    print(f"Aktualna temperatura: {info['current']['temperature_2m']} Stopni Celsjusza")
    print("\n")
def country_get_info():
    country = input("Podaj nazwę kraj o którym chcesz uzyskac informacje: (np. Poland, Czechia): ").strip().lower()
    country_info = server_response(f"https://restcountries.com/v3.1/name/{country}?fullText=True")
    
    if not country_info or not isinstance(country_info, list):
        print("Nie znaleziono kraju.")
        return
    country_data = country_info[0]
    
    print("=== INFORMACJE O KRAJU ===")
    print(f"Nazwa: {country_data.get('name', {}).get('common', 'Brak')}")
    
    names = country_data.get('name', {}).get('nativeName', {})
    if names:
        first_lang_key = list(names.keys())[0]
        native = names.get(first_lang_key, {})
        official = native.get('official', 'Brak')
        print(f"Oficjalna nazwa: {official}")

    curr = country_data.get('currencies', {})
    if curr:
        curr_name = list(curr.keys())[0]
        curr_final = curr.get(curr_name, {})
        symbol, nazwa = curr_final.get('symbol', 'Brak'), curr_final.get('name', 'Brak')
        print(f"Symbol waluty: {symbol}")
        print(f"Nazwa waluty: {nazwa}")
    
    capitals = country_data.get('capital', [])
    capitals_formatted = ", ".join(capitals) if capitals else "Brak"
    print(f"Stolica: {capitals_formatted}")
    
    print(f"Region : {country_data.get('region', 'Brak')}")
    print(f"Podregion: {country_data.get('subregion', 'Brak')}")

    languages = country_data.get('languages', {})
    lang_formatted = ", ".join(languages.values()) if languages else "Brak"
    print(f"Języki używane: {lang_formatted}")

    borders = country_data.get('borders', [])
    borders_formatted = ", ".join(borders) if borders else "Brak"
    print(f"Sąsiedzi: {borders_formatted}")


    area = country_data.get('area')
    area_txt = f"{int(area):,} km²".replace(",", " ") if isinstance(area, (int, float)) else "Brak"
    print(f"Powierzchnia: {area_txt}")

    pop = country_data.get('population')
    pop_txt = f"{int(pop):,}".replace(",", " ") if isinstance(pop, (int, float)) else "Brak"
    print(f"Populacja: {pop_txt}")
    
def SpaceX():
    start = server_response("https://api.spacexdata.com/v5/launches/next")
    if not start or not isinstance(start, dict):
        print("Nie udało pobrać się informacji :(")
        return
    
    print("=== INFORMACJE O MISJI ===")
    print(f"Nazwa: {start.get('name','Brak')}")
    print(f"Data: {start.get('date_utc', 'Brak')}")
    
    rocket = start.get('rocket')
    launchpad = start.get('launchpad')
    
    actual_links = "brak"
    links = start.get('links', {}) or {}
    if links:
        urls = [v for v in links.values() if isinstance(v, str) and v.startswith("http")]
        actual_links = ", ".join(urls) if urls else "Brak"
    print(f"Przydatne linki: {actual_links}")
    
    rocket_info = server_response(f"https://api.spacexdata.com/v4/rockets/{rocket}") if rocket else None
    launchpad_info = server_response(f"https://api.spacexdata.com/v4/launchpads/{launchpad}") if launchpad else None

    if rocket_info and isinstance(rocket_info, dict):
        print("=== INFORMACJE O RAKIECIE ===")
        print(f"Nazwa: {rocket_info.get('name', 'Brak')}")
        print(f"Pierwszy lot rakiety: {rocket_info.get('first_flight', 'Brak')}")
        print(f"Wysokość rakiety: {rocket_info.get('height', {}).get('meters', 'Brak')} m, " 
              f" Średnica rakiety: {rocket_info.get('diameter', {}).get('meters', 'Brak')}m "
                )
    if launchpad_info and isinstance(launchpad_info, dict):
        print("=== INFORMACJE O WYRZUTNI ===")
        print(f"Nazwa: {launchpad_info.get('name', 'Brak')}")
        print(f"Lokalizacja: {launchpad_info.get('locality', 'Brak')}")
        print(f"Region: {launchpad_info.get('region', 'Brak')}")  