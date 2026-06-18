import cv2
def show_cutscene():
    img = cv2.imread("tiles/title.png")
    img[-100:] = 0  # last 100 pixel rows are black
    img = cv2.putText(
    img,
    "Press any key to start",
    org=(15, 490),  # x/y position of the text
    fontFace=cv2.FONT_HERSHEY_SIMPLEX,
    fontScale=1,
    color=(255, 255, 255),  # white
    thickness=2,
)
    cv2.imshow("Cutscene", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    