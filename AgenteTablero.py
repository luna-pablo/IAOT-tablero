from Agente import BDIAgent
from creencias_deseos_intenciones import *
import json

from objetos_tablero import Ciudad, Cubo


class TableroAgent(BDIAgent):
    """----------------Métodos Ciclo BDI----------------"""

    async def actualizaCreencias(self, msg):
        """Método sobrescrito por cada tipo de agente"""
        msg_json = json.loads(msg.body)
        if msg_json.get('tipo') == TipoCreencia.JUGADOR_SOLICITA_UNIRSE and msg.get_metadata(
                "performative") == "request":
            miCreencia = Creencia(TipoCreencia.JUGADOR_SOLICITA_UNIRSE, msg.sender)
            self.misCreencias.append(miCreencia)
            self.imprimir_agente("Recibe solicitud unirse a la partida")
            self.imprimir_agente(f"Creencias del tablero ahora:\n   "
                                 f"{[(creencia, creencia.valores) for creencia in self.misCreencias]}")

        if msg_json.get('tipo') == TipoCreencia.TURNO_FINALIZADO:  # para que los jugadores conozcan al resto
            creencia_encontrada = False
            jugador_anterior = msg.sender.localpart + '@' + msg.sender.domain

            miCreencia = Creencia(TipoCreencia.TURNO_FINALIZADO, [jugador_anterior])
            for creencia in self.misCreencias:
                if creencia.tipo == TipoCreencia.TURNO_FINALIZADO:
                    self.misCreencias[self.misCreencias.index(creencia)] = miCreencia
                    creencia_encontrada = True
                    self.imprimir_agente(f"Agente jugador {self.jid} recibe mensaje inform del fin del turno")
                if creencia.tipo == TipoCreencia.CARTA_ENTREGADA:
                    self.misCreencias.remove(creencia)
                if creencia.tipo == TipoCreencia.REPARTIR_CARTA_INFECCION or creencia.tipo == TipoCreencia.REPARTIR_CARTA:
                    self.misCreencias.remove(creencia)
            if not creencia_encontrada:
                self.misCreencias.append(miCreencia)

        if msg_json.get('tipo') == TipoCreencia.SOLICITUD_CARTA and msg.get_metadata("performative") == "request":
            creencia_encontrada = False
            miCreencia = Creencia(TipoCreencia.REPARTIR_CARTA, [msg_json.get('jugador')])
            for creencia in self.misCreencias:
                if creencia.tipo == TipoCreencia.REPARTIR_CARTA:
                    self.misCreencias[self.misCreencias.index(creencia)] = miCreencia
                    creencia_encontrada = True
            if not creencia_encontrada:
                self.misCreencias.append(miCreencia)

            self.imprimir_agente("Recibe solicitud de dar una carta de ciudad que el jugador quiere robar")
            self.imprimir_agente(f"Creencias del tablero ahora:\n   "
                                 f"{[(creencia, creencia.valores) for creencia in self.misCreencias]}")

        if msg_json.get('tipo') == TipoCreencia.SOLICITUD_CARTA_INFECCION and msg.get_metadata(
                "performative") == "request":
            miCreencia = Creencia(TipoCreencia.REPARTIR_CARTA_INFECCION, [msg_json.get('jugador')])
            self.misCreencias.append(miCreencia)
            self.imprimir_agente("Recibe solicitud de dar una carta de infección que el jugador quiere robar")
            self.imprimir_agente(f"Creencias del tablero ahora:\n   "
                                 f"{[(creencia, creencia.valores) for creencia in self.misCreencias]}")

        if msg_json.get('tipo') == TipoCreencia.MAZO_DESCARTES_JUGADOR:
            lista_cartas = []
            lista_cartas_json = msg_json.get('lista_cartas')
            for carta in lista_cartas_json:
                lista_cartas.append(Carta_ciudad(carta.get("ciudad"), (carta.get("color"))))
            miCreencia = Creencia(TipoCreencia.MAZO_DESCARTES_JUGADOR, lista_cartas)
            self.misCreencias.append(miCreencia)

    """----------------Ejecución del agente----------------"""

    async def setup(self):
        self.imprimir_agente(f"TableroAgent {self.jid} started")
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

        # creencias iniciales del tablero

        # objetos iniciales del tablero:
        mazo = [Carta_ciudad("Las Rozas", "Azul"),
                Carta_ciudad("Torrelodones", "Azul"),
                Carta_ciudad("Collado Villalba", "Azul"),
                Carta_ciudad("Colmenarejo", "Amarillo"),
                Carta_ciudad("Getafe", "Amarillo"),
                Carta_ciudad("Leganes", "Amarillo"),
                Carta_ciudad("Aluche", "Rojo"),
                Carta_ciudad("Piramides", "Rojo"),
                Carta_ciudad("Moncloa", "Rojo"),
                Carta_ciudad("San Blas", "Negro"),
                Carta_ciudad("Alcorcón", "Negro"),
                Carta_ciudad("Orcasitas", "Negro")]

        # al iniciarse la partida algunos tienen cubos según lo q haya tocado en funcion de las cartas
        ciudades = [Ciudad("LasRozas", "Azul", 0, ["ColladoVillalba", "Leganes"]),
                    Ciudad("ColladoVillalba", "Azul", 0, ["LasRozas", "Torrelodones", "Getafe"]),
                    Ciudad("Torrelodones", "Azul", 0, ["ColladoVillalba", "Colmenarejo"]),
                    Ciudad("Colmenarejo", "Amarillo", 0, ["Torrelodones", "Getafe", "Moncloa"]),
                    Ciudad("Getafe", "Amarillo", 0, ["ColladoVillalba", "Colmenarejo", "Aluche", "Leganés"]),
                    Ciudad("Leganés", "Amarillo", 0, ["Piramides", "Getafe", "LasRozas"]),
                    Ciudad("Aluche", "Rojo", 0, ["Moncloa", "Orcasitas", "Pirámides", "Getafe"]),
                    Ciudad("Moncloa", "Rojo", 0, ["Aluche", "Colmenarejo", "Alcorcón"]),
                    Ciudad("Pirámides", "Rojo", 0, ["SanBlas", "Leganés", "Aluche"]),
                    Ciudad("Alcorcón", "Negro", 0, ["Orcasitas", "Moncloa"]),
                    Ciudad("Orcasitas", "Negro", 0, ["Aluche", "Alcorcón", "SanBlas"]),
                    Ciudad("SanBlas", "Negro", 0, ["Orcasitas", "Pirámides"])]

        cubos = [Cubo("Rojo", 8),
                 Cubo("Azul", 8),
                 Cubo("Amarillo", 8),
                 Cubo("Negro", 8)]

        tablero_id = "boardiao@magicbroccoli.de"
        creenciaEsTablero = Creencia(TipoCreencia.ES_TABLERO, tablero_id)
        creenciaMazo = Creencia(TipoCreencia.MAZO_JUGADORES, [mazo])
        self.misCreencias.append(creenciaEsTablero)
        self.misCreencias.append(creenciaMazo)

        creenciaCiudades = Creencia(TipoCreencia.CIUDADES, [ciudades])
        creenciaCubos = Creencia(TipoCreencia.CUBOS, [cubos])
        self.misCreencias.append(creenciaCiudades)
        self.misCreencias.append(creenciaCubos)

        creenciaInfectando = Creencia(TipoCreencia.INFECTANDO, [])
        self.misCreencias.append(creenciaInfectando)
        creenciaInfeccionRobada = Creencia(TipoCreencia.CARTA_INFECCION_ROBADA, [ciudades[5]])
        self.misCreencias.append(creenciaInfeccionRobada)

        creenciaMazoDescartes = Creencia(TipoCreencia.MAZO_DESCARTES_JUGADOR, [[]])
        self.misCreencias.append(creenciaMazoDescartes)

        numero_jugadores = 2

        # deseo registrar jugadores
        intencionFinalizarRegistro = Finalizar_registro([numero_jugadores], [])
        intencionRegistroJ2 = Registrar_jugador(["player2iao@magicbroccoli.de"], [intencionFinalizarRegistro])
        intencionRegistroJ1 = Registrar_jugador(["player1iao@magicbroccoli.de"], [intencionRegistroJ2])
        # self.misIntenciones.append(intencionRegistroJ1)
        deseoRegistrarJugadores = RegistrarJugadores([intencionRegistroJ1, intencionRegistroJ2], [numero_jugadores])

        # deseo repartir cartas
        intencionRepartirCartas = Repartir_cartas_iniciales_intencion([], [])
        deseoRepartirCartas = RepartirCartasIniciales([intencionRepartirCartas], [])

        # deseo repartir cartas
        intencionaDarCarta = Dar_carta_intencion([], [])
        deseoDarCartas = DarCarta([intencionaDarCarta], [])

        # deseo infectar ciudad
        IntencionInfectarCiudad = Infectar_ciudad([], [])
        deseoInfectarCiudad = InfectarCiudad([IntencionInfectarCiudad], [])

        # incluir todos los deseos

        intencionErradicarEnfermedadRoja = Erradicar_enfermedad_roja([], [])
        deseoErradicarEnfermedadRoja = ErradicarEnfermedadRoja([intencionErradicarEnfermedadRoja])

        intencionErradicarEnfermedadAzul = Erradicar_enfermedad_azul([], [])
        deseoErradicarEnfermedadAzul = ErradicarEnfermedadAzul([intencionErradicarEnfermedadAzul])

        intencionErradicarEnfermedadNegra = Erradicar_enfermedad_negra([], [])
        deseoErradicarEnfermedadNegra = ErradicarEnfermedadNegra([intencionErradicarEnfermedadNegra])

        intencionErradicarEnfermedadAmarilla = Erradicar_enfermedad_amarilla([], [])
        deseoErradicarEnfermedadAmarilla = ErradicarEnfermedadAmarilla([intencionErradicarEnfermedadAmarilla])

        self.misDeseos.append(deseoRegistrarJugadores)
        self.misDeseos.append(deseoRepartirCartas)
        self.misDeseos.append(deseoDarCartas)
        self.misDeseos.append(deseoInfectarCiudad)
        self.misDeseos.append(deseoErradicarEnfermedadRoja)
        self.misDeseos.append(deseoErradicarEnfermedadAzul)
        self.misDeseos.append(deseoErradicarEnfermedadNegra)
        self.misDeseos.append(deseoErradicarEnfermedadAmarilla)

        cicloBDI = self.BDIBehav()
        self.add_behaviour(cicloBDI)
