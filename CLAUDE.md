# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

E-skin is a bioinspired electronic skin system for robotic applications. It combines:
- **Hardware**: KiCAD PCB designs for FSR (force-sensing resistor) arrays and accelerometer arrays
- **Firmware**: Arduino/Teensy 4.1 sketches for sensor data acquisition
- **Host Software**: C++/Qt desktop application with Python/MATLAB scripts for data logging

The system reads 16x16 or 32x32 FSR arrays plus accelerometer arrays at ~1562.5 Hz sampling rate, communicating via USB serial or Ethernet.

## Build Commands

### C++ Host Application
```bash
cd host
mkdir build && cd build
cmake .. && make
./FSR_array -h  # Show usage
```

Requires: CMake 3.3+, Qt6 (Core, Widgets, PrintSupport), C++11

### Arduino Firmware
- Board: Teensy 4.1 (`teensy:avr`)
- Port: `/dev/ttyACM0`
- Main sketch: `src/Eskin/Eskin.ino`

Upload via Arduino IDE or PlatformIO with Teensy 4.1 configuration.

### Python Scripts
```bash
pip install -r script/requirements.txt  # pyserial, numpy, keyboard, scipy
python script/record.py  # Data acquisition
```

## Code Style

C++ uses `host/.clang-format` with:
- LLVM base style, C++11
- Allman braces (opening brace on new line)
- 4-space indent, no tabs
- No spaces in parentheses

## Architecture

### Host Software (`host/`)
- `src/main.cpp` - C++ demo application
- `lib/com_client/` - Serial/TCP communication library (git submodule)
- `lib/built_lsl/` - Lab Streaming Layer integration (git submodule)
- `CMakeLists.txt` - Build configuration

### Firmware Layer (`src/`)
- `Eskin/Eskin.ino` - Main production firmware for FSR + accelerometer reading
- `MUXEDADC/` - Multiplexed ADC variant
- Other `.ino` folders are experimental variants

### Hardware Layer (`models/`)
- `KiCAD/` - Main control board (multiplexers + ADCs)
- `customSquare16x16/`, `customSquare8x8/` - FSR array PCBs
- `LIS3DH_array/`, `LIS2DH_array/`, `KX134_array/` - Accelerometer array variants
- `inskinacc/`, `inSkinAccv2/` - In-skin accelerometer designs

### Scripts (`script/`)
- `record.py` - Python data recorder (saves to .mat)
- `serialComFSR.m`, `tcpComFSR.m` - MATLAB interfaces

## Git Submodules

Dependencies are managed via git submodules in `host/lib/`. The CMake build system auto-initializes them when online. Manual init:
```bash
git submodule update --init --recursive
```

## Communication Protocol

- **Serial**: 115200 baud on `/dev/ttyACM0`
- **Ethernet**: TCP port 5000
- **Command format**: 1-byte (2 MSB = mode, 6 LSB = array size)
- **Response**: 4-byte timestamp + uint16_t array of sensor values
