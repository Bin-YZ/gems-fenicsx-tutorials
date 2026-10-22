# Von GEMS-Selektor zum Rezept

Das chemische System wird in **GEMS-Selektor** definiert, wo Datenbank, Phasen und Lösungsmodelle liegen. Der Code liest nur die exportierten
**GEMS3K-Dateien**. Ein neuer Fall braucht:

1. das System in GEMS-Selektor aufsetzen und ein Testgleichgewicht rechnen;
2. es als GEMS3K-Eingabedateien exportieren;
3. seine Gesamtzusammensetzung in ein Rezept `initial` (und `inlet`) für `case.yaml` umwandeln.

## 1–2. Die GEMS3K-Dateien exportieren

Berechnen Sie in GEMS-Selektor das Gleichgewicht Ihres Materials und exportieren Sie das System als GEMS3K-Eingabedateien im **JSON**- oder
**Text**format (Binär wird vom Browser-Inspector nicht unterstützt). Der Export liefert vier Dateien; legen Sie sie neben `case.yaml`:

```text
my_case/
├── case.yaml
└── chemistry_data/
    ├── mysys-dat.lst          ← chemistry.project zeigt hierher
    ├── mysys-dch.json         chemische Daten
    ├── mysys-ipm.json         Lösereinstellungen
    └── mysys-dbr-0-0000.json  der exportierte Zustand
```

Die `.lst`-Datei listet nur die drei anderen auf, z. B. `-j "mysys-dch.json" "mysys-ipm.json" "mysys-dbr-0-0000.json"`. Die vier Dateien
zusammen lassen; beim Umbenennen auch die `.lst` anpassen.

Vor dem Schreiben der YAML die Namen im Export prüfen: den Ordner im [GEMS Chemistry Inspector](../tools/inspector.md) öffnen oder die erste
Codezelle von [Tutorial 2](../tutorials/02_single_equilibrium.ipynb) ausführen.

Jede Phase aufnehmen, die sich während des Laufs bilden kann, etwa Sekundärminerale. Soll ein Element später über den Rand hinzukommen, muss es im System
vorhanden sein. Dazu im Rezept eine Spurenmenge angeben.

## 3. Gesamtzusammensetzung → Rezept

Die exportierte DBR-Datei enthält die Elementmengen (`bIC`) des berechneten Systems in mol für **dieses** System. Ein Rezept muss sich auf **1 dm³
Gesamtmaterial** mit der richtigen Menge Porenwasser beziehen. Hat das exportierte System $V_w$ dm³ Lösung und soll die Porosität φ sein, werden alle
Mengen skaliert mit

$$
f = \frac{\phi}{V_w}
$$

Danach prüfen, dass das skalierte Feststoffvolumen plus φ höchstens 1 dm³ beträgt. Der Rest des dm³ ist inertes Material.

Dieses Skript skaliert und gibt YAML zum Einfügen aus:

```{literalinclude} ../../tools/recipe_from_dbr.py
:language: python
```

Für das Standardprojekt und φ = 0,5:

```text
$ python recipe_from_dbr.py chemistry_data/b_time0-dat.lst 0.5
# stored system: 0.5012 dm3 solution, 0.0482 dm3 other phases, pH 12.47
# scaled by 0.99752: solids take 0.048 of 1 dm3 bulk (phi + solids must be <= 1)
initial:
  Ca: 1.11644400166
  Cl: 1e-15
  H: 58.3771472977
  O: 30.9235097918
  Si: 0.309345822605
```

Die Calcitsäule aus Tutorial 5 wurde genauso erstellt: 1 L calcitgesättigte Lösung, skaliert mit 0,31906, sodass 1 dm³ Gesamtmaterial 0,32 dm³
Porenwasser enthält.

Zwei Hinweise:

- In einem **Zement**rezept können Feststoffe einen großen Teil des dm³ einnehmen (Hydratphasen + unreagierter Klinker + Zuschlag). Nur die Phasen in
  `solid_phases` zählen für die Porosität, alles andere ist inert.
- Manche Projekte verwenden unabhängige Komponenten, die keine Elemente sind, z. B. Wasser als `H2` ohne `O`. Verwenden Sie die Namen, die das Projekt
  als Elemente auflistet. Im Calcitbeispiel gibt es kein `O`.

## Die Zustromlösung

Für `inlet` das Randwasser als eigenes GEMS-System exportieren oder berechnen, typischerweise etwa 1 kg Wasser mit den gelösten Salzen, und sein `bIC`
unskaliert übernehmen. Der Code bringt es ins Gleichgewicht und teilt durch das Lösungsvolumen. Zum Beispiel eine 14,6-mM-CaCl₂-Lösung:

```yaml
inlet:
  Ca: 0.01460
  Cl: 0.02919801532501
  H: 111.0167489181          # 55,5 mol H2O
  O: 55.508741415148
  Si: 0.000183
```

Soll das Zustromwasser mit einem Material im Gleichgewicht stehen, z. B. Tonporenwasser, das in Zement eindringt, stattdessen die Zonenform
`inlet: clay` verwenden. Der Code bringt dann das Rezept dieser Zone ins Gleichgewicht und nimmt deren Porenwasser.

## Alternative im Browser

[Case Builder](../tools/case_builder.md) lädt den exportierten Ordner, bietet beim Tippen die Element- und Phasennamen an und schreibt die YAML.
Er eignet sich für Diffusionsfälle mit einem Material. Zonen, Strömung und seitenweise Zustromlösungen werden von Hand bearbeitet.
