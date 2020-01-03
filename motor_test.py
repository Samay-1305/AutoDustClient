from Additional.Interface import Control

controller = Control()

for direction in range(2):
    distance = controller.rotate(direction)
        
controller.release()
