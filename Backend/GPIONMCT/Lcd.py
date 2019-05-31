import time

from RPi import GPIO


class Lcd:

    def __init__(self, data_pins, RS_pin, E_pin ):

        GPIO.setmode(GPIO.BCM)
        self.data_pins = data_pins
        self.RS_pin = RS_pin
        self.E_pin = E_pin

        self.__cursor = 0


        for pin in data_pins: GPIO.setup(pin, GPIO.OUT)
        GPIO.setup(self.__RS_pin, GPIO.OUT)
        GPIO.output(self.__RS_pin, 1)
        GPIO.setup(self.__E_pin, GPIO.OUT)
        GPIO.output(self.__E_pin, 1)
        self.LCD_init()

    def LCD_init(self):
        self.functionset()
        self.displayOn()
        self.reset_LCD()

    def enter(self):
        self.send_instruction(128 + 0x40)
        self.__cursor = 16

    def write_message(self, waarde):
        for letter in waarde:
            self.send_character(ord(letter))
            self.__cursor+= 1
            if self.__cursor == 16:
                self.enter()
            elif self.__cursor == 32:
                self.__cursor = 0
                self.reset_LCD()
    def set_data_bits(self, value):
        # print('instructie: %s', bin(value))
        mask = 0x80
        for i in range(0, 8):
            bite = value & mask >> i
            if bite != 0:
                bite = 1
            # print("pin(%s) bit %s,: %s" % (data_pins[i], i, bite))
            GPIO.output(self.__data_pins[i], bite)

    def send_instruction(self, value):
        GPIO.output(self.__RS_pin, 0)
        GPIO.output(self.__E_pin, 1)
        self.set_data_bits(value)
        time.sleep(0.1)
        GPIO.output(self.__E_pin, 0)

    def send_character(self, value):
        GPIO.output(self.__RS_pin, 1)
        GPIO.output(self.__E_pin, 1)
        self.set_data_bits(value)
        time.sleep(0.0001)
        GPIO.output(self.__E_pin, 0)

    def functionset(self):
        self.send_instruction(0x3c)

    def displayOn(self, blink = False, underscore = False):
        instructie = 0x0f
        if blink==1:
            instructie-=2
        if underscore==1:
            instructie-=1
        # self.send_instruction(0x0f-3)
        self.send_instruction(instructie)

    def reset_LCD(self):
        self.send_instruction(0x01)
        self.__cursor = 0

    @property
    def data_pins(self):
        return self.__data_pins

    @data_pins.setter
    def data_pins(self, value):
        if isinstance(value, list):
            self.__data_pins = value
        else:
            raise('Je moet een lijst met data pins meegeven!')

    @property
    def RS_pin(self):
        return self.__RS_pin

    @RS_pin.setter
    def RS_pin(self, value):
        if isinstance(value, int):
            self.__RS_pin = value
        else:
            raise ('Je moet een int waarde meegeven!')

    @property
    def E_pin(self):
        return self.__E_pin

    @E_pin.setter
    def E_pin(self, value):
        if isinstance(value, int):
            self.__E_pin = value
        else:
            raise ('Je moet een int waarde meegeven!')