#!/usr/bin/env python3

import aiy.audio
import aiy.cloudspeech
import aiy.voicehat
import http.client
import Pyro4

def main():
    recognizer = aiy.cloudspeech.get_recognizer()
    recognizer.expect_phrase('turn off the light')
    recognizer.expect_phrase('turn on the light')
    recognizer.expect_phrase('blink')

    button = aiy.voicehat.get_button()
    led = aiy.voicehat.get_led()
    aiy.audio.get_recorder().start()

    while True:
        print('Press the button and speak')
        button.wait_for_press()
        print('Listening...')
        text = recognizer.recognize()
        if text is None:
            print('Sorry, I did not hear you.')
        else:
            print('You said "', text, '"')
            sent_Post(text)
            if 'turn on the light' in text:
                led.set_state(aiy.voicehat.LED.ON)
            elif 'turn off the light' in text:
                led.set_state(aiy.voicehat.LED.OFF)
            elif 'blink' in text:
                led.set_state(aiy.voicehat.LED.BLINK)
            elif 'new object' in text:
                sent_Post(text)
            elif 'mini switch' in text:
                sent_Post(text)
            elif 'robot' in text:
                sent_Post(text)
            elif 'goodbye' in text:
                break



def sent_Post(msg):
    greeting_maker = Pyro4.Proxy("PYRONAME:example.greeting")    # 
    print(greeting_maker.do_msg(msg))

    
if __name__ == '__main__':
    greeting_maker = Pyro4.Proxy("PYRONAME:example.greeting")
    main()
