// data.js

const rawData = [
  // ========== КАТЕГОРИИ (этапы познания) ==========
  {id: 'cat_phenomenon', title: 'явление',   year: 0},
  {id: 'cat_term',       title: 'термин',    year: 0},
  {id: 'cat_hypothesis', title: 'гипотеза',  year: 0},
  {id: 'cat_theory',     title: 'теория',    year: 0},
  {id: 'cat_formula',    title: 'формула',   year: 0},

  // ============================================================
  // 1. ПЕРВЫЕ НАБЛЮДЕНИЯ И ТЕРМИНЫ
  // ============================================================
  {id: 'quantity_observed',
   title: 'замечено количество',
   year: -50000, category: 'cat_phenomenon',
   child: ['one_to_one'],
   description: 'Человек заметил, что в одной группе предметов столько же, сколько в другой. Первое осознанное наблюдение количества — ещё без чисел.'},

  {id: 'one_to_one',
   title: 'один к одному',
   year: -30000, category: 'cat_term',
   parent: ['quantity_observed'],
   child: ['difference_observed', 'more_less'],
   description: 'Взаимно-однозначное соответствие: камень ↔ овца, палец ↔ предмет. Первый инструмент счёта.'},

  {id: 'difference_observed',
   title: 'замечена разница',
   year: -25000, category: 'cat_phenomenon',
   parent: ['one_to_one'],
   child: ['more_less'],
   description: 'Человек заметил, что одна группа может быть больше или меньше другой. Это явление, а не термин — оно наблюдается.'},

  {id: 'more_less',
   title: 'больше / меньше',
   year: -20000, category: 'cat_term',
   parent: ['difference_observed', 'one_to_one'],
   child: ['counting'],
   description: 'Термины для описания разницы. Основа для понятий порядка и неравенства.'},

  {id: 'counting',
   title: 'счёт',
   year: -10000, category: 'cat_term',
   parent: ['more_less'],
   child: ['number', 'measurement'],
   description: 'Пересчёт предметов: зарубки, узелки, пальцы. Появляется порядковый и количественный счёт.'},

  {id: 'number',
   title: 'число',
   year: -5000, category: 'cat_term',
   parent: ['counting'],
   child: ['digit'],
   description: 'Абстрактное число отрывается от предметов. Появляются системы счисления: вавилонская, римская, десятичная.'},

  {id: 'digit',
   title: 'цифра',
   year: -3000, category: 'cat_term',
   parent: ['number'],
   child: ['operations'],
   description: 'Символ для записи числа. Египетские иероглифы, вавилонская клинопись, индийские цифры (через арабов пришли в Европу).'},

  {id: 'operations',
   title: 'арифметические действия',
   year: -2000, category: 'cat_term',
   parent: ['digit'],
   child: ['measurement'],
   description: 'Сложение, вычитание, умножение, деление — операции над числами для учёта, торговли и строительства.'},

  // ============================================================
  // 2. ИЗМЕРЕНИЕ, ЭТАЛОНЫ, ВЕС
  // ============================================================
  {id: 'measurement',
   title: 'измерение',
   year: -3000, category: 'cat_term',
   parent: ['counting', 'operations'],
   child: ['standard', 'weight_term'],
   description: 'Сравнение с эталоном: локоть, шаг, вес зерна. Появляются единицы измерения длины, массы, времени.'},

  {id: 'standard',
   title: 'эталон',
   year: -2500, category: 'cat_term',
   parent: ['measurement'],
   child: ['balance_scales'],
   description: 'Фиксированный эталон: царский локоть, талант, стадий. Обеспечивает воспроизводимость измерений.'},

  {id: 'weight_observed',
   title: 'замечен вес тел',
   year: -3000, category: 'cat_phenomenon',
   child: ['weight_term'],
   description: 'Человек заметил: одни предметы тяжелее, другие легче. Причина ещё не известна.'},

  {id: 'weight_term',
   title: 'вес',
   year: -2500, category: 'cat_term',
   parent: ['weight_observed', 'measurement'],
   child: ['balance_scales', 'mass_term'],
   description: 'Термин для описания тяжести предмета. Позже будет разделён на массу и вес.'},

  {id: 'balance_scales',
   title: 'весы',
   year: -2000, category: 'cat_term',
   parent: ['weight_term', 'standard'],
   description: 'Инструмент для сравнения веса: рычажные, коромысловые. Основной прибор торговли и лабораторий.'},

  // ============================================================
  // 3. ПОВТОРЯЮЩИЕСЯ ЯВЛЕНИЯ И КАЛЕНДАРЬ
  // ============================================================
  {id: 'repeated_phenomenon',
   title: 'повторяющиеся явления',
   year: -3000, category: 'cat_phenomenon',
   parent: ['measurement'],
   child: ['calendar', 'heliocentric_hypothesis', 'evolution_theory'],
   description: 'Наблюдение циклов: день/ночь, фазы Луны, времена года, разливы рек. Первое осознание периодичности.'},

  {id: 'calendar',
   title: 'календарь',
   year: -2000, category: 'cat_term',
   parent: ['repeated_phenomenon'],
   description: 'Формализация циклов: лунный, солнечный, лунно-солнечный календарь. Позволяет предсказывать сезоны.'},

  // ============================================================
  // 4. АСТРОНОМИЯ: ГИПОТЕЗА КОПЕРНИКА
  // ============================================================
  {id: 'heliocentric_hypothesis',
   title: 'гипотеза Коперника',
   year: 1543, category: 'cat_hypothesis',
   parent: ['repeated_phenomenon'],
   child: ['kepler_laws'],
   description: 'Николай Коперник предположил, что в центре мира — Солнце, а не Земля. Это противоречило церкви, но объясняло движение планет.'},

  {id: 'kepler_laws',
   title: 'законы Кеплера',
   year: 1609, category: 'cat_formula',
   parent: ['heliocentric_hypothesis'],
   child: ['heliocentric_theory'],
   description: 'Три закона движения планет: эллипсы, равные площади за равные времена, T² ∝ a³. Впервые планеты описаны математически.'},

  {id: 'heliocentric_theory',
   title: 'гелиоцентрическая теория',
   year: 1619, category: 'cat_theory',
   parent: ['kepler_laws'],
   child: ['gravity_hypothesis'],
   description: 'Гелиоцентризм подтверждён наблюдениями Галилея (спутники Юпитера, фазы Венеры) и расчётами Кеплера.'},

  // ============================================================
  // 5. ГАЛИЛЕЙ: ПАДЕНИЕ ТЕЛ
  // ============================================================
  {id: 'falling_bodies_observed',
   title: 'замечено ускорение при падении',
   year: 1600, category: 'cat_phenomenon',
   child: ['falling_bodies_hypothesis', 'speed_term'],
   description: 'Галилей заметил: при падении тела движутся всё быстрее. Скорость растёт со временем.'},

  {id: 'speed_term',
   title: 'скорость',
   year: 1600, category: 'cat_term',
   parent: ['falling_bodies_observed'],
   child: ['acceleration_term'],
   description: 'Термин для описания быстроты движения. Позже — путь, делённый на время.'},

  {id: 'acceleration_term',
   title: 'ускорение',
   year: 1600, category: 'cat_term',
   parent: ['speed_term'],
   child: ['force_term'],
   description: 'Термин для изменения скорости со временем. Галилей установил, что при свободном падении ускорение одинаково для всех тел.'},

  {id: 'falling_bodies_hypothesis',
   title: 'гипотеза о свободном падении',
   year: 1600, category: 'cat_hypothesis',
   parent: ['falling_bodies_observed'],
   child: ['inertia_hypothesis'],
   description: 'Галилей предположил: тела падают с одинаковым ускорением независимо от массы. Проверил опытами на наклонной плоскости.'},

  {id: 'pendulum_observed',
   title: 'замечены колебания маятника',
   year: 1602, category: 'cat_phenomenon',
   child: ['inertia_hypothesis'],
   description: 'Галилей заметил: период маятника почти не зависит от амплитуды. Это наблюдение о сохранении движения.'},

  {id: 'inertia_hypothesis',
   title: 'гипотеза инерции',
   year: 1638, category: 'cat_hypothesis',
   parent: ['falling_bodies_hypothesis', 'pendulum_observed'],
   child: ['gravity_hypothesis'],
   description: 'Галилей: тело, на которое не действуют силы, сохраняет скорость. Позже Ньютон сделал это первым законом.'},

  // ============================================================
  // 6. НЬЮТОН: ГРАВИТАЦИЯ И МЕХАНИКА
  // ============================================================
  {id: 'force_term',
   title: 'сила',
   year: 1666, category: 'cat_term',
   parent: ['acceleration_term'],
   child: ['mass_term', 'gravity_hypothesis'],
   description: 'Термин для причины изменения движения. Ньютон связал силу с ускорением и массой.'},

  {id: 'mass_term',
   title: 'масса',
   year: 1666, category: 'cat_term',
   parent: ['weight_term', 'force_term'],
   description: 'Мера инертности тела. Отличается от веса: масса одинакова везде, вес зависит от гравитации.'},

  {id: 'gravity_hypothesis',
   title: 'гипотеза всемирного тяготения',
   year: 1666, category: 'cat_hypothesis',
   parent: ['inertia_hypothesis', 'heliocentric_theory', 'force_term'],
   child: ['newton_mechanics'],
   description: 'Ньютон предположил: все тела притягиваются с силой, пропорциональной массам и обратно пропорциональной квадрату расстояния.'},

  {id: 'newton_mechanics',
   title: 'классическая механика',
   year: 1687, category: 'cat_theory',
   parent: ['gravity_hypothesis'],
   child: ['newton_second_law', 'gravity_law'],
   description: 'Три закона Ньютона и закон всемирного тяготения. Первая количественная теория природы, объясняющая движение тел и планет.'},

  {id: 'newton_second_law',
   title: 'второй закон Ньютона',
   year: 1687, category: 'cat_formula',
   parent: ['newton_mechanics'],
   description: 'F = m·a. Сила равна произведению массы на ускорение. Основной закон динамики.'},

  {id: 'gravity_law',
   title: 'закон всемирного тяготения',
   year: 1687, category: 'cat_formula',
   parent: ['newton_mechanics'],
   description: 'F = G · m₁·m₂ / r². Сила притяжения двух тел. Объясняет падение яблока и движение планет одним законом.'},

  // ============================================================
  // 7. ЭЛЕКТРОМАГНЕТИЗМ
  // ============================================================
  {id: 'electromagnetic_theory',
   title: 'электромагнитная теория',
   year: 1865, category: 'cat_theory',
   parent: ['newton_mechanics'],
   child: ['maxwell_equations'],
   description: 'Максвелл объединил электричество, магнетизм и оптику в единую теорию. Предсказал радиоволны.'},

  {id: 'maxwell_equations',
   title: 'уравнения Максвелла',
   year: 1865, category: 'cat_formula',
   parent: ['electromagnetic_theory'],
   child: ['relativity'],
   description: 'Четыре уравнения, описывающие электромагнитное поле. Из них следует постоянство скорости света.'},

  // ============================================================
  // 8. ТЕОРИЯ ОТНОСИТЕЛЬНОСТИ
  // ============================================================
  {id: 'relativity',
   title: 'теория относительности',
   year: 1905, category: 'cat_theory',
   parent: ['newton_mechanics', 'maxwell_equations'],
   child: ['emc2'],
   description: 'Эйнштейн: пространство и время относительны, скорость света постоянна. Расширяет механику Ньютона для больших скоростей.'},

  {id: 'emc2',
   title: 'E = mc²',
   year: 1905, category: 'cat_formula',
   parent: ['relativity'],
   description: 'Эквивалентность массы и энергии. Масса — это форма энергии, и наоборот.'},

  // ============================================================
  // 9. КВАНТОВАЯ МЕХАНИКА
  // ============================================================
  {id: 'quantum_mechanics',
   title: 'квантовая механика',
   year: 1925, category: 'cat_theory',
   parent: ['electromagnetic_theory'],
   child: ['schrodinger_equation'],
   description: 'Планк, Бор, Шрёдингер, Гейзенберг. Описывает микромир: дискретность энергии, волны вероятности, принцип неопределённости.'},

  {id: 'schrodinger_equation',
   title: 'уравнение Шрёдингера',
   year: 1926, category: 'cat_formula',
   parent: ['quantum_mechanics'],
   description: 'iħ ∂ψ/∂t = Ĥψ. Основное уравнение квантовой механики. Описывает, как меняется волновая функция во времени.'},

  // ============================================================
  // 10. БИОЛОГИЯ: ДАРВИН
  // ============================================================
  {id: 'evolution_theory',
   title: 'теория эволюции',
   year: 1859, category: 'cat_theory',
   parent: ['repeated_phenomenon'],
   description: 'Дарвин: виды меняются под действием естественного отбора. Объясняет разнообразие жизни на Земле.'},
];
