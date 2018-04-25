# coding=utf-8
import logging
import sys
import os
import subprocess
import time
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram import KeyboardButton, ReplyKeyboardMarkup
from telegram import ReplyKeyboardRemove

usuIdName = {"Ale": 448634285, "Artemi": 6471791}
usuChatId = [448634285, 6471791]
hostIps = ["10.0.1.91", "10.2.34.65", "10.2.34.63", "10.0.1.26"]
host_name = os.popen("hostname").read()
route = "/usr/local/src/telegram/"
location_logs = "Datos_telegram/logs_telegram.txt"
comandos = {"/echo": "Devuelve el mensaje mandado", "/caps": "Devuelve el argumento en mayusculas",
            "/stop": "Detiene el bot", "/multi_msg": "Manda un argumento a todos los integrantes del grupo",
            "/chat_id": "Devuelve la id del chat", "/reboot": "Reinicio de servidores",
            "/read_logs": "Devuelve los ultimos logs, acepta argumentos para realizar un grep",
            "/write_logs": "Crea un log aceptando un argumento"}
rebootServers = []

print("Vamos a empezar.")

updater = Updater(token='427931544:AAEdDnK2cAqh2HtJZnPTORHhAOp1L8LupfE')
dispatcher = updater.dispatcher

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


def start(bot, update):
    write_logs(bot, update, ["/start"])
    bot.send_message(chat_id=update.message.chat_id, text="Yo soy un bot, Por favor hablame!")


def echo(bot, update):  # disabled
    bot.send_message(chat_id=update.message.chat_id, text=update.message.text)


# funcion para devolver los argumentos mandandos en mayusculas
def caps(bot, update, args):
    text_caps = ' '.join(args).upper()
    if text_caps == ' ':
        bot.send_message(chat_id=update.message.chat_id, text='Introduce argumentos al comando')
    else:
        write_logs(bot, update, ["/caps"])
        bot.send_message(chat_id=update.message.chat_id, text=text_caps)


def stop(bot, update): # disabled
    bot.send_message(chat_id=update.message.chat_id, text="Cierro la conexion, vuelva a iniciarme en el script")
    write_logs(bot, update, ["/stop"])
    updater.stop()
    sys.exit(0)


