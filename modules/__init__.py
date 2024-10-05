"""
Add-on modules
"""
from bpy.types import Panel


class JurajisToolsPanel(Panel):
    """
    Base class for this add-on's panels.
    """
    bl_category = "Juraji's Tools"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
