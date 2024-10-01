import sys
from enum import Enum
from abc import ABC, abstractmethod
from spade.message import Message
from objetos_tablero import Carta_ciudad, Carta_evento
import json


class Creencia:  # clase sin metodos, solo sirve para encapsular datos
    def __init__(self, tipo_creencia, valores_creencia):
        self.tipo = tipo_creencia
        # self.valores.append(valores_creencia)
        self.valores = valores_creencia
        self.prioridad = 0

    def __repr__(self):
        return str(self.tipo) + str(self.valores)


class Intencion(ABC):  # clase abstracta0
    @abstractmethod
    async def comprobaralcanzada(self, creencias):
        pass

    @abstractmethod
    async def comprobaranulada(self, creencias):
        pass

    @abstractmethod
    async def ejecuta(self):
        pass

    async def calcularprioridad(self, creencias):
        self.prioridad = self.coste + self.urgencia


class Deseo(ABC):  # clase abstracta
    @abstractmethod
    async def comprobarimposible(self, creencias):
        pass

    @abstractmethod
    async def comprobarsatisfecho(self, creencias):
        pass

    @abstractmethod
    async def comprobarinteres(self, creencias):
        pass

    @abstractmethod
    async def comprobaractivar(self, creencias):
        pass


class TipoCreencia(int, Enum):
    # algunos de estos tipos de creencias coincidiran con los predicados
    # jugadores:
    UNIDO_A_PARTIDA = 1
    ES_TABLERO = 2
    PEDIDO_UNIRSE = 3
    RECHAZADO_A_PARTIDA = 4

    EN_TURNO = 5
    ERES_JUGADOR = 6

    # Finalizar turno
    NO_ES_MI_TURNO = 7
    TURNO_FINALIZADO = 8
    ACCIONES_TERMINADAS = 9

    JUGADOR1_TIENE_CARTAS = 10
    JUGADOR2_TIENE_CARTAS = 11

    JUGADOR_SOLICITA_UNIRSE = 12
    PARTIDA_LLENA = 13
    CARTAS_REPARTIDAS = 14
    MAZO_JUGADORES = 15
    MAZO_INFECCION = 16
    JUGADOR_DE_PARTIDA = 17

    INFECTANDO = 18
    SOLICITUD_CARTA = 19
    SOLICITUD_CARTA_INFECCION = 20
    CARTA_SOLICITADA = 21

    REPARTIR_CARTA_INFECCION = 22
    REPARTIR_CARTA = 23
    NUM_CARTAS = 24
    ROBANDO = 25
    CARTA_ENTREGADA = 26

    # infectar ciudad
    CARTA_INFECCION_ROBADA = 27
    CIUDADES = 28
    CUBOS = 29
    CIUDAD_INFECTADA = 30

    ENFERMEDAD_ROJA_ERRADICADA = 31
    ENFERMEDAD_AZUL_ERRADICADA = 32
    ENFERMEDAD_NEGRA_ERRADICADA = 33
    ENFERMEDAD_AMARILLA_ERRADICADA = 34

    VACUNA_ROJA_DESCUBIERTA = 35
    VACUNA_AZUL_DESCUBIERTA = 36
    VACUNA_NEGRA_DESCUBIERTA = 37
    VACUNA_AMARILLA_DESCUBIERTA = 38

    MAZO_DESCARTES_JUGADOR = 39


class TipoDeseo(Enum):
    # algunos de estos tipos de deseos coincidiran con los protocolos/servicios
    # jugadores:
    JUGAR = 1
    # Finalizar turno
    JUGAR_TURNO = 2
    INFORMAR_FINAL_TURNO = 3
    ROBAR_CARTA = 4

    # tablero:
    REGISTRAR_JUGADORES = 5
    REPARTIR_CARTAS = 6
    DAR_CARTA = 7

    INFECTAR_CIUDAD = 8

    ERRADICAR_ENFERMEDAD_ROJA = 9
    ERRADICAR_ENFERMEDAD_AZUL = 10
    ERRADICAR_ENFERMEDAD_NEGRA = 11
    ERRADICAR_ENFERMEDAD_AMARILLA = 12

    DESCARTAR_CARTA = 13


class TipoIntencion(Enum):
    # algunos de estos tipos de creencias coincidiran con las acciones
    # jugadores:
    PEDIR_UNIRSE = 1

    JUGAR_TURNO = 2
    # Finalizar turno
    FINALIZAR_TURNO = 3

    # tablero:
    REGISTRAR_JUGADOR = 4
    FINALIZAR_REGISTRO = 5
    REPARTIR_CARTAS = 6
    ROBAR_CARTA = 7
    DAR_CARTA = 8

    INFECTAR_CIUDAD = 9

    ERRADICAR_ENFERMEDAD_ROJA = 10
    ERRADICAR_ENFERMEDAD_AZUL = 11
    ERRADICAR_ENFERMEDAD_NEGRA = 12
    ERRADICAR_ENFERMEDAD_AMARILLA = 13

    DESCARTAR_CARTAS_JUGADOR = 14  # /////////////////////////////////////////////// LUNA


"""----------------Intenciones jugadores-------------------------------------------------------------------------------------------------------------------------"""


class Robar_carta_intencion(Intencion):
    def __init__(self, conceptos_intencion, posteriores):
        self.conceptos = conceptos_intencion
        self.tipo = TipoIntencion.ROBAR_CARTA
        # self.deseo = deseo_intencion
        self.coste = 0
        self.urgencia = 0
        self.prioridad = 0
        self.posteriores = posteriores

    async def comprobaralcanzada(self, creencias):
        for c in creencias:
            if c.tipo == TipoCreencia.CARTA_SOLICITADA:
                return True
        return False

    async def comprobaranulada(self, creencias):
        for c in creencias:
            if c.tipo == TipoCreencia.MAZO_JUGADORES and len(c.valores[0]) == 0:
                return True
        return False

    async def ejecuta(self, creencias):
        for c in creencias:
            if c.tipo == TipoCreencia.ES_TABLERO:
                tablero_id = c.valores[0]
            if c.tipo == TipoCreencia.ERES_JUGADOR:
                jugador = c.valores[0]
        for c in creencias:
            if c.tipo == TipoCreencia.ROBANDO:
                msg = Message(to=tablero_id)  # Instantiate the message
                msg.set_metadata("performative", "request")  # Set the "request" FIPA performative
                msg.body = json.dumps({'tipo': TipoCreencia.SOLICITUD_CARTA, "jugador": jugador})
                msgs = [msg]

            elif c.tipo == TipoCreencia.INFECTANDO:
                msg = Message(to=tablero_id)  # Instantiate the message
                msg.set_metadata("performative", "request")  # Set the "request" FIPA performative
                msg.body = json.dumps({'tipo': TipoCreencia.SOLICITUD_CARTA_INFECCION, "jugador": jugador})
                msgs = [msg]

        miCreencia = Creencia(TipoCreencia.CARTA_SOLICITADA, tablero_id)
        creencias.append(miCreencia)

        return creencias, msgs

    async def calculaprioridad(self, creencias):
        pass


