# Documentation Chris

## Raspberry Pi

### Boot

#### Scripts
Gemäss Anforderungen muss der Raspberry Pi direkt nach Aufstarten startbereit sein. Deswegen ist es für uns wichtig, verschiedene Skripts nach dem Boot automatisch ausführen zu können (z.B. Starten des Bluetooth-Servers, automatischer Login als Root).

**Automatischer Login als User**:

1. User  `pi` erstellen und passwort definieren: `adduser pi`
2. Einstellungen auf "autologin" ändern über `raspi-config`

**Automatischer Login als Root**

Wie bereits erwähnt wollen wir uns als root einloggen oder zumindest als einen User der root-Rechte besitzt. Um sich direkt als root einzuloggen muss folgende Einstellung im `raspi-config` des Raspberry Pi's eingestellt sein:




#### Timing
Wir haben zwei verschiedene Betriebssysteme ausprobiert und beobachteten die Boot-Zeiten beider Systeme auf separaten Raspberries. Die beiden OS heissen **Minibian** und **Rasbian**. Folgende Ergebnisse haben wir ermittelt:

* Time-To-Boot, Raspberry 1, Minibian: 20s
* Time-To-Reboot, Raspberry 1, Minibian: 23s

Wir müssen in einem weiteren Schritt die Messungen durchführen mit Boot und automatischer Ausführung vom Server-Start.



### Wifi

Die Wifi-Einstellungen behandeln wir in der `wpa_cli`-Console. Folgende Befehle im root des Raspberries sind hierfür relevant:

```shell
# wpa_supplicant mit WiFi-Einstellungen erstellen

nano /etc/wpa_supplicant/wpa_supplicant.conf`

network={
        ssid=""
        psk=""
}

wpa_cli -i wlan0 reconfigure
```

## Python

### Threading

Da wir Tasks simultan auf der Raspberry Pi laufen lassen müssen, verwenden wir Threads, um dies sinnvoll umzusetzen. Wir könnten mit Prozessen arbeiten, um die vier Cores des Raspberry Pi's auszunutzen. In unserem Projekt beschränken wir uns jedoch rein auf Threads und verzichten auf richtiges Multithreading.

Weiter unten ist ein konkretes Beispiel und als weitere Lektüre verwenden wir: 

* O'reilly - Programmin Python - Mark Lutz
* https://www.tutorialspoint.com/python/python_multithreading.htm

*Source: Learn Raspberry Pi Programming With Python*

```python
# Define thread object

class myObject(threading.Thread):
	def __init__(self):
 		#function used to initiate the class and thread
 		threading.Thread.__init__(self) #necessary to start the thread
 	def run(self):
 		#function performed while thread is running
```

## Stepper

### Beschleunigung
Wir haben nach einem Test der Aufhängung am Stahldraht bemerkt, dass der Stepper nicht beschleunigt und zu ruckartig vorwärtsbewegt. Deswegen haben wir eine Beschleunigung eingebaut. Da die Schritte des Schrittmotors immer in einem Interval von zwei Delays (HIGH, LOW) funktionieren verwenden wir eine Exponentialfunktion, welche den Delay zwischen HIGH und LOW immer stärker reduziert. Der x-Wert beginnt vorläufig bei `x=5` und wird beendet wenn der y-Wert `y = 0.0005` erreicht hat. Der x-Wert wird vorläufig immer um 0.02 inkrementiert (nach Tests).

> $$y = e^{-x} + 0.0005$$


## Startposition

### Plan A: Genaue Platzierung
Unsere Idee ist es die Lauftkatze immer gleich am Start zu Positionieren. So kennen wir zu Beginn den Nullpunkt.

Wir messen die Position der Laufkatze, die sich auf Höhe des hinteren Rades befindet, und die Position des Elektromagneten, da sich die Last auf dieser Höhe befinden wird. Die Startposition des Elektromagneten kennen wir sobald wir die Position zum ersten Masten kennen (

> $\text{Startposition} = 0mm$<br>
> $\text{Position Last} = \text{Startposition} + 110mm$

### Plan B: Distanzmessung
Unser Backupplan ist die Distanz zum hinteren Masten zu messen und so die Startposition der Laufkatze zu definieren.

## Position bei Fortbewegung