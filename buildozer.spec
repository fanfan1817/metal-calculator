[app]

title = 金属建材计算器
package.name = metalcalculator
package.domain = org.metalcalc

source.include_exts = py,png,jpg,kv,atlas,ttc,ttf
source.dir = .

version = 1.0

requirements = python3,kivy==2.3.1

orientation = portrait

# 全屏显示，防止内容被状态栏遮挡而下移
fullscreen = 1

android.permissions = INTERNET
android.minapi = 21

[buildozer]

log_level = 2

warn_on_root = 1