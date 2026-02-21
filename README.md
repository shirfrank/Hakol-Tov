# Hakol-Tov (הקול טוב!) 🎤🐦

![Hakol-Tov Banner](logo.png)

## Overview
**Hakol-Tov** (a play on the Hebrew phrase for "everything is good" and "the voice is good") is a Python-based GUI application that serves as a central hub for three interactive, voice-controlled mini-games. Designed for both fun and vocal engagement, the application manages user sessions, personalized audio settings, and competitive leaderboards.

---

## 🎮 The Mini-Games

### 1. Squeaky Bird
![Squeaky Bird Asset](logo2.png)

Navigate the bird through obstacles using your voice. 
* **Mechanic**: Modulation of audio input (squeaks or speech) controls the bird's flight.
* **Visuals**: Uses custom assets including:
  <br>
  <img src="bird2.png" alt="Squeaky Bird" width="50"> 
  <img src="column.png" alt="Column" width="25"> 
  <img src="bg2.png" alt="Background" width="60">

### 2. Pitch Perfect
Challenge your vocal precision by hitting specific pitch targets.
* **Focus**: Vocal frequency control and accuracy.

### 3. Voice Target
A game focused on hitting specific vocal targets through sustained or varied audio input.

---

## ✨ Features
* **User & Admin Access**: Secure login system with distinct roles.
* **Personalized Thresholds**: Audio sensitivity is tailored to individual users, stored in `thresholds.json` to ensure the games respond accurately to different voices.
* **Comprehensive Leaderboards**: View rankings including cumulative scores, highest scores, and latest performance.
* **Admin Controls**: Specialized dashboard to manage user thresholds and reset leaderboard data.

---

### 🛠️ Installation

**Steps**

1.  **Clone the repository**:
    ```bash
    git clone [https://github.com/your-username/game-hub.git](https://github.com/your-username/game-hub.git)
    cd game-hub
    ```

2.  **Install required libraries**:
    ```bash
    pip install pillow pygame sounddevice numpy scipy
    ```

3.  **Run the application**:
    ```bash
    python main_final.py
    ```

---

### 📁 File Structure

* **`main_final.py`**: The primary GUI and central hub application.
* **`squeaky_bird_final.py`**: Game logic for **Squeaky Bird**.
    * **Assets**: 
        <img src="bird2.png" alt="Bird" width="40"> 
        <img src="column.png" alt="Pipe" width="20"> 
        <img src="bg2.png" alt="Sky" width="50">
* **`pitch_perfect_final.py`**: Game logic for **Pitch Perfect**.
* **`voice_target_final.py`**: Game logic for **Voice Target**.
* **`thresholds.json`**: Stores personalized audio trigger levels for each user.
* **`score.json`**: Current session scoring and game data.
* **`*_leaderboard.json`**: JSON files for persistent score tracking across games.

---

### 📖 Usage

* **Login**: Access the hub using an existing account.
    * **Admin User**: `clinait`
    * **Standard Users**: `shir`, `tom`, `ofri`, `mai`, `shaked`
* **Navigation**: Use the interactive GUI to select a mini-game or check the leaderboards.
* **Gameplay**: Control the games entirely using your voice and microphone input.

---

### 📜 License

This project is licensed under the **MIT License**.
