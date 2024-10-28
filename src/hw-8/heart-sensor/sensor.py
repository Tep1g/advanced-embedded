import math
from machine import ADC, Pin, Timer
from lcd import NUM_DISPLAY_SAMPLES

_BEAT_ADC_THRESHOLD = const(60_000)
_SAMPLE_PERIOD_MS = const(1_000)

class HeartSensor:
    def __init__(self, adc_gpio: int, duration_ms: int, display=None, beeper=None, print_pulse_period: bool=False):
        self._adc = ADC(Pin(adc_gpio, Pin.IN))
        self.enabled = True
        self._beat_occurring = False
        self._beats = 0
        self._ticks_ms = 0
        self._debounce_counter = 35
        self._duration_ms = duration_ms
        self._display = display
        
        if self._display != None:
            self._samples = []
            self._sample_counter = 0
            self._sample_interval = math.ceil(self._duration_ms / NUM_DISPLAY_SAMPLES)

        self._beeper = beeper
        self._print_pulse_period = print_pulse_period

        self._beeper = beeper
        self._timer = Timer(-1)
        self._timer.init(mode=Timer.PERIODIC, freq=_SAMPLE_PERIOD_MS, callback=self._adc_handler)
    
    def _adc_handler(self, timer: Timer):
        self._ticks_ms += 1
        meas = self._adc.read_u16()
        
        if self._display != None:
            self._sample_counter = (self._sample_counter + 1) % self._sample_interval
            if self._sample_counter == 0:
                self._samples.append(meas)
        
        if meas > _BEAT_ADC_THRESHOLD:
            if not self._beat_occurring:
                self._beats += 1
                self._beat_occurring = True

                if (self._beeper != None) and (not self._beeper.is_beeping):
                    self._beeper.start_beep()

        elif self._beat_occurring:
            self._debounce_counter -= 1
            if self._debounce_counter == 0:
                self._beat_occurring = False
                self._debounce_counter = 35
        
        if self._ticks_ms >= self._duration_ms:
            self._timer.deinit()
            pulse_period_us = round(self._ticks_ms * 1000 / self._beats)

            if self._print_pulse_period:
                print("Time between pulses: {} microseconds".format(pulse_period_us))

            if self._display != None:
                bpm = (self._beats / (self._duration_ms / 1000)) * 60
                self._display.set_bpm(bpm=bpm)
                self._display.set_pulse_period(period_us=pulse_period_us)
                self._display.graph_samples(samples_u16=self._samples)

            self.enabled = False