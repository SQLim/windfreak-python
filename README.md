# windfreak-plus

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/SQLim/windfreak-python/blob/main/LICENSE)
[![GitHub Stars](https://img.shields.io/github/stars/SQLim/windfreak-plus.svg?style=social&label=Star&maxAge=3600)](https://github.com/SQLim/windfreak-python)

This is a fork of [windfreak](https://github.com/christian-hahn/windfreak-python) by Christian Hahn. This fork introduces the following new features and modifications:

* **New Feature 1:** New supported device model - SynthNV PRO.
* **New Feature 2:** SerialDevice dev_clear() method to reset input and output buffers. 
* **Fixed typos:** Minor typos fixed (e.g., 'mhz' to 'MHz')

## Abstract

**windfreak-plus** is a pure Python package to facilitate the use of [Windfreak Technologies](https://windfreaktech.com) devices.

**windfreak-plus** requires Python 3.

**windfreak-plus** is MIT licensed.

## Supported devices

* SynthHD v1.4
* SynthHD PRO v1.4
* SynthHD v2
* SynthHD PRO v2
* **[NEW!]** SynthNV PRO 

## Installation

### Using `pip`:
```text
python -m pip install [--user] git+https://github.com/SQLim/windfreak-python.git
```

### Using `setup.py`:
```text
git clone https://github.com/SQLim/windfreak-python.git
cd windfreak-python
python setup.py install
```

## Example

### SynthNV PRO

```python
from windfreak_plus import SynthNVPro

synth = SynthNVPro('COM4') # Windows 
synth.init()

# Set RFout power and frequency
synth.power = -10.
synth.frequency = 2.e9

# Enable RFout
synth.enable = True

# Get device temperature
synth.temperature # returns float [e.g., 31.0]

# Check if RFout in enabled
synth.enable      # returns bool [e.g., False]
```

### SynthHD

```python
from windfreak_plus import SynthHD

synth = SynthHD('/dev/ttyACM0') # Linux 
synth.init()

# Set channel 0 power and frequency
synth[0].power = -10.
synth[0].frequency = 2.e9

# Enable channel 0
synth[0].enable = True
```

## License
windfreak-plus is covered under the MIT license.
