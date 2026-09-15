import rumps
from rumps.notifications import notify


class PomoTimerApp(rumps.App):
    def __init__(self):
        super(PomoTimerApp, self).__init__("PoMo")
        self.menu = ["Start", "Stop", "Settings", "Test"]
        self.work_min = 25
        self.break_min = 5
        self.timer = rumps.Timer(self.tick, 1)
        self.seconds_left = self.work_min * 60
        self.on_break = False
        self.running = False

    @rumps.clicked("Start")
    def start(self, _):
        if not self.running:
            self.running = True
            self.on_break = False
            self.timer.start()
            self.menu["Settings"].set_callback(None)

    @rumps.clicked("Stop")
    def stop(self, _):
        if self.running:
            self.running = False
            self.timer.stop()
            self.title = "PoMo"
            self.menu["Settings"].set_callback(self.settings)

    @rumps.clicked("Settings")
    def settings(self, _):
        # TODO prevent new second_left from overriding current processes
        settings_window = rumps.Window(
            message=f"set your own timings for work and break.\n\n Work: {self.work_min} \n Break: {self.break_min}",
            title="PoMo Settings",
            dimensions=(0, 0),
        )
        settings_window.add_buttons(["Work 25 / Break 5", "Work 50 / Break 10"])
        response = settings_window.run()
        if not response.clicked == 1:
            if response.clicked == 2:
                self.work_min = 25
                self.break_min = 5
                self.seconds_left = 25 * 60
            elif response.clicked == 3:
                self.work_min = 50
                self.break_min = 10
                self.seconds_left = 50 * 60

    def tick(self, timer):
        self.seconds_left -= 1
        self.title = f"{self.seconds_left // 60:02d}:{self.seconds_left % 60:02d}"
        if self.seconds_left <= 0:
            self.timer.stop()
            self.running = False
            self.seconds_left = self.work_min * 60
            self.title = "PoMo"
            rumps.notification(
                title="PoMo",
                subtitle="Work session complete",
                message="Time for a break!",
                sound=True,
            )


if __name__ == "__main__":
    PomoTimerApp().run()
