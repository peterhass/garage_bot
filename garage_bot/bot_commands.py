from telegram.ext import Updater, CommandHandler
from .door_controller import UnexpectedDoorStateException

class BotCommands:
    def __init__(self, door_controller=None):
        self.door = door_controller

    def status(self, update, context):
        text = 'Garage ist geschlossen'
        if self.door.is_open:
            text = "Garage ist offen"

        update.message.reply_text(text)

    def open_door(self, update, context):
        if not self.door.can_open:
            update.message.reply_text("Garage kann nicht geoffnet werden! Aktueller Status: {}".format(self.door.status_text)) 
            return

        context.job_queue.run_once(self.__open_door_job, 1, context=update.message.chat_id)

    def __open_door_job(self, context):
        chat_id = context.job.context

        context.bot.send_message(chat_id=chat_id, text="Garage wird geoeffnet ...")
        try:
            self.door.open()
            context.bot.send_message(chat_id=chat_id, text="Garage offen!")
        except UnexpectedDoorStateException as e:
            context.bot.send_message(chat_id=chat_id, text="Problem beim oeffnen des Tores: {}".format(e))

    def close_door(self, update, context):
        if not self.door.can_close:
            update.message.reply_text("Garage kann nicht geschlossen werden! Aktueller Status: {}".format(self.door.status_text)) 
            return

        context.job_queue.run_once(self.__close_door_job, 1, context=update.message.chat_id)


    def __close_door_job(self, context):
        chat_id = context.job.context

        context.bot.send_message(chat_id=chat_id, text="Garage wird geschlossen...")
        try:
            self.door.close()
            context.bot.send_message(chat_id=chat_id, text="Garage geschlossen.")
        except UnexpectedDoorStateException as e:
            context.bot.send_message(chat_id=chat_id, text="Problem beim schliessen des Tores: {}".format(e))
