from grove.adc import ADC

class GroveMoistureSensor:
    def __init__(self, channel):
        self.channel = channel
        self.adc = ADC()

    # @property
    def moisture(self):
        '''
        Get the moisture strength value/voltage

        Returns:
            (int): voltage, in mV
        '''
        value = self.adc.read_voltage(self.channel)
        return value