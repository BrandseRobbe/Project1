from serial import Serial

# klasse moet nog gefixt worden

class SerialRaspberry:
    def __init__(self, baudrate,  soort_poort = '/dev/ttyS0'):
        self.soort_poort = soort_poort
        self.baudrate = baudrate
        self.__serieel = Serial(self.__soort_poort, self.__baudrate)

    def schrijf_bericht(self, bericht):
        if isinstance(bericht, str) and bericht != "":
            self.__serieel.write(bericht.encode("utf-8"))
        else:
            raise ("Geef een juist bericht mee.")

    def lees_char(self):
        teken = self.__serieel.read()
        # print(teken)
        uitvoer = ""
        if teken == b'\n':
            uitvoer = "/n"
        else:
            uitvoer = teken.decode("utf-8")
        return uitvoer

    def lees_bericht(self):
        # als het 3 spaties zijn betekent dat het een niewue lijn is
        uitvoer = ""
        doorgaan = True
        # teller = 0
        while doorgaan:
            # print('loop2')
            # teller+=1
            teken = self.lees_char()
            if teken != "/n":
                uitvoer += teken
            # elif teller == 100:
            #     doorgaan  =False
            else :
                doorgaan = False
        # teller = 0
        # print('loop2 done')
        return uitvoer

    @property
    def soort_poort(self):
        return self.__soort_poort

    @soort_poort.setter
    def soort_poort(self, value):
        if isinstance(value, str) and value != "":
            self.__soort_poort = value
        else:
            raise ('Geef een juiste poort mee.')

    @property
    def baudrate(self):
        return self.__baudrate

    @baudrate.setter
    def baudrate(self, value):
        if isinstance(value, int) and value >= 0:
            self.__baudrate = value
        else:
            raise ('Geef een juiste baudrate mee.')
