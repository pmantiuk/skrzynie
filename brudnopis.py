import os, pickle, getpass
import datetime
from pandas import DataFrame as pd

def laduj():  
    global skrzynie
    skrzynie = pickle.load(open('kontrakty.txt', 'rb'))

def zapis():
    pickle.dump(skrzynie, open('kontrakty.txt', 'wb'))
    
def press_enter():
    input('\nNacisnij klawisz \'Enter\', aby powrócić do menu')
    
def wyswietl_liste():
    laduj()
    print('Wybierz cyfrę odpowiadającą kontraktowi po czym naciśnij \'Enter\'.\n')
    global display, wybór
    display = dict(enumerate(skrzynie.keys()))
    for x, k in enumerate(skrzynie.keys()):
                print(x, ':', k)
    try:
        wybór = int(input('\nTwój wybór: '))
    except:
        print('Dokonałes błędnego wyboru.') 
        press_enter()
        menu()
    else:
        print('')
    
def powrot_admin():
    os.system('cls')
    admin_menu()

'''dodaje do bazy danych nowy kontrakt, obsługiwane tylko przez administratora pmnatiuk'''        
def dodaj_kontrakt():
    os.system('cls')
    print('DODAWANIE NOWEGO KONTRAKTU DO BAZY\n')
    kontrakt = input('Podaj nazwę nowego kontraktu: ')
    if input('\nCzy na pewno chcesz dodać {} do bazy? (y/n): '.format(kontrakt)).lower() == 'y':        
        skrzynie[kontrakt] = {}
        zapis()
        print('Dodano', kontrakt, 'do bazy.')       
    else:
        press_enter()
        admin_menu()

'''usuwa z bazy danych kontrakty, obsługiwane tylko przez administratora'''
def usun_kontrakt():
    os.system('cls')
    print('USUWANIE KONTRAKTU Z BAZY\n')
    wyswietl_liste()
    if input('Czy na pewno chcesz usunąć kontrakty z bazy? (y/n): ').lower() == 'y':      
        try:
            del skrzynie[display[wybór]]
        except:
            print('Podaj prawidłowy numer kontraktu.')  
            press_enter()
            usun_kontrakt()
        else:
            print('Usunięto kontrakt:', display[wybór])
            press_enter()
            zapis()
    else:
        press_enter()
        admin_menu()
        
def dodaj_skrzynie():
    os.system('cls')
    print('POBIERANIE NUMERÓW SKRZYŃ\n')
    wyswietl_liste() 
    laduj()
    try: 
        chest_numbers = list(skrzynie[display[wybór]].keys())
    except:
        print('Nie ma kontraktu, który odpowiada Twojemu numerowi...')
        press_enter()
    else:
        if not skrzynie[display[wybór]].values():       
            first_available_number = 1
            print('Nie ma jeszcze skrzyń na tym kontrakcie.')
        else:
            first_available_number = max(chest_numbers) + 1
        quantity = int(input("Ile numerów skrzyń potrzebujesz?\n\n\t"))
        if quantity == 0:
            press_enter()
            menu()
        else:
            last_chest_number = first_available_number + quantity - 1    
        print(f"\nTwoje numery to od {first_available_number} do {last_chest_number}")
        co = input('Wpisz co będzie spakowane w Twoich skrzyniach: ')
        for i in range(first_available_number,last_chest_number+1):
            skrzynie[display[wybór]][i] = {'co': co, "kto" : kto, 'kiedy': kiedy}
        zapis()
        print('\nDodano następujące skrzynie:\n')
        for k in range(first_available_number, last_chest_number+1):
                print('SK-',k,' : ', skrzynie[display[wybór]][k]['co'], '\t', skrzynie[display[wybór]][k]['kto'],'\t', skrzynie[display[wybór]][k]['kiedy'], sep='')
        press_enter()
    
def usun_skrzynie():
    os.system('cls')
    wyswietl_liste()
    k = int(input('Podaj numer skrzyni, którą chcesz usunąć: '))
    del skrzynie[display[wybór]][k]
    print(f'Usunięto skrzynię nr: {k}, kontraktu: {display[wybór]}.')
    zapis()
    press_enter()
        
