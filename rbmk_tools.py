from ReadWriteMemory import ReadWriteMemory
from os import system
import struct as stc

rwm = ReadWriteMemory()
process = rwm.get_process_by_name('RXMODEL2.exe')
rods = list(range(268580976, 268581073, 4))


def cls():
    return system('cls')


def refl(n):
    n = stc.pack('i', n)
    return stc.unpack('f', n)[0]


def reint(n):
    n = stc.pack('f', n)
    return stc.unpack('i', n)[0]


def fuelmenu(n):
    cls()
    selrod = process.get_pointer(rods[n - 1])
    print('Selected fuel channel: ', n)
    print('Fuel left ', fuel[n - 1], '%')
    print('''
1. Remove all fuel
2. Completely refuel
3. Set specific percentage of fuel
Anything else will return to menu''')
    rodmen = input()
    if not rodmen.isdecimal():
        return
    elif 0 < int(rodmen) < 4:
        if int(rodmen) == 1:
            process.write(selrod, reint(0.001))
        elif int(rodmen) == 2:
            process.write(selrod, reint(1.00))
        elif int(rodmen) == 3:
            amount = input('Please enter percentage: ')
            if not amount.isdecimal() or not (0 < int(amount) < 101):
                return
            else:
                process.write(selrod, reint(int(amount) / 100))
        else:
            return
    else:
        return


process.open()
fuel = []


def getcur():
    fuel.clear()
    for t in rods:
        curr = process.get_pointer(t)
        curr2 = process.read(curr)
        fuel.append("%.2f" % (refl(curr2) * 100))


def mainmenu():
    getcur()
    for i in range(0, 21, 5):
        print(f'Fuel in', f'0{i + 1}:' if i + 1 < 10 else f'{i + 1}:', f'{fuel[i]}'.rjust(8) + '% |\t\t',
              f'Fuel in', f'0{i + 2}:' if i + 2 < 10 else f'{i + 2}:', f'{fuel[i + 1]}'.rjust(8) + '% |\t',
              f'Fuel in', f'0{i + 3}:' if i + 3 < 10 else f'{i + 3}:', f'{fuel[i + 2]}'.rjust(8) + '% |\t',
              f'Fuel in', f'0{i + 4}:' if i + 4 < 10 else f'{i + 4}:', f'{fuel[i + 3]}'.rjust(8) + '% |\t',
              f'Fuel in', f'0{i + 5}:' if i + 5 < 10 else f'{i + 5}:', f'{fuel[i + 4]}'.rjust(8) + '% |\t',)
    print('''
Enter a fuel channel number, zoe for all, exit to exit or anything else/nothing to reload data''')
    select = input()

    if select == 'zoe':
        cls()
        print('Caution, refueling all channels at once can lead to a very high keff and cause a meltdown, especially '
              'while the plant is online')
        allert = input('''
1. Refuel all channels (DANGEROUS)
2. Unload all channels
3. Fill all channels to specific percentage
Anything else will return to menu
''')
        if not allert.isdecimal():
            return

        elif int(allert) == 1:
            cls()
            print('This might immediately cause a SCRAM and/or worse. Acknowledge by entering "ack"')
            isack = input()
            if isack == 'ack':
                for t in rods:
                    process.write(t, reint(1.00))

        elif int(allert) == 2:
            if input('Cancel with anything, else just press enter') == '':
                for k in rods:
                    process.write(k, reint(0.001))

        elif int(allert) == 3:
            amount = input('Please enter percentage ')
            if not amount.isdecimal() or not (0 < int(amount) < 101):
                return
            else:
                for t in rods:
                    process.write(t, reint(int(amount) / 100))

    elif select == 'exit':
        exit(200)

    elif not select.isdecimal():
        return

    elif 0 < int(select) < 26:
        fuelmenu(int(select))


while 1:
    cls()
    mainmenu()
