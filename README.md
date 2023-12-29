# foot-scan-pro
This project lets you tap into the world of La Liga Santander, providing a user-friendly interface to explore Jornadas (matchdays), Partidos (matches), Equipos (teams), and Jugadores (players).

## Key Features
Jornadas Overview: Get a quick look at each matchday, including scheduled matches and results.

Partidos Insight: Dive into match details.

Equipos Showcase: Check out profiles of La Liga teams.

Jugadores Spotlight: Explore player profiles, including nationality, position, and more.

## Installation

First of all, you need to clone this repository to your local machine. Once this is done, you can continue with:

```bash
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
```
## Usage
```bash
python manage.py runserver
```
Once it is running in your local machine you should go to "Cargar Datos" so you can extract the data. After doing this you are ready to go.
