import pyautogui as pt


# eye_x, eye_y = (1806, 487)

X = 1806
# Y = 487
Y = 520

pt.moveTo(X, Y, duration = 0.1)
color = pt.pixel(X, Y)

print(color)
