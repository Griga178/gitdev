class QuantumState:
    def __init__(self, energy_level, spin, orbital_momentum):
        self.energy_level = energy_level         # уровень энергии, например 1, 2, 3…
        self.spin = spin                         # спин электрона (+1/2, -1/2)
        self.orbital_momentum = orbital_momentum # орбитальный квантовый число

    def __repr__(self):
        return f"QuantumState(E={self.energy_level}, S={self.spin}, L={self.orbital_momentum})"

class Electron:
    def __init__(self, quantum_state):
        self.quantum_state = quantum_state

    def __repr__(self):
        return f"Electron({self.quantum_state})"


class Atom:
    def __init__(self, protons, neutrons, electrons=None):
        self.protons = protons          # число протонов (заряд ядра)
        self.neutrons = neutrons        # число нейтронов
        self.electrons = electrons or [] # список объектов Electron

    @property
    def atomic_number(self):
        return self.protons

    @property
    def mass_number(self):
        return self.protons + self.neutrons

    @property
    def charge(self):
        return self.protons - len(self.electrons)  # заряд иона

    def add_electron(self, electron):
        self.electrons.append(electron)

    def __repr__(self):
        return (f"Atom(protons={self.protons}, neutrons={self.neutrons}, "
                f"electrons={self.electrons}, charge={self.charge})")
class Particle:
    def __init__(self, mass, charge, spin):
        self.mass = mass
        self.charge = charge
        self.spin = spin

class Electron(Particle):
    def __init__(self, quantum_state):
        super().__init__(mass=9.11e-31, charge=-1, spin=0.5)
        self.quantum_state = quantum_state

class Proton(Particle):
    def __init__(self):
        super().__init__(mass=1.67e-27, charge=+1, spin=0.5)

class Neutron(Particle):
    def __init__(self):
        super().__init__(mass=1.67e-27, charge=0, spin=0.5)





# Пример использования
qs1 = QuantumState(1, +0.5, 0)
el1 = Electron(qs1)
atom = Atom(1, 0, [el1])  # атом водорода
print(atom)
