from telethon import TelegramClient, events, sync
from telethon.tl.types import InputChannel
import yaml
import sys
import logging
import requests
from discord_webhook import DiscordWebhook

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logging.getLogger('telethon').setLevel(level=logging.WARNING)
logger = logging.getLogger(__name__)

def increment():
    with open('/home/ec2-user/premiumForwarder/count.txt', 'r+') as f:
        lines = f.readlines()
        curr = int(lines[0])
        incr = curr+1
        f.seek(0)
        f.truncate()
        lines[0] = str(incr)
        f.write(lines[0])
        if ((incr%2)==0):
            return "even"
        return "odd"

def start(config):
    client = TelegramClient(config["session_name"], config["api_id"], config["api_hash"])
    client.start()
    print(client)
    print("starting the client. please wait....")
    input_channels_entities = []
    output_channel_entities = []
    for d in client.iter_dialogs():
        if d.name in config["input_channel_names"] or d.entity.id in config["input_channel_ids"]:
            input_channels_entities.append(InputChannel(d.entity.id, d.entity.access_hash))
        if d.name in config["output_channel_names"] or d.entity.id in config["output_channel_ids"]:
            output_channel_entities.append(InputChannel(d.entity.id, d.entity.access_hash))

    if not output_channel_entities:
        logger.error(f"Could not find any output channels in the user's dialogs")
        sys.exit(1)

    if not input_channels_entities:
        logger.error(f"Could not find any input channels in the user's dialogs")
        sys.exit(1)

    logging.info(f"Listening on {len(input_channels_entities)} channels. Forwarding messages to {len(output_channel_entities)} channels.")

    @client.on(events.NewMessage(chats=input_channels_entities))
    async def handler(event):
        for output_channel in output_channel_entities:
            if ("Take-Profit target 1" in event.text):
                indexStart = event.text.index("Profit:") + len('Profit:') + 1
                indexEnd = event.text.index("%") + len('%') - 1
                percentage = event.text[indexStart:indexEnd]
                Float = float(percentage)
                Float = Float+15
                percentage1 = str("{:.2f}".format(Float))
                event.text = event.text.replace(percentage, percentage1)
                webhook = DiscordWebhook(url='https://discord.com/api/webhooks/1047002920933130260/01Y_QZmyN5ITfz0Q2ofd1IrreuIxxIQuBSjEhjXTW7bVIgnV_5wW84nvXUWffSVITT4o', content=event.message)
                response = webhook.execute()
                await client.send_message(output_channel, event.message)
            elif ("Take-Profit target 2" in event.text):
                indexStart = event.text.index("Profit:") + len('Profit:') + 1
                indexEnd = event.text.index("%") + len('%') - 1
                percentage = event.text[indexStart:indexEnd]
                Float = float(percentage)
                Float = Float+30
                percentage1 = str("{:.2f}".format(Float))
                event.text = event.text.replace(percentage, percentage1)
                webhook = DiscordWebhook(url='https://discord.com/api/webhooks/1047002920933130260/01Y_QZmyN5ITfz0Q2ofd1IrreuIxxIQuBSjEhjXTW7bVIgnV_5wW84nvXUWffSVITT4o', content=event.message)
                response = webhook.execute()
                await client.send_message(output_channel, event.message)
            elif ("Take-Profit target 3" in event.text):
                indexStart = event.text.index("Profit:") + len('Profit:') + 1
                indexEnd = event.text.index("%") + len('%') - 1
                percentage = event.text[indexStart:indexEnd]
                Float = float(percentage)
                Float = Float+50
                percentage1 = str("{:.2f}".format(Float))
                event.text = event.text.replace(percentage, percentage1)
                webhook = DiscordWebhook(url='https://discord.com/api/webhooks/1047002920933130260/01Y_QZmyN5ITfz0Q2ofd1IrreuIxxIQuBSjEhjXTW7bVIgnV_5wW84nvXUWffSVITT4o', content=event.message)
                response = webhook.execute()
                await client.send_message(output_channel, event.message)
            elif ("All take-profit targets" in event.text):
                indexStart = event.text.index("Profit:") + len('Profit:') + 1
                indexEnd = event.text.index("%") + len('%') - 1
                percentage = event.text[indexStart:indexEnd]
                Float = float(percentage)
                Float = Float+75
                percentage1 = str("{:.2f}".format(Float))
                event.text = event.text.replace(percentage, percentage1)
                webhook = DiscordWebhook(url='https://discord.com/api/webhooks/1047002920933130260/01Y_QZmyN5ITfz0Q2ofd1IrreuIxxIQuBSjEhjXTW7bVIgnV_5wW84nvXUWffSVITT4o', content=event.message)
                response = webhook.execute()
                await client.send_message(output_channel, event.message)
            elif ("Phemex, ftx" in event.text):
                value = increment()
                string = event.text.split()[0]
                client.parse_mode = 'html'
                newStr = "🤩 <b>PREMIUM GROUP SIGNAL ALERT</b> 🤩 \n \n " \
                         "<b>#"+string+"</b> is posted in premium group.🔥 \n \n" \
                                    " <b>LONG OR SHORT?</b> Only premium members know that 🤔 \n \n " \
                                    "DIRECTION WILL BE REVEALED TO <b>FREE MEMBERS AFTER T1</b> IS HIT ✅ \n \n " \
                                    "<b>UNMUTE</b> the channel now 🤩 \n \n " \
                                    "<b>Message @highrollertraders now to enroll in premium.</b> \n \n " \
                                    "💎<b>CORNIX BOT AVAILABLE FOR FREE</b>💎"
                if(value=="even"):
                    webhook = DiscordWebhook(url='https://discord.com/api/webhooks/1047002920933130260/01Y_QZmyN5ITfz0Q2ofd1IrreuIxxIQuBSjEhjXTW7bVIgnV_5wW84nvXUWffSVITT4o', content='#'+string+' is posted in premium group.🔥')
                    response = webhook.execute()
                    await client.send_message(output_channel, newStr)
            else:
                print("*")

    client.run_until_disconnected()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} {{CONFIG_PATH}}")
        sys.exit(1)
    with open(sys.argv[1], 'rb') as f:
        config = yaml.safe_load(f)
    start(config)
