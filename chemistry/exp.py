'''
эксперимент с катодными лучами
- Класс Electron моделирует электрон с зарядом, массой, положением и скоростью.
- Класс Field задает поле и вычисляет силу Лоренца.
- В CathodeRayExperiment модель запускает движение электрона в поле
с шагом по времени и сохраняет координаты.
- В конце эксперимент запускается с начальной скоростью
электрона и электрическим полем, создающим отклонение катодного луча.

Таким образом, код моделирует отклонение электрона в электрическом
поле, аналогично опыту Томсона.
'''

import math

# Класс для частицы (электрон)
class Electron:
    def __init__(self, charge=-1.6e-19, mass=9.11e-31):
        self.charge = charge     # заряд электрона, Кл
        self.mass = mass         # масса электрона, кг
        self.position = [0, 0]   # координаты на плоскости (x, y), м
        self.velocity = [0, 0]   # скорость (vx, vy), м/с

    def set_velocity(self, vx, vy):
        self.velocity = [vx, vy]

    def update_position(self, dt):
        # обновление координат с движением по скорости
        self.position[0] += self.velocity[0] * dt
        self.position[1] += self.velocity[1] * dt

# Класс для пространства с полями (электрическим и магнитным)
class Field:
    def __init__(self, E=(0, 0), B=(0, 0, 0)):
        self.E = E  # Электрическое поле (Ex, Ey), В/м
        self.B = B  # Магнитное поле (Bx, By, Bz), Тл

    def lorentz_force(self, particle):
        q = particle.charge
        vx, vy = particle.velocity
        # Возьмем поле B только по оси z (обычно магнитное поле направлено перпендикулярно плоскости движения)
        Bz = self.B[2]

        # Электрическая сила: F = qE
        Fx = q * self.E[0]
        Fy = q * self.E[1]

        # Магнитная сила: F = q(v x B)
        # В двумерной плоскости (x,y) и Bz направлено по z:
        Fx += q * vy * Bz
        Fy -= q * vx * Bz

        return Fx, Fy

# Класс для моделирования эксперимента
class CathodeRayExperiment:
    def __init__(self, electron, field, dt=1e-9, total_time=1e-6):
        self.electron = electron
        self.field = field
        self.dt = dt
        self.total_time = total_time
        self.positions = []

    def run(self):
        t = 0
        while t < self.total_time:
            Fx, Fy = self.field.lorentz_force(self.electron)
            ax = Fx / self.electron.mass
            ay = Fy / self.electron.mass

            # Обновляем скорость
            self.electron.velocity[0] += ax * self.dt
            self.electron.velocity[1] += ay * self.dt

            # Обновляем позицию
            self.electron.update_position(self.dt)

            # Сохраняем положение для анализа
            self.positions.append(tuple(self.electron.position))
            t += self.dt

    def get_trajectory(self):
        return self.positions

# Настройка эксперимента

# Изначальная скорость электрона (вдоль оси x)
electron = Electron()
electron.set_velocity(1e7, 0)  # 10 млн м/с

# Электрическое поле отклонения вдоль y
E_field = (0, 1e4)  # В/м
# Магнитное поле направлено вдоль z
B_field = (0, 0, 0)  # Тл

field = Field(E=E_field, B=B_field)

experiment = CathodeRayExperiment(electron, field, dt=1e-11, total_time=5e-8)
experiment.run()

# Выводим траекторию полученную эксперимента (сокращенно)
trajectory = experiment.get_trajectory()

print("Координаты электрона по времени (образец):")
for i in range(0, len(trajectory), len(trajectory)//10):
    print(f"t={i * experiment.dt:.2e}s - x={trajectory[i][0]:.4e}m, y={trajectory[i][1]:.4e}m")
