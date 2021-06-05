Для разработки 2D игры выбрана библиотека pygame, т.к. она включает в себя все необходимые инструменты для создания игр.
Как вспомогательные библиотеки используются:

os - предоставляет функционал для работы с ОС, на которой запущена игра.
https://docs.python.org/3/library/os.html

threading - реализация потоков в Python
https://docs.python.org/3/library/threading.html

random - генерация псевдорандомных чисел
https://docs.python.org/3/library/random.html

PIL - библиотека для работы с изображениями, состоящая из нескольких модулей
https://pillow.readthedocs.io/en/stable/reference/index.html

Игра представляет из себя платформер, в котором робот перманентно бежит, а игрок управляя им с помощью клавиатуры, должен преодолевать препятствия. Персонаж может прыгать и пригибаться.

Изначально задаются все статичные данные, такие как 
- размер игрового окна
- изначальные позиции и размеры элементов
- скорость игры
- название окна
- массивы картинок для анимации

Объекты игрового мира описаны в классах:
- Robot (игрок, бегущий робот)
- Cloud (облако, как элемент декорации)
- Man (препятствие в виде человека / людей)
- Bird (пролетающая птица)
- Obstacle (препятствие, класс, как родитель для всех препятствий)

Процесс игры осуществляется в вечном цикле `while`, который как раз позволяет создать анимацию и показать результат взаимодействия персонажа с игровым миром.

Оценка игры зависит от максимального времени, до которого игрок врежется в препятствие, при этом скорость игры постоянно повышается, что увеличивает сложность.

Модуль `Image` библиотеки `PIL` понадобился, чтобы обрезать все кадры анимации до определенного размера.

Библиотека `random` использована для случайного появления препятствий.