class RobarCarta(Deseo):
    def __init__(self, intenciones_deseo, conceptos_deseo=None):
        self.intenciones = intenciones_deseo
        self.conceptos = conceptos_deseo
        self.activo = False
        self.tipo = TipoDeseo.ROBAR_CARTA

    def __eq__(self, other):
        return self.tipo == other.tipo

    async def comprobarimposible(self, creencias):
        for c in creencias:
            if c.tipo == TipoCreencia.MAZO_JUGADORES and len(c.valores[0]) == 0:
                return True
        return False

    async def comprobarsatisfecho(self, creencias):
        variables = {"TipoCreencia.JUGADOR1_TIENE_CARTAS": TipoCreencia.JUGADOR1_TIENE_CARTAS,
                     "TipoCreencia.JUGADOR2_TIENE_CARTAS": TipoCreencia.JUGADOR2_TIENE_CARTAS}
        for c in creencias:
            if c.tipo == TipoCreencia.ERES_JUGADOR:  # No lo tengo claro, no se que condicion ponerle
                jugador = c.valores[0]
        for c in creencias:
            if c.tipo == variables.get(
                    f"TipoCreencia.JUGADOR{jugador}_TIENE_CARTAS"):  # No lo tengo claro, no se que condicion ponerle
                mano_cartas = c.valores[0]
            if c.tipo == TipoCreencia.NUM_CARTAS:
                num_cartas_anterior = c.valores[0]
            else:
                num_cartas_anterior = 0
        if len(mano_cartas) == (num_cartas_anterior + 1):
            return True
        return False

    async def comprobarinteres(self, creencias):
        pass

    async def comprobaractivar(self, creencias):
        for c in creencias:
            if c.tipo == TipoCreencia.ROBANDO:
                robando = True
            else:
                robando = False
        for c in creencias:
            if c.tipo == TipoCreencia.EN_TURNO and robando:
                return True
        return False


###########################################################   JUGAR TURNO   #######################################################################
class JugarTurno(Deseo):
    def __init__(self, intenciones_deseo, conceptos_deseo=[]):
        self.intenciones = intenciones_deseo
        self.conceptos = conceptos_deseo
        self.activo = False
        self.tipo = TipoDeseo.JUGAR_TURNO

    def __eq__(self, other):
        return self.tipo == other.tipo

    async def comprobarimposible(self, creencias):
        for c in creencias:
            if c.tipo == TipoCreencia.NO_ES_MI_TURNO:
                return True
        return False

    async def comprobarsatisfecho(self, creencias):
        for c in creencias:
            if c.tipo == TipoCreencia.EN_TURNO:
                return True
        return False

    async def comprobarinteres(self, creencias):
        pass

    async def comprobaractivar(self, creencias):
        for c in creencias:
            if c.tipo == TipoCreencia.ROBANDO:
                robando = True
            else:
                robando = False

        for c in creencias:
            if c.tipo == TipoCreencia.ERES_JUGADOR and not robando:
                return True
        return False


class Jugar_Turno_intencion(Intencion):
    def __init__(self, conceptos_intencion, posteriores):
        """conceptos: baraja de cartas"""
        self.conceptos = conceptos_intencion
        self.tipo = TipoIntencion.JUGAR_TURNO
        # self.deseo = deseo_intencion
        self.coste = 0
        self.urgencia = 0
        self.prioridad = 0
        self.posteriores = posteriores

    def __repr__(self):
        return f"{str(self.tipo)}:{str(self.conceptos)}"

    async def comprobaralcanzada(self, creencias):
        for c in creencias:
            if c.tipo == TipoCreencia.EN_TURNO:
                return True
        return False

    async def comprobaranulada(self, creencias):
        for c in creencias:
            if c.tipo == TipoCreencia.NO_ES_MI_TURNO:
                return True
        return False

    async def ejecuta(self, creencias):
        msgs = []
        miCreencia = Creencia(TipoCreencia.EN_TURNO, [])
        creencias.append(miCreencia)
        miCreencia = Creencia(TipoCreencia.ROBANDO, [])
        creencias.append(miCreencia)
        return creencias, msgs

    async def calculaprioridad(self, creencias):
        pass


###########################################################   UNION A PARTIDA   #######################################################################
class Jugar(Deseo):
    def __init__(self, intenciones_deseo, conceptos_deseo=None):
        self.intenciones = intenciones_deseo
        self.conceptos = conceptos_deseo
        self.activo = False
        self.tipo = TipoDeseo.JUGAR

    def __eq__(self, other):
        return self.tipo == other.tipo

    # como el deseo solo tiene una intencion, coinciden las condiciones (las creencias unido y rechazado) que anulan tanto el deseo como la intencion
    # en un deseo con mas de una intencion, las creencias que los anularán serán distintas
    async def comprobarimposible(self, creencias):
        for c in creencias:
            if c.tipo == TipoCreencia.RECHAZADO_A_PARTIDA:
                return True
        return False

    async def comprobarsatisfecho(self, creencias):
        for c in creencias:
            if c.tipo == TipoCreencia.UNIDO_A_PARTIDA:
                return True
        return False

    async def comprobarinteres(self, creencias):
        pass

    async def comprobaractivar(self, creencias):
        for c in creencias:
            if c.tipo == TipoCreencia.PEDIDO_UNIRSE:
                return False
        return True


class Pedir_Unirse(Intencion):
    def __init__(self, conceptos_intencion, posteriores):
        self.conceptos = conceptos_intencion
        self.tipo = TipoIntencion.PEDIR_UNIRSE
        # self.deseo = deseo_intencion
        self.coste = 0
        self.urgencia = 0
        self.prioridad = 0
        self.posteriores = posteriores

    async def comprobaralcanzada(self, creencias):
        for c in creencias:
            if c.tipo == TipoCreencia.UNIDO_A_PARTIDA or c.tipo == TipoCreencia.PEDIDO_UNIRSE:
                return True
        return False

    async def comprobaranulada(self, creencias):
        for c in creencias:
            if c.tipo == TipoCreencia.RECHAZADO_A_PARTIDA:
                return True
        return False

    async def ejecuta(self, creencias):
        for c in creencias:
            if c.tipo == TipoCreencia.ES_TABLERO:
                tablero_id = c.valores[0]

        msg = Message(to=tablero_id)  # Instantiate the message
        msg.set_metadata("performative", "request")  # Set the "request" FIPA performative
        msg.body = json.dumps({'tipo': TipoCreencia.JUGADOR_SOLICITA_UNIRSE})
        msgs = [msg]

        miCreencia = Creencia(TipoCreencia.PEDIDO_UNIRSE, tablero_id)
        creencias.append(miCreencia)

        return creencias, msgs

    async def calculaprioridad(self, creencias):
        pass


