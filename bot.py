import os
from collections import defaultdict, deque

import discord
from discord.ext import commands
from dotenv import load_dotenv
from google import genai

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not DISCORD_TOKEN:
    raise RuntimeError("Brak DISCORD_TOKEN w .env")

if not GEMINI_API_KEY:
    raise RuntimeError("Brak GEMINI_API_KEY w .env")

client = genai.Client(api_key=GEMINI_API_KEY)

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

conversations = defaultdict(lambda: deque(maxlen=12))


@bot.event
async def on_ready():
    print(f"Zalogowano jako {bot.user}")


@bot.command(name="ai")
async def ai(ctx, *, message: str):
    key = f"{ctx.channel.id}:{ctx.author.id}"

    conversations[key].append({
        "role": "user",
        "text": message
    })

    history_text = "Jesteś pomocnym asystentem na Discordzie. Odpowiadaj po polsku.\n\n"

    for msg in conversations[key]:
        role = "Użytkownik" if msg["role"] == "user" else "AI"
        history_text += f"{role}: {msg['text']}\n"

    async with ctx.typing():
        try:
            response = client.models.generate_content(
                model="gemini-3.5-flash",
                contents=history_text
            )

            answer = response.text.strip()

            conversations[key].append({
                "role": "assistant",
                "text": answer
            })

            if len(answer) > 1900:
                answer = answer[:1900] + "..."

            await ctx.reply(answer)

        except Exception as e:
            await ctx.reply(f"Wystąpił błąd: `{e}`")


@bot.command(name="reset")
async def reset(ctx):
    key = f"{ctx.channel.id}:{ctx.author.id}"
    conversations[key].clear()
    await ctx.reply("Historia rozmowy została wyczyszczona.")


bot.run(DISCORD_TOKEN)
