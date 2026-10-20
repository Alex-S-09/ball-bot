import time
from drivetrain import Drivetrain
from intake import Intake
from flywheel import Flywheel
from indexer import Indexer
from hood import Hood


class Robot:
    def __init__(self):
        self.drive = Drivetrain()
        self.intake = Intake()
        self.flywheel = Flywheel()
        self.indexer = Indexer()
        self.hood = Hood()

    def shoot(self, balls=1, hood_angle=0, delay_s=0.3):
        """Fire `balls` balls, one at a time, at the given hood angle."""
        self.hood.set_angle(hood_angle)
        try:
            self.flywheel.spin_up()
            for _ in range(balls):
                self.indexer.release_one()
                time.sleep(delay_s)  # flywheel recovers between shots
        finally:
            self.flywheel.off()

    def stop(self):
        """Try to stop everything, even if one part fails."""
        for action in (self.drive.stop, self.intake.stop,
                       self.flywheel.off, self.indexer.close):
            try:
                action()
            except Exception as e:
                print(f"stop error in {action.__qualname__}: {e}")