class RegistrarJugadores(Deseo):
    def __init__(self, intenciones_deseo, conceptos_deseo=[]):
        """Conceptos del deseo: número de jugadores esperados,"""
        self.intenciones = intenciones_deseo
        self.conceptos = conceptos_deseo
        self.activo = False
        self.tipo = TipoDeseo.REGISTRAR_JUGADORES

    def __eq__(self, other):
        return self.tipo == other.tipo

    # como el deseo solo tiene una intencion, coinciden las condiciones (las creencias unido y rechazado) que anulan tanto el deseo como la intencion
    # en un deseo con mas de una intencion, las creencias que los anularán serán distintas
    async def comprobarimposible(self, creencias):
        for c in creencias:
            if c.tipo == TipoCreencia.PARTIDA_LLENA:
                return True
        return False

    async def comprobarsatisfecho(self, creencias):
        for c in creencias:
            if c.tipo == TipoCreencia.PARTIDA_LLENA:
                return True
        return False

    async def comprobarinteres(self, creencias):
        pass
        # for c in creencias:
        #     if c.tipo == TipoCreencia.PEDIDO_UNIRSE:
        #         return True
        # return False

    async def comprobaractivar(self, creencias):
        contador_jugadores = 0
        for c in creencias:
            if c.tipo == TipoCreencia.PARTIDA_LLENA:
                return False
            elif c.tipo == TipoCreencia.JUGADOR_SOLICITA_UNIRSE:
                contador_jugadores += 1

        if contador_jugadores != self.conceptos[0]:
            return False
        return True


class Registrar_jugador(Intencion):
    def __init__(self, conceptos_intencion, posteriores):  # (dirección del jugadores, [])
        self.conceptos = conceptos_intencion
        self.tipo = TipoIntencion.REGISTRAR_JUGADOR
        # self.deseo = deseo_intencion
        self.coste = 0
        self.urgencia = 0
        self.prioridad = 0
        self.posteriores = posteriores
        self.direccion_jugador = conceptos_intencion[0]

    def __repr__(self):
        return str(self.tipo) + str(self.conceptos)

    async def comprobaralcanzada(self, creencias):
        for c in creencias:
            if c.tipo == TipoCreencia.UNIDO_A_PARTIDA:
                if c.valores[0] == str(self.direccion_jugador):  # la lista de creencias solo tiene un valor
                    return True
        return False

    async def comprobaranulada(self, creencias):
        for c in creencias:
            if c.tipo == TipoCreencia.PARTIDA_LLENA:
                return True
        return False

    async def ejecuta(self, creencias):
        msg = Message(to=str(self.direccion_jugador))  # Instantiate the message
        msg.set_metadata("performative", "agree")  # Set the "request" FIPA performative
        msg_json = json.dumps({"tipo": TipoCreencia.UNIDO_A_PARTIDA})
        msg.body = msg_json  # Set the message content
        msgs = [msg]

        miCreencia = Creencia(TipoCreencia.UNIDO_A_PARTIDA, [self.direccion_jugador])
        creencias.append(miCreencia)

        return creencias, msgs

    async def calculaprioridad(self, creencias):
        pass


class Finalizar_registro(Intencion):
    """Conceptos de la intención: número de jugadores"""

    def __init__(self, conceptos_intencion, posteriores):
        self.conceptos = conceptos_intencion
        self.tipo = TipoIntencion.FINALIZAR_REGISTRO
        self.coste = 0
        self.urgencia = 0
        self.prioridad = 0
        self.posteriores = posteriores

    async def comprobaralcanzada(self, creencias):
        contador = 0
        for c in creencias:
            if c.tipo == TipoCreencia.UNIDO_A_PARTIDA:
                contador += 1
        if contador == self.conceptos[0]:  # si el número de jugadores unidos es igual al esperado
            return True
        return False

    async def comprobaranulada(self, creencias):
        # no existe caso anulada
        return False

    async def calculaprioridad(self, creencias):
        pass

    async def ejecuta(self, creencias):

        # encontrar jugadores
        jugadores = []
        for creencia in creencias:
            if creencia.tipo == TipoCreencia.UNIDO_A_PARTIDA:
                jugadores.append(creencia.valores[0])  # dirección del jugador

        print("JUGADORES REGISTRADOS EN LA PARTIDA:", jugadores)
        msgs = []
        for jugador in jugadores:
            for resto_jugadores in jugadores:
                if resto_jugadores != jugador:  # Enviar a cada jugador todos los jugadores menos a si mismo
                    msg = Message(to=jugador)
                    msg.set_metadata("performative", "inform")
                    msg.body = json.dumps({"tipo": TipoCreencia.JUGADOR_DE_PARTIDA,
                                           "jugador": resto_jugadores})  # Set the message content
                    msgs.append(msg)

        miCreencia = Creencia(TipoCreencia.PARTIDA_LLENA, [])
        creencias.append(miCreencia)

        creenciaVacunaRoja = Creencia(TipoCreencia.VACUNA_ROJA_DESCUBIERTA,
                                      [])  # ////////////////////////////////////////
        creencias.append(creenciaVacunaRoja)  # ////////////////////////////////////////

        creenciaVacunaAzul = Creencia(TipoCreencia.VACUNA_AZUL_DESCUBIERTA,
                                      [])  # ////////////////////////////////////////
        creencias.append(creenciaVacunaAzul)  # ////////////////////////////////////////

        creenciaVacunaNegra = Creencia(TipoCreencia.VACUNA_NEGRA_DESCUBIERTA,
                                       [])  # ////////////////////////////////////////
        creencias.append(creenciaVacunaNegra)  # ////////////////////////////////////////

        creenciaVacunaAmarilla = Creencia(TipoCreencia.VACUNA_AMARILLA_DESCUBIERTA,
                                          [])  # ////////////////////////////////////////
        creencias.append(creenciaVacunaAmarilla)  # ////////////////////////////////////////

        return creencias, msgs


###########################################################   REPARTIR CARTAS INICIALES  #######################################################################
class RepartirCartasIniciales(Deseo):
    def __init__(self, intenciones_deseo, conceptos_deseo=[]):
        """Conceptos del deseo: []"""
        self.intenciones = intenciones_deseo
        self.conceptos = conceptos_deseo
        self.activo = False
        self.tipo = TipoDeseo.REPARTIR_CARTAS

    def __eq__(self, other):
        return self.tipo == other.tipo

    async def comprobarimposible(self, creencias):
        for c in creencias:
            if c.tipo == TipoCreencia.MAZO_JUGADORES or c.tipo == TipoCreencia.MAZO_INFECCION:
                mazo = c.valores[0]
        if len(mazo) <= 0:
            return True
        return False

    async def comprobarsatisfecho(self, creencias):
        ter = False
        for c in creencias:
            if c.tipo == TipoCreencia.ACCIONES_TERMINADAS:
                ter = True
        for c in creencias:
            if (c.tipo == TipoCreencia.CARTAS_REPARTIDAS) and not ter:
                return True
        return False

    async def comprobarinteres(self, creencias):
        pass

    async def comprobaractivar(self, creencias):
        for c in creencias:
            if c.tipo == TipoCreencia.CARTAS_REPARTIDAS:
                return False
            if c.tipo == TipoCreencia.PARTIDA_LLENA:
                return True
        return False


