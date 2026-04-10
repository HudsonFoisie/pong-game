class BattlePass:
    def __init__(self):
        self.levels = {}  # Dictionary to hold levels and their rewards
        self.current_level = 0  # Player's current level
        self.skins = []  # List to hold acquired skins

    def add_level(self, level, rewards):
        self.levels[level] = rewards

    def progress(self):
        if self.current_level + 1 in self.levels:
            self.current_level += 1
        else:
            print("No more levels to progress to!")

    def get_rewards(self):
        return self.levels.get(self.current_level, "No rewards for this level!")

    def acquire_skin(self, skin):
        self.skins.append(skin)

    def show_progress(self):
        return f'Current Level: {self.current_level}, Skins Acquired: {self.skins}'

# Example of usage
battle_pass = BattlePass()
battle_pass.add_level(1, "Bronze Skin")
battle_pass.add_level(2, "Silver Skin")
battle_pass.add_level(3, "Gold Skin")
battle_pass.progress()
battle_pass.acquire_skin("Bronze Skin")

# Display current progress and rewards
print(battle_pass.show_progress())
print(battle_pass.get_rewards())