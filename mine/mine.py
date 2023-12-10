import tkinter as tk
from tkinter import messagebox, simpledialog
import random

class Minesweeper:
    def __init__(self, master, rows=10, cols=10, mines=10):
        self.master = master
        self.rows = rows
        self.cols = cols
        self.mines = mines
        self.buttons = []
        self.is_game_over = False
        self.is_first_click = True
        self.mine_positions = set()
        self.mines_remaining = self.mines  # 先初始化 mines_remaining
        self.create_widgets()  # 然后调用 create_widgets
        self.create_menu()  # 新增创建菜单的调用

    def create_widgets(self):
        # Reset button and mines counter
        reset_button = tk.Button(self.master, text='重置', command=self.reset_game)
        reset_button.grid(row=0, column=0, columnspan=self.cols, sticky="we")

        self.mines_label = tk.Label(self.master, text=f"剩余雷数: {self.mines_remaining}")
        self.mines_label.grid(row=1, column=0, columnspan=self.cols, sticky="we")

        for x in range(self.rows):
            row = []
            for y in range(self.cols):
                button = tk.Button(self.master, text='', width=3, height=1,
                                   command=lambda x=x, y=y: self.on_click(x, y))
                button.bind('<Button-3>', lambda e, x=x, y=y: self.on_right_click(x, y))
                button.grid(row=x + 2, column=y)
                row.append(button)
            self.buttons.append(row)

    def create_menu(self):
        menu_bar = tk.Menu(self.master)
        self.master.config(menu=menu_bar)

        game_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="游戏", menu=game_menu)
        game_menu.add_command(label="新游戏", command=self.reset_game)
        game_menu.add_command(label="设置", command=self.update_settings)
        game_menu.add_separator()
        game_menu.add_command(label="退出", command=self.master.quit)

    def update_settings(self):
        try:
            rows = simpledialog.askinteger("设置", "行数", initialvalue=self.rows, minvalue=5, maxvalue=20)
            cols = simpledialog.askinteger("设置", "列数", initialvalue=self.cols, minvalue=5, maxvalue=20)
            mines = simpledialog.askinteger("设置", "雷数", initialvalue=self.mines, minvalue=1, maxvalue=min(rows, cols) * 5)
            if not all([rows, cols, mines]):
                raise ValueError("Invalid input")
        except ValueError:
            messagebox.showerror("错误", "无效的输入，设置未更改。")
            return

        self.rows = rows
        self.cols = cols
        self.mines = mines
        self.reset_game()

    def reset_game(self):
        # Clear existing buttons and reset game state
        for row in self.buttons:
            for button in row:
                button.destroy()
        self.buttons = []
        self.is_game_over = False
        self.is_first_click = True
        self.mine_positions = set()
        self.mines_remaining = self.mines
        self.create_widgets()

    def place_mines(self, first_click_position):
        # Ensure the first click is safe
        safe_zone = [(first_click_position[0] + i, first_click_position[1] + j)
                     for i in range(-1, 2) for j in range(-1, 2)
                     if 0 <= first_click_position[0] + i < self.rows and
                        0 <= first_click_position[1] + j < self.cols]

        mines_placed = 0
        while mines_placed < self.mines:
            x, y = random.randint(0, self.rows - 1), random.randint(0, self.cols - 1)
            if (x, y) not in self.mine_positions and (x, y) not in safe_zone:
                self.mine_positions.add((x, y))
                mines_placed += 1

    def reveal(self, x, y):
        # 使用栈来逐个处理需要揭示的格子
        to_reveal = [(x, y)]
        while to_reveal:
            cx, cy = to_reveal.pop()
            if not (0 <= cx < self.rows and 0 <= cy < self.cols) or self.buttons[cx][cy]['state'] == tk.DISABLED:
                continue

            if (cx, cy) in self.mine_positions:
                continue

            mines_count = self.count_mines(cx, cy)
            if mines_count > 0:
                self.buttons[cx][cy].config(text=str(mines_count), state=tk.DISABLED)
                # 根据周围雷数改变按钮颜色
                self.buttons[cx][cy].config(bg='yellow')
            else:
                # 已点击且周围没有雷的区域，使用不同的背景色和边框样式
                self.buttons[cx][cy].config(state=tk.DISABLED, bg='lightgrey', relief=tk.SUNKEN)
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        if dx != 0 or dy != 0:
                            nx, ny = cx + dx, cy + dy
                            if 0 <= nx < self.rows and 0 <= ny < self.cols and self.buttons[nx][ny]['state'] == tk.NORMAL:
                                to_reveal.append((nx, ny))


    def on_click(self, x, y):
        if self.is_game_over:
            return

        if self.is_first_click:
            self.is_first_click = False
            self.place_mines((x, y))
            self.mines_label.config(text=f"剩余雷数: {self.mines_remaining}")

        button = self.buttons[x][y]
        if (x, y) in self.mine_positions:
            self.game_over(False, (x, y))
        else:
            self.reveal(x, y)
            if self.check_win():
                self.game_over(True, None)

    def on_right_click(self, x, y):
        if self.is_game_over or self.buttons[x][y]['state'] == tk.DISABLED:
            return

        button = self.buttons[x][y]
        current_text = button['text']
        if current_text == 'F':
            button.config(text='', bg='SystemButtonFace')
            self.mines_remaining += 1
        else:
            button.config(text='F', bg='red')
            self.mines_remaining -= 1
        self.mines_label.config(text=f"剩余雷数: {self.mines_remaining}")

    def count_mines(self, x, y):
        count = 0
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if (x + dx, y + dy) in self.mine_positions:
                    count += 1
        return count

    def check_win(self):
        for x in range(self.rows):
            for y in range(self.cols):
                if (x, y) not in self.mine_positions and self.buttons[x][y]['state'] == tk.NORMAL:
                    return False
        return True

    def game_over(self, win, mine_triggered):
        self.is_game_over = True
        for x in range(self.rows):
            for y in range(self.cols):
                button = self.buttons[x][y]
                if (x, y) in self.mine_positions:
                    button.config(text='💣')
                if mine_triggered and (x, y) == mine_triggered:
                    button.config(bg='orange')  # Highlight the triggered mine
                button.config(state=tk.DISABLED)

        if win:
            messagebox.showinfo("游戏结束", "你赢了！")
        else:
            messagebox.showerror("游戏结束", "你触雷了！")

def main():
    root = tk.Tk()
    root.title("扫雷")

    # 使用默认设置启动游戏
    default_rows = 10
    default_cols = 10
    default_mines = 15  # 设置一个合理的默认雷数

    Minesweeper(root, rows=default_rows, cols=default_cols, mines=default_mines)
    root.mainloop()

if __name__ == "__main__":
    main()
