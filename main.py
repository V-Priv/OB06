import random

class Weapon:
    def __init__(self, name, attack_boost):
        self.name = name
        self.attack_boost = attack_boost

    def calculate_damage(self):
        return self.attack_boost


class MeleeWeapon(Weapon):
    def __init__(self, name, attack_boost):
        super().__init__(name, attack_boost)


class RangedWeapon(Weapon):
    def __init__(self, name, attack_boost):
        super().__init__(name, attack_boost)


class Hero:
    def __init__(self, name, health=100, base_attack_power=20, weapon=None, shield=False):
        self.name = name
        self.health = health
        self.base_attack_power = base_attack_power
        self.weapon = weapon
        self.shield = shield
        self.weapon_removed_due_to_shield = False

    def attack(self, other):
        if self.weapon_removed_due_to_shield:
            self.weapon = None  # Убираем оружие только на один раунд
            self.weapon_removed_due_to_shield = False

        damage = self.calculate_damage(other)
        other.health -= damage
        weapon_name = self.weapon.name if self.weapon else 'без оружия'
        print(f"{self.name} атакует {other.name} с помощью {weapon_name} и наносит {damage} урона.")

        if other.shield and isinstance(self.weapon, MeleeWeapon):
            print(f"{other.name} использовал щит. {self.name} атакует без оружия в следующем раунде.")
            self.weapon_removed_due_to_shield = True  # Отметка для снятия оружия в следующем раунде

            # Увеличиваем здоровье, если другой герой использовал щит
            other.health += 10
            print(f"{other.name} применил щит и увеличил здоровье на 10. Теперь у него {other.health} здоровья.")

    def calculate_damage(self, other):
        weapon_power = self.weapon.calculate_damage() if self.weapon else 0
        damage = self.base_attack_power + weapon_power

        if other.shield and isinstance(self.weapon, MeleeWeapon):
            damage -= 10

        return max(damage, 0)

    def is_alive(self):
        return self.health > 0


class Game:
    def __init__(self):
        self.player_weapons = [RangedWeapon("арбалет", 10,), MeleeWeapon("меч", 15),RangedWeapon("праща", 20)]
        self.computer_weapons = [MeleeWeapon("топор", 12), RangedWeapon("лук", 8),RangedWeapon("катапульта",40)]
        self.player = self.create_hero("Игрок", self.player_weapons)
        self.computer = self.create_hero("Компьютер", self.computer_weapons)

    def create_hero(self, name, weapons):
        weapon = random.choice(weapons)
        shield = random.choice([True, False])
        return Hero(name, weapon=weapon, shield=shield)

    def start(self):
        print("Начало игры!")
        while self.player.is_alive() and self.computer.is_alive():
            input("Нажмите Enter, чтобы начать раунд...")
            self.round()

        self.declare_winner()

    def round(self):
        self.choose_weapon_for_player()
        self.player.attack(self.computer)
        print(f"У {self.computer.name} осталось {self.computer.health} здоровья.\n")

        if self.computer.is_alive():
            self.choose_weapon_for_computer()
            self.computer.attack(self.player)
            print(f"У {self.player.name} осталось {self.player.health} здоровья.\n")

    def choose_weapon_for_player(self):
        print("Выберите оружие:")
        for i, weapon in enumerate(self.player_weapons, start=1):
            print(f"{i}. {weapon.name} (бонус атаки: {weapon.attack_boost})")

        choice = int(input("Введите номер оружия: ")) - 1
        if 0 <= choice < len(self.player_weapons):
            self.player.weapon = self.player_weapons[choice]
        else:
            print("Неверный выбор, оружие не изменено.")

    def choose_weapon_for_computer(self):
        self.computer.weapon = random.choice(self.computer_weapons)

    def declare_winner(self):
        if self.player.is_alive():
            print("Игрок победил!")
        else:
            print("Компьютер победил!")


if __name__ == "__main__":
    game = Game()
    game.start()