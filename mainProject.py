import time
from AgenteJugador import JugadorAgent
from AgenteTablero import TableroAgent

if __name__ == "__main__":
    AGENTS = {"board": "boardiao@magicbroccoli.de",
              "player1": "player1iao@magicbroccoli.de",
              "player2": "player2iao@magicbroccoli.de"}
    PASSWORD = "qwertyytrewq"

    agentetablero = TableroAgent(AGENTS["board"], PASSWORD)
    future_tablero = agentetablero.start()
    future_tablero.result()
    agentejugador1 = JugadorAgent(AGENTS["player1"], PASSWORD)
    future_jugador1 = agentejugador1.start()
    future_jugador1.result()
    agentejugador2 = JugadorAgent(AGENTS["player2"], PASSWORD)
    future_jugador2 = agentejugador2.start()
    future_jugador2.result()

    while agentetablero.is_alive():
        try:
            time.sleep(0.5)
        except KeyboardInterrupt:
            agentejugador1.stop()
            agentejugador2.stop()
            agentetablero.stop()
            break
    print("Agents finished")


"""
Cosas que hacer:
    - mandar primer ciclo BDI especial al método setup del agente
    - a cada mensaje del agente le asociamos un comportamiento? o solo a algunos mensajes?
    - qué pasa con el bucle while del agente tablero
    - lógica para la primera iteración?
    - deseo jugar instanciarlo con las intenciones dentro
    - si el deseo es un conjunto de intenciones, por qué hay lista de intenciones posteriores asociada a cada intención
    - en registrar jugadores, la creencia siempre tiene un solo valor?
    - AWAIT EN CALCULARPRIORIDADES????
    
Dudas:
    - Enviar mensaje a varios jugadores con una intención
        - enviar varios msg?
        - hay algo en spade? -> ver proxy
    - Que los jugadores hablen entre sí ignorando al tablero
    - Intenciones posteriores, no es la inmediatamente siguiente?
Cosas que ha dicho el profesor (07/11)
    - no debería hacer falta bucle while agente.is_alive()
"""