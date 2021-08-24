import asyncio
import logging

from slixmpp import ClientXMPP

logging.basicConfig(level=logging.DEBUG, format="%(levelname)-8s %(message)s")
class Client(ClientXMPP):

    def __init__(self, jid, password):
        ClientXMPP.__init__(self, jid, password)

        self.add_event_handler("session_start", self.session_start)
        self.add_event_handler("message", self.message)
        self.add_event_handler("register", self.register)

        self.register_plugin('xep_0030') # Service Discovery
        self.register_plugin('xep_0199') # XMPP Ping
        self.register_plugin('xep_0004') # Data forms
        self.register_plugin('xep_0066') # Out-of-band Data
        self.register_plugin('xep_0077') # In-band Registration

    def session_start(self, event):
        print("He entrado al chat exitosamente :)")
        self.send_presence()
        self.get_roster()

    def message(self, msg):
        if msg['type'] in ('chat', 'normal'):
            msg.reply("Thanks for sending\n%(body)s" % msg).send()
        print("Mensaje enviado")

    async def register(self, iq):
        resp = self.Iq()
        resp['type'] = 'set'
        resp['register']['username'] = self.boundjid.user
        resp['register']['password'] = self.password

        try:
            await resp.send()
            print("Cuenta creada")
            logging.info("Account created for %s!" % self.boundjid)
        except IqError as e:
            print("Error al crear cuenta")
            logging.error("Could not register account: %s" %
                    e.iq['error']['text'])
            self.disconnect()
        except IqTimeout:
            print("Error al crear cuenta")
            logging.error("No response from server.")
            self.disconnect()

def register(username, password):
    client = Client(username, password)
    client.use_proxy = True
    client.proxy_config = {'host': 'alumchat.xyz','port': 5222}

    client.register_plugin("xep_0030")
    client.register_plugin("xep_0004")
    client.register_plugin("xep_0199")
    client.register_plugin("xep_0066")
    client.register_plugin("xep_0077")

    # We force the registration
    client["xep_0077"].force_registration = True

    client.connect()
    client.process()

def login(username, password):
    # Instance of the Client class to continue with the request in the async method
    client = Client(username, password)

    client.use_proxy = True
    client.proxy_config = {'host': 'alumchat.xyz','port': 5222}

    client.register_plugin("xep_0030")
    client.register_plugin("xep_0199")
    client.register_plugin('xep_0363')

    client.connect()
    client.process(forever=False)


if __name__ == '__main__':
    dele = True
    while dele:
        print("""Bienvenido porfavor ingrese que desea hacer:
        \t1.login
        \t2.signup
        \t3.salir""")


        option = int(input("Ingrese una opción para poder continuar: "))
        if option == 1:
            user = input("Usuario: ")
            password = input("Contraseña: ")
            register(user, password)

        elif option == 2:
            user = input("Usuario: ")
            password = input("Contraseña: ")
            login(user, password)

        elif option == 3:
            dele = False
        else:
            print("Invalid option")
