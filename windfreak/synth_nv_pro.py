from .device import SerialDevice


class SynthNVPro(SerialDevice):

    """ 
    API DOC: 
    https://windfreaktech.com/wp-content/uploads/2019/10/WFT_NVP_SerialProgramming_API_1.pdf
    GitHub repository (with README): 
    https://github.com/SQLim/windfreak-python/
    """

    # API dictionary
    API = {
        # name              type    write      read
        # Main settings
        'frequency':          (float, 'f{:.8f}', 'f?'),  # Frequency in MHz
        'power':              (float, 'W{:.3f}', 'W?'),  # Power in dBm
        'rf_enable':          (bool,  'h{}',     'h?'),  # RF power OFF/ON [0,1]
        'calibrated':         (bool,  None,      'V'),   # calibration check
        'phase_step':         (float, '~{:.3f}', '~?'),  # Phase step in degrees
        
        'trig_function':      (int,   'y{}',     'y?'),  # Trigger mode
        'reference_mode':     (int,   'x{}',     'x?'),  # {0: External , 1: Internal 27MHz, 2: Internal 10MHz}
        'ref_frequency':      (float, '*{:.8f}', '*?'),  # Internal reference frequency in MHz [10.0, 100.0]
        'ref_freq_doubler':   (bool,  'D{}',     'D?'),  # Reference frequency doubler 
        'pll_power_on':       (bool,  'E{}',     'E?'),  # Phase Lock Loop 
        'pll_cp_current':     (int,   'U{}',     'U?'),  # PLL charge pump current [0, 15]
        'pll_lock':           (bool,  None,      'p'),   # PLL unloacked/locked
        'temperature':        (float, None,      'z'),   # Internal temperature in Celsius
        'temp_comp_mode':     (int,   'Z{}',     'Z?'),  # Temperature compensation {0,1,2,3}
        'vga_dac':            (int,   'a{}',     'a?'),  # VGA DAC value [0, 4000]
        'channel_spacing':    (float, 'i{:.1f}', 'i?'),  # Channel spacing in Hz [0.1, 1000.0]
        'save':               ((),    'e',       None),  # Program all settings to EEPROM for power up boot
        
        # Sweep settings
        'sweep_freq_low':     (float, 'l{:.8f}', 'l?'),  # Sweep lower frequency in [12.5, 6400] MHz
        'sweep_freq_high':    (float, 'u{:.8f}', 'u?'),  # Sweep upper frequency in [12.5, 6400] MHz
        'sweep_freq_step':    (float, 's{:.8f}', 's?'),  # Sweep frequency step in MHz
        'sweep_time_step':    (float, 't{:.3f}', 't?'),  # Sweep time step in [0.1, 60000.0] ms
        'sweep_power_low':    (float, '[{:.3f}', '[?'),  # Sweep lower power [-50, +20] dBm
        'sweep_power_high':   (float, ']{:.3f}', ']?'),  # Sweep upper power [-50, +20] dBm
        'sweep_direction':    (int,   '^{}',     '^?'),  # Sweep direction {0: reverse, 1: forward}
        'sweep_type':         (int,   'X{}',     'X?'),  # Sweep type {0: linear, 1: tabular, 2: percentage]}
        'sweep_single':       (bool,  'g{}',     'g?'),  # Run sweep once (single sweep)
        'sweep_cont':         (bool,  'c{}',     'c?'),  # Enable continuous sweep 

        # Detector settings (RFin connector)
        'detect_power':       (float,   None,    'w'),   # Detects power on RFin connector in dBm
        'detector_mode':      (int,   '&{}',     '&?'),  # {0: instant, 1: average, 2: uncalibrated}
        'detect_powers':      (bool,  'r{}',     'r?'),  # Detects RFin power while sweeping RFout  
        'detect_powers_styl': (int,   'd{}',     'd?'),  # RF sweep detect display style {0: none, 1: MHz and dBm, 2: dBm}

        # Amplitude modulation
        'am_time_step':       (int,   'F{}',     'F?'),  # Time step in microseconds
        'am_num_samples':     (int,   'q{}',     'q?'),  # Number of samples in one burst
        'am_cont':            (bool,  'A{}',     'A?'),  # Enable continuous AM
        'am_lookup_table':    ((int, float), '@{}a{:.3f}', '@{}a?'),  # Program row in lookup table in dBm

        # Pulse modulation
        'pulse_on_time':      (int,   'P{}',     'P?'),  # Pulse on time in range [1, 10e6] us
        'pulse_off_time':     (int,   'O{}',     'O?'),  # Pulse off time in range [2, 10e6] uS
        'pulse_num_rep':      (int,   'R{}',     'R?'),  # Number of repetitions in range [1, 65500]
        'pulse_invert':       (bool,  ':{}',     ':?'),  # Invert pulse polarity
        'pulse_single':       ((),    'G',       None),  # Run PM once (single burst/cycle)
        'pulse_cont':         (bool,  'j{}',     'j?'),  # Enable continuous PM 

        # Frequency modulation
        'fm_frequency':       (int,   '<{}',     '<?'),  # FM frequency [1, 5000]
        'fm_deviation':       (int,   '>{}',     '>?'),  # FM deviation frequency
        'fm_num_samples':     (int,   ',{}',     ',?'),  # Number of samples per burst/cycle
        'fm_mod_type':        (int,   ';{}',     ';?'),  # FM type {0: chirp/ext, 1: sine}
        'fm_cont':            (bool,  '/{}',     '/?'),  # Enable continuous FM

        # Instrument information
        'model_type':         (str,   None,      '+'),   # Model type
        'serial_number':      (int,   None,      '-'),   # Serial number
        'fw_version':         (str,   None,      'v0'),  # Firmware version
        'hw_version':         (str,   None,      'v1'),  # Hardware version
    }

    def __init__(self, devpath):
        super().__init__(devpath)
        self._model = None
        self._model = self.model
        if self.model == 'SynthNV PRO':
            self._f_range = {'start': 12.5e6, 'stop': 6400.e6, 'step': 0.1}
            self._p_range = {'start': -60., 'stop': 20., 'step': 0.001}
            self._vga_range = {'start': 0, 'stop': 4000, 'step': 1}
            self._cspacing_range = {'start': 0.1, 'stop': 1000., 'step': 0.1}
        else:
            self._f_range = None
            self._p_range = None
            self._vga_range = None
            self._cspacing_range = None

    def init(self):
        """Initialize device: put into a known, safe state."""
        self.dev_clear()
        self.rf_enable = False
        f_range = self.frequency_range
        if f_range is not None:
            self.frequency = f_range['start']
        p_range = self.power_range
        if p_range is not None:
            self.power = p_range['start']
        self.phase = 0.
        self.temp_compensation_mode = '10 sec'
        self.reference_mode = 'internal 27MHz'
        self.trigger_mode = 'disabled'
        self.sweep_enable = False
        self.sweep_direction = 'forward'
        self.am_enable = False
        self.pulse_mod_enable = False
        self.fm_enable = False
        self.detect_mode = 'instant'
        self.measure_powers = False
        self.detect_powers_style = 'none'

    @property
    def model(self):
        """Model. This is the binned version that dictates API support.

        Returns:
            str: model version or None if unsupported
        """
        if self._model is not None:
            return self._model
        
        modeltype = self.read('model_type')
        if 'SynthNVP' in modeltype:
            return 'SynthNV PRO'
        else:
            # Unsupported hardware version. Return None.
            return None

    @property
    def serial_number(self):
        """Serial number

        Returns:
            int: serial number
        """
        return self.read('serial_number')

    @property
    def firmware_version(self):
        """Firmware version.

        Returns:
            str: version
        """
        return self.read('fw_version')

    @property
    def hardware_version(self):
        """Hardware version.

        Returns:
            str: version
        """
        return self.read('hw_version')

    def save(self):
        """Save all settings to non-volatile EEPROM."""
        self.write('save')

    @property
    def trigger_modes(self):
        """List of trigger modes.

        Returns:
            tuple: tuple of str of modes
        """
        return (
            'disabled',
            'full frequency sweep',
            'single frequency step',
            'stop all',
            'rf enable',
            'remove interrupts',
            'reserved',
            'reserved',
            'am modulation',
            'fm modulation',
        )

    @property
    def trigger_mode(self):
        """Get trigger mode.

        Returns:
            str: mode
        """
        return self.trigger_modes[self.read('trig_function')]

    @trigger_mode.setter
    def trigger_mode(self, value):
        """Set trigger mode.

        Args:
            value (str): mode
        """
        modes = self.trigger_modes
        if not value in modes:
            raise ValueError('Expected str in set: {}.'.format(modes))
        self.write('trig_function', modes.index(value))

    @property
    def reference_modes(self):
        """List of frequency reference modes.

        Returns:
            tuple: tuple of str of modes
        """
        return ('external', 
            'internal 27MHz', 
            'internal 10MHz'
            )

    @property
    def reference_mode(self):
        """Get frequency reference mode.

        Returns:
            str: mode
        """
        return self.reference_modes[self.read('reference_mode')]

    @reference_mode.setter
    def reference_mode(self, value):
        """Set frequency reference mode.

        Args:
            value (str): mode
        """
        modes = self.reference_modes
        if not value in modes:
            raise ValueError('Expected str in set {}.'.format(modes))
        self.write('reference_mode', modes.index(value))

    @property
    def reference_frequency_range(self):
        """List reference frequency range in Hz.

        Returns:
            dict: frequency range in Hz
        """
        return {'start': 10.e6, 'stop': 100.e6, 'step': 1.e3}

    @property
    def reference_frequency(self):
        """Get reference frequency in Hz.

        Returns:
            float: frequency in Hz
        """
        return self.read('ref_frequency') * 1.e6

    @reference_frequency.setter
    def reference_frequency(self, value):
        """Set reference frequency in Hz.

        Args:
            value (float / int): frequency in Hz
        """
        if not isinstance(value, (float, int)):
            raise ValueError('Expected float or int.')
        f_range = self.reference_frequency_range
        if not f_range['start'] <= value <= f_range['stop']:
            raise ValueError('Expected float in range [{}, {}] Hz.'.format(
                             f_range['start'], f_range['stop']))
        self.write('ref_frequency', value / 1.e6)

    @property
    def temperature(self):
        """Get temperature in Celsius.

        Returns:
            float: temperature
        """
        return self.read('temperature')

    @property
    def sweep_enable(self):
        """Get sweep continuously enabled/disabled.

        Returns:
            bool: enabled/disabled
        """
        return self.read('sweep_cont')

    @sweep_enable.setter
    def sweep_enable(self, value):
        """Set sweep continuously enable.

        Args:
            value (bool): enable
        """
        if not isinstance(value, bool):
            raise ValueError('Expected bool.')
        self.write('sweep_cont', value)

    @property
    def sweep_types(self):
        """List sweep types.

        Returns:
            tuple: Tuple of str of sweep types.
        """
        return (
            'linear', 
            'tabular',
            'percentage'
            )

    @property
    def sweep_type(self):
        """Get sweep type.

        Returns:
            str: sweep type
        """
        return self.sweep_types[self.read('sweep_type')]

    @sweep_type.setter
    def sweep_type(self, value):
        """Set sweep type.

        Args:
            value (str): sweep type.
        """
        types = self.sweep_types
        if value not in types:
            raise ValueError('Expected str in set: {}.'.format(types))
        self.write('sweep_type', types.index(value))

    @property
    def sweep_directions(self):
        """List sweep directions.

        Returns:
            tuple: Tuple of str of sweep directions.
        """
        return (
            'reverse', 
            'forward'
            )

    @property
    def sweep_direction(self):
        """Get sweep direction.

        Returns:
            str: sweep direction
        """
        return self.sweep_directions[self.read('sweep_direction')]

    @sweep_direction.setter
    def sweep_direction(self, value):
        """Set sweep direction.

        Args:
            value (str): sweep direction.
        """
        directions = self.sweep_directions
        if value not in directions:
            raise ValueError('Expected str in set: {}.'.format(directions))
        self.write('sweep_direction', directions.index(value))

    @property
    def am_enable(self):
        """Get AM continuously enable.

        Returns:
            bool: enable
        """
        return self.read('am_cont')

    @am_enable.setter
    def am_enable(self, value):
        """Set AM continuously enable.

        Args:
            value (bool): enable
        """
        if not isinstance(value, bool):
            raise ValueError('Expected bool.')
        self.write('am_cont', value)

    @property
    def pulse_mod_enable(self):
        """Get pulse modulation continuously enable.

        Returns:
            bool: enable
        """
        return self.read('pulse_cont')

    @pulse_mod_enable.setter
    def pulse_mod_enable(self, value):
        """Set pulse modulation continuously enable.

        Args:
            value (bool): enable
        """
        if not isinstance(value, bool):
            raise ValueError('Expected bool.')
        self.write('pulse_cont', value)

    @property
    def fm_enable(self):
        """Get FM continuously enable.

        Returns:
            bool: enable
        """
        return self.read('fm_cont')

    @fm_enable.setter
    def fm_enable(self, value):
        """Set FM continuously enable.

        Args:
            value (bool): enable
        """
        if not isinstance(value, bool):
            raise ValueError('Expected bool.')
        self.write('fm_cont', value)

    @property
    def frequency_range(self):
        """Get frequency range in Hz.

        Returns:
            dict: frequency range or None
        """
        return None if self._f_range is None else self._f_range.copy()

    @property
    def frequency(self):
        """Get frequency in Hz.

        Returns:
            float: frequency in Hz
        """
        return self.read('frequency') * 1e6

    @frequency.setter
    def frequency(self, value):
        """Set frequency in Hz.

        Args:
            value (float / int): frequency in Hz
        """
        if not isinstance(value, (float, int)):
            raise ValueError('Expected float or int.')
        f_range = self.frequency_range
        if f_range is not None and not f_range['start'] <= value <= f_range['stop']:
            raise ValueError('Expected float in range [{}, {}] Hz.'.format(
                             f_range['start'], f_range['stop']))
        self.write('frequency', value / 1e6)

    @property
    def power_range(self):
        """Power range in dBm.

        Returns:
            dict: power range or None
        """
        return None if self._p_range is None else self._p_range.copy()

    @property
    def power(self):
        """Get power in dBm.

        Returns:
            float: power in dBm
        """
        return self.read('power')

    @power.setter
    def power(self, value):
        """Set power in dBm.

        Args:
            value (float / int): power in dBm
        """
        if not isinstance(value, (float, int)):
            raise TypeError('Expected float or int.')
        self.write('power', value)

    @property
    def calibrated(self):
        """Calibration was successful on frequency or amplitude change.

        Returns:
            bool: calibrated
        """
        return self.read('calibrated')

    @property
    def temp_compensation_modes(self):
        """Temperature compensation modes.

        Returns:
            tuple: tuple of str of modes
        """
        return ('none', 'on set', '1 sec', '10 sec')

    @property
    def temp_compensation_mode(self):
        """Temperature compensation mode.

        Returns:
            str: mode
        """
        return self.temp_compensation_modes[self.read('temp_comp_mode')]

    @temp_compensation_mode.setter
    def temp_compensation_mode(self, value):
        """Set temperature compensation mode.
        
        Args:
            value (str): temperature compensation mode.
        """
        modes = self.temp_compensation_modes
        if not value in modes:
            raise ValueError('Expected str in set {}.'.format(modes))
        self.write('temp_comp_mode', modes.index(value))

    @property
    def vga_dac_range(self):
        """VGA DAC value range.

        Returns:
            dict: VGA DAC range or None
        """
        return None if self._vga_range is None else self._vga_range.copy()

    @property
    def vga_dac(self):
        """Get raw VGA DAC value

        Returns:
            int: value
        """
        return self.read('vga_dac')

    @vga_dac.setter
    def vga_dac(self, value):
        """Set raw VGA DAC value.

        Args:
            value (int): value
        """
        if not isinstance(value, int):
            raise TypeError('Expected int.')
        self.write('vga_dac', value)

    @property
    def phase_range(self):
        """Phase step range.

        Returns:
            dict: range
        """
        return {
            'start': 0.,
            'stop': 360.,
            'step': .001,
        }

    @property
    def phase(self):
        """Get phase step value.

        Returns:
            float: value in degrees
        """
        return self.read('phase_step')

    @phase.setter
    def phase(self, value):
        """Set phase step value.

        Args:
            value (float / int): phase in degrees
        """
        if not isinstance(value, (float, int)):
            raise TypeError('Expected float or int.')
        self.write('phase_step', value)

    @property
    def rf_enable(self):
        """RF output enable.

        Returns:
            bool: enable
        """
        return self.read('rf_enable')

    @rf_enable.setter
    def rf_enable(self, value):
        if not isinstance(value, bool):
            raise ValueError('Expected bool.')
        self.write('rf_enable', value)

    @property
    def pll_enable(self):
        """PLL enable.

        Returns:
            bool: enable
        """
        return self.read('pll_power_on')

    @pll_enable.setter
    def pll_enable(self, value):
        if not isinstance(value, bool):
            raise ValueError('Expected bool.')
        self.write('pll_power_on', value)

    @property
    def enable(self):
        """Get output enable.

        Returns:
            bool: enabled
        """
        return self.rf_enable and self.pll_enable

    @enable.setter
    def enable(self, value):
        """Set output enable.

        Args:
            value (bool): enable
        """
        if not isinstance(value, bool):
            raise TypeError('Expected bool.')
        self.rf_enable = value
        self.pll_enable = value

    @property
    def fm_freq(self):
        """Get FM frequency in Hz.

        Args:
            int: FM frequency in Hz.
        """
        return self.read('fm_frequency')

    @fm_freq.setter
    def fm_freq(self, value):
        """Set FM frequency in Hz [1-5000 Hz].

        Args:
            value (int): FM frequency in Hz.
        """
        self.write('fm_frequency', value)

    @property
    def fm_dev(self):
        """Get FM deviation in Hz [1 Hz minimum].

        Args:
            int: FM deviation in Hz.
        """
        return self.read('fm_deviation')

    @fm_dev.setter
    def fm_dev(self, value):
        """Set FM deviation in Hz.

        Args:
            value (int): FM deviation in Hz.
        """
        self.write('fm_deviation', value)

    @property
    def fm_types(self):
        """List of FM mod types.

        Returns:
            tuple: tuple of str of modes
        """
        return (
            'chirp',
            'sine'
        )

    @property
    def fm_type(self):
        """Get FM mod type.

        Args:
            str: FM mod type.
        """
        return self.fm_types[self.read('fm_mod_type')]

    @fm_type.setter
    def fm_type(self, value):
        """Set FM mod type.

        Args:
            value (str): FM mod type.
        """
        types = self.fm_types
        if not value in types:
            raise ValueError('Expected str in set: {}.'.format(types))
        self.write('fm_mod_type', types.index(value))

    @property
    def lock_status(self):
        """PLL lock status.

        Returns:
            bool: locked
        """
        return self.read('pll_lock')

    @property
    def channel_spacing_range(self):
        """Channel Spacing Range in Hz.

           Returns:
               dict: channel spacing range or None
        """
        return None if self._cspacing_range is None else self._cspacing_range.copy()

    @property
    def channel_spacing(self):
        """Channel Spacing in Hz

           Returns:
               float: Channel Spacing setting in Hz
        """
        return self.read('channel_spacing')

    @channel_spacing.setter
    def channel_spacing(self,value):
        """Set Channel Spacing in Hz.

           Args:
               float: Channel spacing in Hz
        """
        if not isinstance(value, (float, int)):
            raise ValueError('Expected float or int.')
        cs_range = self.channel_spacing_range
        if cs_range is not None and not cs_range['start'] <= value <= cs_range['stop']:
            raise ValueError('Expected float in range [{}, {}] Hz.'.format(
                             cs_range['start'], cs_range['stop']))
        self.write('channel_spacing', value)

    @property
    def detect_modes(self):
        """List of detector modes.

        Returns:
            tuple: tuple of str of modes
        """
        return (
            'instant',
            'average',
            'uncalibrated'
        )

    @property
    def detect_mode(self):
        """Get detector mode.

        Returns:
            str: mode
        """
        return self.detect_modes[self.read('detector_mode')]

    @detect_mode.setter
    def detect_mode(self, value):
        """Set detector mode.

        Args:
            value (str): mode
        """
        modes = self.detect_modes
        if not value in modes:
            raise ValueError('Expected str in set: {}.'.format(modes))
        self.write('detector_mode', modes.index(value))

    def measure_power(self):
        """Measure power at RFin in dBm.

        Returns:
            float: power
        """
        power = self.read('detect_power')
        self.dev_clear()
        return power

    @property
    def measure_powers(self):
        """Get measure power during RF sweep enable.

        Returns:
            bool: enable
        """
        return self.read('detect_powers')

    @measure_powers.setter
    def measure_powers(self, value):
        """Set measure power during RF sweep enable.

        Args:
            value (bool): enable
        """
        if not isinstance(value, bool):
            raise ValueError('Expected bool.')
        self.write('detect_powers', value)

    @property
    def detect_powers_styles(self):
        """List of display styles for when
        the RF power is read during sweep.

        Returns:
            tuple: tuple of str of modes
        """
        return (
            'none', 
            'MHz and dBm', 
            'dBm'
        )

    @property
    def detect_powers_style(self):
        """Get power display style.

        Returns:
            str: display style
        """
        return self.detect_powers_styles[self.read('detect_powers_styl')]

    @detect_powers_style.setter
    def detect_powers_style(self, value):
        """Set power display style.

        Args:
            value (str): display style
        """
        styles = self.detect_powers_styles
        if not value in styles:
            raise ValueError('Expected str in set: {}.'.format(styles))
        self.write('detect_powers_styl', styles.index(value))

    # TODO
    # Additional Sweep properties and settings:
    # 'sweep_freq_low':     (float, 'l{:.8f}', 'l?'),  # Sweep lower frequency in [12.5, 6400] MHz
    # 'sweep_freq_high':    (float, 'u{:.8f}', 'u?'),  # Sweep upper frequency in [12.5, 6400] MHz
    # 'sweep_freq_step':    (float, 's{:.8f}', 's?'),  # Sweep frequency step in MHz
    # 'sweep_time_step':    (float, 't{:.3f}', 't?'),  # Sweep time step in [0.1, 60000.0] ms
    # 'sweep_power_low':    (float, '[{:.3f}', '[?'),  # Sweep lower power [-50, +20] dBm
    # 'sweep_power_high':   (float, ']{:.3f}', ']?'),  # Sweep upper power [-50, +20] dBm
    # Additional AM, FM, PM modulation properties and settings