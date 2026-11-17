from intake import Intake

intake = Intake(power=0.3)  # start low; raise it later

print("f = forward, r = reverse, s = stop, q = quit")
try:
    while True:
        cmd = input("> ").strip().lower()
        if cmd == "f":
            intake.intake()
        elif cmd == "r":
            intake.reverse()
        elif cmd == "s":
            intake.stop()
        elif cmd == "q":
            break
finally:
    intake.stop()
    print("stopped")