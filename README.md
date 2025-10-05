## METEOR MADNESS
_______________________________________________________________________________

# Project: Interactive Asteroid Impact Simulator
 
**A web-based interactive visualization and simulation tool that uses real data to help users model asteroid impact scenarios, predict their consequences, and evaluate potential mitigation strategies.**


## About The Project

### The Challenge

The discovery of near-Earth asteroids like the fictional "Impactor-2025" highlights the ongoing risk of celestial objects colliding with our planet. While rare, such impacts could cause widespread devastation, including tsunamis, seismic events, and atmospheric changes, leading to catastrophic damage on a global scale.

Valuable data exists to help us understand these threats. NASA’s Near-Earth Object (NEO) program tracks thousands of asteroids, providing crucial data on their characteristics (size, velocity, orbit) via APIs. Similarly, the U.S. Geological Survey (USGS) offers extensive environmental and geological datasets (topography, population density, tsunami zones) critical for modeling impact effects.

However, a significant gap exists:
* **Siloed Datasets:** These critical datasets are often disconnected, making it difficult to generate a holistic view of an impact scenario.
* **Lack of User-Friendly Tools:** Existing tools are often too technical for the public and policymakers or too simplistic for meaningful scientific analysis.
* **Limited Consequence Modeling:** Most tools focus on orbital tracking but fall short in simulating the complex, ground-level consequences of an impact or evaluating the effectiveness of mitigation strategies like asteroid deflection.

This gap hinders public understanding, preparedness efforts, and effective decision-making.


# Our Solution
This is a web application built with Flask that serves data from two NASA APIs: Astronomy Picture of the Day (APOD) and Near-Earth Object Web Services (NeoWs).
## Features
The application is divided into two main sections:
1. **Astronomy Picture of the Day (APOD) Viewer**
* Fetches and displays the picture or video from NASA's APOD API for the current day by default.
* Includes a date picker that allows users to browse and view historical APOD entries.
* Supports both image and video media types, providing links to high-definition versions when available.
* Displays metadata such as the title, date, copyright, and a detailed explanation for each entry.
2. **Near-Earth Object (NEO) Browser**
* Displays a paginated list of Near-Earth Objects from a local data cache.
* Data is loaded efficiently on application startup from a local 'asteroids.ison' file using a singleton pattern to ensure fast access and minimal memory usage.
* The 'asteroids.ison' file contains detailed information for each object, including its name, size, velocity, closest approach distance, and whether it is potentially hazardous.
## Technology Stack
* **Backend**: Python, Flask
* **Frontend**: HTML (Jinja2 Templates), CSS, JavaScript
* **External Libraries**: requests' (for making API calls)
* **Data Sources**:
* NASA APOD API
* Local 'asteroids ison file (used by the running application)

 -----------------------------------------------------------
## Project Structure
 
 
```
├── app.py
├── requirements.txt
├── .gitignore
├── apod/
│   ├── __init__.py
│   ├── apod.py
│   ├── apod_query.py
│   └── templates/
│       └── apod.html
├── neows/
│   ├── __init__.py
│   ├── asteroid_loader.py
│   ├── asteroids.json
│   ├── fetch_neows_all.py
│   ├── neows.py
│   ├── neows_query.py
│   ├── neowsdata.json
│   ├── process_neows_data.py
│   └── templates/
│       └── neows.html
├── static/
│   ├── favicon.png
│   └── css/
│       ├── apod.css
│       └── neows.css
└── templates/
   ├── about.html
   ├── base.html
   └── homepage.html
 
```
 
*FOLLOW THE NSTRUCTIONS GIVEN HERE: [requirements.txt](https://github.com/AnikaTejaReddy0003/MeteorMadness/blob/d9f621911e38afa9e3357e3c362c71765bdfe086/requirements.md)*
(for the setup and the installation)




--------------------------
# Analysis of Asteroid Simulation & Visualization Tools

## 1. Asteroid Launcher 
**[ASTEROID SIMULATOR]( https://neal.fun/asteroid-launcher/)**


### Overview

The Asteroid Launcher is an interactive, web-based simulator designed to model the catastrophic effects of an asteroid impact on any location on Earth. It is a simplified but powerful educational tool that visualizes the consequences of a theoretical impact event in an accessible and dramatic way.

### Key Features

* **Customizable Impact Scenarios**: Users can define the parameters of the impactor, including:
    * **Type**: Iron, Stone, Carbon, or a Comet.
    * **Size**: Diameter in feet or miles.
    * **Speed**: Impact velocity in miles per second.
    * **Angle**: The angle of impact from 1 to 90 degrees.

* **Global Targeting**: Users can select any point on a global map to serve as the impact site.

* **Detailed Consequence Analysis**: Upon launching the asteroid, the tool calculates and reports on several key effects of the impact:
    * **Crater Formation**: Estimates the final diameter and depth of the impact crater.
    * **Fireball**: Calculates the radius of the fireball and estimates the number of people who would be vaporized or receive third-degree burns.
    * **Shock Wave**: Details the reach and power of the atmospheric shock wave, including wind speeds and the sound level in decibels.
    * **Earthquake**: Predicts the magnitude of the earthquake generated by the impact and the radius within which it would be felt.

* **Statistical Reporting**: The simulation provides clear, step-by-step statistics on the projected damage and casualties, making the abstract numbers of an impact event more tangible.


## 2. NASA's Eyes on Asteroids  
**[EYES ON ASTEROID](https://eyes.nasa.gov/apps/asteroids/#/home)**

### Overview

NASA's Eyes on Asteroids is an official, real-time 3D visualization application from NASA's Jet Propulsion Laboratory (JPL). Instead of simulating hypothetical impacts, this tool tracks the actual orbits of known asteroids and comets, particularly Near-Earth Objects (NEOs), allowing users to explore our solar system and understand the proximity of these objects to Earth.

### Key Features

* **Real-Time 3D Visualization**: Displays the orbits of asteroids and comets within a detailed 3D model of our solar system, showing their positions relative to Earth, the Sun, and other planets.

* **Comprehensive Database**: The application uses up-to-date scientific data to track thousands of known NEOs.

* **Detailed Object Profiles**: Users can select any tracked object to learn more about it, including:
    * Discovery date and discoverer.
    * Orbital parameters (period, inclination, etc.).
    * Physical characteristics like size and dimensions.
    * Details about its next close approach to Earth.

* **Focus on Potentially Hazardous Asteroids (PHAs)**: The tool allows users to filter for and highlight asteroids that are officially classified as "potentially hazardous" based on their size and proximity to Earth's orbit.

* **"Asteroid Watch" Feature**: This section provides a dashboard showing the next five upcoming close approaches, making it easy to see which asteroids will be passing near Earth soon.

* **Scientific and Public Outreach**: Serves as a scientifically accurate tool for public outreach, helping to educate users about NASA's ongoing mission to track and study NEOs.

You can find the [POWERPOINT PRESENTATION](https://github.com/AnikaTejaReddy0003/MeteorMadness/blob/f8d39c3ce9fd7df1cdd09c0f37505f63ac554c42/demo/demo.html) of explaination and [VIDEO](https://github.com/AnikaTejaReddy0003/MeteorMadness/blob/dbcc2bfe0ca7d2b20b39b05e38da6b0770811088/demo/demo.mp4) of the demonstration
