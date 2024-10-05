"""
Export Tools
"""
import os
import re

import bpy
from bpy.props import StringProperty, EnumProperty, PointerProperty
from bpy.types import Operator, Object, Panel, PropertyGroup

from ..functions.batch import batch_run_on_selected_objects
from ..functions.poll import mode_is_object, selected_objects_has_selection

G_SCALE = 1.0


class ExportPartsProperties(PropertyGroup):
    name_separator: StringProperty(
        name="Object Name Separator",
        description="The separator to use for object names",
        default=" -- ",
        maxlen=1024,
    )
    export_path: StringProperty(
        name="Export Directory",
        description="Path to directory where the files are created",
        default="//parts",
        maxlen=1024,
        subtype="DIR_PATH",
    )
    export_format: EnumProperty(
        name="Format",
        description="Export file format",
        items=(
            ("STL", "STL", ""),
        ),
        default="STL",
    )


class OBJECT_OT_ExportParts(Operator):
    bl_idname = "object.juraji_export_parts"
    bl_label = "Export parts"
    bl_description = "Export selected to separate files"
    bl_options = {'REGISTER', 'UNDO'}

    @staticmethod
    def build_export_path(base_path: str, base_name: str, separator: str, object_name: str, extension: str) -> str:
        name = base_name + separator + re.sub(r'[\\/:*?"<>|]', '', object_name)
        export_path = os.path.join(base_path, name)
        return bpy.path.ensure_ext(export_path, extension)

    @staticmethod
    def export_stl(obj: Object, base_name: str, base_path: str, separator: str):
        # Build export path
        export_path = OBJECT_OT_ExportParts.build_export_path(base_path, base_name, separator, obj.name, ".stl")

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
        # noinspection PyUnresolvedReferences
        props: ExportPartsProperties = context.scene.juraji_part_export

        # Build export path
        export_path = bpy.path.abspath(props.export_path)

        if export_path:
            try:
                os.makedirs(export_path, exist_ok=True)
            except OSError:
                self.report({"ERROR"}, f"Could not create directory {export_path}")
                return {"CANCELLED"}

        if bpy.data.is_saved:
            base_name = os.path.basename(bpy.data.filepath)
            base_name = os.path.splitext(base_name)[0]
        else:
            base_name = "untitled"

        batch_run_on_selected_objects(context, lambda o: self.export_stl(
            o, base_name, export_path, props.name_separator))

        self.report({'INFO'}, "Part export completed!")

        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class VIEW3D_PT_ExportParts(Panel):
    bl_category = "Juraji's Tools"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_context = "objectmode"
    bl_label = "Part Export"

    @classmethod
    def poll(cls, context):
        return mode_is_object(context)

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False

        # noinspection PyUnresolvedReferences
        props: ExportPartsProperties = context.scene.juraji_part_export

        layout.prop(props, "export_path", text="")
        layout.prop(props, "export_format")
        layout.prop(props, "name_separator")

        layout.operator("object.juraji_export_parts")


def register():
    bpy.utils.register_class(OBJECT_OT_ExportParts)
    bpy.utils.register_class(VIEW3D_PT_ExportParts)
    bpy.utils.register_class(ExportPartsProperties)

    bpy.types.Scene.juraji_part_export = PointerProperty(type=ExportPartsProperties)


def unregister():
    bpy.utils.unregister_class(OBJECT_OT_ExportParts)
    bpy.utils.unregister_class(VIEW3D_PT_ExportParts)
    bpy.utils.unregister_class(ExportPartsProperties)

    # noinspection PyUnresolvedReferences
    del bpy.types.Scene.juraji_part_export
