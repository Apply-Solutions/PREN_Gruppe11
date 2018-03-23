# Notes ET

23.03.18

## Stepper

### Geschwindigkeit

Im Code des StepperV (V für vertikal) definieren wir zwischen GPIO.HIGH und GPIO.LOW immer ein Delay von .005 s.

$\text{delay} = 0.005s$
$\text{delay per period} = 2 * delay = .01s = 10ms$

Da wir wissen, dass der Stepper in einer Periode 1.8° wandert lässt sich die Zeit pro ganze Umdrehung wie folgt berechnen:

