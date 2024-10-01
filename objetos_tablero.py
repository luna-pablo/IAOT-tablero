class Carta_ciudad:
    def __init__(self, ciudad, color):
        self.ciudad = ciudad
        self.color = color

    def __eq__(self, other):
        return self.ciudad == other.ciudad

    def __repr__(self):
        return f"Ciudad {self.ciudad} de color {self.color}"


class Carta_evento:
    def __init__(self, tipo):
        self.tipo = tipo

    def __eq__(self, other):
        return self.tipo == other.tipo

    def __repr__(self):
        return self.tipo


class Carta_ciudad_infeccion:
    def __init__(self, ciudad, color):
        self.ciudad = ciudad
        self.color = color

    def __eq__(self, other):
        return self.ciudad == other.ciudad

    def __repr__(self):
        return f"Carta de ciudad {self.ciudad} con infección de color {self.color}"


class Ciudad:
    def __init__(self, ciudad, color, cubos, conectada):
        self.ciudad = ciudad
        self.color = color
        self.cubos = cubos
        self.conectada = conectada

    def __eq__(self, other):
        return self.ciudad == other.ciudad

    def __repr__(self):
        return f"Ciudad {self.ciudad} infectada de color {self.color} con {self.cubos} número de cubos"


class Cubo:
    def __init__(self, color, n_cubos):
        self.color = color
        self.n_cubos = n_cubos

    def __eq__(self, other):
        return self.color == other.color

    def __repr__(self):
        return f"Quedan {self.n_cubos} cubos de color {self.color}"