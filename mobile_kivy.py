import os
import sys

# 设置 Android 状态栏兼容
from kivy import Config
Config.set('graphics', 'fullscreen', '0')
Config.set('graphics', 'show_cursor', '1')

from kivy.app import App
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.core.text import LabelBase
from kivy.core.window import Window
from kivy.utils import platform

# 注册中文字体（修复乱码）
font_path = os.path.join(os.path.dirname(__file__), 'msyh.ttc')
if os.path.exists(font_path):
    LabelBase.register(name='ChineseFont', fnt_regular=font_path, fnt_bold=font_path)

# Android 全屏兼容（修复 UI 靠下）
if platform == 'android':
    from jnius import autoclass, cast
    from android.runnable import run_on_ui_thread
    try:
        activity = autoclass('org.kivy.android.PythonActivity').mActivity
        WindowManager = autoclass('android.view.WindowManager$LayoutParams')
        activity.getWindow().addFlags(WindowManager.FLAG_LAYOUT_NO_LIMITS)
        # 沉浸式状态栏
        View = autoclass('android.view.View')
        activity.getWindow().getDecorView().setSystemUiVisibility(
            View.SYSTEM_UI_FLAG_LAYOUT_STABLE
            | View.SYSTEM_UI_FLAG_LAYOUT_FULLSCREEN
            | View.SYSTEM_UI_FLAG_LAYOUT_HIDE_NAVIGATION
        )
    except Exception:
        pass

Window.softinput_mode = 'below_target'


def calc_sequential(*args):
    """Calculate by sequential order, no operator precedence"""
    result = args[0]
    for val in args[1:]:
        result = result * val
    return result


def get_font_name(size=None, bold=False):
    """返回中文字体名"""
    return 'ChineseFont'


class CalculatorTab(BoxLayout):
    def __init__(self, title, formula_text, inputs, calc_func, result_label, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 20
        self.spacing = 10

        font_name = get_font_name()

        # Title
        title_label = Label(
            text=title,
            font_size='18sp',
            bold=True,
            size_hint_y=0.1,
            font_name=font_name
        )
        self.add_widget(title_label)

        # Formula description
        self.add_widget(Label(
            text=formula_text,
            font_size='11sp',
            color=(0.5, 0.5, 0.5, 1),
            size_hint_y=0.1,
            font_name=font_name
        ))

        # Inputs
        self.input_widgets = {}
        for inp_name, unit in inputs:
            row = BoxLayout(size_hint_y=0.12)
            label_widget = Label(
                text=f'{inp_name} ({unit}):',
                font_size='13sp',
                text_size=self.size,
                valign='middle',
                font_name=font_name
            )
            row.add_widget(label_widget)
            inp = TextInput(
                hint_text='0',
                multiline=False,
                input_filter='float',
                font_size='14sp',
                size_hint_x=0.5
            )
            row.add_widget(inp)
            self.input_widgets[inp_name] = inp
            self.add_widget(row)

        # Optional meter input
        self.meter_input = TextInput(
            hint_text='选填',
            multiline=False,
            input_filter='float',
            font_size='14sp',
            size_hint_y=0.1
        )
        meter_label = Label(text='总米数（米，选填）:', font_size='13sp', size_hint_y=0.08, font_name=font_name)
        self.add_widget(meter_label)
        self.add_widget(self.meter_input)

        # Calculate button
        self.calc_btn = Button(
            text='计算',
            font_size='16sp',
            background_color=(0.15, 0.39, 0.92, 1),
            size_hint_y=0.12,
            font_name=font_name
        )
        self.calc_btn.bind(on_press=lambda x: self.do_calc(calc_func, result_label))
        self.add_widget(self.calc_btn)

        # Result label
        result_label.font_size = '24sp'
        result_label.color = (0.15, 0.39, 0.92, 1)
        result_label.bold = True
        result_label.size_hint_y = 0.15
        result_label.font_name = font_name
        self.add_widget(result_label)

    def do_calc(self, calc_func, result_label):
        try:
            vals = {}
            for name, inp in self.input_widgets.items():
                v = inp.text.strip()
                if not v:
                    result_label.text = '请输入所有参数'
                    return
                vals[name] = float(v)

            meter = self.meter_input.text.strip()
            meter_val = float(meter) if meter else None

            result = calc_func(vals, meter_val)
            result_label.text = f'{result:.4f} kg'
        except ValueError:
            result_label.text = '请输入有效数字'
        except Exception as e:
            result_label.text = f'错误: {e}'


def pipe_calc(vals, meter):
    d = vals['直径']
    t = vals['厚度']
    r = d - t
    r = r * t
    r = r * t
    r = r * 0.02466
    if meter:
        r = r * meter
    return r


def square_calc(vals, meter):
    p = vals['周长']
    t = vals['厚度']
    r = p / 3.14
    r = r - t
    r = r * t
    r = r * 0.02466
    if meter:
        r = r * meter
    return r


def wire_calc(vals, meter):
    l = vals['长度']
    d = vals['丝径']
    r = l * d
    r = r * d
    r = r * 0.00617
    if meter:
        r = r * meter
    return r


def flange_calc(vals, meter):
    a = vals['边长1']
    b = vals['边长2']
    t = vals['厚度']
    r = 7.85 * a
    r = r * b
    r = r * t
    if meter:
        r = r * meter
    return r


class MetalCalculatorApp(App):
    def build(self):
        self.title = '金属建材计算器'
        root = TabbedPanel(tab_pos='top_mid')
        root.do_default_tab = False

        font_name = get_font_name()

        # Tab 1: 圆管
        tab1 = CalculatorTab(
            title='圆管重量计算',
            formula_text='(直径-厚度) × 厚度 × 厚度 × 0.02466',
            inputs=[('直径', '毫米'), ('厚度', '毫米')],
            calc_func=pipe_calc,
            result_label=Label(text='-- kg', font_name=font_name)
        )
        root.add_widget(tab1)

        # Tab 2: 方管
        tab2 = CalculatorTab(
            title='方管重量计算',
            formula_text='((周长÷3.14)-厚度) × 厚度 × 0.02466',
            inputs=[('周长', '毫米'), ('厚度', '毫米')],
            calc_func=square_calc,
            result_label=Label(text='-- kg', font_name=font_name)
        )
        root.add_widget(tab2)

        # Tab 3: 丝径
        tab3 = CalculatorTab(
            title='丝径重量计算',
            formula_text='长度 × 丝径 × 丝径 × 0.00617',
            inputs=[('长度', '米'), ('丝径', '毫米')],
            calc_func=wire_calc,
            result_label=Label(text='-- kg', font_name=font_name)
        )
        root.add_widget(tab3)

        # Tab 4: 法兰盘
        tab4 = CalculatorTab(
            title='法兰盘重量计算',
            formula_text='7.85 × 边长1 × 边长2 × 厚度',
            inputs=[('边长1', '米'), ('边长2', '米'), ('厚度', '毫米')],
            calc_func=flange_calc,
            result_label=Label(text='-- kg', font_name=font_name)
        )
        root.add_widget(tab4)

        return root


if __name__ == '__main__':
    MetalCalculatorApp().run()