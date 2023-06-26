from dataclasses import dataclass, asdict
from typing import Type


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    message: str = ('Тип тренировки: {training_type};'
                    ' Длительность: {duration:.3f} ч.;'
                    ' Дистанция: {distance:.3f} км;'
                    ' Ср. скорость: {speed:.3f} км/ч;'
                    ' Потрачено ккал: {calories:.3f}.')

    def get_message(self) -> str:
        """Вывод сообщения на экран."""
        return self.message.format(**asdict(self))


class Training:
    """Базовый класс тренировки."""

    LEN_STEP = 0.65
    M_IN_KM = 1000
    H_IN_MIN = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return self.duration * self.weight

    def duration_in_min(self) -> float:
        """Перевод длительности тренировки в минуты."""
        return self.duration * self.H_IN_MIN

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__, self.duration,
                           self.get_distance(),
                           self.get_mean_speed(), self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""
    CALORIES_MEAN_SPEED_MULTIPLIER = 18
    CALORIES_MEAN_SPEED_SHIFT = 1.79

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return (((self.CALORIES_MEAN_SPEED_MULTIPLIER
                  * self.get_mean_speed()
                  + self.CALORIES_MEAN_SPEED_SHIFT)
                 * self.weight)
                / self.M_IN_KM) * self.duration_in_min()


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    CALORIES_WEIGHT_RATIO_SPENT_MULTIPLIER = 0.035
    CALORIES_MEAN_SPEED_RATIO_MULTIPLIER = 0.029
    KM_PER_H_IN_METR_PER_SEC = 0.278
    SM_IN_M = 100

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        mean_sport_speed = (self.get_mean_speed()
                            * self.KM_PER_H_IN_METR_PER_SEC)
        spent_calories = ((self.CALORIES_WEIGHT_RATIO_SPENT_MULTIPLIER
                           * self.weight + (mean_sport_speed ** 2
                                            / (self.height / self.SM_IN_M))
                           * self.CALORIES_MEAN_SPEED_RATIO_MULTIPLIER
                           * self.weight) * self.duration_in_min())
        return spent_calories


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP = 1.38
    CALORIES_WEIGHT_RATIO_SPENT_MULTIPLIER = 2
    CALORIES_MEAN_SPEED_SHIFT = 1.1

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: int
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return ((self.get_mean_speed() + self.CALORIES_MEAN_SPEED_SHIFT)
                * self.CALORIES_WEIGHT_RATIO_SPENT_MULTIPLIER
                * self.weight * self.duration)


def read_package(workout_name: str, statistics: list[float]) -> Training:
    """Прочитать данные полученные от датчиков."""
    commands: dict[str, Type[Training]] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    if workout_name not in commands:
        raise ValueError('Такого вида тренировки не существует.')
    return commands[workout_name](*statistics)


def main(session: Training) -> None:
    """Главная функция."""
    info = session.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
