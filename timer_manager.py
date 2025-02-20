import time

class TimerManager:
    def __init__(self, max_time):
        self.max_time = max_time
        self.red_time = max_time
        self.black_time = max_time
        self.last_move_time = time.time()
        self.red_turn = True  # Keep track of whose turn it is here

    def update_timers(self):
        current_time = time.time()
        time_elapsed = current_time - self.last_move_time

        if self.red_turn:
            self.red_time -= time_elapsed
            if self.red_time < 0:
                self.red_time = 0
                # Handle game over (black wins)
        else:
            self.black_time -= time_elapsed
            if self.black_time < 0:
                self.black_time = 0
                # Handle game over (red wins)

        self.last_move_time = current_time

    def switch_turn(self):
        self.red_turn = not self.red_turn
        self.last_move_time = time.time()  # Reset timer after turn switch

    def get_times(self):
        return self.red_time, self.black_time

    def get_turn(self):
        return self.red_turn

    def set_time(self, red_time, black_time):  # For resetting or setting initial time
        self.red_time = red_time
        self.black_time = black_time

    def reset(self): # reset all
        self.red_time = self.max_time
        self.black_time = self.max_time
        self.last_move_time = time.time()
        self.red_turn = True