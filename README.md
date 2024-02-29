# software_engineering

five person team, weekly sprints
test

Team Number: 19
| Name                | Github       |
|---------------------|--------------|
| Ethan Potts         | empotts      |
| Ogden Wells         | BatSmacker84 |
| Jordi Castro        | jordicastro  |
| Russell Rathbun     | wrrath       |
| Nicholas DeVilliers | nmdevill     |

## How to run the project

1. Clone the repository and navigate to the project directory:

   ```sh
    git clone https://github.com/jordicastro/software_engineering.git
    cd software_engineering
    ```

2. Run the main script:

   ```sh
   python main.py
   ```

3. If you want to test the supabase integration

   ```sh
   python database.py
   ```

## How to set up the development environment

1. Clone the repository and navigate to the project directory:

   ```sh
    git clone https://github.com/jordicastro/software_engineering.git
    cd software_engineering
    ```

2. Create a python virtual environment:

   **Linux/MacOS**

    ```sh
    python3 -m venv venv
    ```

   **Windows**

    ```powershell
    python -m venv venv
    ```

3. Activate the virtual environment:

   **Linux/MacOS**

    ```sh
    source venv/bin/activate
    ```

   **Windows**

    ```powershell
    venv\Scripts\activate
    ```

4. Install the required python packages:

    ```sh
    pip install -r requirements.txt
    ```

## How to play Photon

1. Make sure you have the required packages installed (see above)

2. Run ```python3 main.py``` in the project directory

3. Enter Player ID in the lower most text box (it may be hard to see on larger monitors)

4. Enter Equipment ID in the text box above the Player ID

5. Press the ```Add Player``` button to add the player to the game

6. If the Player ID is not found in the database, enter the player's name in the top text box and press the ```Create Player``` button to add the player to the database

7. Press ```F12``` to clear all players

8. Once all players have been added, press ```F5``` to start the game

9. The game will take 6 minutes

10. Check the display window to see updates for which team is winning

11. When the game is completer, return to the home base to see which team wins!
