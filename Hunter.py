
from tkinter import Canvas, Tk, ALL, messagebox
from random import choice, randrange
import random
import winsound
import requests #Added requests==2.28.1 (pip install requests==2.28.1)
import os #added but you don't need to install anything

#checks if the song is downloaded, if it isn't, it downloads it
if os.path.exists("tetris.wav") == False:
    messagebox.showinfo("Tkinter Tetris","Initializing. If this takes more than a minute or two, please check your internet connection and try again!")
    response = requests.get("https://raw.githubusercontent.com/YungSamzy/Hunter-Tetris/main/tetris.wav")
    open("tetris.wav", "wb").write(response.content)

winsound.PlaySound('tetris.wav', winsound.SND_LOOP + winsound.SND_ASYNC) #SND_LOOP makes the song loop until the program closes
# prints a random value from the list
list1 = [1, 5, 10, 25, 100, 500, 1000, 2000, 5000, 10000]

#I changed this from 500
POLL_MS = (random.choice(list1))
CVS_WIDTH = 380
W_BOX_NUM = 19
H_BOX_NUM = 22
BOX_L = int(CVS_WIDTH / W_BOX_NUM)
CVS_HEIGHT = BOX_L * H_BOX_NUM
#You can probably see what I did here
SCORES = {1: 10, 2: 20, 3: 50, 4: 100}
FONT = f'Fixedsys {int(BOX_L/2)} bold'
DASH = (int(BOX_L / 2), int(BOX_L / 4))
FIGURE_SHAPES = (
    ('square', 'yellow', (5, 1), (6, 1), (5, 2), (6, 2)),
    ('line', 'cyan', (5, 1), (6, 1), (7, 1), (8, 1)),
    ('right_l', 'dark blue', (7, 1), (5, 2), (6, 2), (7, 2)),
    ('left_l', 'orange', (5, 1), (5, 2), (6, 2), (7, 2)),
    ('right_z', 'lime', (5, 2), (6, 2), (6, 1), (7, 1)),
    ('left_z', 'red', (5, 1), (6, 1), (6, 2), (7, 2)),
    ('_|_', 'purple', (6, 1), (5, 2), (6, 2), (7, 2))
)


class Utils:
    @staticmethod
    def convert_coords(x, y, x_size=0, y_size=0):
        return BOX_L * x, BOX_L * y, BOX_L * (x + x_size), BOX_L * (y + y_size)
    @staticmethod
    def find_overlaps(x, y, x_size, y_size, canvas, excluded_items):
        x1, y1, x2, y2 = Utils.convert_coords(x, y, x_size, y_size)
        all_overlaps = canvas.find_enclosed(x1 - 1, y1 - 1, x2 + 1, y2 + 1)
        return list(set(all_overlaps) - set(excluded_items))
    @staticmethod
    def tgm3_randomizer():
        pool = list(range(7)) * 5
        order = []
        target_idx = None
        rand_idx = None
        first_index = choice([1, 2, 3, 6])
        yield first_index
        history = [4, 5, 4, first_index]
        while True:
            for roll in range(6):
                rand_idx = randrange(len(pool))
                target_idx = pool[rand_idx]
                if target_idx not in history or roll == 5:
                    break
                if order:
                    pool[rand_idx] = order[0]
            if target_idx in order:
                order.remove(target_idx)
            order.append(target_idx)
            pool[rand_idx] = order[0]
            history.pop(0)
            history.append(target_idx)
            yield target_idx


