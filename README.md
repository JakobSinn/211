# Einhüllende Vermessen
Ein Tool, welches in python die Einhüllende eines Signals vermisst. Für das Plotten (was aber auch auskommentiert werden kann) muss _plotnine_ installiert sein, siehe plotnine.org . Erstellt für PAP-Versuch 211 an der Uni Heidelberg, 2024

Zur benutzung: An die Funktion werden zeit-arry, signal-array, ein string a la "Mittlere Kupplung, linkes Pendel" und eine schätzung der Breite eines Bauches in der Einhuellenden in sekunden eingegeben. Ich empfehle, die funktion einmal ohne solch eine schätzung ablaufen zu lassen - auf dem plot kann dann, wenn der fit noch nicht passt, eine Schätzung abgelesen werden. Die frequenzen werden zur Zeit noch in rotationen/s, nicht rad/s, ausgegeben (zumindest auf dem plot). 
