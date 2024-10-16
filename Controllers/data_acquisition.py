import urllib.parse
import requests
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import filters, ConversationHandler, \
CommandHandler, MessageHandler, ContextTypes, CallbackContext, CallbackQueryHandler



PSA,PAA, TAA, NAA, CA, ENDA, PSB, PAB, TAB, NAB, CB, ENDB, CONFIRM= range(13)

class UserProfileController:
 
    @staticmethod
    async def get_PSA( update: Update, context: ContextTypes.DEFAULT_TYPE ):
        await update.message.reply_text("Escribe la Presión de succicón del compresor A:")
        return PAA

    @staticmethod
    async def get_PAA( update: Update, context: ContextTypes.DEFAULT_TYPE ):
        context.user_data["PSA"] = update.message.text
        await update.message.reply_text("Escribe la Presión de aceite del compresor A:")
        return TAA
    
    @staticmethod
    async def get_TAA( update: Update, context: ContextTypes.DEFAULT_TYPE ):
        context.user_data["PAA"] = update.message.text
        await update.message.reply_text("Escribe la Temperatura de aceite del compresor A:")
        return NAA
    
    @staticmethod
    async def get_NAA( update: Update, context: ContextTypes.DEFAULT_TYPE ):
        context.user_data["TAA"] = update.message.text
        await update.message.reply_text("Escribe el nivel de aceite del compresor A:")
        return CA
    
    @staticmethod
    async def get_CA( update: Update, context: ContextTypes.DEFAULT_TYPE ):
        context.user_data["NAA"] = update.message.text
        await update.message.reply_text("Escribe la corriente del compresor A:")
        return ENDA
    
    @staticmethod
    async def ENDA( update: Update, context: ContextTypes.DEFAULT_TYPE ):
        context.user_data["CA"] = update.message.text
        await update.message.reply_text("Toma de Datos Compresor A, terminado.\nEscribe la Presión de succicón del compresor B:")
        return PAB

    @staticmethod
    async def get_PAB( update: Update, context: ContextTypes.DEFAULT_TYPE ):
        context.user_data["PSB"] = update.message.text
        await update.message.reply_text("Escribe la Presión de aceite del compresor B:")
        return TAB
    
    @staticmethod
    async def get_TAB( update: Update, context: ContextTypes.DEFAULT_TYPE ):
        context.user_data["PAB"] = update.message.text
        await update.message.reply_text("Escribe la Temperatura de aceite del compresor B:")
        return NAB
    
    @staticmethod
    async def get_NAB( update: Update, context: ContextTypes.DEFAULT_TYPE ):
        context.user_data["TAB"] = update.message.text
        await update.message.reply_text("Escribe el nivel de aceite del compresor B:")
        return CB
    
    @staticmethod
    async def get_CB( update: Update, context: ContextTypes.DEFAULT_TYPE ):
        context.user_data["NAB"] = update.message.text
        await update.message.reply_text("Escribe la corriente del compresor B:")
        return ENDB
    
    @staticmethod
    async def ENDB( update: Update, context: ContextTypes.DEFAULT_TYPE ):
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

    @staticmethod    
    async def CONFIRM ( update: Update, context: ContextTypes.DEFAULT_TYPE):
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
            else:
                print(f"Error al enviar el mensaje: {response.status_code}")
            return ConversationHandler.END

        if update.message.text == "No":
            await update.message.reply_text("Envie cualquier mensaje para continuar con la correción.")
            return PSA
            

    @staticmethod
    async def cancel_operation( update: Update, context: ContextTypes.DEFAULT_TYPE ):
        await update.message.reply_text("Operacion cancelada")
        return ConversationHandler.END
    
user_profile_controller_conversation_handler = ConversationHandler(

    entry_points=[CommandHandler("RUN", UserProfileController.get_PSA)],
    states={
        PAA:    [MessageHandler(filters.TEXT & ~filters.COMMAND, UserProfileController.get_PAA)],
        TAA:    [MessageHandler(filters.ALL & ~filters.COMMAND, UserProfileController.get_TAA)],
        NAA:    [MessageHandler(filters.ALL & ~filters.COMMAND, UserProfileController.get_NAA)],
        CA:     [MessageHandler(filters.ALL & ~filters.COMMAND, UserProfileController.get_CA)],
        ENDA:   [MessageHandler(filters.ALL & ~filters.COMMAND, UserProfileController.ENDA)],
        PAB:    [MessageHandler(filters.TEXT & ~filters.COMMAND, UserProfileController.get_PAB)],
        TAB:    [MessageHandler(filters.ALL & ~filters.COMMAND, UserProfileController.get_TAB)],
        NAB:    [MessageHandler(filters.ALL & ~filters.COMMAND, UserProfileController.get_NAB)],
        CB:     [MessageHandler(filters.ALL & ~filters.COMMAND, UserProfileController.get_CB)],
        ENDB:   [MessageHandler(filters.ALL & ~filters.COMMAND, UserProfileController.ENDB)],
        CONFIRM:[MessageHandler(filters.ALL & ~filters.COMMAND, UserProfileController.CONFIRM)],
        PSA:    [MessageHandler(filters.ALL & ~filters.COMMAND, UserProfileController.get_PSA)]
    },
    fallbacks=[CommandHandler("CANCEL", UserProfileController.cancel_operation)]
)