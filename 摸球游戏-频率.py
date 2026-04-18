import tkinter as tk
from tkinter import ttk
import random


class BallFrequencySimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("摸球频率模拟器")
        self.root.geometry("760x520")

        # 袋子中的球：红1，橙14，黄6，绿20，蓝9
        self.ball_counts = {
            "红色": 1,
            "橙色": 14,
            "黄色": 6,
            "绿色": 20,
            "蓝色": 9,
        }

        self.total_balls = sum(self.ball_counts.values())
        self.pool = []
        for color, count in self.ball_counts.items():
            self.pool.extend([color] * count)

        self.result_counts = {color: 0 for color in self.ball_counts}
        self.total_draws = 0
        self.running = False
        self.job = None

        self.build_ui()
        self.update_display()

    def build_ui(self):
        title = tk.Label(
            self.root,
            text="独立重复随机事件：摸球频率模拟器",
            font=("Microsoft YaHei", 18, "bold"),
        )
        title.pack(pady=12)

        intro = (
            "袋中小球：红1，橙14，黄6，绿20，蓝9（摸后放回）\n"
            "默认每秒摸 10 次。随着次数增加，各颜色频率会逐渐稳定在对应概率附近。"
        )
        tk.Label(self.root, text=intro, font=("Microsoft YaHei", 11), justify="center").pack(pady=6)

        control_frame = tk.Frame(self.root)
        control_frame.pack(pady=10)

        tk.Label(control_frame, text="每秒摸球次数：", font=("Microsoft YaHei", 11)).grid(row=0, column=0, padx=6)

        self.speed_var = tk.StringVar(value="10")
        speed_box = ttk.Combobox(
            control_frame,
            textvariable=self.speed_var,
            values=["1", "5", "10", "20", "50", "100"],
            width=8,
            state="readonly",
        )
        speed_box.grid(row=0, column=1, padx=6)

        self.start_button = tk.Button(
            control_frame,
            text="开始",
            width=10,
            command=self.start,
            font=("Microsoft YaHei", 11),
        )
        self.start_button.grid(row=0, column=2, padx=10)

        self.stop_button = tk.Button(
            control_frame,
            text="暂停",
            width=10,
            command=self.stop,
            state="disabled",
            font=("Microsoft YaHei", 11),
        )
        self.stop_button.grid(row=0, column=3, padx=10)

        self.reset_button = tk.Button(
            control_frame,
            text="清零",
            width=10,
            command=self.reset,
            font=("Microsoft YaHei", 11),
        )
        self.reset_button.grid(row=0, column=4, padx=10)

        summary_frame = tk.Frame(self.root)
        summary_frame.pack(pady=10)

        self.total_draws_label = tk.Label(summary_frame, text="总摸球次数：0", font=("Microsoft YaHei", 13, "bold"))
        self.total_draws_label.pack()

        columns = ("color", "count", "freq", "prob")
        self.tree = ttk.Treeview(self.root, columns=columns, show="headings", height=8)
        self.tree.heading("color", text="颜色")
        self.tree.heading("count", text="出现次数")
        self.tree.heading("freq", text="实验频率")
        self.tree.heading("prob", text="理论概率")

        self.tree.column("color", width=140, anchor="center")
        self.tree.column("count", width=160, anchor="center")
        self.tree.column("freq", width=160, anchor="center")
        self.tree.column("prob", width=160, anchor="center")
        self.tree.pack(pady=10)

        explain = (
            "说明：\n"
            "1. 每次都是‘摸出后放回’，所以每次摸球互相独立。\n"
            "2. 次数少时，频率波动较大；次数多时，频率会逐渐稳定。\n"
            "3. 例如红球理论概率 = 1 ÷ 50 = 0.02。"
        )
        tk.Label(
            self.root,
            text=explain,
            justify="left",
            font=("Microsoft YaHei", 10),
        ).pack(pady=8)

    def draw_one_ball(self):
        color = random.choice(self.pool)
        self.result_counts[color] += 1
        self.total_draws += 1

    def run_simulation(self):
        if not self.running:
            return

        speed = int(self.speed_var.get())
        for _ in range(speed):
            self.draw_one_ball()

        self.update_display()
        self.job = self.root.after(1000, self.run_simulation)

    def update_display(self):
        self.total_draws_label.config(text=f"总摸球次数：{self.total_draws}")

        for item in self.tree.get_children():
            self.tree.delete(item)

        for color, ball_count in self.ball_counts.items():
            count = self.result_counts[color]
            freq = count / self.total_draws if self.total_draws > 0 else 0
            prob = ball_count / self.total_balls
            self.tree.insert(
                "",
                "end",
                values=(
                    color,
                    count,
                    f"{freq:.4f}",
                    f"{prob:.4f}",
                ),
            )

    def start(self):
        if not self.running:
            self.running = True
            self.start_button.config(state="disabled")
            self.stop_button.config(state="normal")
            self.run_simulation()

    def stop(self):
        self.running = False
        self.start_button.config(state="normal")
        self.stop_button.config(state="disabled")
        if self.job is not None:
            self.root.after_cancel(self.job)
            self.job = None

    def reset(self):
        self.stop()
        self.result_counts = {color: 0 for color in self.ball_counts}
        self.total_draws = 0
        self.update_display()


if __name__ == "__main__":
    root = tk.Tk()
    app = BallFrequencySimulator(root)
    root.mainloop()
