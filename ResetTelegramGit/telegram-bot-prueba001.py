# coding=utf-8
import logging
import sys
import os
import subprocess
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import KeyboardButton, ReplyKeyboardMarkup


usuIdName = {"usuario1": num_chat_id1, "usuario2": num_chat_id2}
usuChatId = [num_chat_id1, num_chat_id2]
hostIps = ["IpServer1", "IpServer2"]
comandos = {"/echo": "Devuelve el mensaje mandado", "/caps": "Devuelve el argumento en mayusculas",
            "/stop": "Detiene el bot", "/multi_msg": "Manda un argumento a todos los integrantes del grupo",
            "/chat_id": "Devuelve la id del chat", "/reset": "Reinicia servidor '/reset_help' para mas info",
            "/read_logs": "Devuelve los ultimos logs, acepta argumentos para realizar un grep",
            "/write_logs": "Crea un log aceptando un argumento"}
host_name = os.popen("hostname").read()
route = "/usr/local/src/ResetTelegramGit/"
location_logs = "Datos_telegram/logs_telegram.txt"
# rebootServers = []

print("Vamos a empezar.")

updater = Updater(token='TokendelBot')
dispatcher = updater.dispatcher

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


def start(bot, update):
    write_logs(bot, update, ["/start"])
    bot.send_message(chat_id=update.message.chat_id, text="Yo soy un bot, Por favor hablame!")


def echo(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text=update.message.text)


# funcion para devolver los argumentos mandandos en mayusculas
def caps(bot, update, args):
    text_caps = ' '.join(args).upper()
    if text_caps == ' ':
        bot.send_message(chat_id=update.message.chat_id, text='Introduce argumentos al comando')
    else:
        write_logs(bot, update, ["/caps"])
        bot.send_message(chat_id=update.message.chat_id, text=text_caps)


