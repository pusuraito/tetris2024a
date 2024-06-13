import tkinter as tk
import random

# 定数
FIELD_WIDTH = 10
FIELD_HEIGHT = 20
BLOCK_SIZE = 30
UPDATE_INTERVAL = 500

# テトリミノの形状と色
SHAPES = [
    [(1, 1, 1, 1)],  # I
    [(1, 1, 1), (0, 1, 0)],  # T
    [(1, 1), (1, 1)],  # O
    [(1, 1, 0), (0, 1, 1)],  # Z
    [(0, 1, 1), (1, 1, 0)],  # S
    [(1, 1, 1), (1, 0, 0)],  # L
    [(1, 1, 1), (0, 0, 1)]   # J
]
COLORS = ["cyan", "purple", "yellow", "red", "green", "orange", "blue"]

class Tetris:
    def __init__(self, root):
        self.root = root
        self.canvas = tk.Canvas(root, width=FIELD_WIDTH * BLOCK_SIZE, height=FIELD_HEIGHT * BLOCK_SIZE, bg="black")
        self.canvas.pack()
        self.field = [[0 for _ in range(FIELD_WIDTH)] for _ in range(FIELD_HEIGHT)]
        self.current_shape = None
        self.current_color = None
        self.current_pos = [0, 0]
        self.game_over = False
        self.speed = UPDATE_INTERVAL
        self.init_game()
        self.root.bind("<KeyPress>", self.key_press)
        self.update_game()

    def init_game(self):
        self.spawn_shape()

    def spawn_shape(self):
        self.current_shape = random.choice(SHAPES)
        self.current_color = COLORS[SHAPES.index(self.current_shape)]
        self.current_pos = [0, FIELD_WIDTH // 2 - len(self.current_shape[0]) // 2]
        # テトリミノを表示してから衝突チェック
        if self.collision(self.current_shape, self.current_pos):
            self.game_over = True
        self.draw_shape()

    def draw_block(self, x, y, color):
        self.canvas.create_rectangle(x * BLOCK_SIZE, y * BLOCK_SIZE, (x + 1) * BLOCK_SIZE, (y + 1) * BLOCK_SIZE, fill=color, outline="black")

    def draw_shape(self):
        for y, row in enumerate(self.current_shape):
            for x, cell in enumerate(row):
                if cell:
                    self.draw_block(self.current_pos[1] + x, self.current_pos[0] + y, self.current_color)

    def erase_shape(self):
        for y, row in enumerate(self.current_shape):
            for x, cell in enumerate(row):
                if cell:
                    self.draw_block(self.current_pos[1] + x, self.current_pos[0] + y, "black")

    def collision(self, shape, pos):
        for y, row in enumerate(shape):
            for x, cell in enumerate(row):
                if cell:
                    new_x = pos[1] + x
                    new_y = pos[0] + y
                    if new_x < 0 or new_x >= FIELD_WIDTH or new_y >= FIELD_HEIGHT:
                        return True
                    if new_y >= 0 and self.field[new_y][new_x]:
                        return True
        return False

    def lock_shape(self):
        for y, row in enumerate(self.current_shape):
            for x, cell in enumerate(row):
                if cell:
                    self.field[self.current_pos[0] + y][self.current_pos[1] + x] = self.current_color

    def clear_lines(self):
        new_field = [row for row in self.field if not all(row)]
        lines_cleared = FIELD_HEIGHT - len(new_field)
        for _ in range(lines_cleared):
            new_field.insert(0, [0 for _ in range(FIELD_WIDTH)])
        self.field = new_field

    def move(self, dx, dy):
        new_pos = [self.current_pos[0] + dy, self.current_pos[1] + dx]
        if not self.collision(self.current_shape, new_pos):
            self.erase_shape()
            self.current_pos = new_pos
            self.draw_shape()
            return True
        return False

    def rotate(self):
        new_shape = [list(row) for row in zip(*self.current_shape[::-1])]
        if not self.collision(new_shape, self.current_pos):
            self.erase_shape()
            self.current_shape = new_shape
            self.draw_shape()

    def hard_drop(self):
        while self.move(0, 1):
            pass
        self.update_game()

    def key_press(self, event):
        if event.keysym == "Left":
            self.move(-1, 0)
        elif event.keysym == "Right":
            self.move(1, 0)
        elif event.keysym == "Down":
            self.move(0, 1)
        elif event.keysym == "Up":
            self.rotate()
        elif event.keysym == "space":
            self.hard_drop()

    def update_game(self):
        if not self.game_over:
            if not self.move(0, 1):
                self.lock_shape()
                self.clear_lines()
                self.spawn_shape()
            self.canvas.delete("all")
            for y, row in enumerate(self.field):
                for x, cell in enumerate(row):
                    if cell:
                        self.draw_block(x, y, cell)
            self.draw_shape()
            self.root.after(self.speed, self.update_game)
        else:
            self.canvas.create_text(FIELD_WIDTH * BLOCK_SIZE // 2, FIELD_HEIGHT * BLOCK_SIZE // 2, text="Game Over", fill="white", font=("Helvetica", 24))

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Tetris")
    game = Tetris(root)
    root.mainloop()
