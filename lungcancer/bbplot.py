from PyQt5 import QtGui, QtWidgets, QtCore
from typing import List, Dict

from bbutil import BB, BBCollections

class BBView(QtWidgets.QWidget):
    sliceChanged = QtCore.pyqtSignal(str, str)
    def __init__(self, bb_gt: BBCollections, bb_pred: BBCollections):
        super().__init__()
        self.bb_gt = bb_gt
        self.bb_pred = bb_pred
        self.confidence_min = 0.3
        self._slice = ''
        self.patients = sorted(bb_gt.keys())
        self.set_patient(self.patients[0])
        self.setFocus()

    def set_patient(self, patient: str):
        if not patient in self.bb_gt:
            raise ValueError(f'Invalid patient{patient}')
        self.patient = patient
        self.slices = sorted(self.bb_gt[self.patient].keys())
        self.slice = self.slices[0]
        self.repaint()
        self.sliceChanged.emit(self.patient, self.slice)

    def next_patient(self):
        i = self.patients.index(self.patient)
        if i == len(self.patients) - 1:
            return False
        patient = self.patients[i+1]
        self.set_patient(patient)
        return True

    def prev_patient(self):
        i = self.patients.index(self.patient)
        if i == 0:
            return False
        patient = self.patients[i-1]
        self.set_patient(patient)
        return True

    def next_slice(self) -> bool:
        i = self.slices.index(self.slice)
        if i == len(self.slices) - 1:
            if not self.next_patient():
                return False
            self.slice = self.slices[0]
        else:
            self.slice = self.slices[i+1]
            self.repaint()
        self.sliceChanged.emit(self.patient, self.slice)
        return True

    def prev_slice(self) -> bool:
        i = self.slices.index(self.slice)
        if i == 0:
            if not self.prev_patient():
                return False
            self.slice = self.slices[-1]
        else:
            self.slice = self.slices[i-1]
            self.repaint()
        self.sliceChanged.emit(self.patient, self.slice)
        return True

    def xformPoint(self, x, y):
        x = x * self.scalex + self.transx
        y = y * self.scaley + self.transy
        return (x, y)

    def xformRect(self, x, y, w, h):
        x, y = self.xformPoint(x, y)
        w = w * self.scalex
        h = h * self.scaley
        return x, y, w, h

    def setup_view(self):
        margin = 40
        ww = self.width()
        wh = self.height()
        # (0, 0) -> (margin, wh - margin) (left, bottom)
        # (1, 1) -> (ww - margin, margin) (right, top)
        # x = margin + x * (ww - margin)
        # y = wh - margin - y * (wh - 2*margin)
        self.scalex = ww - margin
        self.scaley = -(wh - 2*margin)
        self.transx = margin
        self.transy = wh - margin

    def paintEvent(self, ev: QtGui.QPaintEvent) -> None:
        print('paintEvent')
        self.setup_view()
        qp = QtGui.QPainter()
        qp.begin(self)
        self.drawXY(qp)
        qp.end()

    def drawXY(self, qp: QtGui.QPainter):
        gt_slice = self.bb_gt[self.patient][self.slice]
        pred_slice = self.bb_pred[self.patient][self.slice]
        print(self.patient, self.slice, gt_slice, pred_slice)
        # gt color
        color = QtGui.QColor(255, 0, 0)
        pen = QtGui.QPen(color, 3, QtCore.Qt.SolidLine)
        qp.setPen(pen)
        for bb in gt_slice:
            if bb.klass == 1:
                pen.setStyle(QtCore.Qt.SolidLine)
            else:
                pen.setStyle(QtCore.Qt.DashLine)
            qp.setPen(pen)
            x = bb.x - bb.w/2
            y = bb.y + bb.h/2
            x, y, w, h = self.xformRect(x, y, bb.w, bb.h)
            print('gt', x,y,w,h)
            qp.drawRect(x, y, w, h)

        color = QtGui.QColor(0, 255, 0)
        pen.setColor(color)
        qp.setPen(pen)
        for bb in pred_slice:
            if bb.confidence < self.confidence_min:
                continue
            if bb.klass == 1:
                pen.setStyle(QtCore.Qt.SolidLine)
            else:
                pen.setStyle(QtCore.Qt.DashLine)
            x = bb.x - bb.w/2
            y = bb.y + bb.h/2
            x, y, w, h = self.xformRect(x, y, bb.w, bb.h)
            print('pred', x,y,w,h)
            qp.drawRect(x, y, w, h)

    def drawYZ(self):
        pass

    def mousePressEvent(self, ev: QtGui.QMouseEvent) -> None:
        pass

    def keyPressEvent(self, ev: QtGui.QKeyEvent) -> None:
        print('keyPress', ev)

