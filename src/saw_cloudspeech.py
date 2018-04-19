#!/usr/bin/env python3

import aiy.audio
import aiy.cloudspeech
import aiy.voicehat
import http.client
import subprocess

import time

def checkWait(wait_count, max_wait, wait_toButtonMode_count, max_waitToButtonMode, mode_button, voice_warning, warning_msg):
    
    if mode_button == False:
         wait_count += 1
         wait_toButtonMode_count += 1

    if(wait_count > max_wait):
         if voice_warning == True :
             sent_Post(warning_msg)
         print("Resetting wait count, you should hear a message warning")
         wait_count = 0

    if wait_toButtonMode_count > max_waitToButtonMode:
         wait_toButtonMode_count = 0
         mode_button = True
         sent_Post("I haven't heard from you. Defaulting to button trigger mode") 
    return wait_count, wait_toButtonMode_count, mode_button

def main():
    recognizer = aiy.cloudspeech.get_recognizer()
    recognizer.expect_phrase('reset')    
    recognizer.expect_phrase('new object')    
    recognizer.expect_phrase('new place')    
    recognizer.expect_phrase('execute now')    

    voice_warning = True
    mode_button= True 
    msg_long = False
    max_wait = 3
    max_waitToButtonMode = 10
    wait_toButtonMode_count = 0;
    wait_count = 0;    
    
    warning_msg = "I haven't heard from you for a while. \
                Please disable free voice if not in use. You can say: set free voice mode off. To disable this warning say\
                : set voice warning off"
 
    button = aiy.voicehat.get_button()
    led = aiy.voicehat.get_led()
    aiy.audio.get_recorder().start()
    
    start_time = time.time()
    
    if msg_long == True:
        sent_Post("Hello. Voice system is on. Press the button to speak. To disable button mode, \
        You can say: set free voice mode on. To disable free voice and enable button press mode, \
        you can say: set free voice mode off. To talk in free voice mode say: ok Tibby." )
    else:
        print("Hello. Voice system is on. Press the button to speak.")
    while True:
        if mode_button:
            print('\nReady. Press the button and speak')
        else :
            print('Say keyword and speak')

    
        if mode_button:
            wait_count = 0;
            wait_toButtonMode_count = 0;
            button.wait_for_press()
            print('Button was pressed...')
        
        if aiy.audio.get_recorder()._closed:
           print('Recorder was closed. Starting again...')
           aiy.audio.get_recorder().stop()
           aiy.audio.get_recorder().start()
        else: print('Recorder is on.')

        text = recognizer.recognize(immediate=True)
        print ('Recognized:', text)

        if text is None:
            print('Sorry, I did not hear you.')
            wait_count, wait_toButtonMode_count, mode_button = checkWait(wait_count, max_wait, wait_toButtonMode_count,\
                                                                max_waitToButtonMode, mode_button, voice_warning, warning_msg )
        elif mode_button:
            sent_Post(text)
        else:
            print('You said "', text, '"')
           
          
        wait_count, wait_toButtonMode_count, mode_button = checkWait(wait_count, max_wait, wait_toButtonMode_count,\
                                                                   max_waitToButtonMode,  mode_button, voice_warning,\
                                                                   warning_msg)
                                              
def sent_Post(msg):
    c = http.client.HTTPConnection('localhost', 8081)
    c.request('POST', '/process', '{"msg":"'+ msg.strip() +'"}')
    doc = c.getresponse().read()


if __name__ == '__main__':
    main()
