class GamifiedCLI:
    def __init__(self):
        self.progress = 0
        self.milestones = [25, 50, 75, 100]

    def update_progress(self, increment: int) -> None:
        self.progress += increment
        self.progress = min(self.progress, 100)  # Cap progress at 100%
        print(f"Progress updated: {self.progress}%")
        self._check_milestones()

    def _check_milestones(self) -> None:
        for milestone in self.milestones:
            if self.progress >= milestone:
                self.display_achievement(f"Reached {milestone}% milestone!")
                self.milestones.remove(milestone)

    @staticmethod
    def display_achievement(message: str) -> None:
        print(f"🎉 Achievement Unlocked: {message}")
