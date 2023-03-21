class Camera:
    def __init__(self, offset_x: int, offset_y: int, window_size: list[int], fraction = 1, true_scroll = [0,0]):
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.fraction = fraction
        self.true_scroll = true_scroll
        self.scroll = [0,0]

        # Boundary Setup
        self.on_boundary = False
        self.window_size = window_size
        self.margin_x = self.boundary_x / 2.5
        self.margin_y = self.boundary_y / 2.5

    def setup_scroll(self, target): # Use in a loop
        self.true_scroll[0] += (target.x - self.true_scroll[0] - self.offset_x) / self.fraction
        self.true_scroll[1] += (target.y - self.true_scroll[1] - self.offset_y) / self.fraction
        self.scroll = list(map(int, self.true_scroll))

    def apply_boundary(self, target):
        if self.scroll[0] >= self.boundary_x:
            if (target.x < self.margin_x):
                self.on_boundary = False
            else:
                self.on_boundary = True

    def run(self, target):
        # self.apply_boundary(target)
        # if not self.on_boundary:
        self.setup_scroll(target)
