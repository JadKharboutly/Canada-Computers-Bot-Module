from discord_webhook import DiscordEmbed,DiscordWebhook
from bs4 import BeautifulSoup
from main import atc,shipping,payment,status
import emoji

import lxml
soup_atc = BeautifulSoup(atc.content, 'lxml')
image_url = str((soup_atc.find('img', attrs={'class':'img-inside'})['src']))
soup_price = BeautifulSoup(shipping.content, 'lxml')
price_tag = str(soup_price.find('span', attrs={'class':'float-right'})).split('<')
price = price_tag[1].split('>')[-1]
soup_name = BeautifulSoup(atc.content, 'lxml')
name = str(soup_name.find('a', attrs={'class':'text-dblue'})).split('<')[1].split('>')[-1].strip()
soup_location = BeautifulSoup(payment.content, 'lxml')
location = str(soup_location.find('div', attrs={'class':"row pt-1"})).split('<p>')[1].split('<br/>')[0]

webhook_url = DiscordWebhook(url='https://discord.com/api/webhooks/832073019970289704/7vb8FAqtPdKJqYo3cSH1h5cpEbdKzZLoRBcjFHyLH95k-FeFPuqOSgFTR2WWEO76VlvK')
if status == 1:
    embed = DiscordEmbed(title=emoji.emojize('CanadaComputers-V0.0.1 | Successful Checkout :white_check_mark: '), color='82EEFD')
else:
    embed = DiscordEmbed(title=emoji.emojize('CanadaComputers-V0.0.1 | Checkout Failed :x: '), color='FF0000')
# embed.set_image(url= image_url.replace('80x80','200x200'))
embed.set_thumbnail(url=image_url.replace('80x80','150x150'))
embed.set_timestamp()
embed.add_embed_field(name='Product', value=name, inline=False)
embed.add_embed_field(name='Price', value= price, inline=True)
embed.add_embed_field(name='Pickup Location:', value=location, inline=True)
embed.add_embed_field(name='Email:', value='Kharbouj@mcmaster.ca', inline=False)
webhook_url.add_embed(embed)
response = webhook_url.execute()