---
layout: page
title: "Tutorial"
---

# How to Make the E-Skin

This tutorial covers the step-by-step fabrication and assembly process, including a short video demonstration. You’ll need:

- **Materials:** Smooth-On Ecoflex or DragonSkin, 3D-printed moulds, force-sensing resistor (FSR) arrays, accelerometers (LIS3DH or similar), flexible PCBs.
- **Tools:** 3D printer, soldering iron, small oven or hot air station (optional), mixing scales.

![Silicone mould and FSR arrays](/assets/img/silicone_mould_fsr.jpg)

---

## 1. Creating the Silicone Layers

1. **Print or prepare your mould:** Ensure the internal dimensions accommodate the sensor arrays.  
2. **Mix silicone:** Follow the manufacturer’s instructions (e.g. 1:1 ratio by weight).  
3. **Pour a thin base:** This becomes your “outer layer.”  
4. **Cure:** Let the silicone cure fully (time depends on product, typically 2–4 hours).

---

## 2. Placing the Sensors

1. **Position FSR Arrays:** Gently set one 16×16 array onto the partially cured silicone.  
2. **Add a second thin silicone pour:** This partially encapsulates the first FSR layer.  
3. **Place the second FSR layer:** Ensure alignment with the first layer.  
4. **Accelerometer Array:** Lay or mount the small boards near the top side, bridging them to the main PCB.  

![Accelerometer layer on flexible PCB](/assets/img/accelerometer_layer.jpg)

---

## 3. Wiring and Electronics

1. **Solder the demultiplexers and ADCs** to a control PCB (or breadboard).  
2. **Connect the FSR rows/columns** and accelerometer chip-select lines.  
3. **Use a Teensy 4.1** (or similar) for high-speed acquisition.  
4. **Check your data rate:** We aim for 800 Hz sampling across all sensors.

---

## 4. Final Encapsulation

1. **Top Silicone Pour:** Once all sensors are in place, pour the final layer.  
2. **Degas:** If you have a vacuum chamber, remove air bubbles for a cleaner finish.  
3. **Cure Thoroughly:** Follow the recommended cure schedule so everything sets properly.

---

## Video Demonstration

Below is a link to a demonstration video. Click the thumbnail to watch:

[![Video of e-skin build process](https://img.youtube.com/vi/VIDEO_ID/0.jpg)](https://www.youtube.com/watch?v=VIDEO_ID)

*(Replace `VIDEO_ID` with the actual YouTube video ID.)*

---

## 5. Testing

Once built, test the e-skin by pressing or brushing against different objects. If you have a robotic arm, mount the e-skin on the end-effector with a bracket or other fixture, and check real-time data streams from your microcontroller.

**We hope you enjoy making your own e-skin!** 

Feel free to return to our **[Home page](/)** or read the **[Project Summary](/article)**.
