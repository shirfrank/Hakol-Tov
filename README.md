# Hakol-Tov

## Overview
This project is a Python-based GUI application that serves as a hub for three mini-games:
- **Squeaky Bird**
- **Pitch Perfect**
- **Voice Target**

The application includes user and admin access, leaderboards, and thresholds for gameplay. Players can log in to play games, view their scores, and compete with others.

---

## Features
- **User Login**: Secure access for users and admins with individual thresholds.
- **Play Games**: Run any of the three mini-games directly from the application.
- **Leaderboards**: View scores and rankings, including cumulative, highest, and latest scores.
- **Admin Controls**:
  - Manage thresholds for users.
  - Reset leaderboards.

---

## Installation
### Prerequisites
1. Python 3.10 or above
2. Required Python libraries:
   - `tkinter`
   - `PIL`
   - `subprocess`
   - `json`
   - `pygame`
   - `sounddevice`
   - `numpy`
   - `scipy`

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/game-hub.git
   ```
2. Navigate to the project folder:
   ```bash
   cd game-hub
   ```
3. Install dependencies:
   ```bash
   pip install pillow pygame sounddevice numpy scipy
   ```
4. Run the application:
   ```bash
   python main_final.py
   ```

---

## File Structure
- `main_final.py`: The main script for the Game Hub application.
- `squeaky_bird_final.py`: Game script for Squeaky Bird.
  - Dependencies: `pygame`, `pyaudio`, `numpy`, `math`, `json`.
- `pitch_perfect_final.py`: Game script for Pitch Perfect.
  - Dependencies: `pygame`, `random`, `sounddevice`, `numpy`, `scipy`.
- `voice_target_final.py`: Game script for Voice Target.
  - Dependencies: `pygame`, `pyaudio`, `numpy`, `math`, `time`.
- `squeaky_bird_leaderboard.json`: JSON file to store leaderboard data for Squeaky Bird.
- `pitch_perfect_leaderboard.json`: JSON file to store leaderboard data for Pitch Perfect.
- `voice_target_leaderboard.json`: JSON file to store leaderboard data for Voice Target.

---

## Usage
1. Start the application with `python main_final.py`.
2. Log in using an existing username and password.
   - Admin username: `clinait`
   - Default user usernames: `shir`, `tom`, `ofri`, `mai`, `shaked`
3. Navigate to the desired game or leaderboard using the GUI.
4. Play games and check scores on the leaderboard.

---

## Contribution
1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Commit your changes and open a pull request.

---

## License
### MIT License

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

