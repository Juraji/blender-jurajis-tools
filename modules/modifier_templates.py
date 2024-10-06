"""
Modifier templates
"""
import bpy
from bpy.props import PointerProperty, IntProperty, FloatProperty
from bpy.types import Object, PropertyGroup, Operator, Panel

from functions.poll import selected_objects_has_selection
from ..functions.poll import mode_is_object


class ModifierTemplatesProperties(PropertyGroup):
    pass

class OBJECT_OT_ApplyModifierTemplate(Operator):
    bl_idname = "object.juraji_apply_modifier_template"
    bl_label = "Apply Template"
    bl_description = "Apply this modifier template to the currently selected objects"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return mode_is_object(context) and selected_objects_has_selection(context)

    def execute(self, context):
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class VIEW3D_PT_ModifierTemplates(Panel):
    bl_category = "Juraji's Tools"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_context = "objectmode"
    bl_label = "Modifier Templates"

    @classmethod
    def poll(cls, context):
        return mode_is_object(context)

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False

        # noinspection PyUnresolvedReferences
        props: ModifierTemplatesProperties = context.scene.juraji_modifier_templates

        # layout.prop(props, "decimate_ratio")
        # layout.prop(props, "repeat_n_times")
        #
        # layout.operator(operator="object.juraji_auto_decimate")


def register():
    bpy.utils.register_class(OBJECT_OT_ApplyModifierTemplate)
    bpy.utils.register_class(VIEW3D_PT_ModifierTemplates)
    bpy.utils.register_class(ModifierTemplatesProperties)

    bpy.types.Scene.juraji_modifier_templates = PointerProperty(type=ModifierTemplatesProperties)


def unregister():
    bpy.utils.unregister_class(OBJECT_OT_ApplyModifierTemplate)
    bpy.utils.unregister_class(VIEW3D_PT_ModifierTemplates)
    bpy.utils.unregister_class(ModifierTemplatesProperties)

    # noinspection PyUnresolvedReferences
    del bpy.types.Scene.juraji_modifier_templates
