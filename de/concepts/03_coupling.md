# Konzentration ↔ Masse, Porosität und Initialisierung

Der Transport arbeitet mit Konzentrationen (mol pro m³ Fluid), GEMS mit Stoffmengen (mol pro Knoten). OGS
rechnet mit zwei Funktionen zwischen beiden um; die Vorlage übernimmt sie Zeile für Zeile.

## Konzentration → Masse (vor GEMS)

```{literalinclude} ../../GEMS_FEniCSx_OGS5_Template/gems_ogs.py
:language: python
:pyobject: OGSGEMS.concentration_to_mass
```

Die transportierte Konzentration wird mit dem Fluidvolumen $V_f$ multipliziert, das der Knoten *vor* dem
Transport hatte, negative Werte werden durch ihren Betrag ersetzt, das Lösungsmittel Wasser wird wieder
addiert, und sehr kleine Summen werden auf $10^{-16}$ gesetzt (GEMS kann mit Nullen nicht umgehen).

## Masse → Konzentration (nach GEMS)

```{literalinclude} ../../GEMS_FEniCSx_OGS5_Template/gems_ogs.py
:language: python
:pyobject: OGSGEMS.mass_to_concentration
```

- Die **Porosität** ist $\phi = 1 - \sum V_\text{fest}$ (OGS `CalcPorosity`; das Knotenvolumen ist 1 m³),
  begrenzt auf `[MIN_POROSITY, MAX_POROSITY]`.
- GEMS liefert ein eigenes Volumen der wässrigen Phase $V_{aq}$, das nie genau $\phi$ ist. Was dann passiert,
  bestimmt die Option `hydrology`:

| `hydrology` | OGS-Eingabe | Regel |
|---|---|---|
| `'full'` | `$FLAG_COUPLING_HYDROLOGY 1` | die ganze wässrige Phase wird mit $\phi/V_{aq}$ skaliert; $V_f = \phi$; die Differenz $V_{aq}-\phi$ wird zur Strömungsquelle |
| `'hayekit'` | `$FLAG_HAYEKIT 1` | nur das Lösungsmittel Wasser wird skaliert |
| `'none'` | `$FLAG_COUPLING_HYDROLOGY 0` | keine Skalierung; $c = b_{aq}/V_{aq}$ und später $b = b_\text{fix} + c\,\phi$ |

## Initialisierung

Ein OGS-GEM-Lauf kann auf zwei Arten beginnen:

- **aus b-Gesamtvektoren** (`.ic`-Datei) — `init_from_bulk`. OGS rechnet GEMS, teilt den b-Vektor durch das
  resultierende Systemvolumen $V_s$, damit jeder Knoten genau 1 m³ enthält, und rechnet GEMS erneut (zwei Durchläufe);
- **aus Restartdateien** (`$RELOAD`) — `init_from_restart`. Gespeicherte Porosität, Fluidvolumen, `b_fix`,
  Speziesmengen und kinetische Schranken werden geladen und GEMS einmal damit gerechnet. Mehrere Benchmarks
  (HAYEKIT, comedy2d, TransLay2d) ergeben nur ab ihrem Restartzustand Sinn.
