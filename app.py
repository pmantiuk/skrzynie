import datetime, getpass, os, pickle, sys
from pandas import DataFrame as pd

kiedy = datetime.datetime.today().strftime ('%Y-%m-%d')
kto = getpass.getuser() 
admin = ['pmantiuk', 'Paweł', 'mbruj']

def menu():
    os.system("cls")
    print ("""Cześć""", kto,"""! \nWitam Cię w kreatorze numerów skrzyń.\nWybierz odpowiedni numer z klawiatury po czym nacisnij klawisz 'Enter'\n
    MENU:\n
    1 : pobierz numery\n
    2 : edytuj zawartość skrzyni\n
    3 : wyświetl zestawienie skrzyń\n
    4 : eksportuj zestawienie do excela\n
    9 : opcje administratora\n
    0 : zakończ program\n\n""")
    try:
        menu_choice = int(input("\nTwój wybór: "))
    except:
        print('Dokonałeś błędnego wyboru.') 
        press_enter()
        menu()
    else:
        if menu_choice == 1:
            dodaj_skrzynie()
            menu()  
            
        elif menu_choice == 2:
            edytuj_zawartosc()
            menu()
            
        elif menu_choice == 3:
            wyswietl_zestawienia()
            menu() 
        
        elif menu_choice == 4:
            excel_eksport()
            menu() 
            
        elif menu_choice == 9:  
            if kto in admin:
                admin_menu()
            else:
                os.system('cls')
                print('Nie masz uprawnień. Nie kombinuj...')
                press_enter()
                menu()
        elif menu_choice == 69:
            print('\nO czym Ty myślisz Świntuchu?! :P\nWybierz prawidłową cyfrę.')
            press_enter()
            menu()
            
        elif menu_choice == 0:
            sys.exit()
        else: 
            print('Wybierz prawidłową cyfrę.')
            press_enter()
            menu()

def laduj():  
    global skrzynie
    skrzynie = pickle.load(open('numery.txt', 'rb'))

def zapis():
    pickle.dump(skrzynie, open('numery.txt', 'wb'))
    
def press_enter():
    input('\nNacisnij klawisz \'Enter\', aby powrócić do menu')
    
def dodaj_skrzynie():
    os.system('cls')
    print('POBIERANIE NUMERÓW SKRZYŃ\n')
    wyswietl_liste() 
    laduj()
    try: 
        chest_numbers = list(skrzynie[display[wybór]].keys())
    except:
        print('Nie ma kontraktu, który odpowiada Twojemu numerowi.')
        press_enter()
    else:
        try:
            quantity = int(input("Ile numerów skrzyń potrzebujesz?\n\n\t"))
        except:
            print('\nWprowadź poprawną wartość liczbową.')
        else:
            if quantity == 0:
                print('\nWybrałeś 0 skrzyń, chyba nie o to Ci chodziło. Spróbuj ponownie.')
                press_enter()
                menu()
            else:
                laduj()
                chest_numbers = list(skrzynie[display[wybór]].keys())
                if not skrzynie[display[wybór]].values():       
                    first_available_number = 1
                    last_chest_number = quantity
                else:
                    first_available_number = max(chest_numbers) + 1
                    last_chest_number = first_available_number + quantity - 1     
            for i in range(first_available_number,last_chest_number + 1):
                skrzynie[display[wybór]][i] = {'co': '?', 'kto' : kto, 'kiedy': kiedy}
            zapis()
            print(f"\nTwoje numery to od {first_available_number} do {last_chest_number}")
            co = input('Wpisz co będzie spakowane w Twoich skrzyniach (nie więcej niż 40 znaków): ')
            while len(co) > 40:
                print('\nWprowadziłeś więcej niż 40 znaków, spróbuj ponownie.')
                co = input('Wpisz co będzie spakowane w Twoich skrzyniach (nie więcej niż 40 znaków): ')
            laduj()
            for i in range(first_available_number,last_chest_number + 1):
                skrzynie[display[wybór]][i] = {'co': co, 'kto' : kto, 'kiedy': kiedy}
            zapis()
            print('\nDodano następujące skrzynie:\n')
            for k in range(first_available_number, last_chest_number + 1):
                print(f'SK-{k : <3} : {skrzynie[display[wybór]][k]["co"] : <40} {skrzynie[display[wybór]][k]["kto"] : ^20} {skrzynie[display[wybór]][k]["kiedy"] : >12}')
        press_enter()