def unknown(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Lo siento, No entiendo el comando.")


# testeame esta
def reboot(bot, update):
    """ reset interfaz"""
    kb_server = []

    for server in hostIps:
        if server not in rebootServers:
            kb_server.append([InlineKeyboardButton(server, callback_data=server)])
    kb_server.insert(0, [InlineKeyboardButton("All", callback_data="all")])
    # kb_server.append([InlineKeyboardButton("All", callback_data="all")])

    """kb_server = [[InlineKeyboardButton(u'11', callback_data='1')],
                 [InlineKeyboardButton(u'22', callback_data='2')],
                 [InlineKeyboardButton(u'33', callback_data='3')]]"""

    reply_markup = InlineKeyboardMarkup(kb_server)

    update.message.reply_text('Seleccione el servidor que desea reiniciar: ', reply_markup=reply_markup)


def teclado(bot, update):
    kb_servert = [["/reboot"], ["/reset"], ["/read_logs"]]

    kb_markup = ReplyKeyboardMarkup(kb_servert)

    bot.send_message(chat_id=update.message.chat_id, text="Elige una opcion", reply_markup=kb_markup)

    time.sleep(5)
    bot.send_message(chat_id=update.message.chat_id, text="Elige una opcion",
                     reply_markup=ReplyKeyboardRemove(kb_servert))


def button(bot, update):
    query = update.callback_query

    # "Selected option: {}".format( )
    # bot.edit_message_text(text=query.data, chat_id=query.message.chat_id, message_id=query.message.message_id)

    admision = [[InlineKeyboardButton("Reiniciar", callback_data="reset"),
                 InlineKeyboardButton("Cancelar", callback_data="cancel")]]

    reply_markupt = InlineKeyboardMarkup(admision)

    if query.data == "cancel":
        bot.answerCallbackQuery(callback_query_id=update.callback_query.id,
                                text="Se cancela el proceso de reinicio del servidor: {}".format(rebootServers[-1]))
        bot.send_message(text="Escriba '/reboot' para repetir la orden",
                         chat_id=query.message.chat_id,
                         message_id=query.message.message_id)

        del rebootServers[:]

    elif query.data == "reset":
        bot.answerCallbackQuery(callback_query_id=update.callback_query.id,
                                text="Procedemos al reinicio del servidor: {}".format(rebootServers[-1]))
        bot.send_message(text="Escriba '/reboot' para repetir la orden",
                         chat_id=query.message.chat_id,
                         message_id=query.message.message_id)
        """
        bot.send_message(text="Procedemos al reinicio del servidor: {}".format(rebootServers[-1]),
                         chat_id=query.message.chat_id,
                         message_id=query.message.message_id)
        """
        reset(bot, update, rebootServers[-1])

    elif query.data == "all":
        rebootServers.append(query.data)
        bot.answerCallbackQuery(callback_query_id=update.callback_query.id,
                                text="Procedemos al reinicio todos los servidores")
        """
        bot.send_message(text="Procedemos al reinicio todos los servidores",
                         chat_id=query.message.chat_id,
                         message_id=query.message.message_id)
        """
        reset(bot, update, rebootServers[-1])
    else:
        bot.answerCallbackQuery(callback_query_id=update.callback_query.id, text="Procesando...")
        rebootServers.append(query.data)
        bot.send_message(text="¿Desea Reiniciar el servidor? {}".format(query.data), chat_id=query.message.chat_id,
                         message_id=query.message.message_id,
                         reply_markup=reply_markupt)

    """String_rebootServers = ''


    for serv in rebootServers:
        String_rebootServers += ''.join(serv) + ' '


    bot.edit_message_text(text="Servers a reinciar: {}, si quiere añadir otro haga '/test'".format(String_rebootServers),
                          chat_id=query.message.chat_id,
                          message_id=query.message.message_id)"""


# funcion para lanzar un mensaje a todos los usuarios
def multi_msg(bot, update, args):
    text_in = ' '.join(args)
    if text_in == ' ':
        bot.send_message(chat_id=update.message.chat_id, text='Introduce un argumento para mandar')
    else:
        for cId in usuChatId:
            write_logs(bot, update, ["/multi_msg"])
            bot.send_message(chat_id=cId, text=text_in)


# funcion para lanzar un mensaje a todos los usuarios con query
def multi_msg_query(bot, update, args):
    text_in = ' '.join(args)
    for cId in usuChatId:
        write_logs_query(bot, update, ["/multi_msg"])
        bot.send_message(text=text_in,
                         chat_id=cId,
                         message_id=update.callback_query.message.message_id)


# funcion para saber la id del usuario
def chat_id(bot, update):
    write_logs(bot, update, ["/chat_id"])
    bot.send_message(chat_id=update.message.chat_id, text=update.message.chat_id)


# funcion de reinicio de PC
def reset(bot, update, args):
    servers = [args[:]]

    """
    bot.send_message(text=servers,
                     chat_id=update.callback_query.message.chat_id,
                     message_id=update.callback_query.message.message_id)
    """

    if not servers:
        # bot.send_message(chat_id=update.message.chat_id, text="Introduzca el/los servidores a reiniciar")
        bot.send_message(text="Introduzca el/los servidores a reiniciar",
                         chat_id=update.callback_query.message.chat_id,
                         message_id=update.callback_query.message.message_id)

    elif perm(bot, update) == "true":
        if servers[0] == "all":
            multi_msg_query(bot, update, "Reiniciando todos los servidores")
            write_logs_query(bot, update, ["/reset total"])
            # os.system("shutdown -r now")
            for rebootServer in hostIps:
                # Formateo de strings
                formatCommandReset = "{}{}{}".format("ssh root@", rebootServer, " shutdown -r now")
                formatCommandRestMyself = "shutdown -r now"

                # bot.send_message(chat_id=update.message.chat_id, text=formatCommandReset)
                if rebootServer != "10.0.1.26":
                    os.system(formatCommandReset)
                else:
                    os.system(formatCommandRestMyself)
            del rebootServers[:]
            print rebootServers[:]

        elif servers[0] != "all":
            if servers[0] in hostIps:
                """
                bot.send_message(text="{}{}{}".format("El servidor ", servers[0],
                                                      " existe y se procede a su reinicio."),
                                 chat_id=update.callback_query.message.chat_id,
                                 message_id=update.callback_query.message.message_id)
                """
                write_logs_query(bot, update, ["{}{}".format("/reset del servidor: ", servers[0])])

                if servers[0] != "10.0.1.26":
                    os.system("{}{}{}".format("ssh root@", servers[0], " shutdown -r now"))
                else:
                    os.system("shutdown -r now")

            else:
                bot.send_message(text="{}{}{}".format("El servidor ", servers[0],
                                                      " no existe y se cancela su reinicio."),
                                 chat_id=update.callback_query.message.chat_id,
                                 message_id=update.callback_query.message.message_id)
            del rebootServers[:]
            # print rebootServers[:]


# funcion para habilitar los permisos
def perm(bot, update):
    key = [usuChatId[0], usuChatId[1]]

    if update.callback_query.message.chat_id in key:
        bot.send_message(text="Permiso aceptado",
                         chat_id=update.callback_query.message.chat_id,
                         message_id=update.callback_query.message.message_id)
        # bot.send_message(chat_id=update.message.chat_id, text="Aceptado")
        return "true"
    else:
        bot.send_message(text="Permiso denegado",
                         chat_id=update.callback_query.message.chat_id,
                         message_id=update.callback_query.message.message_id)
        # bot.send_message(chat_id=update.message.chat_id, text="Denegado")

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


# funcion de logs de comandos query
def write_logs_query(bot, update, args):
    """Formateo de strings"""
    text_add = ' '.join(args)
    to_log = [os.popen("date").read()[:-1] + " ", host_name[:-1] + " ", update.callback_query.message.chat_id,
              " " + text_add + "\n"]
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
        bot.send_message(text="Ha ocurrido un error al crear el log",
                         chat_id=update.callback_query.message.chat_id,
                         message_id=update.callback_query.message.message_id)

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
    text_in = ' '  # type: str
    for c in m:
        text_in += c + ': ' + m.get(c) + '\n'
    write_logs(bot, update, ["/help"])
    bot.send_message(chat_id=update.message.chat_id, text=text_in)


updater.start_polling()
start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

# echo_handler = MessageHandler(Filters.text, echo)
# dispatcher.add_handler(echo_handler)

callback_handler = CallbackQueryHandler(button)
dispatcher.add_handler(callback_handler)

caps_handler = CommandHandler('caps', caps, pass_args=True)
dispatcher.add_handler(caps_handler)

# stop_handler = CommandHandler('stop', stop)
# dispatcher.add_handler(stop_handler)

chat_id_handler = CommandHandler('chat_id', chat_id)
dispatcher.add_handler(chat_id_handler)

reboot_handler = CommandHandler('reboot', reboot)
dispatcher.add_handler(reboot_handler)

multi_msg_handler = CommandHandler('multi_msg', multi_msg, pass_args=True)
dispatcher.add_handler(multi_msg_handler)

# reset_handler = CommandHandler('reset', reset, pass_args=True)
# dispatcher.add_handler(reset_handler)

write_logs_handler = CommandHandler('write_logs', write_logs, pass_args=True)
dispatcher.add_handler(write_logs_handler)

read_logs_handler = CommandHandler('read_logs', read_logs, pass_args=True)
dispatcher.add_handler(read_logs_handler)

help_handler = CommandHandler('help', help)
dispatcher.add_handler(help_handler)

# perm_handler = CommandHandler('perm', perm)
# dispatcher.add_handler(perm_handler)

unknown_handler = MessageHandler(Filters.command, unknown)
dispatcher.add_handler(unknown_handler)

print("Estoy en linea.")
