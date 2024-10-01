from Agente import BDIAgent
from creencias_deseos_intenciones import *
import json

class JugadorAgent(BDIAgent):
    def __init__(self, agent_jid, agent_password):
        super(BDIAgent, self).__init__(agent_jid, agent_password)
        #Atributo para diferenciar la primera ejecución del ciclo BDI
        self.iniciada_llamada_tablero = False

    """----------------Métodos Ciclo BDI----------------"""

    async def actualizaCreencias(self, msg):
        # actualizaciones de las creencias?

        msg_decodificado = json.loads(msg.body)

        if msg_decodificado.get('tipo') == TipoCreencia.UNIDO_A_PARTIDA and msg.get_metadata("performative") == "agree":
            tablero_id = msg.sender
            miCreencia = Creencia(TipoCreencia.UNIDO_A_PARTIDA, [tablero_id])
            self.misCreencias.append(miCreencia)
            self.imprimir_agente(f"Agente jugador {self.jid} recibe mensaje agree a petición de unirse a la partida")

        if msg_decodificado.get('tipo') == TipoCreencia.JUGADOR_DE_PARTIDA:# para que los jugadores conozcan al resto
            miCreencia = Creencia(TipoCreencia.JUGADOR_DE_PARTIDA, [msg_decodificado.get('jugador')])
            self.misCreencias.append(miCreencia)

        if msg_decodificado.get('tipo') == TipoCreencia.TURNO_FINALIZADO:# para que los jugadores conozcan al resto
            creencia_encontrada = False
            jugador_anterior = msg.sender.localpart + '@' + msg.sender.domain
            miCreencia = Creencia(TipoCreencia.TURNO_FINALIZADO, [jugador_anterior])
            for creencia in self.misCreencias:
                if creencia.tipo == TipoCreencia.TURNO_FINALIZADO:
                    creencia = miCreencia
                    creencia_encontrada = True
                    self.imprimir_agente(f"Agente jugador {self.jid} recibe mensaje inform del fin del turno")
                    self.imprimir_agente(f"Creencias de {self.jid} ahora: {self.misCreencias}")
            if not creencia_encontrada:
                self.misCreencias.append(miCreencia)

        if msg_decodificado.get('tipo') == TipoCreencia.JUGADOR1_TIENE_CARTAS:
            lista_cartas_json = msg_decodificado.get('lista_cartas')
            if msg_decodificado.get('carta_robada'):
                miCreencia = Creencia(TipoCreencia.ACCIONES_TERMINADAS, [])
                self.misCreencias.append(miCreencia)
                for creencias in self.misCreencias:
                    if creencias.tipo == TipoCreencia.ROBANDO:
                        self.misCreencias.remove(creencias)
            for carta in lista_cartas_json:
                for creencia in self.misCreencias:
                    if creencia.tipo == TipoCreencia.JUGADOR1_TIENE_CARTAS:
                        creencia.valores[0].append(Carta_ciudad(carta.get("ciudad"), carta.get("color")))

        if msg_decodificado.get('tipo') == TipoCreencia.JUGADOR2_TIENE_CARTAS:
            lista_cartas_json =  msg_decodificado.get('lista_cartas')
            if msg_decodificado.get('carta_robada'):
                miCreencia = Creencia(TipoCreencia.ACCIONES_TERMINADAS, [])
                self.misCreencias.append(miCreencia)
                for creencias in self.misCreencias:
                    if creencias.tipo == TipoCreencia.ROBANDO:
                        self.misCreencias.remove(creencias)
            for carta in lista_cartas_json:
                for creencia in self.misCreencias:
                    if creencia.tipo == TipoCreencia.JUGADOR2_TIENE_CARTAS:
                        creencia.valores[0].append(Carta_ciudad(carta.get("ciudad"), carta.get("color")))

        if msg_decodificado.get('tipo') == TipoCreencia.ERES_JUGADOR:
            miCreencia = Creencia(TipoCreencia.ERES_JUGADOR, [msg_decodificado.get('num_jugador')])
            self.misCreencias.append(miCreencia)

            variables = {"TipoCreencia.JUGADOR1_TIENE_CARTAS": TipoCreencia.JUGADOR1_TIENE_CARTAS, "TipoCreencia.JUGADOR2_TIENE_CARTAS": TipoCreencia.JUGADOR2_TIENE_CARTAS}
            for c in self.misCreencias:
                if c.tipo == variables.get(f"TipoCreencia.JUGADOR{msg_decodificado.get('num_jugador')}_TIENE_CARTAS"):
                    mano_cartas = c.valores[0]
            miCreencia = Creencia(TipoCreencia.NUM_CARTAS, [len(mano_cartas)])
            self.misCreencias.append(miCreencia)

        # /////////////////////////////////////////////// INICIO LUNA ///////////////////////////////////////////////
        if msg_decodificado.get('tipo') == TipoCreencia.MAZO_DESCARTES_JUGADOR:
            lista_cartas = []
            lista_cartas_json = msg_decodificado.get('lista_cartas')
            for carta in lista_cartas_json:
                lista_cartas.append(Carta_ciudad(carta.get("ciudad"), (carta.get("color"))))
            miCreencia = Creencia(TipoCreencia.MAZO_DESCARTES_JUGADOR, lista_cartas)
            self.misCreencias.append(miCreencia)
        # /////////////////////////////////////////////// FIN LUNA ///////////////////////////////////////////////

        # /////////////////////////////////////////////// INICIO JORGE ///////////////////////////////////////////////
        if msg_decodificado.get(
                'tipo') == TipoCreencia.ENFERMEDAD_ROJA_ERRADICADA:  # para que todos los jugadores sepan que la enfermedad se ha erradicado
            miCreencia = Creencia(TipoCreencia.ENFERMEDAD_ROJA_ERRADICADA, [])
            self.misCreencias.append(miCreencia)

        if msg_decodificado.get(
                'tipo') == TipoCreencia.ENFERMEDAD_AZUL_ERRADICADA:  # para que todos los jugadores sepan que la enfermedad se ha erradicado
            miCreencia = Creencia(TipoCreencia.ENFERMEDAD_AZUL_ERRADICADA, [])
            self.misCreencias.append(miCreencia)

        if msg_decodificado.get(
                'tipo') == TipoCreencia.ENFERMEDAD_NEGRA_ERRADICADA:  # para que todos los jugadores sepan que la enfermedad se ha erradicado
            miCreencia = Creencia(TipoCreencia.ENFERMEDAD_NEGRA_ERRADICADA, [])
            self.misCreencias.append(miCreencia)

        if msg_decodificado.get(
                'tipo') == TipoCreencia.ENFERMEDAD_AMARILLA_ERRADICADA:  # para que todos los jugadores sepan que la enfermedad se ha erradicado
            miCreencia = Creencia(TipoCreencia.ENFERMEDAD_AMARILLA_ERRADICADA, [])
            self.misCreencias.append(miCreencia)
        # /////////////////////////////////////////////// FIN JORGE ///////////////////////////////////////////////
    """----------------Ejecución del agente jugador----------------"""

    async def setup(self):
        print(f"JugadorAgent {self.jid} started")
        # buscaria en el df al tablero
        # time.sleep(1) # le damos tiempo al tablero a registrarse en el df
        # dad = spade.DF.DfAgentDescription()
        # sd  = spade.DF.ServiceDescription()
        # sd.setName("Tablero")
        # dad.addService(sd)
        # Tablero_Id = agent.searchService (sd)
        # tablero_Id = "idmitablero"  # alternativamente le asignamos el id de la cuenta de xmpp correspondiente como si ya lo conociera
        self.misCreencias = []
        self.misIntenciones = []
        self.misDeseos = []
        self.nuevo_fichero_imprimir()

        creenciaMazoJ1 = Creencia(TipoCreencia.JUGADOR1_TIENE_CARTAS, [[]])
        creenciaMazoJ2 = Creencia(TipoCreencia.JUGADOR2_TIENE_CARTAS, [[]])
        self.misCreencias.append(creenciaMazoJ1)
        self.misCreencias.append(creenciaMazoJ2)
        tablero_id = ["boardiao@magicbroccoli.de"]
        miCreencia = Creencia(TipoCreencia.ES_TABLERO, tablero_id)
        self.misCreencias.append(miCreencia)

        miIntencion = Pedir_Unirse([], [])
        # self.misIntenciones.append(miIntencion)

        miDeseo = Jugar([miIntencion])
        miDeseo.activo = False
        self.misDeseos.append(miDeseo)

        miIntencion = Finalizar_Turno([], [])
        miDeseo = Informar_Final_Turno([miIntencion])
        miDeseo.activo = False
        self.misDeseos.append(miDeseo)

        intencionJugarTurno = Jugar_Turno_intencion([],[])
        deseoJugarTurno = JugarTurno([intencionJugarTurno], [])
        self.misDeseos.append(deseoJugarTurno)

        #deseo robar cartas
        intencionRobarCarta = Robar_carta_intencion([],[])
        deseoRobarCarta = RobarCarta([intencionRobarCarta], [])
        self.misDeseos.append(deseoRobarCarta)

        # deseo repartir cartas
       # intencionDescartarCarta = Descartar_carta_Intencion([], [])
       # deseoDescartarCarta = DescartarCarta([intencionDescartarCarta])
       # miDeseo.activo = False
       # self.misDeseos.append(deseoDescartarCarta)

        cicloBDI = self.BDIBehav()
        self.add_behaviour(cicloBDI)