def wyswietl_liste():
    laduj()
    print('Wybierz cyfrę odpowiadającą kontraktowi po czym naciśnij \'Enter\'.\n')
    global display, wybór
    display = dict(enumerate(skrzynie.keys(), start=1))
    for x, k in enumerate(skrzynie.keys(), start=1):
                print(x, ':', k)
    try:
        wybór = int(input('\nTwój wybór: '))
        skrzynie[display[wybór]]
    except:
        print('Dokonałes błędnego wyboru.') 
        press_enter()
        menu()
    else:
        print('')
      
def edytuj_zawartosc():
    os.system('cls')
    print('EDYCJA ZAWARTOŚCI SKRZYŃ\n')
    wyswietl_liste()
    # try:
    #     skrzynie[display[wybór]]
    if skrzynie[display[wybór]].keys():
        for k in skrzynie[display[wybór]].keys():
            print(f'SK-{k : <3} : {skrzynie[display[wybór]][k]["co"] : <40} {skrzynie[display[wybór]][k]["kto"] : ^20} {skrzynie[display[wybór]][k]["kiedy"] : >12}')
        k = input('\nPodaj numer skrzyni, lub skrzyń, dla których chcesz edytować zawartość: np.: 4, 15-17: ')
        x = k.rsplit('-')
        try:   
            x = [int(i) for i in x]
        except:
            print('\nPodaj numer skrzyni w prawidłowym formacie. Przykładowe prawidłowe formaty:\n4 : w celu edycji skrzyni numer SK-4\n15-17 : w celu edycji skrzyń SK-15, SK-16 i SK-17')
            press_enter()
        else:      
            mn = x[0]
            try:
                mx = x[1]
            except:
                mx = mn
            if mn == mx:
                try:
                    skrzynie[display[wybór]][mn]
                except:
                    print('\nSkrzynie nie zostaną edytowane. Prawdopodobnie podałeś numer skrzyni, której nie ma w zestawieniu. Spróbuj ponownie.')
                    press_enter()
                else:                           
                    pakujący = skrzynie[display[wybór]][mn]['kto']
                    if pakujący == kto or kto in admin:
                        co = input('Wpisz co pakujesz: ')
                        while len(co) > 40:
                            print('\nWprowadziłeś więcej niż 40 znaków, spróbuj ponownie.')
                            co = input('Wpisz co będzie spakowane w Twoich skrzyniach (nie więcej niż 40 znaków): ')
                        if input('\nCzy na pewno chcesz edytować zawartość skrzyni? (y/n): ').lower() == 'y': 
                            if mn in skrzynie[display[wybór]]:
                                skrzynie[display[wybór]][mn]['co'] = co
                                zapis()
                                print(f'\nZedytowano następujący wpis:\nSK-{mn} : {skrzynie[display[wybór]][mn]["co"]} \t{skrzynie[display[wybór]][mn]["kto"]} \t{skrzynie[display[wybór]][mn]["kiedy"]}')
                                press_enter()
                            else:
                                print('\nNie ma takiego numeru skrzyni w zestawieniu.')
                                press_enter()
                        else:
                            print('\nZrezygnowano z edycji wpisu.')    
                            press_enter()
                            menu()
            elif mn > mx:
                print('\nPodaj numery skrzyń w kolejności od najmniejszego do największego.')
                press_enter()
            else:
                try:
                    skrzynie[display[wybór]][mn]
                    skrzynie[display[wybór]][mx]
                except:
                    print('\nSkrzynie nie zostaną edytowane. Prawdopodobnie podałeś numery skrzyń, których nie ma w zestawieniu. Spróbuj ponownie.') 
                    press_enter()
                else:
                    weryfikacja = []
                    for i in range(mn, mx + 1):
                        pakujący = skrzynie[display[wybór]][i]['kto']   
                        weryfikacja.append(bool(pakujący == kto or kto in admin))
                    if weryfikacja:
                        co = input('Wpisz co pakujesz: ')
                        while len(co) > 40:
                            print('\nWprowadziłeś więcej niż 40 znaków, spróbuj ponownie.')
                            co = input('Wpisz co będzie spakowane w Twoich skrzyniach (nie więcej niż 40 znaków): ')
                        if input('\nCzy na pewno chcesz edytować zawartość skrzyni? (y/n): ').lower() == 'y': 
                            print('\nDokonano następującej edycji:')
                            for i in range(mn, mx + 1):
                                if i in skrzynie[display[wybór]]:
                                    skrzynie[display[wybór]][i]['co'] = co
                                    zapis()
                                    print(f'SK-{i} : {skrzynie[display[wybór]][i]["co"]} \t{skrzynie[display[wybór]][i]["kto"]} \t{skrzynie[display[wybór]][i]["kiedy"]}')
                            press_enter()
                        else:
                            print('\nZrezygnowano z edycji wpisów.')    
                            press_enter()
                            menu()
                    else:
                        print('\nChcesz dokonać edycji wpisów, których nie pakowałeś. Sprawdź jeszcze raz poprawność zakresu edycji.')
                        press_enter()
    else:
        print('Ten kontrakt nie ma jeszcze żadnej spakowanej skrzyni.')
        press_enter()
        
