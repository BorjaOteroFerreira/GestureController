import  gestures.GestureController as Gc
import gestures.HandsTogether as Ht 
import gestures.OpenHand as Oh 
import gestures.OpenMouth as Om
import gestures.HeadTilt as Het 

# Template to Monkey Ball Gc (Dolphin Emulator)

OPEN_MOUTH = 'c'        #LAUNCH ITEMS
HANDS_TOGHETTER = 'v'   #SWAP CHARACTERS
OPEN_LEFT_HAND = 'x'    #ACELERATE
OPEN_RIGHT_HAND = 'z'   #BACK
HEAD_LEFT = 'a'         #TURN LEFT (PAD)
HEAD_RIGHT = 'd'        #TURN RIGHT (PAD)


# Initialize the gesture controller

controller = Gc.GestureController()
controller.add_gesture(Om.OpenMouth(OPEN_MOUTH))
controller.add_gesture(Ht.HandsTogether(HANDS_TOGHETTER))
controller.add_gesture(Oh.OpenHand(OPEN_LEFT_HAND,OPEN_RIGHT_HAND))
controller.add_gesture(Het.HeadTilt(HEAD_LEFT, HEAD_RIGHT))

#Run gesture controller
controller.run()
