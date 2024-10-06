"""
Add-on init
"""
from .modules import auto_decimate, scale_converter, export, modifier_templates

modules = [
    auto_decimate,
    scale_converter,
    export,
    modifier_templates
]


def register():
    for module in modules:
        module.register()


def unregister():
    for module in reversed(modules):
        module.unregister()
