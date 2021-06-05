from PIL import Image


# width, height = im.size
# Setting the points for cropped image
left = 0
top = 30
right = 100
bottom = 100

for frame in range(0, 121):
    if frame < 10:
        num = "00" + str(frame)
    elif 9 < frame < 100:
        num = "0" + str(frame)
    else:
        num = str(frame)

    im = Image.open(r"/assets/robot/down/Robo7." + num + ".png")
    im1 = im.crop((left, top, right, bottom))

    im1.save("/assets/robot/down/resized/Robo7." + num + ".png")