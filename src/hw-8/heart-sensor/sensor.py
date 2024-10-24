from machine import ADC, Pin, Timer

_ADC_THRESHOLD = const(32768)
_S_TO_US = const(1_000_000)
_BPM_FACTOR = const(60_000_000)
_DISPLAY_INTERVAL_US = const(100_000)

class HeartSensor:
    def __init__(self, adc_gpio: int, display, beeper, print_pulse_period: bool=False):
        self.adc = ADC(Pin(adc_gpio, Pin.IN))
        self._pulse_period_us = 0
        self._display_ticks_us = 0
        self._bpm = 0
        self._display = display
        self._beeper = beeper
        self._print_pulse_period = print_pulse_period

        self._beeper = beeper
        self._timer = Timer(-1)
        self._timer.init(mode=Timer.ONE_SHOT, freq=_S_TO_US, callback=self._adc_handler)
    
    def _adc_handler(self, timer: Timer):
        self._pulse_period_us += 1
        self._display_ticks_us += 1
        meas = self.adc.read_u16()
        
        if meas > _ADC_THRESHOLD:
            self._bpm = _BPM_FACTOR / self._pulse_period_us
            
            if self._print_pulse_period:
                period_s = "{:.6f}".format(self._pulse_period_us / _S_TO_US)
                print("Time between pulses: {} seconds".format(period_s))
            self._pulse_period_us = 0

            if self._beeper != None:
                self._beeper.start_beep()
        
        if (self._display != None) and (self._display_ticks_us >= _DISPLAY_INTERVAL_US):
            if self._display.bpm_enabled:
                self._display.update_bpm(bpm=self._bpm)

            if self._display.pulse_period_enabled:
                self._display.update_pulse_period(period_s=period_s)

            if self._display.graph_enabled:
                self._display.update_graph(sample_u16=meas)
                
            self._display_ticks_us = 0