class Repartir_cartas_iniciales_intencion(Intencion):
    def __init__(self, conceptos_intencion, posteriores):
        """conceptos: baraja de cartas"""
        self.conceptos = conceptos_intencion
        self.tipo = TipoIntencion.REPARTIR_CARTAS
        # self.deseo = deseo_intencion
        self.coste = 0
        self.urgencia = 0
        self.prioridad = 0
        self.posteriores = posteriores

    def __repr__(self):
        return f"{str(self.tipo)}:{str(self.conceptos)}"

    async def comprobaralcanzada(self, creencias):
        for c in creencias:
            if c.tipo == TipoCreencia.CARTAS_REPARTIDAS:
                return True
        return False

    async def comprobaranulada(self, creencias):
        for c in creencias:
            if c.tipo == TipoCreencia.MAZO_JUGADORES or c.tipo == TipoCreencia.MAZO_INFECCION:
                mazo = c.valores[0]
        if len(mazo) <= 0:
            return True
        return False

    async def ejecuta(self, creencias):
        # mazo = self.conceptos[0]
        # encontrar mazo
        for creencia in creencias:
            if creencia.tipo == TipoCreencia.MAZO_JUGADORES:
                mazo = creencia.valores[0]  # cargamos los objetos carta del mazo
                break

        # encontrar jugadores
        jugadores = []
        for creencia in creencias:
            if creencia.tipo == TipoCreencia.UNIDO_A_PARTIDA:
                jugadores.append(creencia.valores[0])  # dirección del jugador

        variables = {"TipoCreencia.JUGADOR1_TIENE_CARTAS": TipoCreencia.JUGADOR1_TIENE_CARTAS,
                     "TipoCreencia.JUGADOR2_TIENE_CARTAS": TipoCreencia.JUGADOR2_TIENE_CARTAS}
        # n_cartas = 3 - (len(jugadores) - 3) # formula teroicamente correcta
        n_cartas = len(jugadores)
        msgs = []
        for jugador in jugadores:
            cartas_jug_json = []
            for carta in range(n_cartas):
                cartas_jug_json.append(mazo.pop(0).__dict__)  # dict para poder serializar con json
            for jugador_envio in jugadores:
                msg = Message(to=jugador_envio)
                msg.set_metadata("performative", "inform")
                info = json.dumps(
                    {"tipo": variables.get(f"TipoCreencia.JUGADOR{jugadores.index(jugador) + 1}_TIENE_CARTAS"),
                     "lista_cartas": cartas_jug_json})
                msg.body = info  # Set the message content
                msgs.append(msg)

            if jugadores.index(jugador) == 0:
                msg = Message(to=jugador)
                msg.set_metadata("performative", "inform")
                info = json.dumps({"tipo": TipoCreencia.ERES_JUGADOR, "num_jugador": (jugadores.index(jugador) + 1)})
                msg.body = info  # Set the message content
                msgs.append(msg)

        miCreencia = Creencia(TipoCreencia.CARTAS_REPARTIDAS, [])
        creencias.append(miCreencia)

        return creencias, msgs

    async def calculaprioridad(self, creencias):
        pass


###########################################################   REPARTIR CARTA  #######################################################################
class DarCarta(Deseo):
    def __init__(self, intenciones_deseo, conceptos_deseo=[]):
        """Conceptos del deseo: []"""
        self.intenciones = intenciones_deseo
        self.conceptos = conceptos_deseo
        self.activo = False
        self.tipo = TipoDeseo.DAR_CARTA

    def __eq__(self, other):
        return self.tipo == other.tipo

    async def comprobarimposible(self, creencias):
        for c in creencias:
            if c.tipo == TipoCreencia.MAZO_JUGADORES or c.tipo == TipoCreencia.MAZO_JUGADORES:
                mazo = c.valores[0]
        if len(mazo) <= 0:
            return True
        return False

    async def comprobarsatisfecho(self, creencias):
        for c in creencias:
            if c.tipo == TipoCreencia.CARTA_ENTREGADA:
                return True
        return False

    async def comprobarinteres(self, creencias):
        pass

    async def comprobaractivar(self, creencias):
        for c in creencias:
            if c.tipo == TipoCreencia.CARTA_ENTREGADA:
                return False
            if c.tipo == TipoCreencia.REPARTIR_CARTA_INFECCION or c.tipo == TipoCreencia.REPARTIR_CARTA:
                return True
        return False


class Dar_carta_intencion(Intencion):
    def __init__(self, conceptos_intencion, posteriores):
        """conceptos: baraja de cartas"""
        self.conceptos = conceptos_intencion
        self.tipo = TipoIntencion.DAR_CARTA
        # self.deseo = deseo_intencion
        self.coste = 0
        self.urgencia = 0
        self.prioridad = 0
        self.posteriores = posteriores

    def __repr__(self):
        return f"{str(self.tipo)}:{str(self.conceptos)}"

    async def comprobaralcanzada(self, creencias):
        for c in creencias:
            if c.tipo == TipoCreencia.CARTA_ENTREGADA:
                return True
        return False

    async def comprobaranulada(self, creencias):
        for c in creencias:
            if c.tipo == TipoCreencia.MAZO_JUGADORES or c.tipo == TipoCreencia.MAZO_INFECCION:
                mazo = c.valores[0]
        if len(mazo) <= 0:
            return True
        return False

    async def ejecuta(self, creencias):
        # mazo = self.conceptos[0]
        # escoges el mazo de jugadores en funcion de si es el inicio de partida o te estan solicitando una carta a robar de tipo infeccion o normal
        for creencia in creencias:
            if creencia.tipo == TipoCreencia.REPARTIR_CARTA_INFECCION:
                jugador = creencia.valores[0]
                carta_robada = False
                for creencia1 in creencias:
                    if creencia1.tipo == TipoCreencia.MAZO_INFECCION:
                        mazo = creencia1.valores[0]
                        break
                break
            elif creencia.tipo == TipoCreencia.REPARTIR_CARTA:
                jugador = creencia.valores[0]
                carta_robada = True
                for creencia1 in creencias:
                    if creencia1.tipo == TipoCreencia.MAZO_JUGADORES:
                        mazo = creencia1.valores[0]
                        break
                break

        # encontrar jugadores
        jugadores = []
        for creencia in creencias:
            if creencia.tipo == TipoCreencia.UNIDO_A_PARTIDA:
                jugadores.append(creencia.valores[0])  # dirección del jugador

        for j in jugadores:
            if jugador == jugadores.index(j) + 1:
                dir_jugador = j

        variables = {"TipoCreencia.JUGADOR1_TIENE_CARTAS": TipoCreencia.JUGADOR1_TIENE_CARTAS,
                     "TipoCreencia.JUGADOR2_TIENE_CARTAS": TipoCreencia.JUGADOR2_TIENE_CARTAS}
        carta = mazo.pop(0).__dict__
        msgs = []
        msg = Message(to=dir_jugador)
        msg.set_metadata("performative", "agree")
        info = json.dumps(
            {"tipo": variables.get(f"TipoCreencia.JUGADOR{jugador}_TIENE_CARTAS"), "lista_cartas": [carta],
             "carta_robada": carta_robada})
        msg.body = info  # Set the message content
        msgs.append(msg)

        for jugador_envio in jugadores:
            if jugador != jugadores.index(jugador_envio) + 1:
                msg = Message(to=jugador_envio)
                msg.set_metadata("performative", "inform")
                info = json.dumps(
                    {"tipo": variables.get(f"TipoCreencia.JUGADOR{jugador}_TIENE_CARTAS"), "lista_cartas": [carta]})
                msg.body = info  # Set the message content
                msgs.append(msg)

        miCreencia = Creencia(TipoCreencia.CARTA_ENTREGADA, [])
        creencias.append(miCreencia)

        return creencias, msgs

    async def calculaprioridad(self, creencias):
        pass


