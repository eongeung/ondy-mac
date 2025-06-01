from PyQt5.QtWidgets import QApplication, QLabel, QWidget
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QTimer
import sys, random

class OndyWidget(QLabel):
    def __init__(self, parent, image_path):
        super().__init__(parent)
        pixmap = QPixmap(image_path).scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        if pixmap.isNull():
            print("image로드 실패")
        self.setPixmap(pixmap)
        self.resize(100, 100)
        self.dx = random.choice([-3, 3])
        self.dy = random.choice([-3, 3])
        self.move(random.randint(0, 500), random.randint(0, 300))
        self.show()

    def move_step(self, max_width, max_height):
        x, y = self.x() + self.dx, self.y() + self.dy
        if x < 0 or x + self.width() > max_width:
            self.dx *= -1
        if y < 0 or y + self.height() > max_height:
            self.dy *= -1
        self.move(self.x() + self.dx, self.y() + self.dy)

    def mouseDoubleClickEvent(self, event):
        self.deleteLater()

class TransparentOverlay(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setGeometry(100, 100, 800, 600)  # 일단 위치 보이게

        self.ondys = []
        self.add_ondy()  #시작하자마자 1마리 추가

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_ondys)
        self.timer.start(5)

        self.show()

    def add_ondy(self):
        ondy = OndyWidget(self, "ondy.png")
        self.ondys.append(ondy)

    def update_ondys(self):
        for ondy in self.ondys:
            ondy.move_step(self.width(), self.height())

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Q:
            self.close()
        elif event.key() == Qt.Key_O:
            self.add_ondy()

if __name__ == '__main__':
    print("Ondy 시작")
    app = QApplication(sys.argv)
    overlay = TransparentOverlay()
    sys.exit(app.exec_())
