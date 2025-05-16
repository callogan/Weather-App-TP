# Weather Application with 3D Visualization

## Description
This is a multifunctional weather application developed using Python. The application has two main operating modes:

1. 3D Visualization Mode ( united_graph_elements folder ) - realizes an interactive three-dimensional figure (cube) with various visual effects.
2. Weather Service Mode ( weather_service folder ) - displays current weather data retrieved from an external API and presents it in a user-friendly 
graphical interface.
The application allows users to get up-to-date weather information for a selected city

## Technologies Used
- Python 3.12 - main programming language
- PySide6 - for creating the graphical user interface
- OpenGL - for 3D visualization and rendering
- Pygame - for event handling and text display in OpenGL
- Requests - for interacting with the weather API

## Project Structure
- base_renderer.py - abstract class for rendering
- joint_graphics.py - displays widgets and 3D figure
- weather_service.py - module for interacting with the weather API
- weather_gui.py - graphical interface module for displaying weather
- main_weather_service.py - main file (entry point) for launching the standard application mode
- main_opengl.py - file for launching the 3D visualization mode
- requirements.txt - list of project dependencies

## Installation
1. Make sure you have Python 3.8 or higher installed
2. Clone the repository or unpack the project archive
3. Install the necessary dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

### 3D Visualization Mode
To run the application with 3D visualization, execute:

```bash
python joint_graphics.py
```

In this mode, the following features are available:

- Interactive engagement with the 3D cube model
- Rotating the model using the mouse
- Scaling using the mouse wheel
- Resetting the model position using the "Reset" button

### Weather Service Mode (including GUI with Weather Data)
To run the main application displaying current weather, execute:

```bash
python main_weather_service.py
```
This mode allows you to:

- View current weather for a selected city
- Get information about temperature and other parameters
- Update data manually.