class Window(QtWidgets.QMainWindow):
    def __init__(self, bb_gt: BBCollections, bb_pred: BBCollections):
        super().__init__()
        self.bb_gt = bb_gt
        self.bb_pred = bb_pred
        self.setWindowTitle('PET/CT')
        self.setGeometry(50, 50, 1024, 768)
        w = QtWidgets.QWidget()
        hbox = QtWidgets.QHBoxLayout()
        w.setLayout(hbox)
        vbox = QtWidgets.QVBoxLayout()
        hbox.addLayout(vbox)
        self.makeSelectorBox(vbox)
        self.bb_view = BBView(bb_gt, bb_pred)
        self.bb_view.sliceChanged.connect(self.slice_changed)
        vbox.addWidget(self.bb_view)
        self.setCentralWidget(w)
        self.makeDetail(hbox)

    def makeDetail(self, hbox: QtWidgets.QHBoxLayout):
        pass

    def slice_changed(self, patient: str, slice: str):
        print('slice_changed', patient, slice)
        self.slice.setText(f'slice-{slice}')
        i = self.patients.index(patient)
        self.patient.setCurrentIndex(i)
        # self.patient.setText(f'Patient({patient})')

    def makeSelectorBox(self, vbox: QtWidgets.QVBoxLayout):
        hbox = QtWidgets.QHBoxLayout()
        vbox.addLayout(hbox, stretch=0)

        left_box = QtWidgets.QPushButton('<')
        left_box.setMaximumWidth(50)
        label = QtWidgets.QLabel('Patient:')

        self.patient = QtWidgets.QComboBox()
        self.patients = sorted(self.bb_gt.keys())
        for patient_name in self.patients:
            self.patient.addItem(patient_name)
        def select_cb(i):
            self.bb_view.set_patient(self.patients[i])
        self.patient.currentIndexChanged.connect(select_cb)
        right_box = QtWidgets.QPushButton('>')
        right_box.setMaximumWidth(50)
        hbox.addWidget(left_box)
        hbox.addWidget(label)
        hbox.addWidget(self.patient, stretch=1)
        hbox.addWidget(right_box)
        left_box.clicked.connect(lambda : self.bb_view.prev_patient())
        right_box.clicked.connect(lambda : self.bb_view.next_patient())

        spacer = QtWidgets.QSpacerItem(100, -1, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        hbox.addItem(spacer)

        self.slice = QtWidgets.QLabel()
        left_box = QtWidgets.QPushButton('<')
        left_box.setMaximumWidth(50)
        right_box = QtWidgets.QPushButton('>')
        right_box.setMaximumWidth(50)
        hbox.addWidget(left_box)
        hbox.addWidget(self.slice, stretch=1)
        hbox.addWidget(right_box)
        left_box.clicked.connect(lambda : self.bb_view.prev_slice())
        right_box.clicked.connect(lambda : self.bb_view.next_slice())

        count = hbox.count()
        for i in range(count):
            child = hbox.itemAt(i)
            if isinstance(child, QtWidgets.QWidgetItem):
                child: QtWidgets.QWidgetItem
                child.widget().setFocusPolicy(QtCore.Qt.NoFocus)
            print(child)

    def keyPressEvent(self, ev: QtGui.QKeyEvent) -> None:
        print('keyPress', ev)
        if ev.key() == QtCore.Qt.Key_Left:
            self.bb_view.prev_slice()
        elif ev.key() == QtCore.Qt.Key_Right:
            self.bb_view.next_slice()

def plot(bb_gt, bb_pred):
    import sys
    app = QtWidgets.QApplication(sys.argv)
    win = Window(bb_gt, bb_pred)
    win.show()
    sys.exit(app.exec())