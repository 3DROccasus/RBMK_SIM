from ReadWriteMemory import ReadWriteMemory
from ReadWriteMemory import ReadWriteMemoryError as Rwmerr
from os import system
import struct as stc

rwm = ReadWriteMemory()
try:
    process = rwm.get_process_by_name('RXMODEL.exe')
except Rwmerr:
    try:
        process = rwm.get_process_by_name('RXMODEL2.exe')
    except Rwmerr:
        print('Neither rxmodel.exe nor rxmodel2.exe found\n'
              "You can enter the process name manually, keep in mind that it's case sensitive:")
        processname = input()
        try:
            process = rwm.get_process_by_name(processname)
        except Rwmerr:
            input('Process not found, quitting')
            exit('Error: Process not found')

rods = list(range(268580976, 268581073, 4))
process.open()


def cls():
    return system('cls')


def isfloat(n):
    try:
        float(n)
        return True
    except ValueError:
        return False


def refl(n):
    n = stc.pack('i', n)
    return stc.unpack('f', n)[0]


def reint(n):
    n = stc.pack('f', n)
    return stc.unpack('i', n)[0]


def fuelmenu(n, fuel, rods, process):
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
            if not isfloat(amount) or not (0 < float(amount) < 101):
                return
            else:
                process.write(selrod, reint(float(amount) / 100))
        else:
            return
    else:
        return


fuel = []


def getcur(rods, fuel, process):
    fuel.clear()
    for t in rods:
        fuel.append("%.2f" % (refl(process.read(process.get_pointer(t))) * 100))


def mainmenu():
    getcur(rods, fuel, process)
    for i in range(0, 21, 5):
        print("|\t".join([f"Fuel in 0{j + 1}:{fuel[j]:>8}% " if j < 9 else f"Fuel in {j + 1}:{fuel[j]:>8}% "
                          for j in range(i, i + 5)]))
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
            if not isfloat(amount) or not (0 < float(amount) < 101):
                return
            else:
                for t in rods:
                    process.write(t, reint(float(amount) / 100))

    elif select == 'exit':
        exit(200)

    elif not select.isdecimal():
        return

    elif 0 < int(select) < 26:
        fuelmenu(int(select), fuel, rods, process)


while 1:
    cls()
    mainmenu()
