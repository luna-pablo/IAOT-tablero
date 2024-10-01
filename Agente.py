import getpass
from spade import quit_spade
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour, OneShotBehaviour
from spade.message import Message
from spade.template import Template
from objetos_tablero import Carta_ciudad, Carta_evento, Carta_ciudad_infeccion, Cubo, Ciudad
from creencias_deseos_intenciones import *
import json

class BDIAgent(Agent):
    def __init__(self, agent_jid, agent_password):
        super(BDIAgent, self).__init__(agent_jid, agent_password)
        self.misIntenciones = []
        self.misCreencias = []
        self.misDeseos = []

    def nuevo_fichero_imprimir(self):
        with open(f"./debug/{self.jid}.txt", 'w') as writer:
            writer.write(f"Ejecución de {self.jid}")

    def imprimir_agente(self, texto):
        print(f"{self.jid}:\n   {texto}")
        with open(f"./debug/{self.jid}.txt", 'a') as writer:
            writer.write(f"{texto}\n")

    """----------------Métodos Ciclo BDI----------------"""

    async def actualizaCreencias(self, msg):
        """Cada tipo de agente actualiza sus creencias de forma distinta"""
        pass

    async def actualizaDeseos(self):
        self.imprimir_agente(f"Comienza actualización de deseos del agente {self.jid}, deseos ahora: "
                             f"{[(deseo, deseo.activo) for deseo in self.misDeseos]}")
        for deseo in self.misDeseos:
            if deseo.activo:
                if await deseo.comprobarimposible(
                        self.misCreencias) or await deseo.comprobarsatisfecho(self.misCreencias):
                    self.imprimir_agente(f"Deseo satisfecho o imposible: {deseo}")
                    for intencion in deseo.intenciones:
                        # self.imprimir_agente(
                        #     f"Las intenciones que se comprueban: {intencion}, de tipo {intencion.tipo}")
                        if intencion in self.misIntenciones:
                            self.imprimir_agente(f"Se elimina intencion {intencion} asociada al deseo {deseo}")
                            self.misIntenciones.remove(intencion)
                    deseo.activo = False
                    self.imprimir_agente(f"Desactivado deseo: {deseo}")
            else:
                if await deseo.comprobaractivar(self.misCreencias):
                    self.misIntenciones.append(deseo.intenciones[0])  # ponemos la primera intencion del deseo en las intenciones del agente
                    deseo.activo = True
                    self.imprimir_agente(f"Activado deseo: {deseo}, introducida intencion: {deseo.intenciones[0]}")
        self.imprimir_agente(
            f"Termina actualización de deseos del agente {self.jid}, deseos ahora: "
            f"{[(deseo, deseo.activo) for deseo in self.misDeseos]}")

    async def actualizaIntenciones(self):
        for intencion in self.misIntenciones:
            if await intencion.comprobaralcanzada(self.misCreencias):
                self.imprimir_agente(f"Alcanzada intención: {intencion}")
                if len(intencion.posteriores) > 0: # si hay posteriores se incluyen
                    self.misIntenciones.append(intencion.posteriores.pop(0))
                self.misIntenciones.remove(intencion)  # quita la intencion actual de la lista de intenciones del agente
                # poner siguiente intencion del deseo en la lista de intenciones del agente

            if await intencion.comprobaranulada(self.misCreencias):
                for p in intencion.posteriores:
                    self.misIntenciones.remove(p)  # quita todas las intenciones posteriores de las intenciones del agente
                self.misIntenciones.remove(intencion)


    async def calculaPrioridades(self):
        for intencion in self.misIntenciones:
            await intencion.calculaprioridad(self.misCreencias)

    async def elige_y_ejecutaIntencion(self):
        self.imprimir_agente(f"Intenciones entre las que elige el agente {self.jid}:{self.misIntenciones}")
        if len(self.misIntenciones) == 0:
            msgs = []
            return msgs # si no quedan elementos en la lista, parar función

        maximaprioridad = -1
        for intencion in self.misIntenciones:
            if intencion.prioridad > maximaprioridad:
                maximaprioridad = intencion.prioridad
                intencion_a_ejecutar = intencion

        self.imprimir_agente(f"Lo que decide ejecutar: {intencion_a_ejecutar}")
        # actualiza creencias y recibe lista de mensajes
        self.misCreencias, msgs = await intencion_a_ejecutar.ejecuta(self.misCreencias)
        return msgs

    class BDIBehav(CyclicBehaviour):
        async def run(self):

            self.agent.imprimir_agente(f"Creencias del agente actuales: {self.agent.misCreencias}")
            msg = await self.receive(timeout=3)
            if msg:
                msg_tipo = str(TipoCreencia(json.loads(msg.body)["tipo"]))
                self.agent.imprimir_agente(f"Agente {self.agent.jid} recibe mensaje:\n  {msg}, {msg_tipo}")
                await self.agent.actualizaCreencias(msg)
            await self.agent.actualizaDeseos()  # con las creencias cambiadas en el paso anterior
            await self.agent.actualizaIntenciones()  # con las creencias cambiadas en el paso primero, incluidas las intenciones añadidas en el paso anterior
            await self.agent.calculaPrioridades()  # de las intenciones

            reply_msgs = await self.agent.elige_y_ejecutaIntencion()  # ejecuta la de mayor prioridad
            for msg in reply_msgs:
                msg_tipo = str(TipoCreencia(json.loads(msg.body)["tipo"]))
                self.agent.imprimir_agente(f"Agente envía mensaje:\n    {msg}, {msg_tipo}")
                await self.send(msg)
            # else:
            #     self.agent.imprimir_agente(f"Agent {self.agent.jid} no recibe ningún mensaje")