def stop(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Cierro la conexion, vuelva a iniciarme en el script")
    write_logs(bot, update, ["/stop"])
    updater.stop()
    sys.exit(0)


def unknown(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Lo siento, No entiendo el comando.")


# testeame esta
def test(bot, update):
    kb = [[KeyboardButton('/help')],
          [KeyboardButton('/command2')]]
    kb_markup = ReplyKeyboardMarkup(kb)
    bot.send_message(chat_id=update.message.chat_id,
                     text="your message",
                     reply_markup=kb_markup)
    """kb = [[telegram.KeyboardButton("Option 1")],
          [telegram.KeyboardButton("Option 2")]]
    kb_markup = telegram(chat_id=update.message.chat_id, text="No se ", reply_markup=kb_markup)"""


# funcion para lanzar un mensaje a todos los usuarios
def multi_msg(bot, update, args):
    text_in = ' '.join(args)
    if text_in == ' ':
        bot.send_message(chat_id=update.message.chat_id, text='Introduce un argumento para mandar')
    else:
        for cId in usuChatId:
            write_logs(bot, update, ["/multi_msg"])
            bot.send_message(chat_id=cId, text=text_in)


# funcion para saber la id del usuario
def chat_id(bot, update):
    write_logs(bot, update, ["/chat_id"])
    bot.send_message(chat_id=update.message.chat_id, text=update.message.chat_id)


# funcion de reinicio de PC
def reset(bot, update, args):
    servers = args[:]

    bot.send_message(chat_id=update.message.chat_id, text=servers)
    # bot.send_message(chat_id=update.message.chat_id, text=servidores)
    # bot.send_message(chat_id=update.message.chat_id, text=args[1:])

    if not servers:
        bot.send_message(chat_id=update.message.chat_id, text="Introduzca el/los servidores a reiniciar")

    elif perm(bot, update) == "true":
        if servers[0] == "all":
            multi_msg(bot, update, "Reiniciando todos los servidores")
            write_logs(bot, update, ["/reset total"])
            # os.system("shutdown -r now")
            for rebootServer in hostIps:
                # Formateo de strings
                formatCommandReset = "{}{}{}".format("ssh root@", rebootServer, " shutdown -r now")
                formatCommandRestMyself = "shutdown -r now"

                # bot.send_message(chat_id=update.message.chat_id, text=formatCommandReset)
                if rebootServer != "IpServerMaestro":
                    os.system(formatCommandReset)
                else:
                    os.system(formatCommandRestMyself)

        elif servers[0] != "all":
            for server in servers:
                if server in hostIps:
                    bot.send_message(chat_id=update.message.chat_id,
                                     text="{}{}{}".format("El servidor ", server,
                                                          " existe y se procede a su reinicio."))
                    write_logs(bot, update, ["{}{}".format("/reset del servidor: ", server)])

                    if server != "IpServerMaestro":
                        os.system("{}{}{}".format("ssh root@", server, " shutdown -r now"))
                    else:
                        os.system("shutdown -r now")
                else:
                    bot.send_message(chat_id=update.message.chat_id, text="{}{}{}".format("El servidor ",
                                                                    server, " no existe y se cancela su reinicio."))


# funcion para habilitar los permisos
def perm(bot, update):
    key = [usuChatId[0], usuChatId[1]]

    if update.message.chat_id in key:
        bot.send_message(chat_id=update.message.chat_id, text="Aceptado")
        return "true"
    else:
        bot.send_message(chat_id=update.message.chat_id, text="Denegado")

    """if key == clv:
        if m.get('Ale') == update.message.chat_id:
            bot.send_message(chat_id=update.message.chat_id, text="Aceptado")
            return "true"
        else:
            bot.send_message(chat_id=update.message.chat_id, text="Denegado")
    else:
        bot.send_message(chat_id=update.message.chat_id, text="No estas autorizado")"""


# funcion de logs de comandos
def write_logs(bot, update, args):
    """Formateo de strings"""
    text_add = ' '.join(args)
    to_log = [os.popen("date").read()[:-1] + " ", host_name[:-1] + " ", update.message.chat_id, " " + text_add + "\n"]
    to_log_str = ''

    for tin_log in to_log:
        to_log_str += str(tin_log)

    # Formateo de strings
    to_open = "{}{}".format(route, location_logs)

    f = open(to_open, 'a')
    try:
        f.write(to_log_str)
        # bot.send_message(chat_id=update.message.chat_id, text="El log se ha creado correctamente")
    except:
        bot.send_message(chat_id=update.message.chat_id, text="Ha ocurrido un error al crear el log")

    f.close()


# funcion para leer los ultimos registros
def read_logs(bot, update, args):
    if not args:
        text_devuelto = subprocess.check_output(['tail', '-6', '{}{}'.format(route, location_logs)])

        if not text_devuelto:
            bot.send_message(chat_id=update.message.chat_id, text="El archivo de logs esta vacio")
        else:
            bot.send_message(chat_id=update.message.chat_id, text=text_devuelto)
    else:
        # Formateo de strings
        text_add = ' '.join(args)
        preComandDevuelto_args = "{}{}{}{}{}".format("cat ", route, location_logs, " | grep ", text_add)

        text_devuelto_args = os.popen(preComandDevuelto_args).read()

        if not text_devuelto_args:
            bot.send_message(chat_id=update.message.chat_id, text="No hay coincidencias")
        else:
            bot.send_message(chat_id=update.message.chat_id, text=text_devuelto_args)


# funcion que devuelve una lista de comandos disponibles
def help(bot, update):
    m = comandos
    text_in = ' '
    for c in m:
        text_in += c + ': ' + m.get(c) + '\n'
    write_logs(bot, update, ["/help"])
    bot.send_message(chat_id=update.message.chat_id, text=text_in)


def reset_help(bot, update):
    m = comandos
    text_in = ' '
    helpReset = {"/reset 'usuario' 'all'": "Formato para reiniciar todos los servidores",
                 "/reset 'usuario' 'servidor1' 'servidor2' ...": "Formato para reiniciar 1 o varios servidores"}
    for c in helpReset:
        bot.send_message(chat_id=update.message.chat_id, text="{}{}{}".format(c, " : ", helpReset.get(c)))
        text_in += c + ': ' + helpReset.get(c) + '\n'
    write_logs(bot, update, ["/reset_help"])
    bot.send_message(chat_id=update.message.chat_id, text=text_in)


updater.start_polling()
start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

echo_handler = MessageHandler(Filters.text, echo)
dispatcher.add_handler(echo_handler)

caps_handler = CommandHandler('caps', caps, pass_args=True)
dispatcher.add_handler(caps_handler)

stop_handler = CommandHandler('stop', stop)
dispatcher.add_handler(stop_handler)

chat_id_handler = CommandHandler('chat_id', chat_id)
dispatcher.add_handler(chat_id_handler)

# test_handler = CommandHandler('test', test)
# dispatcher.add_handler(test_handler)

multi_msg_handler = CommandHandler('multi_msg', multi_msg, pass_args=True)
dispatcher.add_handler(multi_msg_handler)

reset_handler = CommandHandler('reset', reset, pass_args=True)
dispatcher.add_handler(reset_handler)

write_logs_handler = CommandHandler('write_logs', write_logs, pass_args=True)
dispatcher.add_handler(write_logs_handler)

read_logs_handler = CommandHandler('read_logs', read_logs, pass_args=True)
dispatcher.add_handler(read_logs_handler)

help_handler = CommandHandler('help', help)
dispatcher.add_handler(help_handler)

reset_help_handler = CommandHandler('reset_help', reset_help)
dispatcher.add_handler(reset_help_handler)

# perm_handler = CommandHandler('perm', perm)
# dispatcher.add_handler(perm_handler)

unknown_handler = MessageHandler(Filters.command, unknown)
dispatcher.add_handler(unknown_handler)

print("Estoy en linea.")