def wyswietl_zestawienia():
    os.system('cls')
    print('ZESTAWIENIE SKRZYŃ\n')
    wyswietl_liste()
    try:
        skrzynie[display[wybór]].keys()
    except:
        print('Nie ma kontraktu, który odpowiada Twojemu numerowi...')
        press_enter()
    else:
        if skrzynie[display[wybór]].keys():
            for k in skrzynie[display[wybór]].keys():
                print('SK-',k,' : ', skrzynie[display[wybór]][k]['co'], '\t', skrzynie[display[wybór]][k]['kto'],'\t', skrzynie[display[wybór]][k]['kiedy'], sep='')
            press_enter()
        else:
            print('Ten kontrakt nie ma jeszcze żadnej spakowanej skrzyni.')
            press_enter()

def edytuj_zawartosc():
    os.system('cls')
    print('EDYCJA ZAWARTOŚCI SKRZYŃ\n')
    wyswietl_liste()
    try:
        skrzynie[display[wybór]]
    except:
        print('Nie ma kontraktu, który odpowiada Twojemu numerowi...')
        press_enter()
    else:
        try:
            k = int(input('Podaj numer skrzyni, dla której chcesz edytować zawartosć: '))
        except:
            print('Dokonałes błędnego wyboru.') 
            press_enter()
            menu()
        else:
            try:
                skrzynie[display[wybór]][k]    
            except:
                print('Nie ma takego numeru skrzyni dla tego kontraktu...')
                press_enter()
            else:
                pakujący = skrzynie[display[wybór]][k]['kto']
                if pakujący == kto:
                    co = input('Wpisz co pakujesz: ')
                    if k in skrzynie[display[wybór]]:
                        skrzynie[display[wybór]][k]['co'] = co
                        zapis()
                    else:
                        print('Nie ma takiego numeru skrzyni w zestawieniu...')
                else:
                    print(f'Nie możesz edytować zawartosci skrzyni, której nie pakowałes...\nTę skrzynię pakował: {pakujący}')
                    press_enter()
                    
def excel_eksport():
    os.system('cls')
    wyswietl_liste()
    df = pd.from_dict(skrzynie[display[wybór]].values())
    df.index += 1
    patka = fr'C:\\users\{kto}\Desktop\zestawienie skrzyń - {display[wybór]}.xlsx'
    df.to_excel(patka, index = True, sheet_name=display[wybór])
    print(f'Pomyslnie wyeksporotowano zestawienie {display[wybór]} do pliku excel.\nZnajduje się ono na Twoim pulpicie.')
    press_enter()
    menu()

def admin_menu():
    os.system('cls')
    print ("""Tu możesz zarządzać bazą kontraktów i skzyń.\nWybierz odpowiedni numer z klawiatury po czym nacisnij klawisz 'Enter'\n 
    1 : dodaj kontrakt do bazy\n
    2 : usuń kontrakt z bazy\n
    3 : usuń skrzynie z zestawienia\n
    4 : wróc do menu głównego\n\n""")
    menu_choice = int(input("\nTwój wybór: "))  
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
        menu()
        
    else: 
        print('Wybierz prawidłową cyfrę...')
        powrot_admin()

def menu():
    os.system("cls")
    print ("""Cześć""",kto,"""! \nWitam Cię w kreatorze numerów skrzyń.\nWybierz odpowiedni numer z klawiatury po czym nacisnij klawisz 'Enter'\n
    MENU:\n
    1 : pobierz numery\n
    2 : edytuj zawartość skrzyni\n
    3 : wyświetl zestawienie skrzyń\n
    4 : eksportuj zestawienie do excela\n
    9 : opcje adminstratora\n
    0 : zakończ program\n\n""")
    try:
        menu_choice = int(input("\nTwój wybór: "))
    except:
        print('Dokonałes błędnego wyboru.') 
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
            if kto == 'Pawka' or kto == 'pmantiuk':
                admin_menu()
            else:
                os.system('cls')
                print('Nie masz uprawnień. Nie kombinuj...')
                press_enter()
                menu()
            
        elif menu_choice == 0:
            sys.exit()
        else: 
            print('Wybierz prawidłową cyfrę...')
            press_enter()
            menu()
            
kiedy = datetime.datetime.today().strftime ('%Y-%m-%d')
kto = getpass.getuser() 

laduj()
menu()

