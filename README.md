# E-Skin

A bioinspired electronic skin system for robotic applications, combining FSR (force-sensing resistor) arrays and accelerometer arrays.

## Overview

The electronic board uses two multiplexers and two 16-channel ADCs to read the FSRs. The multiplexers select the row or column of the FSR array, while the ADCs read the sensor values. A Teensy 4.1 controls the multiplexers and ADCs and sends data to the computer via USB or Ethernet.

**Operation modes:**
- **Single mode**: Connect one FSR array with up to 32x32 sensors
- **Dual mode**: Connect two FSR arrays with up to 16x16 sensors each

**Sampling rate:** ~400 KHz/channel (1562.5 Hz for a 16x16 array)

## Project Structure

```
e-skin/
├── host/           # C++/Qt host application
│   ├── src/        # Source code (main.cpp)
│   └── lib/        # Git submodules (com_client, built_lsl)
├── src/            # Teensy firmware
│   └── Eskin/      # Main production firmware
├── models/         # KiCAD PCB designs
│   ├── KiCAD/              # Main control board (MUX + ADC)
│   ├── customSquare16x16/  # 16x16 FSR array
│   ├── customSquare8x8/    # 8x8 FSR array
│   ├── LIS2DH_array/       # LIS2DH accelerometer array
│   ├── KX134_array/        # KX134 accelerometer array
│   └── inskinacc/          # In-skin accelerometer
└── script/         # Python/MATLAB data acquisition scripts
```

## Requirements

### Host Application
- CMake 3.3+
- Qt6 (Core, Widgets, PrintSupport)
- C++11 compiler

### Firmware
- Arduino IDE or PlatformIO
- Teensy 4.1 board support

### Python Scripts
- Python 3.x
- Dependencies: `pip install -r script/requirements.txt`

## Building

### Host Application

```bash
cd host
mkdir build && cd build
cmake .. && make
./FSR_array -h  # Show usage
```

### Firmware

Upload `src/Eskin/Eskin.ino` to Teensy 4.1 using Arduino IDE or PlatformIO.

- Board: Teensy 4.1
- Port: `/dev/ttyACM0` (Linux) or `COMx` (Windows)

### Python Data Recorder

```bash
pip install -r script/requirements.txt
python script/record.py <port> <array_size>
# Example: python script/record.py /dev/ttyACM0 16
```

## Communication Protocol

- **Serial**: 500000 baud
- **Ethernet**: TCP port 5000
- **Command format**: 1 byte (2 MSB = mode, 6 LSB = array size)
  - Mode 0: Request 1 FSR array
  - Mode 1: Request 2 FSR arrays
  - Mode 2: Request 1 ACC array
  - Mode 3: Request 1 ACC array + 2 FSR arrays
- **Response**: 4-byte timestamps + uint16_t sensor data

## Submodule Dependencies

- [built_lsl](host/lib/built_lsl/README.md) - Lab Streaming Layer integration
- [com_client](host/lib/com_client/README.md) - Serial/TCP communication library

Initialize submodules:
```bash
git submodule update --init --recursive
```

## Example

See [main.cpp](host/src/main.cpp) for an example of how to use the communication library.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.
