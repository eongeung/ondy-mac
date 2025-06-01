#pip install opencv-python numpy로 설치하세요.
import cv2
import numpy as np
import random

#온디 클래스
class Ondy:
    def __init__(self, img, x, y):
        self.img = img
        self.x = x
        self.y = y
        self.dx = random.choice([-1, 1]) * random.randint(1, 3)
        self.dy = random.choice([-1, 1]) * random.randint(1, 3)

    def move(self, frame_shape):
        h, w = frame_shape[:2]
        self.x += self.dx
        self.y += self.dy
        if self.x < 0 or self.x + self.img.shape[1] > w:
            self.dx *= -1
        if self.y < 0 or self.y + self.img.shape[0] > h:
            self.dy *= -1

    def draw(self, frame):
        h, w = self.img.shape[:2]
        frame[self.y:self.y+h, self.x:self.x+w] = self.img

    def contains(self, px, py):
        return self.x <= px <= self.x + self.img.shape[1] and self.y <= py <= self.y + self.img.shape[0]

# 초기 설정
ondys = []
click_count = {}

def add_ondy():
    ondy = Ondy(ondy_img.copy(), random.randint(0, 400), random.randint(0, 400))
    ondys.append(ondy)

def mouse_callback(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        for ondy in ondys[:]:
            if ondy.contains(x, y):
                ondys.remove(ondy)
                break
            
ondy_img = cv2.imread("ondy.png")  # 또는 작은 캐릭터 이미지

cv2.namedWindow("Ondy App")
cv2.setMouseCallback("Ondy App", mouse_callback)

while True:
    frame = 255 * np.ones((600, 800, 3), dtype=np.uint8)  # 흰 배경

    for ondy in ondys:
        ondy.move(frame.shape)
        ondy.draw(frame)

    cv2.imshow("Ondy App", frame)

    key = cv2.waitKey(50)
    if key == ord('q'):
        break
    elif key == ord('o'):  # 'o' 키를 누르면 온디 추가
        add_ondy()

cv2.destroyAllWindows()
