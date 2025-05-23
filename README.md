# windfreak-python [![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/christian-hahn/windfreak-python/blob/master/LICENSE)

## Abstract

**windfreak** is a pure Python package to facilitate the use of [Windfreak Technologies](https://windfreaktech.com) devices.

**windfreak** requires Python 3.

**windfreak** is MIT licensed.

## Supported devices

* SynthHD v1.4
* SynthHD PRO v1.4
* SynthHD v2
* SynthHD PRO v2
* SynthNV PRO

## Installation

### Using `pip`:
```text
pip install windfreak
```

### Using `setup.py`:
```text
git clone https://github.com/christian-hahn/windfreak-python.git
cd windfreak-python
python setup.py install
```

### Using `conda`:
Add `conda-forge` to your channels with
```text
conda config --add channels conda-forge
conda config --set channel_priority strict
```

then install the package with `conda`:
```text
conda install windfreak
```

or with `mamba`:
```text
mamba install windfreak
```

## Example

### SynthHD

```python
from windfreak import SynthHD

synth = SynthHD('/dev/ttyACM0') # Linux 
synth.init()

# Set channel 0 power and frequency
synth[0].power = -10.
synth[0].frequency = 2.e9

# Enable channel 0
synth[0].enable = True
```

### SynthNV PRO

```python
from windfreak import SynthNVPro

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

## License
windfreak-python is covered under the MIT license.
