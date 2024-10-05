"""
Add-on init
"""
from .modules import auto_decimate, scale_converter, export

modules = [
    auto_decimate,
    scale_converter,
    export
]


def register():
    for module in modules:
        module.register()


def unregister():
    for module in reversed(modules):
        module.unregister()
