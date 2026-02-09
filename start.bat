@echo off
echo Powering up Gesture Drop... 🚀
echo.

echo [1/3] Starting Secure Tunnel (Ngrok)... 🔒
start "Gesture Drop Tunnel" cmd /c "ngrok http 5000"

echo waiting for tunnel to establish...
timeout /t 5 /nobreak >nul

echo [2/3] Starting Backend Server... 🖥️
start "Gesture Drop Server" cmd /k "python server.py"

echo waiting for server to initialize...
timeout /t 3 /nobreak >nul

echo [3/3] Starting Gesture Sender... 🖐️
start "Gesture Drop Sender" cmd /k "python gesture_sender.py"

echo.
echo ========================================================
echo ✅ ALL SYSTEMS GO!
echo.
echo 1. Scan the QR code shown in the 'Gesture Drop Server' window with your phone. 📷
echo 2. Allow camera permissions on your phone.
echo 3. Use the 'Gesture Drop Sender' window to send text!
echo    (Press 'F' key if hand tracking is unavailable)
echo ========================================================
echo.
pause
