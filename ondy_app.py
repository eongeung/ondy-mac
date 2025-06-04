import os
from PyQt5.QtWidgets import QApplication, QLabel, QWidget
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QTimer
import sys, random

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ICON_DIR = os.path.join(BASE_DIR, "ondyicon")

class OndyWidget(QLabel):
    def __init__(self, parent, image_path):
        super().__init__(parent)
        pixmap = QPixmap(image_path).scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        if pixmap.isNull():
            print(f"이미지 로드 실패: {image_path}")
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
        self.setGeometry(100, 100, 800, 600)

        self.ondys = []

        # ✅ 1. 이미지 목록 준비
        self.icon_paths = [os.path.join(ICON_DIR, f"cat{str(i).zfill(2)}.png") for i in range(1, 10)]
        random.shuffle(self.icon_paths)  # ✅ 순서를 무작위로 섞음
        self.icon_index = 0  # 현재까지 생성한 인덱스

        self.add_ondy()

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_ondys)
        self.timer.start(30)

        self.spawn_timer = QTimer()
        self.spawn_timer.timeout.connect(self.add_ondy)
        self.spawn_timer.start(1500)

        self.show()

    def add_ondy(self):
        # ✅ 2. 9마리 넘으면 생성 안함
        if self.icon_index >= len(self.icon_paths):
            return

        image_path = self.icon_paths[self.icon_index]
        self.icon_index += 1

        ondy = OndyWidget(self, image_path)
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
