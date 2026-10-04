from flask import Flask, render_template, request, jsonify
import pyautogui
import socket

app = Flask(__name__)


# =========================================================
# HOME / REMOTE UI
# =========================================================

@app.route("/")
def home():
    return render_template("remote.html")


# =========================================================
# CONNECTION STATUS
# =========================================================

@app.route("/status")
def status():
    hostname = socket.gethostname()

    return jsonify({
        "status": "connected",
        "hostname": hostname
    })


# =========================================================
# REMOTE CONTROL
# =========================================================

@app.route("/control", methods=["POST"])
def control():

    data = request.get_json(silent=True) or {}
    cmd = data.get("cmd")

    if not cmd:
        return jsonify({
            "success": False,
            "message": "No command received"
        }), 400

    try:

        # ---------------- MOUSE ----------------

        if cmd == "CLICK":
            pyautogui.click()

        elif cmd == "RIGHT_CLICK":
            pyautogui.rightClick()

        elif cmd == "UP_m":
            pyautogui.moveRel(0, -30)

        elif cmd == "DOWN_m":
            pyautogui.moveRel(0, 30)

        elif cmd == "LEFT_m":
            pyautogui.moveRel(-30, 0)

        elif cmd == "RIGHT_m":
            pyautogui.moveRel(30, 0)

        # ---------------- VOLUME ----------------

        elif cmd == "VOLUP":
            pyautogui.press("volumeup")

        elif cmd == "VOLDOWN":
            pyautogui.press("volumedown")

        # ---------------- MEDIA ----------------

        elif cmd == "PLAY":
            pyautogui.press("playpause")

        elif cmd == "FORWARD":
            pyautogui.press("right")

        elif cmd == "BACKWARD":
            pyautogui.press("left")

        # ---------------- KEYBOARD ARROWS ----------------

        elif cmd == "UP":
            pyautogui.press("up")

        elif cmd == "DOWN":
            pyautogui.press("down")

        elif cmd == "LEFT":
            pyautogui.press("left")

        elif cmd == "RIGHT":
            pyautogui.press("right")

        # ---------------- WINDOWS ----------------

        elif cmd == "MINIMIZE":
            pyautogui.hotkey("win", "m")

        elif cmd == "MAXIMIZE":
            pyautogui.hotkey("win", "shift", "m")

        elif cmd == "ALT_TAB":
            pyautogui.hotkey("alt", "tab")

        else:
            return jsonify({
                "success": False,
                "message": f"Unknown command: {cmd}"
            }), 400

        return jsonify({
            "success": True,
            "command": cmd
        })

    except Exception as e:

        return jsonify({
            "success": False,
            "message": str(e)
        }), 500


# =========================================================
# START SERVER
# =========================================================

if __name__ == "__main__":

    print("=" * 50)
    print("       LAPTOP REMOTE V2")
    print("=" * 50)

    print(f"Local:   http://127.0.0.1:5000")
    print(f"Network: http://<YOUR-LAPTOP-IP>:5000")

    print("=" * 50)

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )