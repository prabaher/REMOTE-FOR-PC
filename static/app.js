// =====================================================
// ELEMENTS
// =====================================================

const statusDot =
    document.getElementById("status-dot");

const statusText =
    document.getElementById("status-text");

const hostname =
    document.getElementById("hostname");

const message =
    document.getElementById("message");

const touchpad =
    document.getElementById("touchpad");


// =====================================================
// SEND COMMAND
// =====================================================

async function sendCommand(
    command,
    extraData = {}
) {

    try {

        const response = await fetch(
            "/control",
            {
                method: "POST",

                headers: {
                    "Content-Type":
                        "application/json"
                },

                body: JSON.stringify({
                    cmd: command,
                    ...extraData
                })
            }
        );


        const data =
            await response.json();


        if (data.success) {

            showMessage(
                "✓ " + command
            );

        } else {

            showMessage(
                "⚠ " + data.message
            );

        }

    }

    catch (error) {

        console.error(error);

        showMessage(
            "Connection failed"
        );

        setOffline();
    }
}


// =====================================================
// MESSAGE
// =====================================================

function showMessage(text) {

    message.textContent = text;

    clearTimeout(
        window.messageTimer
    );


    window.messageTimer =
        setTimeout(() => {

            message.textContent = "";

        }, 1000);
}


// =====================================================
// CONNECTION
// =====================================================

function setOnline(deviceName) {

    statusDot.classList.remove(
        "offline"
    );

    statusDot.classList.add(
        "online"
    );

    statusText.textContent =
        "Connected";

    hostname.textContent =
        deviceName || "Laptop";
}


function setOffline() {

    statusDot.classList.remove(
        "online"
    );

    statusDot.classList.add(
        "offline"
    );

    statusText.textContent =
        "Disconnected";

    hostname.textContent =
        "Laptop unavailable";
}


// =====================================================
// CONNECTION CHECK
// =====================================================

async function checkConnection() {

    try {

        const response =
            await fetch(
                "/status",
                {
                    method: "GET",
                    cache: "no-store"
                }
            );


        if (!response.ok) {

            throw new Error(
                "Server unavailable"
            );

        }


        const data =
            await response.json();


        if (
            data.status ===
            "connected"
        ) {

            setOnline(
                data.hostname
            );

        } else {

            setOffline();

        }

    }

    catch (error) {

        console.error(
            "Status check failed:",
            error
        );

        setOffline();
    }
}


// =====================================================
// TOUCHPAD VARIABLES
// =====================================================

let lastX = 0;

let lastY = 0;

let touchStartX = 0;

let touchStartY = 0;

let touchMoved = false;

let touchStartTime = 0;

let lastTapTime = 0;


// =====================================================
// TOUCHPAD START
// =====================================================

touchpad.addEventListener(
    "touchstart",
    function(event) {

        event.preventDefault();


        const touch =
            event.touches[0];


        lastX =
            touch.clientX;

        lastY =
            touch.clientY;


        touchStartX =
            touch.clientX;

        touchStartY =
            touch.clientY;


        touchStartTime =
            Date.now();


        touchMoved = false;
    },
    {
        passive: false
    }
);


// =====================================================
// TOUCHPAD MOVE
// =====================================================

touchpad.addEventListener(
    "touchmove",
    function(event) {

        event.preventDefault();


        // =============================================
        // TWO FINGER SCROLL
        // =============================================

        if (
            event.touches.length === 2
        ) {

            const touch1 =
                event.touches[0];

            const touch2 =
                event.touches[1];


            const currentY =
                (
                    touch1.clientY +
                    touch2.clientY
                ) / 2;


            const previousY =
                lastY;


            const movement =
                currentY -
                previousY;


            if (
                Math.abs(movement) > 2
            ) {

                sendCommand(
                    "SCROLL",
                    {
                        amount:
                            -movement / 8
                    }
                );

            }


            lastY =
                currentY;


            return;
        }


        // =============================================
        // ONE FINGER MOUSE MOVEMENT
        // =============================================

        const touch =
            event.touches[0];


        const currentX =
            touch.clientX;

        const currentY =
            touch.clientY;


        const dx =
            currentX - lastX;

        const dy =
            currentY - lastY;


        if (
            Math.abs(dx) > 1 ||
            Math.abs(dy) > 1
        ) {

            touchMoved = true;


            sendCommand(
                "MOUSE_MOVE",
                {
                    dx: dx,
                    dy: dy
                }
            );

        }


        lastX =
            currentX;

        lastY =
            currentY;

    },
    {
        passive: false
    }
);


// =====================================================
// TOUCHPAD END
// =====================================================

touchpad.addEventListener(
    "touchend",
    function(event) {

        event.preventDefault();


        const touchDuration =
            Date.now() -
            touchStartTime;


        const distanceX =
            Math.abs(
                lastX -
                touchStartX
            );


        const distanceY =
            Math.abs(
                lastY -
                touchStartY
            );


        const distance =
            Math.max(
                distanceX,
                distanceY
            );


        // =============================================
        // TAP
        // =============================================

        if (
            !touchMoved &&
            distance < 10 &&
            touchDuration < 300
        ) {

            const now =
                Date.now();


            // Double tap

            if (
                now - lastTapTime <
                350
            ) {

                sendCommand(
                    "DOUBLE_CLICK"
                );

                lastTapTime = 0;

            } else {

                sendCommand(
                    "CLICK"
                );

                lastTapTime =
                    now;
            }
        }

    },
    {
        passive: false
    }
);


// =====================================================
// DISABLE CONTEXT MENU
// =====================================================

touchpad.addEventListener(
    "contextmenu",
    function(event) {

        event.preventDefault();

    }
);


// =====================================================
// START
// =====================================================

checkConnection();


setInterval(
    checkConnection,
    3000
);