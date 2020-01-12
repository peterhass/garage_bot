
from telegram.ext import Updater, CommandHandler, Filters
from .door_controller import DoorController, UnexpectedDoorStateException
from .door_io import DoorIO
from .bot_commands import BotCommands
from .config import Config
import logging

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
        command_args = { 'filters': chat_filter, 'pass_job_queue':True }
    
        dispatcher.add_handler(CommandHandler('garage_status', commands.status, **command_args))
        dispatcher.add_handler(CommandHandler('garage_auf', commands.open_door, **command_args))
        dispatcher.add_handler(CommandHandler('garage_zu', commands.close_door, **command_args))
    
        updater.start_polling()
        updater.idle()
        io.cleanup()
