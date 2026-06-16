import tkinter as tk
from tkinter import ttk, messagebox


class CalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("金属建材计算器")
        self.root.geometry("480x560")
        self.root.resizable(False, False)

        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)

        self.create_circular_pipe_tab()
        self.create_square_pipe_tab()
        self.create_wire_tab()
        self.create_flange_tab()

    # ---------- 圆管 ----------
    def create_circular_pipe_tab(self):
        frame = ttk.Frame(self.notebook, padding=20)
        self.notebook.add(frame, text="圆管")

        title = ttk.Label(frame, text="圆管重量计算", font=("微软雅黑", 14, "bold"))
        title.pack(pady=(0, 5))

        desc = ttk.Label(
            frame,
            text="(直径 - 厚度) × 厚度 × 厚度 × 0.02466",
            font=("微软雅黑", 9),
            foreground="gray",
        )
        desc.pack(pady=(0, 15))

        frm_d = ttk.Frame(frame)
        frm_d.pack(fill="x", pady=5)
        ttk.Label(frm_d, text="直径（毫米）:", font=("微软雅黑", 10)).pack(side="left")
        self.pipe_d = ttk.Entry(frm_d, width=15, font=("微软雅黑", 10))
        self.pipe_d.pack(side="right")

        frm_t = ttk.Frame(frame)
        frm_t.pack(fill="x", pady=5)
        ttk.Label(frm_t, text="厚度（毫米）:", font=("微软雅黑", 10)).pack(side="left")
        self.pipe_t = ttk.Entry(frm_t, width=15, font=("微软雅黑", 10))
        self.pipe_t.pack(side="right")

        frm_m = ttk.Frame(frame)
        frm_m.pack(fill="x", pady=5)
        ttk.Label(frm_m, text="总米数（米）:", font=("微软雅黑", 10)).pack(side="left")
        self.pipe_m = ttk.Entry(frm_m, width=15, font=("微软雅黑", 10))
        self.pipe_m.pack(side="right")
        ttk.Label(frm_m, text="（选填）", font=("微软雅黑", 9), foreground="gray").pack(side="right", padx=5)

        ttk.Frame(frame, height=5).pack()

        btn = ttk.Button(frame, text="计  算", command=self.calc_pipe)
        btn.pack(pady=5)

        frm_res = ttk.Frame(frame, borderwidth=2, relief="groove")
        frm_res.pack(fill="x", pady=15)
        ttk.Label(
            frm_res, text="总重量:", font=("微软雅黑", 10)
        ).pack(side="left", padx=10, pady=12)
        self.pipe_result = ttk.Label(
            frm_res, text="-- kg", font=("微软雅黑", 12, "bold"), foreground="green"
        )
        self.pipe_result.pack(side="right", padx=10, pady=12)

    def calc_pipe(self):
        try:
            d = float(self.pipe_d.get())
            t = float(self.pipe_t.get())
            r = d - t
            r = r * t
            r = r * t
            r = r * 0.02466
            m = self.pipe_m.get().strip()
            if m:
                r = r * float(m)
            self.pipe_result.config(text=f"{r:.4f} kg")
        except ValueError:
            messagebox.showerror("输入错误", "请输入有效的数字")

    # ---------- 方管 ----------
    def create_square_pipe_tab(self):
        frame = ttk.Frame(self.notebook, padding=20)
        self.notebook.add(frame, text="方管")

        title = ttk.Label(frame, text="方管重量计算", font=("微软雅黑", 14, "bold"))
        title.pack(pady=(0, 5))

        desc = ttk.Label(
            frame,
            text="（（周长 ÷ 3.14）- 厚度）× 厚度 × 0.02466",
            font=("微软雅黑", 9),
            foreground="gray",
        )
        desc.pack(pady=(0, 15))

        frm_p = ttk.Frame(frame)
        frm_p.pack(fill="x", pady=5)
        ttk.Label(frm_p, text="周长（毫米）:", font=("微软雅黑", 10)).pack(side="left")
        self.square_p = ttk.Entry(frm_p, width=15, font=("微软雅黑", 10))
        self.square_p.pack(side="right")

        frm_t = ttk.Frame(frame)
        frm_t.pack(fill="x", pady=5)
        ttk.Label(frm_t, text="厚度（毫米）:", font=("微软雅黑", 10)).pack(side="left")
        self.square_t = ttk.Entry(frm_t, width=15, font=("微软雅黑", 10))
        self.square_t.pack(side="right")

        frm_m = ttk.Frame(frame)
        frm_m.pack(fill="x", pady=5)
        ttk.Label(frm_m, text="总米数（米）:", font=("微软雅黑", 10)).pack(side="left")
        self.square_m = ttk.Entry(frm_m, width=15, font=("微软雅黑", 10))
        self.square_m.pack(side="right")
        ttk.Label(frm_m, text="（选填）", font=("微软雅黑", 9), foreground="gray").pack(side="right", padx=5)

        ttk.Frame(frame, height=5).pack()

        btn = ttk.Button(frame, text="计  算", command=self.calc_square)
        btn.pack(pady=5)

        frm_res = ttk.Frame(frame, borderwidth=2, relief="groove")
        frm_res.pack(fill="x", pady=15)
        ttk.Label(
            frm_res, text="总重量:", font=("微软雅黑", 10)
        ).pack(side="left", padx=10, pady=12)
        self.square_result = ttk.Label(
            frm_res, text="-- kg", font=("微软雅黑", 12, "bold"), foreground="green"
        )
        self.square_result.pack(side="right", padx=10, pady=12)

    def calc_square(self):
        try:
            p = float(self.square_p.get())
            t = float(self.square_t.get())
            r = p / 3.14
            r = r - t
            r = r * t
            r = r * 0.02466
            m = self.square_m.get().strip()
            if m:
                r = r * float(m)
            self.square_result.config(text=f"{r:.4f} kg")
        except ValueError:
            messagebox.showerror("输入错误", "请输入有效的数字")

    # ---------- 丝径 ----------
    def create_wire_tab(self):
        frame = ttk.Frame(self.notebook, padding=20)
        self.notebook.add(frame, text="丝径")

        title = ttk.Label(frame, text="丝径重量计算", font=("微软雅黑", 14, "bold"))
        title.pack(pady=(0, 5))

        desc = ttk.Label(
            frame,
            text="长度 × 丝径 × 丝径 × 0.00617",
            font=("微软雅黑", 9),
            foreground="gray",
        )
        desc.pack(pady=(0, 15))

        frm_l = ttk.Frame(frame)
        frm_l.pack(fill="x", pady=5)
        ttk.Label(frm_l, text="长度（米）:", font=("微软雅黑", 10)).pack(side="left")
        self.wire_l = ttk.Entry(frm_l, width=15, font=("微软雅黑", 10))
        self.wire_l.pack(side="right")

        frm_d = ttk.Frame(frame)
        frm_d.pack(fill="x", pady=5)
        ttk.Label(frm_d, text="丝径（毫米）:", font=("微软雅黑", 10)).pack(side="left")
        self.wire_d = ttk.Entry(frm_d, width=15, font=("微软雅黑", 10))
        self.wire_d.pack(side="right")

        frm_m = ttk.Frame(frame)
        frm_m.pack(fill="x", pady=5)
        ttk.Label(frm_m, text="总米数（米）:", font=("微软雅黑", 10)).pack(side="left")
        self.wire_m = ttk.Entry(frm_m, width=15, font=("微软雅黑", 10))
        self.wire_m.pack(side="right")
        ttk.Label(frm_m, text="（选填）", font=("微软雅黑", 9), foreground="gray").pack(side="right", padx=5)

        ttk.Frame(frame, height=5).pack()

        btn = ttk.Button(frame, text="计  算", command=self.calc_wire)
        btn.pack(pady=5)

        frm_res = ttk.Frame(frame, borderwidth=2, relief="groove")
        frm_res.pack(fill="x", pady=15)
        ttk.Label(
            frm_res, text="总重量:", font=("微软雅黑", 10)
        ).pack(side="left", padx=10, pady=12)
        self.wire_result = ttk.Label(
            frm_res, text="-- kg", font=("微软雅黑", 12, "bold"), foreground="green"
        )
        self.wire_result.pack(side="right", padx=10, pady=12)

    def calc_wire(self):
        try:
            l = float(self.wire_l.get())
            d = float(self.wire_d.get())
            r = l * d
            r = r * d
            r = r * 0.00617
            m = self.wire_m.get().strip()
            if m:
                r = r * float(m)
            self.wire_result.config(text=f"{r:.4f} kg")
        except ValueError:
            messagebox.showerror("输入错误", "请输入有效的数字")

    # ---------- 法兰盘 ----------
    def create_flange_tab(self):
        frame = ttk.Frame(self.notebook, padding=20)
        self.notebook.add(frame, text="法兰盘")

        title = ttk.Label(frame, text="法兰盘重量计算", font=("微软雅黑", 14, "bold"))
        title.pack(pady=(0, 5))

        desc = ttk.Label(
            frame,
            text="7.85 × 边长1 × 边长2 × 厚度",
            font=("微软雅黑", 9),
            foreground="gray",
        )
        desc.pack(pady=(0, 15))

        frm_a = ttk.Frame(frame)
        frm_a.pack(fill="x", pady=5)
        ttk.Label(frm_a, text="边长1（米）:", font=("微软雅黑", 10)).pack(side="left")
        self.flange_a = ttk.Entry(frm_a, width=15, font=("微软雅黑", 10))
        self.flange_a.pack(side="right")

        frm_b = ttk.Frame(frame)
        frm_b.pack(fill="x", pady=5)
        ttk.Label(frm_b, text="边长2（米）:", font=("微软雅黑", 10)).pack(side="left")
        self.flange_b = ttk.Entry(frm_b, width=15, font=("微软雅黑", 10))
        self.flange_b.pack(side="right")

        frm_t = ttk.Frame(frame)
        frm_t.pack(fill="x", pady=5)
        ttk.Label(frm_t, text="厚度（毫米）:", font=("微软雅黑", 10)).pack(side="left")
        self.flange_t = ttk.Entry(frm_t, width=15, font=("微软雅黑", 10))
        self.flange_t.pack(side="right")

        frm_m = ttk.Frame(frame)
        frm_m.pack(fill="x", pady=5)
        ttk.Label(frm_m, text="总米数（米）:", font=("微软雅黑", 10)).pack(side="left")
        self.flange_m = ttk.Entry(frm_m, width=15, font=("微软雅黑", 10))
        self.flange_m.pack(side="right")
        ttk.Label(frm_m, text="（选填）", font=("微软雅黑", 9), foreground="gray").pack(side="right", padx=5)

        ttk.Frame(frame, height=5).pack()

        btn = ttk.Button(frame, text="计  算", command=self.calc_flange)
        btn.pack(pady=5)

        frm_res = ttk.Frame(frame, borderwidth=2, relief="groove")
        frm_res.pack(fill="x", pady=15)
        ttk.Label(
            frm_res, text="总重量:", font=("微软雅黑", 10)
        ).pack(side="left", padx=10, pady=12)
        self.flange_result = ttk.Label(
            frm_res, text="-- kg", font=("微软雅黑", 12, "bold"), foreground="green"
        )
        self.flange_result.pack(side="right", padx=10, pady=12)

    def calc_flange(self):
        try:
            a = float(self.flange_a.get())
            b = float(self.flange_b.get())
            t = float(self.flange_t.get())
            r = 7.85 * a
            r = r * b
            r = r * t
            m = self.flange_m.get().strip()
            if m:
                r = r * float(m)
            self.flange_result.config(text=f"{r:.4f} kg")
        except ValueError:
            messagebox.showerror("输入错误", "请输入有效的数字")


if __name__ == "__main__":
    root = tk.Tk()
    app = CalculatorApp(root)
    root.mainloop()