def wyswietl_zestawienia():
    os.system('cls')
    print('ZESTAWIENIE SKRZYŃ\n')
    wyswietl_liste()
    try:
        skrzynie[display[wybór]].keys()
    except:
        print('Nie ma kontraktu, który odpowiada Twojemu numerowi.')
        press_enter()
    else:
        if skrzynie[display[wybór]].keys():
            for k in skrzynie[display[wybór]].keys():
                print(f'SK-{k : <3} : {skrzynie[display[wybór]][k]["co"] : <40} {skrzynie[display[wybór]][k]["kto"] : ^20} {skrzynie[display[wybór]][k]["kiedy"] : >12}')
            press_enter()
        else:
            print('Ten kontrakt nie ma jeszcze żadnej spakowanej skrzyni.')
            press_enter()

def excel_eksport():
    os.system('cls')
    wyswietl_liste()
    df = pd.from_dict(skrzynie[display[wybór]].values())
    df.index += 1
    patka = fr'C:\\users\{kto}\Desktop\zestawienie skrzyń - {display[wybór]}.xlsx'
    df.to_excel(patka, index = True, sheet_name=display[wybór])
    print(f'Pomyślnie wyeksporotowano zestawienie {display[wybór]} do pliku excel.\nZnajduje się ono na Twoim pulpicie.')
    press_enter()
    menu()
    
'''dodaje do bazy danych nowy kontrakt, obsługiwane tylko przez administratora'''          
def dodaj_kontrakt():
    os.system('cls')
    print('DODAWANIE NOWEGO KONTRAKTU DO BAZY\n')
    kontrakt = input('Podaj nazwę nowego kontraktu: ')
    if kontrakt != '':
        if input('\nCzy na pewno chcesz dodać {} do bazy? (y/n): '.format(kontrakt)).lower() == 'y':        
            skrzynie[kontrakt] = {}
            zapis()
            print('Dodano', kontrakt, 'do bazy.')       
        else:
            press_enter()
            admin_menu()
    else:
        print('\nNie podałeś nazwy kontraktu, spróbuj ponownie.')
        press_enter()
        admin_menu()
        
def powrot_admin():
    os.system('cls')
    admin_menu()

'''usuwa z bazy danych numery, obsługiwane tylko przez administratora'''
def usun_kontrakt():
    os.system('cls')
    print('USUWANIE KONTRAKTU Z BAZY\n')
    wyswietl_liste()
    if input('Czy na pewno chcesz usunąć kontrakt z bazy? (y/n): ').lower() == 'y':      
        try:
            del skrzynie[display[wybór]]
        except:
            print(f'\nPodaj prawidłowy numer kontraktu. Pod numerem: {wybór} nie kryje się żaden kontrakt.')  
            press_enter()
            usun_kontrakt()
        else:
            print('Usunięto kontrakt:', display[wybór])
            press_enter()
            zapis()
    else:
        press_enter()
        admin_menu()
        