class Finalizar_Turno(Intencion):
    def __init__(self, conceptos_intencion, posteriores):
        self.conceptos = conceptos_intencion
        self.tipo = TipoIntencion.FINALIZAR_TURNO
        self.coste = 0
        self.urgencia = 0
        self.prioridad = 0
        self.posteriores = posteriores

    async def comprobaralcanzada(self, creencias):
        for c in creencias:
            if c.tipo == TipoCreencia.NO_ES_MI_TURNO:
                return True
        return False

    async def comprobaranulada(self, creencias):
        for c in creencias:
            if c.tipo == TipoCreencia.NO_ES_MI_TURNO:
                return True
        return False

    async def ejecuta(self, creencias):
        jugadores = []
        tablero = ''
        eres_jugador = ''
        for creencia in creencias:
            if creencia.tipo == TipoCreencia.JUGADOR_DE_PARTIDA:
                jugadores.append(creencia.valores[0])  # dirección del jugador
            if creencia.tipo == TipoCreencia.ES_TABLERO:
                jugadores.append(creencia.valores[0])
                # tablero = creencia.valores[0]
            if creencia.tipo == TipoCreencia.ACCIONES_TERMINADAS:
                creencias.remove(creencia)
            # Al pasar el turno se eliminarian estas creencias dando paso al siguiente
            if creencia.tipo == TipoCreencia.ROBANDO:  # or creencia.tipo == TipoCreencia.EN_TURNO or creencia.tipo == TipoCreencia.SOLICITUD_CARTA:
                creencias.remove(creencia)
            # if creencia.tipo == TipoCreencia.ERES_JUGADOR:
            #    eres_jugador = creencias.valores[0]

        msgs = []
        for jugador in jugadores:
            msg = Message(to=jugador)
            msg.set_metadata("performative", "inform")
            # Envio la creencia de que finalizo el turno
            msg.body = json.dumps({"tipo": TipoCreencia.TURNO_FINALIZADO})  # Set the message content
            msgs.append(msg)
            print(jugador, "Informado del fin de turno")

        # Actualizo creencia de que no es mi turno cuando lo decido finalizar
        miCreencia = Creencia(TipoCreencia.NO_ES_MI_TURNO, [])
        creencias.append(miCreencia)

        sys.exit(0)  # se finaliza la ejecución para que no se quede en bucle infinito.
        return creencias, msgs

    async def calculaprioridad(self, creencias):
        pass


class Informar_Final_Turno(Deseo):
    def __init__(self, intenciones_deseo, conceptos_deseo=None):
        self.intenciones = intenciones_deseo
        self.conceptos = conceptos_deseo
        self.activo = False
        self.tipo = TipoDeseo.INFORMAR_FINAL_TURNO

    def __eq__(self, other):
        return self.tipo == other.tipo

    # como el deseo solo tiene una intencion, coinciden las condiciones (las creencias unido y rechazado) que anulan tanto el deseo como la intencion
    # en un deseo con mas de una intencion, las creencias que los anularán serán distintas
    async def comprobarimposible(self, creencias):
        for c in creencias:
            if c.tipo == TipoCreencia.NO_ES_MI_TURNO:
                return True
        return False

    async def comprobarsatisfecho(self, creencias):
        for c in creencias:
            if c.tipo == TipoCreencia.TURNO_FINALIZADO:
                return True
        return False

    async def comprobarinteres(self, creencias):
        pass

    async def comprobaractivar(self, creencias):
        for c in creencias:
            if c.tipo == TipoCreencia.ACCIONES_TERMINADAS:
                return True
        return False


"""Infectar ciduad"""


class Infectar_ciudad(Intencion):

    def __init__(self, conceptos_intencion, posteriores):
        self.conceptos = conceptos_intencion
        self.tipo = TipoIntencion.INFECTAR_CIUDAD
        self.coste = 0
        self.urgencia = 0
        self.prioridad = 0
        self.posteriores = posteriores
        self.ciudad_infectar = 0

    def __repr__(self):
        return str(self.tipo) + str(self.conceptos)

    async def comprobaralcanzada(self, creencias):
        for c in creencias:
            if (c.tipo == TipoCreencia.CIUDAD_INFECTADA) and (self.ciudad_infectar == c.valores[0]):
                return True
        return False

    async def comprobaranulada(self, creencias):
        """for c in creencias:
            if (c.tipo == TipoCreencia.MAX_CUBOS) or (c.tipo == TipoCreencia.NO_MAS_CUBOS):
                return True"""
        return False

    async def ejecuta(self, creencias):
        jugadores = []
        ciudades = []
        for creencia in creencias:
            if creencia.tipo == TipoCreencia.UNIDO_A_PARTIDA:
                jugadores.append(creencia.valores[0])  # dirección del jugador
            if creencia.tipo == TipoCreencia.CIUDADES:
                ciudades.append(creencia.valores[0])  # dirección del jugador
            if creencia.tipo == TipoCreencia.CARTA_INFECCION_ROBADA:
                self.ciudad_infectar = creencia.valores[0].ciudad
            if creencia.tipo == TipoCreencia.INFECTANDO:
                creencias.remove(creencia)

        msgs = []
        for ciudad in range(len(ciudades[0])):
            if ciudades[0][ciudad].ciudad == self.ciudad_infectar:
                ciudades[0][ciudad].cubos += 1
                # se informa a todos los jugadores que la ciudad ha sido infectada con un cubo
                for jugador in jugadores:
                    msg = Message(to=jugador)  # Instantiate the message
                    msg.set_metadata("performative", "inform")  # Set the "inform" FIPA performative
                    # Se envia la creencia de que la ciudad ha sido infectada
                    msg_json = json.dumps({"tipo": TipoCreencia.CIUDAD_INFECTADA})
                    msg.body = msg_json
                    msgs.append(msg)

                print(f"Se ha infectado {ciudades[0][ciudad].ciudad}, tiene {ciudades[0][ciudad].cubos} cubos.")
                creenciaCiudadInfectada = Creencia(TipoCreencia.CIUDAD_INFECTADA,
                                                   [ciudades[0][ciudad].ciudad, ciudades[0][ciudad].cubos])
                creencias.append(creenciaCiudadInfectada)

        return creencias, msgs

    async def calculaprioridad(self, creencias):
        pass


