from pyrogram import Client
from pyrogram.types import Message
from moodle import delet
import random
from config import *

#cortesia de anonedev
bot = Client("bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)
auth = {}
proxy_list = ['0']

def crypt_char(char):
    map = '@./=#$%&:,;_-|0123456789abcd3fghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    i = 0
    for ch in map:
        if ch == char:
            return map[len(map) - 1 - i]
        i+=1
    return char

def proxydec(text):
    i = 0
    decryptText = ''
    while i < len(text):
        decryptText += crypt_char(text[i])
        i+=2
    return decryptText

@bot.on_message()
async def messages_control(c: Client, m: Message):
	usern = m.from_user.username
	msg = m.text
	
	if msg is None:
		msg = ''
		
	if usern == useradm:
		pass
	else:
		await m.reply('❌Sin acceso ponga su usuario omitiendo @')
		return
	
	if msg == '/start':
		await m.reply('Bienvenido '+usern+'👋\nSoy un bot de limpieza de moodles, puedes enviarme lo mismo un enlace que un txt borrare todo lo que me envies de la moodle, asi te ayudare a cuidarla😋')
		return
			
	if msg.startswith('/auth'):
		splitmsg = msg.split(' ')
		auth[usern] = {'user':splitmsg[1],'passw':splitmsg[2],'moodle':splitmsg[3]}
		
		await m.reply('Se guardaron las credenciales✅')
		return
	
	if '/proxy' in msg:
		proxysplit = msg.split(' ')[1]
		proxy_token = proxydec(proxysplit.split('://')[1]).split(':')
		ip = proxy_token[0]
		port = int(proxy_token[1])
		proxy_final = dict(https=f'socks5://{ip}:{port}', http=f'socks5://{ip}:{port}')
		proxy_list[0] = proxy_final
		await m.reply('Proxy guardado✅')
	
	if msg.startswith('https') or msg.startswith('http'):
		urlss = m.text
		proxy = None
		if proxy_list[0] != '0':
			proxy = proxy_list[0]
			
		if auth == {}:
			await m.reply('Debe configurar credenciales primero\n\nAqui un ejemplo👇\n\n/auth usuario contraseña https://eduvirtual.uho.edu.cu\n\nSi quiere añadir un proxy aqui tiene un ejemplo👇\n\n/proxy socks5://KHGDJEYFJKLGFKYGKGIDCEYKKHKKEGRKIFGEHKKDJF')
		else:
			msgedit = await m.reply("⌛Revisando autorizacion...\n")
			
			ret = delet(auth[usern]['user'],auth[usern]['passw'],auth[usern]['moodle'],urlss,proxy)
			if 'melogee' in ret:
				await msgedit.edit("Credenciales correctas✅")
				if 'borre' in ret:
					await msgedit.edit(f"Se borro de la moodle✅\n\nLoegate y accede para comprobarlo👇\n\n{urlss}")
				else:
					await msgedit.edit("Ocurrio un error al borrar,la moodle se encuentra caida en este mismo instante o incluso ban❌")
			else:
				await msgedit.edit("Credenciales invalidas o moodle caida❌")
	
	if m.document:
		proxy = None
		if proxy_list[0] != '0':
			proxy = proxy_list[0]
				
		if auth == {}:
			await m.reply('Debe configurar credenciales primero\n\nAqui un ejemplo👇\n\n/auth usuario contraseña https://eduvirtual.uho.edu.cu\n\nSi quiere añadir un proxy aqui tiene un ejemplo👇\n\n/proxy socks5://KHGDJEYFJKLGFKYGKGIDCEYKKHKKEGRKIFGEHKKDJF')
		else:
			txt = await c.download_media(m.document)
			msgeditt = await m.reply('⌛Extrayendo enlaces del txt...')
			
			with open(txt, 'r') as txtfile:
				txtlines = txtfile.read().split('\n')
				
				await msgeditt.edit('⏳Revisando autorizacion...')
				
				delurls = 0
				for line in txtlines:
					ret = delet(auth[usern]['user'],auth[usern]['passw'],auth[usern]['moodle'],line,proxy)
					
					if 'melogee' in ret:
						try:
							await msgeditt.edit("Credenciales correctas✅")
						except:
							pass
						
						if 'borre' in ret:
							delurls+= 1
							try:
								await msgeditt.edit(f"Se borro {delurls} enlaces de la nube☁")
							except:
								pass
							
							if len(txtlines) == delurls:
								await msgeditt.edit('TXT borrado exitosamente✅\nGracias por usar👋\nCreated by @anonedev')
								break

						else:
							await msgeditt.edit("Ocurrio un error al borrar❌")
							break
					else:
						await msgeditt.edit("Credenciales incorrectas❌")
						break
					
if __name__ == "__main__":
	print("Bot iniciado")
	bot.run()