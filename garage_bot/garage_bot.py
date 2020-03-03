
from datetime import datetime, timedelta
from telegram.ext import Updater, CommandHandler, Filters, BaseFilter
from .door_controller import DoorController, UnexpectedDoorStateException
from .door_io import DoorIO
from .bot_commands import BotCommands
from .config import Config
import logging

class _RecentFilter(BaseFilter):
    def filter(self, message):
        threshold = datetime.utcnow() - timedelta(seconds = 80)

        return message.date > threshold


class GarageBot:
    def __init__(self):
        config = Config('/etc/garage_bot.conf')
        log_levels = {
                'DEBUG': logging.DEBUG,
                'INFO': logging.INFO,
                'ERROR': logging.ERROR
                }
        
        logger = logging.getLogger()
        logger.setLevel(log_levels[config.log_level])
        
        logging.info("Init ...")
        io = DoorIO()
        try:
            door_controller = DoorController(door_io=io)
            commands = BotCommands(door_controller=door_controller)
            logging.info("Init COMPLETE")
        except:
            io.cleanup()
            raise

        self.config = config
        self.io = io
        self.commands = commands
        
        
        
    def run(self):
        config = self.config
        commands = self.commands
        io = self.io

        updater = Updater(config.bot_token, use_context=True)
    
        dispatcher = updater.dispatcher
    
        chat_filter = Filters.chat(int(config.group_chat_id))
        recent_filter = _RecentFilter()
        command_args = { 'filters': chat_filter & recent_filter, 'pass_job_queue':True }
    
        dispatcher.add_handler(CommandHandler('garage_status', commands.status, **command_args))
        dispatcher.add_handler(CommandHandler('garage_auf', commands.open_door, **command_args))
        dispatcher.add_handler(CommandHandler('garage_zu', commands.close_door, **command_args))
    
        updater.start_polling()
        updater.idle()
        io.cleanup()
