from flask import Flask, request, redirect
import pyautogui

app = Flask(__name__)


# ---------------- REMOTE UI ----------------
@app.route("/remote")
def remote():
    return """
    <style>
    body {
        background:#121212;
        color:white;
        text-align:center;
        font-family:times new roman;
        padding:20px;
    }
    html, body {
    touch-action: manipulation;
    }
    h1 {
        margin-bottom:100px;
        font-size:50px;
    }

    button {
        height:100px;
        width:200px;
        padding:18px 22px;
        margin:10px;
        border-radius:12px;
        background:#333;
        color:white;
        font-weight:bold;
        border:none;
        font-size:25px;
        min-width:100px;
    }

    input {
        padding:14px;
        margin:10px;
        border-radius:10px;
        width:65%;
        font-size:16px;
    }

    .arrow-grid {
        margin-top:20px;
    }

    .row {
        display:flex;
        justify-content:center;
    }

    .player_controls {
        margin:40px;
        border:5px solid #333;
    }

    .mouse_controls {
        margin:40px;
        border:5px solid #333;
    }
    </style>

    <h1>💻 My Laptop Remote</h1>

    

    <div class="player_controls">
        <h1>🎬 Player Controls</h1> <br>
        <div>
        
            <button onclick="send('VOLUP')">🔊+</button>
            <button onclick="send('VOLDOWN')">🔉-</button>
            <button onclick="send('PLAY')">⏯️</button>
        </div>
    
        <div>
            <button onclick="send('BACKWARD')">⏪ 10s</button>
            <button onclick="send('FORWARD')">⏩ 10s</button>
        </div>
    
    
        <div class="arrow-grid">
            <div class="row">
                <button onclick="send('UP')">⬆</button>
            </div>
            <div class="row">
                <button onclick="send('LEFT')">⬅</button>
                <button onclick="send('DOWN')">⬇</button>
                <button onclick="send('RIGHT')">➡</button>
            </div>
        </div>
    </div>


    

    <div class="mouse_controls">
        <h1>🖱️ Mouse Controls</h1> <br>
        <div>
            <button onclick="send('LEFT_m')">⬅️</button>
            <button onclick="send('UP_m')">⬆️</button>
            <button onclick="send('RIGHT_m')">➡️</button>
            <button onclick="send('DOWN_m')">⬇️</button>
        </div>
        <button onclick="send('CLICK')">Click</button>
        <button onclick="send('RIGHT_CLICK')">Right Click</button>
    </div>

    <div>
        <button onclick="send('MINIMIZE')"> ➖ Minimize</button>
        <button onclick="send('MAXIMIZE')"> ➕ Maximize</button>
        <button onclick="send('Alt_TAB')">Alt+Tab</button>
    </div>
    

    <script>
    function send(cmd){
        fetch('/control?cmd=' + cmd);
    }
    </script>
    """


# ---------------- CONTROLS ----------------
@app.route("/control")
def control():
    cmd = request.args.get("cmd")

    if cmd == "CLICK":
        pyautogui.click()
    elif cmd == "RIGHT_CLICK":
        pyautogui.rightClick()
    elif cmd == "VOLUP":
        pyautogui.press("volumeup")
    elif cmd == "VOLDOWN":
        pyautogui.press("volumedown")
    elif cmd == "PLAY":
        pyautogui.press("playpause")
    elif cmd == "UP":
        pyautogui.press("up")
    elif cmd == "DOWN":
        pyautogui.press("down")
    elif cmd == "LEFT":
        pyautogui.press("left")
    elif cmd == "RIGHT":
        pyautogui.press("right")
    elif cmd == "FORWARD":
        pyautogui.press("right")  # works in YouTube/video players
    elif cmd == "BACKWARD":
        pyautogui.press("left")
    elif cmd == "MINIMIZE":
        pyautogui.hotkey("win", "m")
    elif cmd == "MAXIMIZE":
        pyautogui.hotkey("win", "shift", "m")
    elif cmd == "Alt_TAB":
        pyautogui.hotkey("alt", "tab")

    elif cmd == "UP_m":
        pyautogui.moveRel(0, -30)
    elif cmd == "DOWN_m":
        pyautogui.moveRel(0, 30)
    elif cmd == "LEFT_m":
        pyautogui.moveRel(-30, 0)
    elif cmd == "RIGHT_m":
        pyautogui.moveRel(30, 0)

    return "OK"

@app.route("/")
def home():
    return remote()


app.run(host="0.0.0.0", port=5000)

