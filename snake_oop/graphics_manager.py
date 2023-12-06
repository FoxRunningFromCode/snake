import cv2
import os
import time

#Handles the graphics screens shown at the start and end of game plus inbetween.
class snakegraphics():
    def show_start_screen():
        
        # Get the directory of the script
        script_directory = os.path.dirname(__file__)
        
        # Construct the full file path
        file_path = os.path.join(script_directory, 'front.png')
        
        print(file_path)
        image_path = file_path
        # Read the image
        image = cv2.imread(image_path)

        if image is None:
            print("Error: Unable to read the image.")
            return

        # Display the image
        cv2.imshow('Image', image)

        # Wait for a key press
        key = cv2.waitKey(0)

        # Check if the key pressed is the ESC key (27 is the ASCII code for ESC)
        if key == ord('f'):
            cv2.destroyAllWindows()  # Close the window if ESC is pressed
            
    def show_inbetween_level(level, delay):
        cv2.destroyAllWindows()
        # Get the directory of the script
        script_directory = os.path.dirname(__file__)
        
        # Construct the full file path
        file_path = os.path.join(script_directory, 'blank.png')
        
        
        image_path = file_path
        # Read the image
        image2 = cv2.imread(image_path)
        
        text = str(level)
        org = (380,300)
        color = (1.0,1.0,1.0)
        
        #add the level data to the blank screen
        cv2.putText(image2,text,org,cv2.FONT_HERSHEY_COMPLEX,2,color,2)
        
        cv2.imshow('Image', image2)
        key = cv2.waitKey(1)
        time.sleep(delay)
        cv2.destroyAllWindows()
        

    def show_ending(ending, delay):
        
        if ending == 'win':
            file = 'win.png'
        if ending == 'lost':
            file = 'lost.png'
        if ending == 'bye':
            file = 'bye.png'
        
        
        cv2.destroyAllWindows()
        # Get the directory of the script
        script_directory = os.path.dirname(__file__)
        
        # Construct the full file path
        file_path = os.path.join(script_directory, file)
        
        image_path = file_path
        # Read the image
        image2 = cv2.imread(image_path)
        
        cv2.imshow('Image', image2)
        key = cv2.waitKey(1)
        time.sleep(delay)
        cv2.destroyAllWindows()


    
    
    