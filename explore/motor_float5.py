from ina219 import INA219
from ina219 import DeviceRangeError

SHUNT_OHMS = 0.1


def read():

    # Initialize INA219 with SMBus and default address (0x40)
    ina = INA219(SHUNT_OHMS, busnum=1)  # Specify bus number directly

    # Configure for 32V and 2A
    ina.configure(voltage_range=ina.RANGE_32V,
                  gain=ina.GAIN_AUTO,
                  bus_adc=ina.ADC_128SAMP,
                  shunt_adc=ina.ADC_128SAMP)

    print("Bus Voltage: %.3f V" % ina.voltage())
    try:
        print("Bus Current: %.3f mA" % ina.current())
        print("Power: %.3f mW" % ina.power())
        print("Shunt voltage: %.3f mV" % ina.shunt_voltage())
    except DeviceRangeError as e:
        print(f"Current measurement error: {e}")


if __name__ == "__main__":
    read()