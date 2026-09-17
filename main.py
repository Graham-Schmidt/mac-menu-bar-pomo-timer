import rumps


class PomoTimerApp(rumps.App):
    def __init__(self):
        super(PomoTimerApp, self).__init__("PoMo")
        self.menu = ["Start", "Stop", "Settings"]
        self.work_min = 25
        self.break_min = 5
        self.timer = rumps.Timer(self.tick, 1)
        self.seconds_left = self.work_min * 60
        self.on_break = False
        self.running = False

    @rumps.clicked("Start")
    def start(self, _):
        if not self.running:
            if not self.on_break:
                self.seconds_left = self.work_min * 60
            else:
                self.seconds_left = self.break_min * 60
            self.running = True
            self.timer.start()
            self.menu["Settings"].set_callback(None)
            self.add_skip_menu_item()
            self.set_skip_label()

    @rumps.clicked("Stop")
    def stop(self, _):
        if self.running:
            self.running = False
            self.timer.stop()
            self.title = "PoMo"
            self.enable_settings()

    @rumps.clicked("Settings")
    def settings(self, _):
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
    
    def skip(self, _):
        if self.on_break:
            self.menu["Skip"].title = "Skip Break"
        else:
            self.menu["Skip"].title = "Skip Work"
        self.stop(None)
        self.remove_skip_menu_item()
        self.swap_break_status()
    
    def tick(self, timer):
        self.seconds_left -= 1
        self.title = f"{self.seconds_left // 60:02d}:{self.seconds_left % 60:02d}"
        if self.seconds_left <= 0:
            self.timer.stop()
            self.running = False
            self.title = "PoMo"
            self.swap_break_status()
            if self.on_break:
                self.notify_break_end()
            else:
                self.notify_work_end()
            self.enable_settings()

    def swap_break_status(self):
        self.on_break = not self.on_break

    def notify_work_end(self):
        rumps.notification(
            title="PoMo",
            subtitle="Work session complete",
            message="Time for a break!",
            sound=True,
        )
        self.enable_settings()

    def notify_break_end(self):
        rumps.notification(
            title="PoMo",
            subtitle="Break session complete",
            message="Time for work!",
            sound=True,
        )
        self.enable_settings()

    def enable_settings(self):
        self.menu["Settings"].set_callback(self.settings)

    def set_skip_label(self):
        if self.on_break:
            self.menu["Skip"].title = "Skip Break"
        else:
            self.menu["Skip"].title = "Skip Work"

    def add_skip_menu_item(self):
        self.menu.insert_before("Settings", self.skip_menu)

    def remove_skip_menu_item(self):
        if "Skip Break" in self.menu.keys():
            self.menu.pop("Skip Break")
        # elif "Skip Work" in self.menu.keys():
        else:
            print(self)
            self.menu.pop("Skip Work")

    skip_menu = rumps.MenuItem(
        title="Skip",
        callback=skip
        )

# TODO build standalone "Skip" menu item, insert only after start(), change name

if __name__ == "__main__":
    PomoTimerApp().run()
