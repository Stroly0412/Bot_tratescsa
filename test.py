from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CommandHandler, ApplicationBuilder, MessageHandler, JobQueue, ConversationHandler, filters
import datetime, time

TOKEN = "7743298044:AAFx-U6VgWITNgX8XIyIlrYUeKlB7SSeK1k"

from Controllers.data_acquisition import user_profile_controller_conversation_handler
   
application = ApplicationBuilder().token(TOKEN).build()
application.add_handler( user_profile_controller_conversation_handler )

 # Variable global para almacenar el chat_id
chat_id = None

async def starting_get_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global chat_id
    chat_id = update.effective_chat.id  # Guardar el chat_id
    await update.message.reply_text("Bienvenido al sistema de toma de datos de tratecsa. Este bot solicita el ingreso de variables operativas cada dia de 9pm a 7am, estos datos van directamente a gerenia.")

async def send_scheduled_message(context: ContextTypes.DEFAULT_TYPE):
    # Enviar el mensaje de bienvenida automáticamente al chat guardado
    if chat_id:
        await context.bot.send_message(chat_id=chat_id, text="Bienvenido al sistema de toma de datos de tratecsa. Para comenzar click aqui /RUN, para cancelar en cualquier momento click aqui /CANCEL")

def schedule_jobs(job_queue: JobQueue):
    # Configurar el horario de envío (cada hora entre 9 PM y 7 AM)
    now = datetime.datetime.now()
    start_time = now.replace(hour=21, minute=0, second=0, microsecond=0)
    end_time = now.replace(hour=7, minute=0, second=0, microsecond=0) + datetime.timedelta(days=1)

    # Programar el trabajo cada hora dentro del rango
    current_time = start_time
    while current_time <= end_time:
        job_queue.run_repeating(send_scheduled_message, interval=3600, first=current_time)
        current_time += datetime.timedelta(hours=1)

application.add_handler(CommandHandler("start",starting_get_info))
# Programar el mensaje automático al iniciar el bot
schedule_jobs(application.job_queue)

application.run_polling(allowed_updates=Update.ALL_TYPES)