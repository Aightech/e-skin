import sys
import time
import numpy as np
import serial
from PyQt5 import QtCore, QtWidgets
import pyqtgraph.opengl as gl
from pyqtgraph.opengl import MeshData, GLMeshItem

class SerialReader(QtCore.QThread):
    data_received = QtCore.pyqtSignal(np.ndarray)

    def __init__(self, port, parent=None):
        super().__init__(parent)
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
        mode = 0b01
        size = 16
        cmd = (mode << 6) | size
        cmd_bytes = cmd.to_bytes(1, 'big')
        data_len = 8 + 512
        while self.running:
            try:
                self.ser.write(cmd_bytes)
                d = self.ser.read(data_len)
                if len(d) != data_len:
                    continue
                fsr = np.frombuffer(d[8:], dtype=np.uint16).reshape((16, 1, 16))
                fsr = np.concatenate((fsr[:8], np.flip(fsr[8:], axis=0)))
                fsr = fsr.transpose((2, 1, 0))  # shape (1, 16, 16)
                self.data_received.emit(fsr)
            except Exception as e:
                print("Serial read error:", e)
                self.running = False

    def stop(self):
        self.running = False
        self.wait()
        if hasattr(self, 'ser') and self.ser.is_open:
            self.ser.close()

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, serial_port, smooth=False, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Real-time 3D Plot")
        self.widget = gl.GLViewWidget()
        self.setCentralWidget(self.widget)
        self.widget.opts['distance'] = 40

        # tare setup
        self.tare_count = 0
        self.tare_sum = np.zeros((16,16), dtype=np.float64)
        self.tare_mean = None

        # initial flat mesh
        meshdata = self._make_mesh(np.zeros((16,16)))
        self.surface = GLMeshItem(
            meshdata=meshdata,
            smooth=smooth,
            drawEdges=not smooth,
            shader='shaded',
            color=(1,0,0,0.5)
        )
        self.widget.addItem(self.surface)

        self.serial_thread = SerialReader(serial_port)
        self.serial_thread.data_received.connect(self.update_data)
        self.serial_thread.start()

    def _make_mesh(self, fsr0):
        R = 8.0
        h_pts, w_pts = fsr0.shape
        angles = np.linspace(-np.pi/2, np.pi/2, w_pts)
        heights = np.linspace(-8.0, 8.0, h_pts)
        A, H = np.meshgrid(angles, heights)
        R2 = R + fsr0
        X = R2 * np.cos(A)
        Y = H
        Z = R2 * np.sin(A)

        verts = np.column_stack((X.ravel(), Y.ravel(), Z.ravel()))
        faces = []
        for i in range(h_pts - 1):
            for j in range(w_pts - 1):
                idx = i * w_pts + j
                faces += [
                    [idx, idx + 1, idx + w_pts],
                    [idx + 1, idx + w_pts + 1, idx + w_pts]
                ]
        faces = np.array(faces)
        return MeshData(vertexes=verts, faces=faces)

    def update_data(self, fsr):
        raw = fsr[:, 0, :].astype(np.float32)  # shape (16,16)
        if self.tare_mean is None:
            # accumulate tare
            if self.tare_count < 100:
                self.tare_sum += raw
                self.tare_count += 1
                if self.tare_count == 100:
                    self.tare_mean = self.tare_sum / 100.0
                    print("Tare complete")
                return
        # subtract tare and scale
        fsr0 = (raw - self.tare_mean) / 100.0
        meshdata = self._make_mesh(fsr0)
        self.surface.setMeshData(meshdata=meshdata)

    def closeEvent(self, event):
        self.serial_thread.stop()
        event.accept()

if __name__ == '__main__':
    if len(sys.argv) < 2 or len(sys.argv) > 3 or (len(sys.argv) == 3 and sys.argv[2] != 'smooth'):
        print(f"Usage:\n\t{sys.argv[0]} arduino_port [smooth]")
        sys.exit(1)
    port = sys.argv[1]
    smooth_flag = (len(sys.argv) == 3 and sys.argv[2] == 'smooth')
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow(port, smooth=smooth_flag)
    window.show()
    sys.exit(app.exec_())
