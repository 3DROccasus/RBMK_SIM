from ReadWriteMemory import ReadWriteMemory
from os import system
import struct as stc
rwm = ReadWriteMemory()
process = rwm.get_process_by_name('RXMODEL2.exe')
rods = []
for i in range(268580976, 268581073, 4):
    rods.append(i)


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
    selrod = process.get_pointer(rods[n-1])
    print('Selected fuel channel: ', n)
    left = process.read(rods[n-1])
    print('Fuel left ', "%.2f" % (refl(left) * 100), '%')
    print('''
1. Remove all fuel
2. Completely refuel
3. Set specific percentage of fuel
Anything else will return to menu''')
    rodmen = input()
    if not rodmen.isdecimal():
        cls()
        return
    elif 0 < int(rodmen) < 4:
        if int(rodmen) == 1:
            process.write(selrod, reint(0.001))
        elif int(rodmen) == 2:
            process.write(selrod, reint(1.00))
        elif int(rodmen) == 3:
            amount = input('Please enter percentage: ')
            if not amount.isdecimal() or not (0 < int(amount) < 101):
                cls()
                return
            else:
                process.write(selrod, reint(int(amount) / 100))
        else:
            cls()
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
    print('Fuel in 1 :', fuel[0], '% |  Fuel in 2 :', fuel[1], '% |  Fuel in 3 :', fuel[2], '% |  Fuel in 4 :', fuel[3],
          '% |   Fuel in 5 :', fuel[4], '%')
    print()
    print('Fuel in 6 :', fuel[5], '% |  Fuel in 7 :', fuel[6], '% |  Fuel in 8 :', fuel[7], '% |  Fuel in 9 :', fuel[8],
          '% |   Fuel in 10:', fuel[9], '%')
    print()
    print('Fuel in 11:', fuel[10], '% |  Fuel in 12:', fuel[11], '% |  Fuel in 13:', fuel[12], '% |  Fuel in 14:',
          fuel[13], '% |   Fuel in 15:', fuel[14], '%')
    print()
    print('Fuel in 16:', fuel[15], '% |  Fuel in 17:', fuel[16], '% |  Fuel in 18:', fuel[17], '% |  Fuel in 19:',
          fuel[18], '% |   Fuel in 20:', fuel[19], '%')
    print()
    print('Fuel in 21:', fuel[20], '% |  Fuel in 22:', fuel[21], '% |  Fuel in 23:', fuel[22], '% |  Fuel in 24:',
          fuel[23], '% |   Fuel in 25:', fuel[24], '%')
    print('''
Enter a fuel channel number, zoe for all, exit or anything else/nothing to reload data''')
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
            cls()
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
                cls()
                return
            else:
                for t in rods:
                    process.write(t, reint(int(amount) / 100))

    elif select == 'exit':
        exit(200)

    elif not select.isdecimal():
        cls()
        return

    elif 0 < int(select) < 26:
        fuelmenu(int(select))


while 1:
    mainmenu()
    cls()
