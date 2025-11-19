import logging

from src.domain.interfaces.base_command import BaseCommand
from src.domain.interfaces.shootable_object import IShootableObject
from src.domain.interfaces.targetable_object import ITargetableObject
from src.domain.models.vector import Vector
from src.domain.exceptions import shoot as exceptions

logger = logging.getLogger(__name__)


class ShootCommand(BaseCommand):
    """Абстрактная команда для выполнения выстрела"""

    def __init__(
            self,
            shooter: IShootableObject,
            targets: list[ITargetableObject]
    ):
        self._shooter = shooter
        self._targets = targets

    def execute(self) -> None:
        weapon = self._shooter.get_weapon()
        if not weapon.can_shoot():
            raise exceptions.WeaponCanNotShootError("Shoot failed: Weapon is not ready.")

        range_limit = weapon.get_range()
        for target in self._targets:
            if target is self._shooter:
                continue
            if not target.is_alive():
                continue
            # Проверка попадания
            if self._is_target_in_line_of_fire(target.get_position(), range_limit):
                current_health_points = target.get_health_points()
                new_health_points = max(0, current_health_points - weapon.get_damage())
                target.set_health_points(new_health_points)

    def _is_target_in_line_of_fire(
            self,
            target_position: Vector,
            max_range: int | None = None
    ) -> bool:
        shooter_position = self._shooter.get_position()
        weapon_direction = self._shooter.get_velocity()

        # Вектор от стреляющего к цели
        diff_x = target_position.x - shooter_position.x
        diff_y = target_position.y - shooter_position.y

        # Векторное произведение
        cross = diff_x * weapon_direction.y - diff_y * weapon_direction.x
        print(f"cross: {cross}")
        if cross != 0:
            return False

        # Скалярное произведение
        dot = diff_x * weapon_direction.x + diff_y * weapon_direction.y
        if dot < 0:
            return False

        # Проверка дальности
        if max_range is not None:
            dist_sq = diff_x * diff_x + diff_y * diff_y
            if dist_sq > max_range * max_range:
                return False

        return True
