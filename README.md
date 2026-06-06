# Instalacja
1. Zainstaluj potrzebne pakiety python:
   ```
   pip install discord.py google-genai python-dotenv
   ```
2. Stwórz plik `.env` z zawartością, którą znajdziesz niżej:
   ```
   DISCORD_TOKEN=twój_token_bota_discord
   GEMINI_API_KEY=twój_klucz_gemini
   ```
3. Klucz API do Gemini znajdziesz na https://aistudio.google.com/app/api-keys
4. Token do bota Discord znajdziesz na platformie: https://discord.com/developers/home

# Konfiguracja
### Jeżeli chcesz dodać custom prompt to całej odpowiedzi modelu, użyj dedykowanej zmiennej: `history_text`
