# Raspberry Pi Update

## Masse

Working Voltage：DC 5V <br>
Working Current： 400mA <br>
Standby current： 200uA <br>
Load Weight： 1kg <br>
Gewicht: 40g <br>
Grösse: 85 x 56 x 17

## Steuerung

Wir haben das Raspberry Pi mit dem Betriebssystem Minibian aufgesetzt. Dieses abgespeckte OS verfügt **nur** über die von uns installierten Packages und Libraries. Somit sparen wir viel Platz und durch den Verzicht auf ein GUI viel Leistung. Um die einzelnen Sensoren und Motoren anzusteuern, nutzen wir die GPIO I/O der Raspberry Pi (siehe Abbildung).

<img src="https://docs.microsoft.com/en-us/windows/iot-core/media/pinmappingsrpi/rp2_pinout.png">

Um die Bilderkennung zu ermöglichen wird zudem der für die RaspiCam zur Verfügung gestellter IN genutzt.


