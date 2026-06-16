import os

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

# Android 沉浸式全屏（修复 UI 靠下）
if platform == 'android':
    try:
        from jnius import autoclass
        activity = autoclass('org.kivy.android.PythonActivity').mActivity
        WindowManager = autoclass('android.view.WindowManager$LayoutParams')
        activity.getWindow().addFlags(WindowManager.FLAG_LAYOUT_NO_LIMITS)
        View = autoclass('android.view.View')
        activity.getWindow().getDecorView().setSystemUiVisibility(
            View.SYSTEM_UI_FLAG_LAYOUT_STABLE
            | View.SYSTEM_UI_FLAG_LAYOUT_FULLSCREEN
            | View.SYSTEM_UI_FLAG_LAYOUT_HIDE_NAVIGATION
        )
    except Exception:
        pass

Window.softinput_mode = 'below_target'

FONT_NAME = 'ChineseFont'


def make_tab(parent, title, formula_text, inputs, calc_func):
    """Factory to build one calculator tab"""
    layout = BoxLayout(orientation='vertical', padding=15, spacing=8)

    # Title
    layout.add_widget(Label(
        text=title,
        font_size='18sp',
        bold=True,
        size_hint_y=None,
        height=40,
        font_name=FONT_NAME
    ))

    # Formula
    layout.add_widget(Label(
        text=formula_text,
        font_size='10sp',
        color=(0.5, 0.5, 0.5, 1),
        size_hint_y=None,
        height=25,
        font_name=FONT_NAME
    ))

    # Input fields
    inp_widgets = {}
    for inp_name, unit in inputs:
        row = BoxLayout(size_hint_y=None, height=45)
        lbl = Label(
            text=f'{inp_name} ({unit}):',
            font_size='13sp',
            text_size=(Window.width * 0.45, None),
            valign='middle',
            font_name=FONT_NAME
        )
        inp = TextInput(
            hint_text='0',
            multiline=False,
            input_filter='float',
            font_size='14sp',
            size_hint_x=0.55,
            padding=[5, 5]
        )
        inp_widgets[inp_name] = inp
        row.add_widget(lbl)
        row.add_widget(inp)
        layout.add_widget(row)

    # Meter input (optional)
    meter_inp = TextInput(
        hint_text='选填',
        multiline=False,
        input_filter='float',
        font_size='13sp',
        size_hint_y=None,
        height=40
    )
    layout.add_widget(Label(text='总米数（米，选填）:', font_size='12sp', color=(0.5, 0.5, 0.5, 1), size_hint_y=None, height=22, font_name=FONT_NAME))
    layout.add_widget(meter_inp)

    # Result label
    result_lbl = Label(
        text='-- kg',
        font_size='22sp',
        color=(0.15, 0.39, 0.92, 1),
        bold=True,
        size_hint_y=None,
        height=50,
        font_name=FONT_NAME
    )

    def do_calc(instance):
        try:
            vals = {}
            for name, w in inp_widgets.items():
                v = w.text.strip()
                if not v:
                    result_lbl.text = '请输入所有参数'
                    return
                vals[name] = float(v)
            m_text = meter_inp.text.strip()
            meter_val = float(m_text) if m_text else None
            result = calc_func(vals, meter_val)
            result_lbl.text = f'{result:.4f} kg'
        except ValueError:
            result_lbl.text = '请输入有效数字'
        except Exception:
            result_lbl.text = '错误'

    btn = Button(
        text='计算',
        font_size='16sp',
        background_color=(0.15, 0.39, 0.92, 1),
        size_hint_y=None,
        height=48,
        font_name=FONT_NAME
    )
    btn.bind(on_press=do_calc)
    layout.add_widget(btn)

    layout.add_widget(result_lbl)
    return layout


def pipe_calc(v, m):
    r = v['直径'] - v['厚度']
    r = r * v['厚度']
    r = r * v['厚度']
    r = r * 0.02466
    return r * m if m else r


def square_calc(v, m):
    r = v['周长'] / 3.14 - v['厚度']
    r = r * v['厚度']
    r = r * 0.02466
    return r * m if m else r


def wire_calc(v, m):
    r = v['长度'] * v['丝径'] * v['丝径'] * 0.00617
    return r * m if m else r


def flange_calc(v, m):
    r = 7.85 * v['边长1'] * v['边长2'] * v['厚度']
    return r * m if m else r


class MetalCalculatorApp(App):
    def build(self):
        self.title = '金属建材计算器'
        root = TabbedPanel(tab_pos='top_mid', do_default_tab=False)

        root.add_widget(make_tab(
            None, '圆管重量计算',
            '(直径-厚度) × 厚度 × 厚度 × 0.02466',
            [('直径', '毫米'), ('厚度', '毫米')],
            pipe_calc
        ))
        root.add_widget(make_tab(
            None, '方管重量计算',
            '((周长÷3.14)-厚度) × 厚度 × 0.02466',
            [('周长', '毫米'), ('厚度', '毫米')],
            square_calc
        ))
        root.add_widget(make_tab(
            None, '丝径重量计算',
            '长度 × 丝径 × 丝径 × 0.00617',
            [('长度', '米'), ('丝径', '毫米')],
            wire_calc
        ))
        root.add_widget(make_tab(
            None, '法兰盘重量计算',
            '7.85 × 边长1 × 边长2 × 厚度',
            [('边长1', '米'), ('边长2', '米'), ('厚度', '毫米')],
            flange_calc
        ))
        return root


if __name__ == '__main__':
    MetalCalculatorApp().run()