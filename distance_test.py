from Additional.Interface import Control

controller = Control()

base_distance = 10

running = True
while running:
    distance = controller.distance()
    print(distance)
    if distance < base_distance:
        running = False
        
controller.release()