class InfectarCiudad(Deseo):
    def __init__(self, intenciones_deseo, conceptos_deseo=[]):
        """Conceptos del deseo: []"""
        self.intenciones = intenciones_deseo
        self.conceptos = conceptos_deseo
        self.activo = False
        self.tipo = TipoDeseo.INFECTAR_CIUDAD

    def __eq__(self, other):
        return self.tipo == other.tipo

    async def comprobarimposible(self, creencias):
        cubos = []
        ciudades = []
        for creencia in creencias:
            if creencia.tipo == TipoCreencia.CUBOS:
                cubos.append(creencia.valores[0])
            if creencia.tipo == TipoCreencia.CIUDADES:
                ciudades.append(creencia.valores[0])
            if creencia.tipo == TipoCreencia.CARTA_INFECCION_ROBADA:
                ciudad_infectar = creencia.valores[0]

        if ciudad_infectar.cubos >= 3:
            return True

        for cubo in range(len(cubos[0])):
            if (cubos[0][cubo].color == ciudad_infectar.color) and (cubos[0][cubo].n_cubos <= 0):
                return True
        return False

    async def comprobarsatisfecho(self, creencias):
        for c in creencias:
            if c.tipo == TipoCreencia.CIUDAD_INFECTADA:
                return True
        return False

    async def comprobarinteres(self, creencias):
        pass

    async def comprobaractivar(self, creencias):
        llena = False
        for c1 in creencias:
            if c1.tipo == TipoCreencia.PARTIDA_LLENA:
                llena = True
        for c1 in creencias:
            if (c1.tipo == TipoCreencia.INFECTANDO) and llena:
                for c2 in creencias:
                    if (c2.tipo == TipoCreencia.CARTA_INFECCION_ROBADA) and llena:
                        return True

        return False


"""DESCARTAR CARTA"""


class Descartar_carta_Intencion(Intencion):
    def __init__(self, conceptos_intencion, posteriores):
        self.conceptos = conceptos_intencion
        self.tipo = TipoIntencion.DESCARTAR_CARTAS_JUGADOR
        self.coste = 0
        self.urgencia = 0
        self.prioridad = 0
        self.posteriores = posteriores

    async def comprobaralcanzada(self, creencias):
        # comprobar que un jugador tiene menos de 7 cartas
        for c in creencias:
            if c.tipo == TipoCreencia.EN_TURNO:
                jugador = c.valores[0]
                break

        variables = {"TipoCreencia.JUGADOR1_TIENE_CARTAS": TipoCreencia.JUGADOR1_TIENE_CARTAS,
                     "TipoCreencia.JUGADOR2_TIENE_CARTAS": TipoCreencia.JUGADOR2_TIENE_CARTAS}

        for c in creencias:
            if c.tipo == variables.get(jugador):
                if len(c.valores[0]) <= 7:
                    return True
        return False

    async def comprobaranulada(self, creencias):
        return False

    async def ejecuta(self, creencias):
        # determinamos los jugadores
        jugadores = []
        for creencia in creencias:
            if creencia.tipo == TipoCreencia.JUGADOR_DE_PARTIDA:
                jugadores.append(creencia.valores[0])  # dirección del jugador

        # determinamos el tablero
        for c in creencias:
            if c.tipo == TipoCreencia.ES_TABLERO:
                tablero_id = c.valores

        # determinamos el jugador actual
        for c in creencias:
            if c.tipo == TipoCreencia.EN_TURNO:
                jugador = c.valores[0]
                break

        variables = {"TipoCreencia.JUGADOR1_TIENE_CARTAS": TipoCreencia.JUGADOR1_TIENE_CARTAS,
                     "TipoCreencia.JUGADOR2_TIENE_CARTAS": TipoCreencia.JUGADOR2_TIENE_CARTAS}

        tipoCreenciaJugador = variables.get(jugador)

        for c in creencias:
            if c.tipo == tipoCreenciaJugador:
                mano = c.valores[0]
                break

        # sacar carta de la  mano
        carta_descartada = mano.pop(0)._dict_

        # meter carta en mazo descartes
        for creencia in creencias:
            if creencia.tipo == TipoCreencia.MAZO_DESCARTES_JUGADOR:
                creencia.valores[0].append(carta_descartada)
                mazo_descartes = creencia.valores[0]

        # mensajes para informar a otros jugadores y al tablero
        info_mano = json.dumps({"tipo": tipoCreenciaJugador, "lista_cartas": mano._dict_})
        info_desc = json.dumps({"tipo": TipoCreencia.MAZO_DESCARTES_JUGADOR, "lista_cartas": mazo_descartes._dict_})

        msgs = []
        for jugador_envio in jugadores:
            msg = Message(to=jugador_envio)
            msg.set_metadata("performative", "inform")
            msg.body = info_mano
            msgs.append(msg)  # Nueva Mano
            msg.body = info_desc
            msgs.append(msg)  # Descarte

        # A tablero
        msg = Message(to=tablero_id)
        msg.set_metadata("performative", "inform")
        msg.body = info_desc
        msgs.append(msg)  # Descarte

    async def calculaprioridad(self, creencias):
        pass


class DescartarCarta(Deseo):
    def __init__(self, intenciones_deseo, conceptos_deseo=[]):
        """Conceptos del deseo: []"""
        self.intenciones = intenciones_deseo
        self.conceptos = conceptos_deseo
        self.activo = False
        self.tipo = TipoDeseo.DESCARTAR_CARTA

    def __eq__(self, other):
        return self.tipo == other.tipo

    async def comprobarimposible(self, creencias):
        return False

    async def comprobarsatisfecho(self, creencias):
        # comprobar que un jugador tiene menos de 7 cartas
        for c in creencias:
            if c.tipo == TipoCreencia.EN_TURNO:
                jugador = c.valores[0]
                break

        variables = {"TipoCreencia.JUGADOR1_TIENE_CARTAS": TipoCreencia.JUGADOR1_TIENE_CARTAS,
                     "TipoCreencia.JUGADOR2_TIENE_CARTAS": TipoCreencia.JUGADOR2_TIENE_CARTAS}

        for c in creencias:
            if c.tipo == variables.get(jugador):
                if len(c.valores[0]) <= 7:
                    return True
        return False

    async def comprobarinteres(self, creencias):
        pass

    async def comprobaractivar(self, creencias):
        # comprobar que un jugador tiene más de 7 cartas
        for c in creencias:
            if c.tipo == TipoCreencia.EN_TURNO:
                jugador = c.valores[0]
                break

        variables = {"TipoCreencia.JUGADOR1_TIENE_CARTAS": TipoCreencia.JUGADOR1_TIENE_CARTAS,
                     "TipoCreencia.JUGADOR2_TIENE_CARTAS": TipoCreencia.JUGADOR2_TIENE_CARTAS}
        for c in creencias:
            if c.tipo == variables.get(jugador):
                if len(c.valores[0]) > 7:
                    return True
        return False



"""ERRADICAR ENFERMEDAD"""


class Erradicar_enfermedad_roja(Intencion):
    def __init__(self, conceptos_intencion, posteriores):
        """conceptos: baraja de cartas"""
        self.conceptos = conceptos_intencion
        self.tipo = TipoIntencion.ERRADICAR_ENFERMEDAD_ROJA
        # self.deseo = deseo_intencion
        self.coste = 0
        self.urgencia = 0
        self.prioridad = 0
        self.posteriores = posteriores

    def __repr__(self):
        return f"{str(self.tipo)}:{str(self.conceptos)}"

    async def comprobaralcanzada(self, creencias):
        for c in creencias:
            if c.tipo == TipoCreencia.ENFERMEDAD_ROJA_ERRADICADA:
                return True
        return False

    async def comprobaranulada(self, creencias):
        return False

    async def ejecuta(self, creencias):
        # encontrar jugadores
        jugadores = []
        for creencia in creencias:
            if creencia.tipo == TipoCreencia.UNIDO_A_PARTIDA:
                jugadores.append(creencia.valores[0])  # dirección del jugador

        msgs = []
        print("No hay ciudades de color rojo con cubos, por lo que se ha erradicado la enfermedad roja.")
        print("\n\n\n ---------------------------- ERRADICAR ROJA ----------------------------------- \n\n\n")
        miCreencia = Creencia(TipoCreencia.ENFERMEDAD_ROJA_ERRADICADA,
                              [])  # se añade la creencia de que la enfermedad está erradicada
        creencias.append(miCreencia)
        for jugador in jugadores:
            msg = Message(to=jugador)
            msg.set_metadata("performative", "inform")
            print("Se informa al jugador", jugador, "de que se ha erradicado la enfermedad de color rojo.")
            msg.body = json.dumps({"tipo": TipoCreencia.ENFERMEDAD_ROJA_ERRADICADA})  # Set the message content
            msgs.append(msg)

        return creencias, msgs

    async def calculaprioridad(self, creencias):
        pass


