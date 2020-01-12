# garage_bot

Allows to control garage doors using a telegram bot. 

## Installation

- (needed on raspbian) `apt-get install libffi-dev python3-dev libssl-dev`
- `python3 setup.py install`

## Configuration

- `garage_bot_config config > /etc/garage_bot.conf`
- Telegram: Create new bot in bot father
- Set bot_token in `/etc/garage_bot.conf`
- Add bot to some private group (everybody in this group will be able to use the bot!)
- Set chat_id in `/etc/garage_bot.conf` (try `log_level=DEBUG` to find your group's chat_id)
- `garage_bot`

### Systemd

(tested on raspbian)

- `garage_bot_config systemd > /lib/systemd/system/garage_bot.service` 
- `systemctl daemon-reload`
- `systemctl enable garage_bot.service`
- `systemctl start garage_bot.service`
