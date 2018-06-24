# make a fancy looking decode program that doesn't actually decode
from time import sleep
import string, os, getpass


def listprint(message, time=0.1):
    try:
        for char in list(message):
            print(char, end='', flush=True)
            sleep(time)
    except KeyboardInterrupt:
        print('\n')
        print('ERROR. EXITING')
        print('\n')
        sleep(2)
        exit(5)
def passwdcheck():
    p = getpass.getpass(prompt='').lower()
    return p
try:
        listprint('Decryptor v0.1 - Published 29-06-2018 21:00')
        print('')
        i = 0
        for i in range(0,3):
            listprint('Password:')
            if passwdcheck() not in ["etiam", "steadfast"]:
                listprint('WRONG PASSWORD')
                print('')
                continue
            else:
                listprint('ACCESS GRANTED')
                print('')
                listprint('Retreiving message')
                sleep(0.3)
                listprint('...............')
                print('')


                def replacement(number):
                    base = '.........'
                    message = base[:number] + ',' + base[number:]
                    listprint(message)


                # use coordinates for tanoa base
                coordinates = 'GR137100'
                for char in list(coordinates):
                    if char == '.':
                        listprint('..........')
                        print('')
                    else:
                        if char in string.ascii_uppercase:
                            listprint('*' * (string.ascii_lowercase.index(char.lower()) + 1))
                            print('')
                        elif char == '-' or char == ' ':
                            print('')
                        else:
                            replacement(int(char))
                            print('')

                print('\n')
                listprint('Retreival complete.')
                print('\n')
                try:
                    os.system('pause')
                    exit(1)
                except:
                    exit(1)

        print('\n')
        listprint('ACCESS DENIED')
        print('\n')
        sleep(2)
        exit(5)

except KeyboardInterrupt:
        print('\n')
        listprint('ACCESS DENIED')
        print('\n')
        sleep(2)
        exit(5)

