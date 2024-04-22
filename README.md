# software_engineering

five person team, weekly sprints

Team Number: 19
| Name                | GitHub       |
|---------------------|--------------|
| Ethan Potts         | empotts      |
| Ogden Wells         | BatSmacker84 |
| Jordi Castro        | jordicastro  |
| Russell Rathbun     | wrrath       |
| Nicholas DeVilliers | nmdevill     |

## How to run the project

1. Clone the repository and navigate to the project directory:

   ```bash
    git clone https://github.com/jordicastro/software_engineering.git
    cd software_engineering
    ```

2. Create a python virtual environment:

   **Linux/macOS**

    ```bash
    python3 -m venv venv
    ```

   **Windows**

    ```powershell
    python -m venv venv
    ```

3. Activate the virtual environment:

   **Linux/macOS**

    ```bash
    source venv/bin/activate
    ```

   **Windows**

    ```powershell
    venv\Scripts\activate
    ```

4. Install the required python packages:

    ```bash
    pip install -r requirements.txt
    ```

## How to play Photon

1. Run ```main.py```

2. Enter players by inputting their player_id and equipment_id into the respective fields and pressing the ```Add Player``` button.

3. If the player does not exist in the database, a name field will appear. Enter the player's name and press the ```Add Player``` button again.

4. Press ```F12``` to clear all players

5. Once all players have been added, press the ```Start``` button to start the game

6. The game will take 6 minutes

7. Check the display window to see updates for which team is winning

8. When the game is completed, return to the home base to see which team wins!
