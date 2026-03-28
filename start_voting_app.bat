@echo off
echo Starting the Secure Blockchain Voting System...
echo Please wait while the environment is set up.

:: Check if the virtual environment exists, if not, create it
if not exist "venv\Scripts\python.exe" (
    echo Creating virtual environment...
    python -m venv venv
)

:: Activate background virtual environment silently
call venv\Scripts\activate.bat

:: Install requirements silently
echo Checking dependencies...
pip install -r requirements.txt -q

if not exist contract_address.txt (
    echo Deploying Ethereum smart contract...
    python eth_integration.py
)

:: Start the Flask app in the background
echo Starting local server...
start /b python app.py

:: Give the server a couple of seconds to boot up
timeout /t 3 >nul

:: Open the browser to the local app
echo Opening browser...
start http://127.0.0.1:5000/

echo.
echo Application is running! 
echo Keep this window open. Closing this window will NOT stop the server immediately.
echo To forcefully stop the server, you can close the Python background process or type taskkill /F /IM python.exe
echo.
pause
