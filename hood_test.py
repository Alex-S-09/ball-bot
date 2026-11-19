from hood import Hood

hood = Hood()   # moves to angle 0 immediately, so keep the hood clear

print("Type an angle between -40 and 40, 'c' to center, or 'q' to quit")
try:
    while True:
        cmd = input("> ").strip().lower()
        if cmd == "q":
            break
        elif cmd == "c":
            hood.set_angle(0)
        else:
            try:
                hood.set_angle(float(cmd))
                print(f"angle = {hood.angle}")
            except ValueError:
                print("type a number, c, or q")
finally:
    hood.servo.detach()   # stops sending the signal so it doesn't buzz
    print("done")