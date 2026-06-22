import cv2
def show_cutscene():
    img = cv2.imread("tiles/title.png")
    img[-100:] = 0  # last 100 pixel rows are black
    img = cv2.putText(
    img,
    "The dungeon has many riches, and many dangers",
    org=(15, 490),  # x/y position of the text
    fontFace=cv2.FONT_HERSHEY_SIMPLEX,
    fontScale=0.8,
    color=(255, 255, 255),  # white
    thickness=2,
)
    img = cv2.putText(
    img,
    "Enter if you dare",
    org=(15, 530),  # x/y position of the text
    fontFace=cv2.FONT_HERSHEY_SIMPLEX,
    fontScale=0.8,
    color=(255, 255, 255),  # white
    thickness=2,
)
    cv2.imshow("Cutscene", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def show_victory():
    img = cv2.imread("tiles/victory_scene1.png")
    img[-100:] = 0  # last 100 pixel rows are black
    img = cv2.putText(
    img,
    "You extracted with your treasure!",
    org=(15, 490),  # x/y position of the text
    fontFace=cv2.FONT_HERSHEY_SIMPLEX,
    fontScale=1,
    color=(255, 255, 255),  # white
    thickness=2,
)
    cv2.imshow("Cutscene", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    