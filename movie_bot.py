import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

TELEGRAM_TOKEN = "7981217399:AAHUfxKwq44tUq4us_972G_Tr5yMhWwtvpc"  
TMDB_API_KEY = "a6310e0f4b7822560d598cb0e55332de"  

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "مرحبًا! أنا بوت اقتراح الأفلام. 🎬\n"
        "اكتب /suggest ونوع الفيلم (مثال: /suggest action)"
    )

async def suggest_movie(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    genre = context.args[0] if context.args else "action"
    
    genres = {
        "action": 28, "comedy": 35, "horror": 27,
        "romance": 10749, "sci-fi": 878
    }
    
    url = f"https://api.themoviedb.org/3/discover/movie?api_key={TMDB_API_KEY}&with_genres={genres.get(genre, 28)}"
    response = requests.get(url).json()
    
    if response["results"]:
        movie = response["results"][0]  
        message = (
            f"🎬 الفيلم: {movie['title']} ({movie['release_date'][:4]})\n"
            f"⭐ التقييم: {movie['vote_average']}/10\n"
            f"📖 القصة: {movie['overview']}\n"
            f"📸 ملصق الفيلم: https://image.tmdb.org/t/p/w500{movie['poster_path']}"
        )
    else:
        message = "⚠️ لم أجد أفلامًا من هذا النوع. جرب /suggest action!"
    
    await update.message.reply_text(message)

def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
     
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("suggest", suggest_movie))
    
    print("البوت يعمل! 🚀")
    app.run_polling()

if __name__ == "__main__":
    main()
