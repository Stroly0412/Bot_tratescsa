from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ContextTypes, CommandHandler, ApplicationBuilder, MessageHandler, JobQueue, ConversationHandler, filters, CallbackContext, CallbackQueryHandler
import datetime, time
import urllib.parse
import requests

TOKEN = "7743298044:AAFx-U6VgWITNgX8XIyIlrYUeKlB7SSeK1k"
PSA,PAA, TAA, NAA, CA, ENDA, PSB, PAB, TAB, NAB, CB, ENDB, CONFIRM= range(13)
  
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

async def get_PSA( update: Update, context: ContextTypes.DEFAULT_TYPE ):
        await update.message.reply_text("Escribe la Presión de succicón del compresor A:")
        return PAA

async def get_PAA( update: Update, context: ContextTypes.DEFAULT_TYPE ):
        context.user_data["PSA"] = update.message.text
        await update.message.reply_text("Escribe la Presión de aceite del compresor A:")
        return TAA 

async def get_TAA( update: Update, context: ContextTypes.DEFAULT_TYPE ):
        context.user_data["PAA"] = update.message.text
        await update.message.reply_text("Escribe la Temperatura de aceite del compresor A:")
        return NAA
    
async def get_NAA( update: Update, context: ContextTypes.DEFAULT_TYPE ):
        context.user_data["TAA"] = update.message.text
        await update.message.reply_text("Escribe el nivel de aceite del compresor A:")
        return CA
    
async def get_CA( update: Update, context: ContextTypes.DEFAULT_TYPE ):
        context.user_data["NAA"] = update.message.text
        await update.message.reply_text("Escribe la corriente del compresor A:")
        return ENDA
   
async def get_ENDA( update: Update, context: ContextTypes.DEFAULT_TYPE ):
        context.user_data["CA"] = update.message.text
        await update.message.reply_text("Toma de Datos Compresor A, terminado.\nEscribe la Presión de succicón del compresor B:")
        return PAB

async def get_PAB( update: Update, context: ContextTypes.DEFAULT_TYPE ):
        context.user_data["PSB"] = update.message.text
        await update.message.reply_text("Escribe la Presión de aceite del compresor B:")
        return TAB  
   
async def get_TAB( update: Update, context: ContextTypes.DEFAULT_TYPE ):
        context.user_data["PAB"] = update.message.text
        await update.message.reply_text("Escribe la Temperatura de aceite del compresor B:")
        return NAB
    
async def get_NAB( update: Update, context: ContextTypes.DEFAULT_TYPE ):
        context.user_data["TAB"] = update.message.text
        await update.message.reply_text("Escribe el nivel de aceite del compresor B:")
        return CB
     
async def get_CB( update: Update, context: ContextTypes.DEFAULT_TYPE ):
        context.user_data["NAB"] = update.message.text
        await update.message.reply_text("Escribe la corriente del compresor B:")
        return ENDB
      
async def get_ENDB( update: Update, context: ContextTypes.DEFAULT_TYPE ):
        context.user_data["CB"] = update.message.text
        await update.message.reply_text(f"Info Compresor A: \nPresión succión {context.user_data['PSA']}PSI\nPresión aceite: {context.user_data['PAA']}PSI\nTemperatura aceite: {context.user_data['TAA']}°F\nNivel Aceite: {context.user_data['NAA']}%\nCorriente Compresor: {context.user_data['CA']}A\nInfo Compresor B: \nPresión succión {context.user_data['PSB']}PSI\nPresión aceite: {context.user_data['PAB']}PSI\nTemperatura aceite: {context.user_data['TAB']}°F\nNivel Aceite: {context.user_data['NAB']}%\nCorriente Compresor: {context.user_data['CB']}A")
        keyboard = ReplyKeyboardMarkup([
            [
                KeyboardButton("Si"),
                KeyboardButton("No")
            ]
        ])
        await update.message.reply_text("Los datos regitrados son correctos?",reply_markup=keyboard)
        return CONFIRM

async def get_CONFIRM ( update: Update, context: ContextTypes.DEFAULT_TYPE):
        if update.message.text == "Si":
            mensaje = f"""Info Compresor A:
            Presión succión {context.user_data['PSA']} PSI
            Presión aceite: {context.user_data['PAA']} PSI
            Temperatura aceite: {context.user_data['TAA']} °F
            Nivel Aceite: {context.user_data['NAA']}%
            Corriente Compresor: {context.user_data['CA']} A
            Info Compresor B:
            Presión succión {context.user_data['PSB']} PSI
            Presión aceite: {context.user_data['PAB']} PSI
            Temperatura aceite: {context.user_data['TAB']} °F
            Nivel Aceite: {context.user_data['NAB']}%
            Corriente Compresor: {context.user_data['CB']} A"""
            print(mensaje)
            
            # Codificación del mensaje en formato URL
            mensaje_codificado = urllib.parse.quote(mensaje)

            # URL para enviar el mensaje
            url = f"https://api.callmebot.com/whatsapp.php?phone=573167517733&text={mensaje_codificado}&apikey=4037050"

            # Envío de la solicitud HTTP GET
            response = requests.get(url)
            # Verificación de la respuesta
            if response.status_code == 200:
                print("Mensaje enviado con éxito")
                await update.message.reply_text("Datos Enviados")
            else:
                print(f"Error al enviar el mensaje: {response.status_code}")
            return ConversationHandler.END

        if update.message.text == "No":
            await update.message.reply_text("Envie cualquier mensaje para continuar con la correción.")
            return PSA
            
async def cancel_operation( update: Update, context: ContextTypes.DEFAULT_TYPE ):
        await update.message.reply_text("Operacion cancelada")
        return ConversationHandler.END
    
user_profile_controller_conversation_handler = ConversationHandler(

    entry_points=[CommandHandler("RUN", get_PSA)],
    states={
        PAA:    [MessageHandler(filters.TEXT & ~filters.COMMAND, get_PAA)],
        TAA:    [MessageHandler(filters.TEXT & ~filters.COMMAND, get_TAA)],
        NAA:    [MessageHandler(filters.TEXT & ~filters.COMMAND, get_NAA)],
        CA:     [MessageHandler(filters.TEXT & ~filters.COMMAND, get_CA)],
        ENDA:   [MessageHandler(filters.TEXT & ~filters.COMMAND, get_ENDA)],
        PAB:    [MessageHandler(filters.TEXT & ~filters.COMMAND, get_PAB)],
        TAB:    [MessageHandler(filters.TEXT & ~filters.COMMAND, get_TAB)],
        NAB:    [MessageHandler(filters.TEXT & ~filters.COMMAND, get_NAB)],
        CB:     [MessageHandler(filters.TEXT & ~filters.COMMAND, get_CB)],
        ENDB:   [MessageHandler(filters.TEXT & ~filters.COMMAND, get_ENDB)],
        CONFIRM:[MessageHandler(filters.TEXT & ~filters.COMMAND, get_CONFIRM)],
        PSA:    [MessageHandler(filters.TEXT & ~filters.COMMAND, get_PSA)]
    },
    fallbacks=[CommandHandler("CANCEL", cancel_operation)]
)

application = ApplicationBuilder().token(TOKEN).build()
application.add_handler(user_profile_controller_conversation_handler)
application.add_handler(CommandHandler("start",starting_get_info))
schedule_jobs(application.job_queue)
application.run_polling(allowed_updates=Update.ALL_TYPES)