class Erradicar_enfermedad_azul(Intencion):
    def __init__(self, conceptos_intencion, posteriores):
        """conceptos: baraja de cartas"""
        self.conceptos = conceptos_intencion
        self.tipo = TipoIntencion.ERRADICAR_ENFERMEDAD_AZUL
        # self.deseo = deseo_intencion
        self.coste = 0
        self.urgencia = 0
        self.prioridad = 0
        self.posteriores = posteriores

    def __repr__(self):
        return f"{str(self.tipo)}:{str(self.conceptos)}"

    async def comprobaralcanzada(self, creencias):
        for c in creencias:
            if c.tipo == TipoCreencia.ENFERMEDAD_AZUL_ERRADICADA:
                return True
        return False

    async def comprobaranulada(self, creencias):
        return False

    async def ejecuta(self, creencias):
        # encontrar jugadores
        jugadores = []
        for creencia in creencias:
            if creencia.tipo == TipoCreencia.UNIDO_A_PARTIDA:
                jugadores.append(creencia.valores[0])  # dirección del jugador

        msgs = []
        print("No hay ciudades de color azul con cubos, por lo que se ha erradicado la enfermedad azul.")
        print("\n\n\n ---------------------------- ERRADICAR AZUL ----------------------------------- \n\n\n")
        miCreencia = Creencia(TipoCreencia.ENFERMEDAD_AZUL_ERRADICADA,
                              [])  # se añade la creencia de que la enfermedad está erradicada
        creencias.append(miCreencia)
        for jugador in jugadores:
            msg = Message(to=jugador)
            msg.set_metadata("performative", "inform")
            print("Se informa al jugador", jugador, "de que se ha erradicado la enfermedad de color azul.")
            msg.body = json.dumps({"tipo": TipoCreencia.ENFERMEDAD_AZUL_ERRADICADA})  # Set the message content
            msgs.append(msg)

        return creencias, msgs

    async def calculaprioridad(self, creencias):
        pass


class Erradicar_enfermedad_negra(Intencion):
    def __init__(self, conceptos_intencion, posteriores):
        """conceptos: baraja de cartas"""
        self.conceptos = conceptos_intencion
        self.tipo = TipoIntencion.ERRADICAR_ENFERMEDAD_NEGRA
        # self.deseo = deseo_intencion
        self.coste = 0
        self.urgencia = 0
        self.prioridad = 0
        self.posteriores = posteriores

    def __repr__(self):
        return f"{str(self.tipo)}:{str(self.conceptos)}"

    async def comprobaralcanzada(self, creencias):
        for c in creencias:
            if c.tipo == TipoCreencia.ENFERMEDAD_NEGRA_ERRADICADA:
                return True
        return False

    async def comprobaranulada(self, creencias):
        return False

    async def ejecuta(self, creencias):
        # encontrar jugadores
        jugadores = []
        for creencia in creencias:
            if creencia.tipo == TipoCreencia.UNIDO_A_PARTIDA:
                jugadores.append(creencia.valores[0])  # dirección del jugador

        msgs = []
        print("No hay ciudades de color negro con cubos, por lo que se ha erradicado la enfermedad negra.")
        print("\n\n\n ---------------------------- ERRADICAR NEGRA ----------------------------------- \n\n\n")
        miCreencia = Creencia(TipoCreencia.ENFERMEDAD_NEGRA_ERRADICADA,
                              [])  # se añade la creencia de que la enfermedad está erradicada
        creencias.append(miCreencia)
        for jugador in jugadores:
            msg = Message(to=jugador)
            msg.set_metadata("performative", "inform")
            print("Se informa al jugador", jugador, "de que se ha erradicado la enfermedad de color negro.")
            msg.body = json.dumps({"tipo": TipoCreencia.ENFERMEDAD_NEGRA_ERRADICADA})  # Set the message content
            msgs.append(msg)

        return creencias, msgs

    async def calculaprioridad(self, creencias):
        pass


class Erradicar_enfermedad_amarilla(Intencion):
    def __init__(self, conceptos_intencion, posteriores):
        """conceptos: baraja de cartas"""
        self.conceptos = conceptos_intencion
        self.tipo = TipoIntencion.ERRADICAR_ENFERMEDAD_AMARILLA
        # self.deseo = deseo_intencion
        self.coste = 0
        self.urgencia = 0
        self.prioridad = 0
        self.posteriores = posteriores

    def __repr__(self):
        return f"{str(self.tipo)}:{str(self.conceptos)}"

    async def comprobaralcanzada(self, creencias):
        for c in creencias:
            if c.tipo == TipoCreencia.ENFERMEDAD_AMARILLA_ERRADICADA:
                return True
        return False

    async def comprobaranulada(self, creencias):
        return False

    async def ejecuta(self, creencias):
        # encontrar jugadores
        jugadores = []
        for creencia in creencias:
            if creencia.tipo == TipoCreencia.UNIDO_A_PARTIDA:
                jugadores.append(creencia.valores[0])  # dirección del jugador

        msgs = []
        print(
            "No hay ciudades de color amarillo con cubos, por lo que se ha erradicado la enfermedad amarilla.")
        print(
            "\n\n\n ---------------------------- ERRADICAR AMARILLA ----------------------------------- \n\n\n")
        miCreencia = Creencia(TipoCreencia.ENFERMEDAD_AMARILLA_ERRADICADA,
                              [])  # se añade la creencia de que la enfermedad está erradicada
        creencias.append(miCreencia)
        for jugador in jugadores:
            msg = Message(to=jugador)
            msg.set_metadata("performative", "inform")
            print("Se informa al jugador", jugador, "de que se ha erradicado la enfermedad de color amarillo.")
            msg.body = json.dumps(
                {"tipo": TipoCreencia.ENFERMEDAD_AMARILLA_ERRADICADA})  # Set the message content
            msgs.append(msg)

        return creencias, msgs

    async def calculaprioridad(self, creencias):
        pass


