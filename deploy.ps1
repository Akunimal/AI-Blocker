.\.venv\Scripts\python.exe update_translations.py
Remove-Item update_translations.py
.\.venv\Scripts\python.exe -m PyInstaller --onefile --windowed --uac-admin --add-data "translations.json;." --add-data "icon.ico;." --add-data "icon_green.ico;." --add-data "icon_red.ico;." --name "AI-Router-Blocker-AiO" --clean ai_blocker.py
Copy-Item "dist\AI-Router-Blocker-AiO.exe" "AI-Router-Blocker-AiO.exe" -Force
git add .
git commit -m "chore: release v1.2.0 with mini-improvements"
git push