class TetrisGame:
    canvas = None
    tk = None
    curr_figure = None
    next_figure = None
    background_items = []
    limit_coords = None
    score = 0
    rand = None
    def start(self):
        self.tk = Tk()
        self.tk.title('Tkinter-Tetris')
        self.canvas = Canvas(self.tk, bg='black', width=CVS_WIDTH, height=CVS_HEIGHT)
        self.Draw_Background()
        self.rand = Utils.tgm3_randomizer()
        self.curr_figure = Figure(self.canvas, FIGURE_SHAPES[next(self.rand)],             
self.background_items, self.limit_coords)
        self.next_figure = Figure(self.canvas, FIGURE_SHAPES[next(self.rand)], 
self.background_items, self.limit_coords)
        self.curr_figure.Create()
        self.next_figure.Create(next_area=True)
        self.canvas.pack()
        self.tk.bind("<Key>", self.Handle_Events)
        self.run()
        self.tk.mainloop()

    def Draw_Background(self):
        play_area_id = self.canvas.create_rectangle(Utils.convert_coords(1, 1, 10, 20),         
fill='green', tag='TRS')
        next_area_id = self.canvas.create_rectangle(Utils.convert_coords(12, 1, 6, 5),         
fill='green')
        self.limit_coords = self.canvas.coords(play_area_id)
        self.canvas.create_rectangle(Utils.convert_coords(12, 7, 6, 4), fill='green')
        self.canvas.create_text(Utils.convert_coords(15, 2)[0:2], fill='snow3', text='NEXT',     
font=FONT)
        self.canvas.create_text(Utils.convert_coords(15, 8)[0:2], fill='snow3', text='SCORE',     
font=FONT)
        self.canvas.create_text(Utils.convert_coords(15, 9)[0:2], fill='snow3', text='0000000', 
font=FONT, tag='SCR')
        self.background_items.append(play_area_id)
        self.background_items.append(next_area_id)
        for i in range(2, 21):
            line_id = self.canvas.create_line(Utils.convert_coords(1, i, 10, 0), dash=DASH, 
fill='orange')
            self.background_items.append(line_id)
        for i in range(2, 11):
            line_id = self.canvas.create_line(Utils.convert_coords(i, 1, 0, 20), dash=DASH,         
fill='yellow')
            self.background_items.append(line_id)

    def Handle_Events(self, event):
        if event.keysym == "Escape":
            self.tk.quit()
        elif event.keysym == "Left":
            self.curr_figure.move((-1, 0))
        elif event.keysym == "Right":
            self.curr_figure.move((1, 0))
        elif event.keysym == "Down":
            self.curr_figure.move((0, 1))
        elif event.keysym == "Up":
            self.curr_figure.rotate()

    def run(self):
        self.Delete_Lines()
        if self.curr_figure.stopped:
            [self.canvas.delete(blk) for blk in self.next_figure.blocks]
            self.curr_figure = self.next_figure
            self.next_figure = Figure(self.canvas, FIGURE_SHAPES[next(self.rand)], 
self.background_items, self.limit_coords)
            if not self.curr_figure.Create():
                self.Game_Over()
            self.next_figure.Create(next_area=True)
        if all([self.curr_figure._move_allowed(0, 1, self.canvas.coords(block)) for block in 
self.curr_figure.blocks]):
            self.curr_figure.move((0, 1))
        else:
            self.curr_figure.stopped = True
        self.tk.after((random.choice(list1)), self.run)

    def Delete_Lines(self):
        full_lines = []
        for i in range(1, 21):
            overlap_items = Utils.find_overlaps(1, i, 10, 1, self.canvas, self.background_items)
            if len(overlap_items) == 10:
                full_lines.append(i)
                [self.canvas.delete(curr_blk) for curr_blk in overlap_items]
                blocks_to_move = Utils.find_overlaps(1, 1, 10, i, self.canvas, self.background_items)
                [self.canvas.move(block, 0, BOX_L) for block in blocks_to_move]
        if full_lines:
            self.Update_Score(SCORES[len(full_lines)])

    def Update_Score(self, score):
        self.score += score
        self.canvas.itemconfigure(self.canvas.find_withtag('SCR')[0], text=f'{self.score:07}')

    def Game_Over(self):
        self.canvas.delete(ALL)
        self.tk.quit()
        messagebox.showinfo("End of Game", f'Game Over\nYour score: {self.score:07}')


class Figure:
    def __init__(self, canvas, shape_data: tuple, background_items, limit_coords):
        self.canvas = canvas
        self.tag = shape_data[0]
        self.color = shape_data[1]
        self.blk_coords = shape_data[2:]
        self.limit_coords = limit_coords
        self.rotation_parity = 1
        self.background_items = background_items
        self.stopped = False
        self.blocks = []

    def Create(self, next_area=False):
        self.blocks = []
        for (p_x, p_y) in self.blk_coords:
            if next_area:
                p_x, p_y = p_x + 8, p_y + 2
            overlap_items = Utils.find_overlaps(p_x, p_y, 1, 1, self.canvas, self.background_items)
            if overlap_items:
                return False
            block = self.canvas.create_rectangle(Utils.convert_coords(p_x, p_y, 1, 1), fill=self.color)
            self.blocks.append(block)
        return True

    def _move_allowed(self, x_delta, y_delta, item_coords):
        if item_coords and len(item_coords) == 4:
            new_x1, new_y1 = item_coords[0] + x_delta * BOX_L, item_coords[1] + y_delta * BOX_L
            new_x2, new_y2 = item_coords[2] + x_delta * BOX_L, item_coords[3] + y_delta * BOX_L
            if new_x1 >= self.limit_coords[0] and new_y1 >= self.limit_coords[1]:
                if new_x2 <= self.limit_coords[2] and new_y2 <= self.limit_coords[3]:
                    overlap_items = Utils.find_overlaps(new_x1 // BOX_L, new_y1 // BOX_L, 1, 1,     self.canvas, self.background_items + self.blocks)
                    if not overlap_items:
                        return True
        return False

    def rotate(self):
        if self.tag != 'square':
            coords = [(self.canvas.coords(block)) for block in self.blocks]
            if coords and len([xy for block_coords in coords for xy in block_coords]) == 16:
                grouped_coords = list(zip(*coords))
                min_x, min_y = min(grouped_coords[0]), min(grouped_coords[1])
                max_x, max_y = max(grouped_coords[2]), max(grouped_coords[3])
                cx, cy = (max_x - min_x) / 2 + min_x, (max_y - min_y) / 2 + min_y
                coords_after_rotation = []
                for (up_l_x, up_l_y, _, _) in coords:
                    rx, ry = cx - up_l_x, cy - up_l_y
                    new_x, new_y = ry + cx, -rx + cy
                    new_x_aligned, new_y_aligned = (new_x - up_l_x) // BOX_L, (new_y - up_l_y) // BOX_L
                    if self.rotation_parity % 2 == 0:
                        new_x_aligned -= 1
                        new_y_aligned += 1
                    coords_after_rotation.append((new_x_aligned, new_y_aligned))
                self.move(coords_after_rotation)
                self.rotation_parity += 1

    def move(self, coords):
        coords_list = coords if len(coords) == 4 else [coords] * 4
        if all([self._move_allowed(x, y, self.canvas.coords(self.blocks[i])) for i, (x, y) in enumerate(coords_list)]):
            for i, curr_item in enumerate(self.blocks):
                x_delta, y_delta = coords_list[i]
                self.canvas.move(curr_item, x_delta * BOX_L, y_delta * BOX_L)


if __name__ == "__main__":
    tetris_game = TetrisGame()
    tetris_game.start()