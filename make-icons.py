"""아이콘 에셋 생성기 — 로고 색·모양을 바꾸면 이 스크립트를 다시 돌린다.

    python make-icons.py

헤더 로고(.blob, index.html)와 같은 도형을 그려 favicon / 홈화면 아이콘을 만든다.
생성물: favicon.ico, favicon-96.png, icon.svg,
        apple-touch-icon.png, icon-192.png, icon-512.png
"""
from PIL import Image, ImageDraw

PURPLE = (124, 108, 255, 255)   # --down  #7c6cff
PINK   = (255, 214, 228, 255)   # 로고 안쪽 점 #ffd6e4
CREAM  = (251, 245, 238, 255)   # --bg    #fbf5ee
TRANSPARENT = (0, 0, 0, 0)

DOT_RATIO = 14 / 38   # 헤더 .blob 의 안쪽 점 / 바깥 원 비율
SS = 8                # 슈퍼샘플링 배율 (가장자리 계단 제거)


def render(size, bg, circle_frac):
    """circle_frac: 바깥 보라 원의 지름 / 캔버스 변 길이"""
    s = size * SS
    img = Image.new("RGBA", (s, s), bg)
    d = ImageDraw.Draw(img)
    c = s / 2
    r_out = s * circle_frac / 2
    r_dot = r_out * DOT_RATIO
    d.ellipse([c - r_out, c - r_out, c + r_out, c + r_out], fill=PURPLE)
    d.ellipse([c - r_dot, c - r_dot, c + r_dot, c + r_dot], fill=PINK)
    return img.resize((size, size), Image.LANCZOS)


# 파비콘 — 배경 투명, 원이 캔버스를 꽉 채운다
render(96, TRANSPARENT, 1.0).save("favicon-96.png", optimize=True)
render(256, TRANSPARENT, 1.0).save("favicon.ico", sizes=[(16, 16), (32, 32), (48, 48)])

# 홈 화면·바로가기 타일 — 불투명 배경 필수(투명하면 iOS 가 검게 채운다).
# 원은 72% 로 두어 안드로이드 마스커블 안전영역(80%) 안에 들어가게 한다.
render(180, CREAM, 0.72).save("apple-touch-icon.png", optimize=True)
render(192, CREAM, 0.72).save("icon-192.png", optimize=True)
render(512, CREAM, 0.72).save("icon-512.png", optimize=True)

# SVG — 탭에서 어느 배율에도 선명하게
with open("icon.svg", "w", encoding="utf-8", newline="") as f:
    f.write(
        "<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'>"
        "<circle cx='16' cy='16' r='16' fill='#7c6cff'/>"
        "<circle cx='16' cy='16' r='5.9' fill='#ffd6e4'/>"
        "</svg>\n"
    )

print("아이콘 생성 완료")
