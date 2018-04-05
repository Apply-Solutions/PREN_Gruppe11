# Documentation Chris

## Raspberry Pi

### Boot

#### Scripts
Gemäss Anforderungen muss der Raspberry Pi direkt nach Aufstarten startbereit sein. Deswegen ist es für uns wichtig, verschiedene Skripts nach dem Boot automatisch ausführen zu können (z.B. Starten des Bluetooth-Servers, automatischer Login als Root).

**Automatischer Login als User**:

1. User  `pi` erstellen und passwort definieren: `adduser pi`
2. Einstellungen auf "autologin" ändern über `raspi-config`

**Automatischer Login als Root**

// TODO


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
