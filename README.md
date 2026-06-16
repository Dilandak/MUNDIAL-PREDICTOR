# 🏆 Mundial 2026 — Predictor Estadístico en Vivo

> Herramienta de línea de comandos que descarga resultados reales del Mundial 2026, analiza estadísticas de cada selección y predice partidos pendientes con probabilidades, goles esperados (xG) y goleadores probables.

---

## ✨ ¿Qué hace?

- 🌐 **Descarga datos en vivo** cada vez que lo corres (resultados, goles, minutos)
- 📋 **Muestra resultados reales** de todos los partidos jugados con goleadores
- 🥇 **Tabla de goleadores** del torneo actualizada automáticamente
- 🎯 **Predice partidos pendientes** usando:
  - Ratings FIFA y estadísticas de ataque/defensa
  - Forma real del equipo **en el torneo** (no datos históricos genéricos)
  - Modelo de goles esperados (xG) con distribución de Poisson
  - Probabilidades de victoria, empate y derrota
- 👕 **Squads reales** — muestra los XI probables y goleadores de cada selección convocados al Mundial 2026
- ⚽ **Goleadores inteligentes** — prioriza jugadores que ya marcaron en el torneo

---

## 📦 Requisitos

- Python 3.8 o superior
- Conexión a internet (para descargar resultados en vivo)

Verifica tu versión de Python:
```bash
python3 --version
```

---

## 🚀 Instalación

### 1. Clona el repositorio

```bash
git clone https://github.com/TU_USUARIO/mundial2026-predictor.git
cd mundial2026-predictor
```

### 2. Instala la dependencia

```bash
pip3 install requests --break-system-packages
```

> En algunos sistemas puede que necesites usar `pip` en lugar de `pip3`.

### 3. Corre el script

```bash
python3 mundial2026_predictor.py
```

¡Listo! El script se conecta a internet, descarga los datos y muestra el menú.

---

## 🖥️ Uso

Al correrlo verás este menú:

```
══════════════════════════════════════════════════════════════════
  🌍 MUNDIAL 2026 | Jugados: 16 | Pendientes: 88
──────────────────────────────────────────────────────────────────
  [1] Resultados reales (con goleadores y minutos)
  [2] Tabla de goleadores del torneo
  [3] Predecir TODOS los partidos pendientes
  [4] Predecir UN partido específico
  [5] Partidos más parejos
  [6] Ver squad + titulares de un equipo
  [7] Salir
──────────────────────────────────────────────────────────────────
  ► Opción:
```

### Opciones explicadas

| Opción | Descripción |
|--------|-------------|
| `1` | Todos los resultados jugados con goleadores y minutos exactos |
| `2` | Ranking de goleadores del torneo en tiempo real |
| `3` | Predicción completa de todos los partidos que faltan |
| `4` | Elige un partido específico para analizar en detalle |
| `5` | Los 10 partidos más competitivos estadísticamente |
| `6` | XI probable, goleadores convocados y goles reales de un equipo |

---

## 📊 ¿Cómo funciona la predicción?

Cada predicción combina varios factores:

```
Rating base (FIFA)
    + Forma real en el torneo (W/D/L)
    + Goles marcados y recibidos en el Mundial
    + Ataque vs Defensa de cada equipo
    + Ventaja de condición local
    ↓
xG (Goles Esperados) → Distribución de Poisson
    ↓
Probabilidades + Escenarios posibles + Marcador más probable
```

### Ejemplo de salida de predicción

```
══════════════════════════════════════════════════════════════════
  #39 | Group J | 📅 2026-06-16
══════════════════════════════════════════════════════════════════
  🏠 ARGENTINA (#1)  🆚  ARGELIA (#38)

  👕 XI PROBABLE Argentina:
     Emiliano Martínez | Nahuel Molina | Cristian Romero | ...

  🔥 Forma en el torneo:
     Argentina           : Debut   GF:0 GC:0
     Argelia             : Debut   GF:0 GC:0

  📊 PROBABILIDADES:
     🏆 Argentina        :  78.3%  ███████████████
     🤝 Empate           :  12.0%  ██
     🏆 Argelia          :   9.7%  █

  ⚽ xG: Argentina 2.1 — 0.4 Argelia
  🎯 Marcador probable: 2-0

  📈 Escenarios:
     2-0   →  24.5%  ████████
     1-0   →  22.3%  ███████
     3-0   →  16.1%  █████

  🌟 Goleadores probables:
     ⚽ Argentina: Lionel Messi
     ⚽ Argentina: Lautaro Martínez
     ⚽ Argelia: Riyad Mahrez
```

---

## 📁 Estructura del proyecto

```
mundial2026-predictor/
│
├── mundial2026_predictor.py   # Script principal
└── README.md                  # Este archivo
```

---

## 🔄 ¿Con qué frecuencia se actualiza?

Los datos se descargan **cada vez que corres el script** desde:

```
https://github.com/openfootball/world-cup.json
```

Este repositorio es mantenido por la comunidad open source y se actualiza tras cada partido del Mundial. No necesitas hacer nada — solo corre el script y siempre tendrás los datos más recientes.

---

## 🛠️ Solución de problemas

**Error: `No module named 'requests'`**
```bash
pip3 install requests --break-system-packages
```

**Error de conexión al correr el script**
- Verifica tu conexión a internet
- Intenta de nuevo en unos minutos (puede ser el servidor de datos)

**`python3` no reconocido**
- En Windows usa `python` en lugar de `python3`
- En Mac asegúrate de tener Python instalado: `brew install python3`

---

## 🤝 Contribuir

¿Quieres mejorar el predictor? Pull requests bienvenidos.

Algunas ideas:
- [ ] Agregar historial H2H (head to head) entre selecciones
- [ ] Notificaciones cuando empiece un partido
- [ ] Exportar predicciones a PDF o Excel
- [ ] Modo torneo completo (simular hasta la final)

---

## 📄 Licencia

MIT — úsalo como quieras.

---

<div align="center">
  Hecho con amor en Colombia — <strong>¡Vamos con toda!</strong>
</div>