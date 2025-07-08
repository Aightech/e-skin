import sys
import time
import numpy as np
import serial
from PyQt5 import QtCore, QtWidgets
import pyqtgraph.opengl as gl

class SerialReader(QtCore.QThread):
    data_received = QtCore.pyqtSignal(np.ndarray, np.ndarray)
    
    def __init__(self, port, parent=None):
        super(SerialReader, self).__init__(parent)
        self.port = port
        self.running = True
        try:
            self.ser = serial.Serial(port, 500000, timeout=3)
            time.sleep(1)
            self.ser.reset_input_buffer()
            self.ser.reset_output_buffer()
        except Exception as e:
            print("Serial connection error:", e)
            self.running = False

    def run(self):
        mode = 0b11
        size = 16
        cmd = (mode << 6) | size
        cmd_bytes = cmd.to_bytes(1, 'big')
        data_len = 8 + 96 + 1024  # Total data length (in bytes)
        while self.running:
            try:
                self.ser.write(cmd_bytes)
                d = self.ser.read(data_len)
                if len(d) != data_len:
                    continue
                # timestamps (unused here)
                _ = int.from_bytes(d[0:4], "little")
                _ = int.from_bytes(d[4:8], "little")
                # 16 accelerometer readings, each with 3 values (int16)
                acc = np.frombuffer(d[8:8 + 16*6], dtype=np.int16).reshape(16, 3)
                # FSR data: 16 readings, 2 layers, each with 16 values (uint16)
                fsr = np.frombuffer(d[8 + 16*6:], dtype=np.uint16).reshape(16, 2, 16)
                self.data_received.emit(acc, fsr)
            except Exception as e:
                print("Serial read error:", e)
                self.running = False

    def stop(self):
        self.running = False
        self.wait()
        if hasattr(self, 'ser') and self.ser.is_open:
            self.ser.close()

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, serial_port, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setWindowTitle("Real-time 3D Plot")
        self.widget = gl.GLViewWidget()
        self.setCentralWidget(self.widget)
        self.widget.opts['distance'] = 40
        
        # tare variables
        self.tare_count = 0
        self.tare_sum0 = np.zeros((16, 16), dtype=np.float64)
        self.tare_sum1 = np.zeros((16, 16), dtype=np.float64)
        self.tare_mean0 = None
        self.tare_mean1 = None
        
        # 1D arrays for FSR surfaces
        self.xgrid = np.linspace(0, 15, 16)
        self.ygrid = np.linspace(0, 15, 16)
        
        # Create FSR surfaces for two layers
        self.surface_fsr0 = gl.GLSurfacePlotItem(
            x=self.xgrid, y=self.ygrid, z=np.zeros((16, 16)),
            shader='shaded', color=(1, 0, 0, 0.5))
        self.surface_fsr0.translate(-8, -8, 0)
        self.widget.addItem(self.surface_fsr0)
        
        self.surface_fsr1 = gl.GLSurfacePlotItem(
            x=self.xgrid, y=self.ygrid, z=np.zeros((16, 16)),
            shader='shaded', color=(0, 1, 0, 0.5))
        self.surface_fsr1.translate(-8, -8, 0)
        self.widget.addItem(self.surface_fsr1)
        
        # Scatter plot for accelerometer data
        self.scatter_acc = gl.GLScatterPlotItem(
            pos=np.zeros((16, 3)), size=20, color=(0, 0, 1, 1))
        self.widget.addItem(self.scatter_acc)
        
        # Start serial thread
        self.serial_thread = SerialReader(serial_port)
        self.serial_thread.data_received.connect(self.update_data)
        self.serial_thread.start()
        
    def update_data(self, acc, fsr):
        raw0 = fsr[:, 0, :].astype(np.float32)
        raw1 = fsr[:, 1, :].astype(np.float32)
        
        # tare phase: first 100 samples
        if self.tare_mean0 is None:
            if self.tare_count < 100:
                self.tare_sum0 += raw0
                self.tare_sum1 += raw1
                self.tare_count += 1
                if self.tare_count == 100:
                    self.tare_mean0 = self.tare_sum0 / 100.0
                    self.tare_mean1 = self.tare_sum1 / 100.0
                    print("Tare complete")
                return
        
        # subtract tare and scale
        fsr0 = (raw0 - self.tare_mean0) / 100.0 + 4.0
        fsr1 = (raw1 - self.tare_mean1) / 100.0
        
        #set the first column of fsr0 to 0
        fsr0[:, 6] = (fsr0[:, 5] + fsr0[:, 7]) / 2.0
        
        self.surface_fsr0.setData(z=fsr0)
        self.surface_fsr1.setData(z=fsr1)
        
        # accelerometer scatter
        acc_float = acc.astype(np.float32) / 16384.0
        lookupArr = [0,7,8,9,5,6,15,10,4,2,12,11,3,1,14,13]
        acc_float = acc_float[lookupArr]
        for ix in range(4):
            for iy in range(4):
                idx = ix*4 + iy
                acc_float[idx, 0] += ix*4 - 8
                acc_float[idx, 1] += iy*4 - 8
                acc_float[idx, 2] += 6
        self.scatter_acc.setData(pos=acc_float)
        
    def closeEvent(self, event):
        self.serial_thread.stop()
        event.accept()

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage:")
        print(f"\t{sys.argv[0]} arduino_port")
        sys.exit(1)
        
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow(sys.argv[1])
    window.show()
    sys.exit(app.exec_())
