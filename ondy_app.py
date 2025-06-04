import os
import math
import sys
import random
from PyQt5.QtWidgets import QApplication, QLabel, QWidget
from PyQt5.QtGui import QPixmap, QCursor
from PyQt5.QtCore import Qt, QTimer

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ICON_DIR = os.path.join(BASE_DIR, "ondyicon")

class OndyWidget(QLabel):
    def __init__(self, parent, image_path, x, y):
        super().__init__(parent)
        self.parent = parent  # 부모에서 ondy 리스트 접근용
        pixmap = QPixmap(image_path).scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.setPixmap(pixmap)
        self.resize(100, 100)
        self.move(x, y)
        self.show()

        speed = random.uniform(1.5, 4.5)
        angle = random.uniform(0, 360)
        radian = angle * math.pi / 180
        self.dx = speed * math.cos(radian)
        self.dy = speed * math.sin(radian)

    def move_step(self, max_width, max_height):
        # 마우스 위치 추적
        mouse_pos = QCursor.pos()
        parent_mouse_pos = self.parent.mapFromGlobal(mouse_pos)

        cx = self.x() + self.width() / 2
        cy = self.y() + self.height() / 2

        dx = parent_mouse_pos.x() - cx
        dy = parent_mouse_pos.y() - cy

        dist = math.hypot(dx, dy)
        if dist != 0:
            dx /= dist
            dy /= dist

        speed = min(max(dist / 20, 3), 10)
        self.dx = dx * speed
        self.dy = dy * speed

        # 온디끼리 너무 가까우면 반발력 추가
        for other in self.parent.ondys:
            if other is self:
                continue
            ox = other.x() + other.width() / 2
            oy = other.y() + other.height() / 2
            d = math.hypot(ox - cx, oy - cy)
            if d < 110 and d > 0:  # 너무 가까우면 반발력
                repel_strength = (110 - d) / 110  # 가까울수록 강하게
                rx = (cx - ox) / d
                ry = (cy - oy) / d
                self.dx += rx * repel_strength * 2
                self.dy += ry * repel_strength * 2

        # 이동
        new_x = self.x() + self.dx
        new_y = self.y() + self.dy

        if new_x < 0 or new_x + self.width() > max_width:
            self.dx *= -1
        if new_y < 0 or new_y + self.height() > max_height:
            self.dy *= -1

        if random.random() < 0.1:
            angle_change = random.uniform(-30, 30)
            speed = math.hypot(self.dx, self.dy)
            new_angle = math.atan2(self.dy, self.dx) + math.radians(angle_change)
            self.dx = speed * math.cos(new_angle)
            self.dy = speed * math.sin(new_angle)

        self.move(int(self.x() + self.dx), int(self.y() + self.dy))

    def mouseDoubleClickEvent(self, event):
        self.deleteLater()

class TransparentOverlay(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)

        screen = QApplication.primaryScreen().geometry()
        self.setGeometry(0, 0, screen.width(), screen.height())
        self.setFocusPolicy(Qt.StrongFocus)

        self.ondys = []
        self.icon_paths = [os.path.join(ICON_DIR, f"cat{str(i).zfill(2)}.png") for i in range(1, 10)]
        random.shuffle(self.icon_paths)
        self.icon_index = 0

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_ondys)
        self.timer.start(30)

        self.spawn_timer = QTimer()
        self.spawn_timer.timeout.connect(self.add_ondy)
        self.spawn_timer.start(1500)

        self.show()

    def add_ondy(self):
        if self.icon_index >= len(self.icon_paths):
            return

        width, height = 100, 100
        max_attempts = 100

        for _ in range(max_attempts):
            x = random.randint(0, self.width() - width)
            y = random.randint(0, self.height() - height)

            overlap = False
            for other in self.ondys:
                if (x < other.x() + other.width() and x + width > other.x() and
                    y < other.y() + other.height() and y + height > other.y()):
                    overlap = True
                    break

            if not overlap:
                image_path = self.icon_paths[self.icon_index]
                self.icon_index += 1
                ondy = OndyWidget(self, image_path, x, y)
                self.ondys.append(ondy)
                return

        print("겹치지 않는 위치 찾기 실패")

    def update_ondys(self):
        for ondy in self.ondys:
            ondy.move_step(self.width(), self.height())

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Q:
            self.close()
            QApplication.quit()
            sys.exit(0)

if __name__ == '__main__':
    print("Ondy 시작")
    app = QApplication(sys.argv)
    overlay = TransparentOverlay()
    sys.exit(app.exec_())
