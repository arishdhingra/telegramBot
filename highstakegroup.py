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

def percentage(percentage, number):
    percent = percentage + 100
    multiplier = percent/100
    return number*multiplier

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
        logger.error(f"Could not find any output  channels in the user's dialogs")
        sys.exit(1)

    if not input_channels_entities:
        logger.error(f"Could not find any input channels in the user's dialogs")
        sys.exit(1)

    logging.info(f"Listening on {len(input_channels_entities)} channels. Forwarding messages to {len(output_channel_entities)} channels.")

    @client.on(events.NewMessage(chats=input_channels_entities))
    async def handler(event):
        for output_channel in output_channel_entities:
            if ("Binance" not in event.text):

                #examining the input
                command = event.text
                commandarray = command.split();
                coin = commandarray[0]
                side = commandarray[1]
                leverage = commandarray[2]

                #getting the current price of coin
                response = requests.get("https://api.binance.com/api/v3/ticker/price?symbol="+coin+"USDT")
                responseJSON = response.json()
                priceStr = responseJSON['price']
                currPrice = float(priceStr)

                #checking if short or long
                if (side == "L"):
                    entry1 = str("{:.4f}".format(percentage(-0.2,currPrice)))
                    entry2 = str("{:.4f}".format(percentage(0.2,currPrice)))
                    target1 = str("{:.4f}".format(percentage(1,currPrice)))
                    target2 = str("{:.4f}".format(percentage(2,currPrice)))
                    target3 = str("{:.4f}".format(percentage(3,currPrice)))
                    target4 = str("{:.4f}".format(percentage(4,currPrice)))
                    stoploss = str("{:.4f}".format(percentage(-4,currPrice)))
                    line1 = coin+"/USDT #LONG"
                    line2 = "MEXC, Binance Futures, Kucoin, Phemex, ftx, Bybit USDT"
                    line3 = "Leverage "+leverage+"x"
                    line4 = "Buy "+entry1+"-"+entry2
                    line5 = "Sell "+ target1+", "+ target2+", "+ target3+", "+ target4
                    line6 = "Stop "+stoploss
                    signalFinal = line1+"\n"+line2+"\n"+line3+"\n"+line4+"\n"+line5+"\n"+line6
                    webhook = DiscordWebhook(url='https://discord.com/api/webhooks/1046903787232698408/YipyctAoGZvXJVv02GiT6FqRb3UEPkIZD3KOdKtz4_vwL7mJv113ijedqk_TxsW0jQkY', content=signalFinal)
                    response = webhook.execute()
                    await client.send_message(output_channel, signalFinal)

                else:
                    entry1 = str("{:.4f}".format(percentage(-0.2,currPrice)))
                    entry2 = str("{:.4f}".format(percentage(0.2,currPrice)))
                    target1 = str("{:.4f}".format(percentage(-1,currPrice)))
                    target2 = str("{:.4f}".format(percentage(-2,currPrice)))
                    target3 = str("{:.4f}".format(percentage(-3,currPrice)))
                    target4 = str("{:.4f}".format(percentage(-4,currPrice)))
                    stoploss = str("{:.4f}".format(percentage(4,currPrice)))
                    line1 = coin+"/USDT #SHORT"
                    line2 = "Binance Futures, Kucoin, Phemex, ftx, Bybit USDT"
                    line3 = "Leverage "+leverage+"x"
                    line4 = "Buy "+entry1+"-"+entry2
                    line5 = "Sell "+ target1+", "+ target2+", "+ target3+", "+ target4
                    line6 = "Stop "+stoploss
                    signalFinal = line1+"\n"+line2+"\n"+line3+"\n"+line4+"\n"+line5+"\n"+line6
                    webhook = DiscordWebhook(url='https://discord.com/api/webhooks/1046903787232698408/YipyctAoGZvXJVv02GiT6FqRb3UEPkIZD3KOdKtz4_vwL7mJv113ijedqk_TxsW0jQkY', content=signalFinal)
                    response = webhook.execute()
                    await client.send_message(output_channel, signalFinal)

    client.run_until_disconnected()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} {{CONFIG_PATH}}")
        sys.exit(1)
    with open(sys.argv[1], 'rb') as f:
        config = yaml.safe_load(f)
    start(config)
