# Grove Electromagnet

## Masse


Grösse:	89 x 140 x 18.8 <br>
Working Voltage：DC 5V <br>
Working Current: 400mA <br>
Standby Current：  200uA <br>
Load Weight： 1kg <br>
Peak Suction: 1kg 

Quelle: http://wiki.seeed.cc/Grove-Electromagnet/

## Eigenschaften

Um die Last (Würfel) aufheben zu können, verwenden wir den Grove Electromagnet und den magnetischen Haken der Last. Der Elektromagnet eignet sich besser als einen normalen Magneten, da wir die Last auf das Zielfeld wieder abwerfen können indem wir das Magnetfeld entfernen. Das Magnetfeld wir durch elektrischen Strom erzeugt.

## Ansteuerung

Da der Elektromagnet nicht direkt ansprechbar ist mit einem Raspberry Pi, werden wir dazu gezwungen die Ansteuerung über einen GrovePi machen. Darauf sind wir nach einem gescheiterten Test gekommen bei dem wir verschiedene Skripts vom Raspberry Pi ausgeführt haben und keiner funktioniert hat. Eines dieser Python-Skripts sieht folgendermassen aus:

```python
# Libraries
import RPi.GPIO as GPIO
import time

# GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BOARD)

# set GPIO Pins
GPIO_TRIGGER = 12

# set GPIO direction (IN / OUT)
PGIO.setup(GPIO_TRIGGER, PGIO.OUT)

def magnet():
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, GPIO.HIGH)

    print("On")

    time.sleep(5000)
    GPIO.output(GPIO_TRIGGER, GPIO.LOW)

    print("Off")

if __name__ == '__main__':
  try:
      while True:
          print("sucking...")
  except KeyboardInterrupt:
      GPIO.cleanup()
```

Bevor wir uns definitiv auf ein GrovePi einigen, werden einige weitere Skripts getestet.

## Testing

Um zu wissen wie konsistent und verlässlich die Senosren messen, werden wir Testfälle dazu erstellen. Für den Elektromagneten haben wir jedoch noch keine konkreten Testfälle erstellt.
