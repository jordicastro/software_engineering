# Player Data Class
class Player:
    def __init__(self, player_id: int, name: str, equip_id: int, score: int):
        self.player_id = player_id
        self.name = name
        self.equip_id = equip_id
        self.team = equip_id % 2 != 0
        self.score = score

    # Returns a string representation of the player object
    def __str__(self):
        return f'Player {self.player_id}: {self.name}, on {"Red" if self.team else "Green"} team, with {self.score} points'

    # Helper for encoding player data to json for database
    def encode(self):
        return {'player_id': self.player_id, 'name': self.name, 'equip_id': self.equip_id, 'team': self.team, 'score': self.score}
