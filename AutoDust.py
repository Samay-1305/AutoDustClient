from time import sleep
from Additional.Connection import Client
from Additional.Interface import Control
from datetime.datetime import now as current_time

USE_PI_CAMERA = False
DEVICE_NAME = "AutoDust-01"
SERVER_HOST = ""
SERVER_PORT = 8080
IMAGE_FILE_PATH = "Additional/Images/AutoDustImage.jpg"
DISTANCE_THRESHOLD = 10

if USE_PI_CAMERA:
    from picamera import PiCamera
    camera = PiCamera()
    camera.start_preview()
else:
    import os
    WEBCAM_COMMAND = "fswebcam -r 1240x720-v -S 10 --set brightness=100% {}".format(IMAGE_FILE_PATH)

if __name__ == "__main__":
    controller = Control()

    conn = Client(DEVICE_NAME)
    conn.connect(SERVER_HOST, SERVER_PORT)

    sleep(1)

    running = True
    while running:
        try:
            controller.listen_for_change()

            sleep(0.5)

            if USE_PI_CAMERA:
                camera.capture(IMAGE_FILE_PATH)
            else:
                os.system(WEBCAM_COMMAND)

            print("{}: Image Captured".format(current_time().strftime("%d-%m-%Y %H:%M:%S")))
            
            conn.send_msg("IMG")
            conn.recv_msg(1)
            conn.send_file(IMAGE_FILE_PATH)

            print("{}: Image Sent".format(current_time().strftime("%d-%m-%Y %H:%M:%S")))
            
            motor_action = conn.recv_msg()
            
            print("{}: Motor Rotation Value {} initiated".format(current_time().strftime("%d-%m-%Y %H:%M:%S"), motor_action))
           
            gpio_success = controller.rotate(motor_action)
            if gpio_success == False:
                raise Exception("{}: GPIO Failure".format(current_time().strftime("%d-%m-%Y %H:%M:%S")))
            else:
                print("{}: Action Completed".format(current_time().strftime("%d-%m-%Y %H:%M:%S")))
            
            if controller.distance() <= DISTANCE_THRESHOLD:
                raise Exception("{}: Termination Initiated".format(current_time().strftime("%d-%m-%Y %H:%M:%S")))

        except Exception as CriticalError:
            print("{}: {}".format(current_time().strftime("%d-%m-%Y %H:%M:%S"), CriticalError))
            
            conn.send_msg("!END")
            
            controller.release()
            
            if USE_PI_CAMERA:
                camera.stop_preview()
            
            running = False
    
    print("{}: Program Terminated".format(current_time().strftime("%d-%m-%Y %H:%M:%S")))

