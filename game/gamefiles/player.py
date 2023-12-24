# At first I thought creating another class for the bullet but it's probably not necessary.

class Player:
    def __init__(self, position, direction):
        self.position = position        # First position info should be received from the server
        self.health = 3
        self.direction = direction      # W(up), A(Left), S(Down), D(Right), I(Idle)
        self.shoot = False
        self.hit = False
        self.powerup = 0                # I thought something like values: 0 = None, 1 = Extra Heart, 2 = Faster Bullets, 3 = Increased bullet damage

    def update_position(self, new_position):
        self.position = new_position

    def set_direction(self, new_direction):
        self.direction = new_direction

    def set_shoot(self, value):
        self.shoot = value

    def set_hit(self, value):
        self.hit = value

    def set_powerup(self, powerup_type):
        self.powerup = powerup_type
        self.apply_powerup()

    def apply_powerup(self):
        if self.powerup == 1:                                 # Extra Heart
            self.health += 1
        elif self.powerup == 2:                               # Faster Bullets
            self.shoot_bullet = self.shoot_bullet_fast
        elif self.powerup == 3:                               # Increased bullet damage
            self.shoot_bullet = self.shoot_bullet_strong
        
    def shoot_bullet(self):
        bullet_speed = 10
        bullet_damage = 1
        return Bullet(self.position, self.direction, bullet_speed, bullet_damage)         #This will be shooting the bullet

    def shoot_bullet_fast(self):
        bullet_speed = 20  # Doubled bullet speed
        bullet_damage = 1
        return Bullet(self.position, self.direction, bullet_speed, bullet_damage)

    def shoot_bullet_strong(self):
        bullet_speed = 10
        bullet_damage = 2  # Doubled bullet damage
        return Bullet(self.position, self.direction, bullet_speed, bullet_damage)

    def hit_by_bullet(self, bullet):
        if self.position == bullet.position:
            self.health -= bullet.damage
