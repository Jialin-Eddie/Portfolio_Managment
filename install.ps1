# Set up and activate virtual environment
# cd to portfolio managment first or equal directory with install.ps1
Write-Host "Setting up virtual environment..."
python -m venv .venv
Write-Host "Activating virtual environment..."
.venv\Scripts\Activate.ps1
Write-Host "Installing dependencies..."
pip install -r requirements.txt
Write-Host "Setup complete. Ready to use!"
