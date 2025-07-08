---
layout: post
title: "Summary"
date: 2025-01-29
author: "A. W. M. Devillard, A. Dutta, Z. Zhang, X. Cheng, M. Kaboli, E. Burdet"
---

![E-skin layers diagram](/assets/img/eskin_diagram.jpg)

## Abstract

The human skin is a complex system playing several roles in everyday life. Not only does it sense the environment, it also protects the body. To build a bioinspired haptic sensor, the density and type of sensors are important, but one must also consider the skin’s mechanical properties and overall robustness. 

In this study, we present a bioinspired **modular and scalable** design of a soft electronic skin (e-skin) to investigate the role of the skin's mechanical attributes in tactile sensing for robotic applications. We characterise and evaluate our system using objects with varied mechanical properties, showing how our e-skin can capture both forces and vibrations and differentiate between objects of different stiffness or surface textures.

---

## 1. Introduction

Research in haptic sensing aims to replicate the richness of human touch in robotic end-effectors, prostheses, and more. Human skin’s dermis and epidermis contain multiple receptors detecting pressure, vibration, and temperature. By mimicking this layered approach with modern soft materials and off-the-shelf sensors, we can produce large-area, flexible e-skins that provide normal and shear force measurements as well as high-frequency vibration data.

**Key Features:**
- **Layered Silicone Encapsulation:** Inspired by epidermis and dermis.
- **Multimodal Sensing:** Force-sensing resistors (FSRs) for normal and shear, accelerometers for vibration.
- **Scalable Electronics:** A multiplexed design reduces wiring complexity.

![Kinova robot with e-skin](assets/img/setup/experimental_setup.pdf)

---

## 2. Design & Fabrication

### 2.1 Layered Structure

1. **Top Silicone Layer:** Acts like an epidermis, protecting internal sensors.
2. **Accelerometer Layer:** A small-array PCB for vibration detection.
3. **Inter-layer Silicone:** Adds compliance to allow slight shear displacements.
4. **FSR Layers:** Two stacked 16×16 FSR arrays to measure normal pressures but also infer shear forces.
5. **Base Silicone:** Final protective layer.

### 2.2 Electronics

- **Accelerometers:** SPI-based array with demultiplexers to manage up to 16 devices on minimal lines.
- **FSRs:** Each 16×16 array read by scanning 16 row lines and 16 column lines. 
- **Microcontroller:** A Teensy 4.1 capturing up to 800 Hz from all sensors, streaming data via USB.


---

## 3. Experiments

We mounted the e-skin onto a Kinova robotic arm equipped with a 6-axis force/torque sensor. We tested interactions (pressing, rolling, slipping) against a series of ‘wave objects’ featuring different stiffnesses and surface textures. Our aim was to see how well the e-skin could estimate normal and shear forces, and classify objects by texture and compliance.

---

## 4. Results and Discussion

- **Force Estimation:** The two FSR layers and compliant silicone enable basic shear reconstruction (X-Y), plus normal force (Z).
- **Object Classification:** Combining force and vibration data in a neural network yields clear separation of soft vs. rigid objects, and differentiates surfaces with different spatial frequencies.

### Future Directions
Ongoing improvements involve reconfigurable sensor densities, adding temperature or humidity sensors, and adapting the silicone’s thickness/hardness for varied tasks.

---

## References

1. Howe, R., & Cutkosky, M. "Tactile sensing and control of robotic manipulation." *Advanced Robotics*, 1993.  
2. Kim, D., et al. "Highly sensitive tactile sensors using microstructured dielectrics." *Advanced Materials*, 2012.  
3. Chen, X., et al. "Self-powered flexible pressure sensors with ZnO nanowires." *Nano Energy*, 2015.

And others…

