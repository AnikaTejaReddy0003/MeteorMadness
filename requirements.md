* TO RUN THE WEBSITE INSTALL THE DEPENDENCIES

## Setup and Installation

To get a local copy up and running, follow these steps.

### Prerequisites
* Python 3.8+ and Pip
* Git

### Instructions

1.  **Clone the Repository(in the TERMINAL)**
    ```sh
    git clone https://github.com/AnikaTejaReddy0003/MeteorMadness
    ```

2.  **Navigate into the Directory**
    ```sh
    cd MeteorMadness
    ```

3.  **Create a Virtual Environment**
    This will create a `venv` folder in your directory to isolate project dependencies.
    ```sh
    python -m venv venv
    ```

4.  **Activate the Virtual Environment**
    * **On Windows:**
        ```sh
        .\venv\Scripts\Activate
        ```
    * **On macOS/Linux:**
        ```sh
        source venv/bin/activate
        ```

5.  **Install Dependencies**
    Install all the required Python packages from the `requirements.txt` file.
    ```sh
    pip install flask requests
    ```

6.  **Run the Server**
    This will start the local Flask development server.
    ```sh
    python app.py
    ```
    Once running, open your web browser and navigate to `http://127.0.0.1:5000`.

## Data Fetching Script

The project includes a script `fetch_neows_all.py` to download the entire Near-Earth Object dataset from NASA. This is then processed by `process_neows_data.py` to create the smaller, cleaned `asteroids.json` file used by the app.

**Note:** The fetching script makes thousands of API calls and will take a considerable amount of time to complete. It is not required to run the main application, which uses the provided `asteroids.json` file.

To run the script:
```sh
python neows/fetch_neows_all.py
