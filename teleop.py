import curses
from robot import Robot

HOOD_STEP = 5
SPEED_STEP = 0.1


class Test:
    def __init__(self):
        self.r = Robot()

    def main(self, screen):
        r = self.r
        screen.timeout(150)  # getch() returns -1 if no key within 150 ms
        speed = 0.4
        intake_on = False
        flywheel_on = False
        driving = False
        last = "ready"

        try:
            while True:
                screen.erase()
                screen.addstr(0, 0, "TELEOP TEST  (hold a drive key to move; release to stop)")
                screen.addstr(2, 0, "W/S  forward / back       A/D  turn left / right")
                screen.addstr(3, 0, "SPACE stop                +/-  drive speed")
                screen.addstr(4, 0, "I    intake on/off        R    intake reverse (jam)")
                screen.addstr(5, 0, "F    flywheel on/off      X    fire one ball")
                screen.addstr(6, 0, "[ ]  hood angle down/up   Q    quit (stops everything)")
                screen.addstr(8, 0, f"speed={speed:.1f}  hood={r.hood.angle}  "
                                    f"intake={'ON' if intake_on else 'off'}  "
                                    f"flywheel={'ON' if flywheel_on else 'off'}")
                screen.addstr(9, 0, f"last: {last}")
                screen.refresh()

                key = screen.getch()

                # No key pressed recently: stop driving
                if key == -1:
                    if driving:
                        r.drive.stop()
                        driving = False
                    continue

                c = chr(key).lower() if 0 <= key < 256 else ""
                if not c:
                    continue  # arrow keys, resize events, etc.

                if c == "q":
                    break
                elif c == "w":
                    r.drive.move(speed); driving = True; last = "forward"
                elif c == "s":
                    r.drive.move(-speed); driving = True; last = "back"
                elif c == "a":
                    r.drive.move(0, -speed); driving = True; last = "turn left"
                elif c == "d":
                    r.drive.move(0, speed); driving = True; last = "turn right"
                elif c == " ":
                    r.drive.stop(); driving = False; last = "drive stopped"
                elif c in "+=":
                    speed = min(1.0, speed + SPEED_STEP); last = "speed up"
                elif c in "-_":
                    speed = max(0.1, speed - SPEED_STEP); last = "speed down"
                elif c == "i":
                    intake_on = not intake_on
                    if intake_on:
                        r.intake.intake()
                    else:
                        r.intake.stop()
                    last = "intake toggled"
                elif c == "r":
                    r.intake.reverse(); intake_on = False
                    last = "intake reversed (press I twice to restart)"
                elif c == "f":
                    flywheel_on = not flywheel_on
                    if flywheel_on:
                        screen.addstr(9, 0, "spinning up...            ")
                        screen.refresh()
                        r.flywheel.spin_up()
                    else:
                        r.flywheel.off()
                    last = "flywheel toggled"
                elif c == "x":
                    if flywheel_on:
                        r.indexer.release_one(); last = "fired one ball"
                    else:
                        last = "turn flywheel on first (F)"
                elif c == "[":
                    r.hood.set_angle(r.hood.angle - HOOD_STEP); last = "hood down"
                elif c == "]":
                    r.hood.set_angle(r.hood.angle + HOOD_STEP); last = "hood up"
        finally:
            r.stop()


if __name__ == "__main__":
    curses.wrapper(Test().main)