class ErradicarEnfermedadRoja(Deseo):
    def __init__(self, intenciones_deseo, conceptos_deseo=[]):
        """Conceptos del deseo: []"""
        self.intenciones = intenciones_deseo
        self.conceptos = conceptos_deseo
        self.activo = False
        self.tipo = TipoDeseo.ERRADICAR_ENFERMEDAD_ROJA

    def __eq__(self, other):
        return self.tipo == other.tipo

    async def comprobarimposible(self, creencias):
        for c in creencias:
            if c.tipo == TipoCreencia.CIUDADES:
                ciudades = c.valores[0]  # cargamos las ciudades
                break

        # que haya ciudades de ese color infectadas
        for ciudad in ciudades:
            if ciudad.color == "Rojo":
                if ciudad.cubos > 0:
                    return True
        return False

    async def comprobarsatisfecho(self, creencias):
        for c in creencias:
            if c.tipo == TipoCreencia.ENFERMEDAD_ROJA_ERRADICADA:
                return True
        return False

    async def comprobarinteres(self, creencias):
        pass

    async def comprobaractivar(self, creencias):
        for c in creencias:
            if c.tipo == TipoCreencia.ENFERMEDAD_ROJA_ERRADICADA:
                return False

        vacuna_descubierta = False
        ciudades_infectadas = False

        for c in creencias:
            if c.tipo == TipoCreencia.VACUNA_ROJA_DESCUBIERTA:
                vacuna_descubierta = True

        # encontrar ciudades
        for c in creencias:
            if c.tipo == TipoCreencia.CIUDADES:
                ciudades = c.valores[0]  # cargamos las ciudades
                break

        # que haya ciudades de ese color infectadas
        for ciudad in ciudades:
            if ciudad.color == "Rojo":
                if ciudad.cubos > 0:
                    ciudades_infectadas = True

        if vacuna_descubierta and not ciudades_infectadas:
            return True
        return False


class ErradicarEnfermedadAzul(Deseo):
    def __init__(self, intenciones_deseo, conceptos_deseo=[]):
        """Conceptos del deseo: []"""
        self.intenciones = intenciones_deseo
        self.conceptos = conceptos_deseo
        self.activo = False
        self.tipo = TipoDeseo.ERRADICAR_ENFERMEDAD_AZUL

    def __eq__(self, other):
        return self.tipo == other.tipo

    async def comprobarimposible(self, creencias):
        for c in creencias:
            if c.tipo == TipoCreencia.CIUDADES:
                ciudades = c.valores[0]  # cargamos las ciudades
                break

        # que haya ciudades de ese color infectadas
        for ciudad in ciudades:
            if ciudad.color == "Azul":
                if ciudad.cubos > 0:
                    return True
        return False

    async def comprobarsatisfecho(self, creencias):
        for c in creencias:
            if c.tipo == TipoCreencia.ENFERMEDAD_AZUL_ERRADICADA:
                return True
        return False

    async def comprobarinteres(self, creencias):
        pass

    async def comprobaractivar(self, creencias):
        for c in creencias:
            if c.tipo == TipoCreencia.ENFERMEDAD_AZUL_ERRADICADA:
                return False

        vacuna_descubierta = False
        ciudades_infectadas = False

        for c in creencias:
            if c.tipo == TipoCreencia.VACUNA_AZUL_DESCUBIERTA:
                vacuna_descubierta = True

        # encontrar ciudades
        for c in creencias:
            if c.tipo == TipoCreencia.CIUDADES:
                ciudades = c.valores[0]  # cargamos las ciudades
                break

        # que haya ciudades de ese color infectadas
        for ciudad in ciudades:
            if ciudad.color == "Azul":
                if ciudad.cubos > 0:
                    ciudades_infectadas = True

        if vacuna_descubierta and not ciudades_infectadas:
            return True
        return False


class ErradicarEnfermedadNegra(Deseo):
    def __init__(self, intenciones_deseo, conceptos_deseo=[]):
        """Conceptos del deseo: []"""
        self.intenciones = intenciones_deseo
        self.conceptos = conceptos_deseo
        self.activo = False
        self.tipo = TipoDeseo.ERRADICAR_ENFERMEDAD_NEGRA

    def __eq__(self, other):
        return self.tipo == other.tipo

    async def comprobarimposible(self, creencias):
        for c in creencias:
            if c.tipo == TipoCreencia.CIUDADES:
                ciudades = c.valores[0]  # cargamos las ciudades
                break

        # que haya ciudades de ese color infectadas
        for ciudad in ciudades:
            if ciudad.color == "Negro":
                if ciudad.cubos > 0:
                    return True
        return False

    async def comprobarsatisfecho(self, creencias):
        for c in creencias:
            if c.tipo == TipoCreencia.ENFERMEDAD_NEGRA_ERRADICADA:
                return True
        return False

    async def comprobarinteres(self, creencias):
        pass

    async def comprobaractivar(self, creencias):
        for c in creencias:
            if c.tipo == TipoCreencia.ENFERMEDAD_NEGRA_ERRADICADA:
                return False

        vacuna_descubierta = False
        ciudades_infectadas = False

        for c in creencias:
            if c.tipo == TipoCreencia.VACUNA_NEGRA_DESCUBIERTA:
                vacuna_descubierta = True

        # encontrar ciudades
        for c in creencias:
            if c.tipo == TipoCreencia.CIUDADES:
                ciudades = c.valores[0]  # cargamos las ciudades
                break

        # que haya ciudades de ese color infectadas
        for ciudad in ciudades:
            if ciudad.color == "Negro":
                if ciudad.cubos > 0:
                    ciudades_infectadas = True

        if vacuna_descubierta and not ciudades_infectadas:
            return True
        return False


class ErradicarEnfermedadAmarilla(Deseo):
    def __init__(self, intenciones_deseo, conceptos_deseo=[]):
        """Conceptos del deseo: []"""
        self.intenciones = intenciones_deseo
        self.conceptos = conceptos_deseo
        self.activo = False
        self.tipo = TipoDeseo.ERRADICAR_ENFERMEDAD_AMARILLA

    def __eq__(self, other):
        return self.tipo == other.tipo

    async def comprobarimposible(self, creencias):
        for c in creencias:
            if c.tipo == TipoCreencia.CIUDADES:
                ciudades = c.valores[0]  # cargamos las ciudades
                break

        # que haya ciudades de ese color infectadas
        for ciudad in ciudades:
            if ciudad.color == "Amarillo":
                if ciudad.cubos > 0:
                    return True
        return False

    async def comprobarsatisfecho(self, creencias):
        for c in creencias:
            if c.tipo == TipoCreencia.ENFERMEDAD_AMARILLA_ERRADICADA:
                return True
        return False

    async def comprobarinteres(self, creencias):
        pass

    async def comprobaractivar(self, creencias):
        for c in creencias:
            if c.tipo == TipoCreencia.ENFERMEDAD_AMARILLA_ERRADICADA:
                return False

        vacuna_descubierta = False
        ciudades_infectadas = False

        for c in creencias:
            if c.tipo == TipoCreencia.VACUNA_AMARILLA_DESCUBIERTA:
                vacuna_descubierta = True

        # encontrar ciudades
        for c in creencias:
            if c.tipo == TipoCreencia.CIUDADES:
                ciudades = c.valores[0]  # cargamos las ciudades
                break

        # que haya ciudades de ese color infectadas
        for ciudad in ciudades:
            if ciudad.color == "Amarillo":
                if ciudad.cubos > 0:
                    ciudades_infectadas = True

        if vacuna_descubierta and not ciudades_infectadas:
            return True
        return False