def usun_skrzynie():
    os.system('cls')
    wyswietl_liste()
    for k in skrzynie[display[wybór]].keys():
        print(f'SK-{k : <3} : {skrzynie[display[wybór]][k]["co"] : <40} {skrzynie[display[wybór]][k]["kto"] : ^20} {skrzynie[display[wybór]][k]["kiedy"] : >12}')
    if not bool(skrzynie[display[wybór]].keys()):
        print('Ten kontrakt nie ma jeszcze żadnej spakowanej skrzyni.')
    else:
        k = input('\nPodaj numer skrzyni, lub skrzyń, które chcesz usunąć, np.: 4, 15-17: ')
        x = k.rsplit('-')
        try:
            x = [int(i) for i in x]
        except:
            print('\nPodaj numer skrzyni w prawidłowym formacie. Przykładowe prawidłowe formaty:\n4 : w celu usunięcia skrzyni numer SK-4\n15-17 : w celu usunięcia skrzyń SK-15, SK-16 i SK-17')
        else:      
            mn = x[0]
            try:
                mx = x[1]
            except:
                mx = mn
            if mn == mx:
                try:
                   skrzynie[display[wybór]][mn]
                except:
                   print('\nSkrzynie nie zostały usunięte. Prawdopodobnie podałeś numer skrzyni, której nie ma w zestawieniu. Spróbuj ponownie.')   
                else:
                    if input('\nCzy na pewno chcesz usunąć skrzynię z bazy? (y/n): ').lower() == 'y': 
                        del skrzynie[display[wybór]][mn] 
                        zapis()
                        print(f'\nZ kontraktu {display[wybór]} usunięto skrzynię nr: SK-{k}.')    
                    else:
                        print('\nZrezygnowano z usunięcia wpisów.')    
                        press_enter()
                        admin_menu()
            elif mn > mx:
                print('\nPodaj numery skrzyń w kolejności od najmniejszego do największego.')
            else:
                try:
                    skrzynie[display[wybór]][mn]
                    skrzynie[display[wybór]][mx]
                except:
                    print('\nSkrzynie nie zostały usunięte. Prawdopodobnie podałeś numery skrzyń, których nie ma w zestawieniu. Spróbuj ponownie.')     
                else:
                    if input('\nCzy na pewno chcesz usunąć skrzynie z bazy? (y/n): ').lower() == 'y': 
                        for i in range(mn, mx + 1):
                            try:
                                del skrzynie[display[wybór]][i]
                            except:
                                next
                            zapis()
                        print(f'\nZ kontraktu {display[wybór]} usunięto skrzynie od SK-{mn} do SK-{mx}.')
                    else:
                        press_enter()
                        admin_menu()
    press_enter()
    
def admin_menu():
    os.system('cls')
    print ("""Tu możesz zarządzać bazą kontraktów i skrzyń.\nWybierz odpowiedni numer z klawiatury po czym nacisnij klawisz 'Enter'\n 
    1 : dodaj kontrakt do bazy\n
    2 : usuń kontrakt z bazy\n
    3 : usuń skrzynie z zestawienia\n
    4 : edytuj zawartość skrzyni\n
    5 : wróć do menu głównego\n\n""")
    try:
        menu_choice = int(input("\nTwój wybór: "))
    except:
        print('Dokonałeś błędnego wyboru.') 
        press_enter()
        admin_menu()
    else: 
        if menu_choice == 1:
            dodaj_kontrakt()
            powrot_admin()          
        elif menu_choice == 2:
            usun_kontrakt()
            powrot_admin()  
            
        elif menu_choice == 3:
            usun_skrzynie()
            powrot_admin()  
        elif menu_choice == 4:
            edytuj_zawartosc()
            powrot_admin()
        elif menu_choice == 5:        
            menu()
            
        else: 
            print('\nWybierz prawidłową cyfrę.')
            press_enter()
            powrot_admin()
        
laduj()            
menu()