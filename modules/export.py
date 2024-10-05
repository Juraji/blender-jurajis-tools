"""
Export Tools
"""
import os
import re
import bpy
from bpy.types import Operator, Object

from . import JurajisToolsPanel
from ..functions.batch import batch_run_on_selected_objects
from ..functions.poll import mode_is_object, selected_objects_has_selection

SEP = ' -- '
ROOT = '//'
G_SCALE = 1.0


class OBJECT_OT_ExportSelected(Operator):
    bl_idname = "object.juraji_export_selected"
    bl_label = "Export STL"
    bl_description = "Export selected to separate STL files"
    bl_options = {'REGISTER', 'UNDO'}

    @staticmethod
    def export_stl(obj: Object, base_name: str, base_path: str):
        # Build export path
        name = base_name + SEP + re.sub(r'[\\/:*?"<>|]', '', obj.name)
        export_path = os.path.join(base_path, name)
        export_path = bpy.path.ensure_ext(export_path, '.stl')

        # Do export
        bpy.ops.wm.stl_export(
            filepath=export_path,
            ascii_format=False,
            global_scale=G_SCALE,
            apply_modifiers=True,
            export_selected_objects=True,
        )

    @classmethod
    def poll(cls, context):
        return mode_is_object(context) and selected_objects_has_selection(context)

    def execute(self, context):
        # Build export path
        base_path = os.path.basename(context.blend_data.filepath)
        base_path = bpy.path.abspath(ROOT + base_path)
        base_name = os.path.splitext(base_path)[0]

        batch_run_on_selected_objects(context, lambda o: self.export_stl(o, base_name, base_path))

        self.report({'INFO'}, "STL export completed")

        return {"FINISHED"}

    def invoke(self, context, event):
        if not context.blend_data.is_saved:
            self.report({'WARNING'}, "This project has not yet been saved. "
                                     "The export can not determine a target export directory.")
            return {'CANCELED'}

        return self.execute(context)


class VIEW3D_PT_Export(JurajisToolsPanel):
    bl_label = "Export"

    @classmethod
    def poll(cls, context):
        return mode_is_object(context)

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False

        layout.operator("object.juraji_export_selected")


def register():
    bpy.utils.register_class(OBJECT_OT_ExportSelected)
    bpy.utils.register_class(VIEW3D_PT_Export)


def unregister():
    bpy.utils.unregister_class(OBJECT_OT_ExportSelected)
    bpy.utils.unregister_class(VIEW3D_PT_Export)
