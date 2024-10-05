"""
Decimation tools
"""
import bpy
from bpy.props import PointerProperty, IntProperty, FloatProperty
from bpy.types import Object, PropertyGroup, Operator, Panel

from ..functions.batch import batch_run_on_selected_objects
from ..functions.poll import mode_is_object, selected_objects_all_is_mesh


class AutoDecimateProperties(PropertyGroup):
    repeat_n_times: IntProperty(
        name="Repeat",
        description="Number of times to repeat the decimate operation",
        default=1,
        min=1,
        step=1,
    )
    decimate_ratio: FloatProperty(
        name="Ratio",
        description="Ratio to decimate the objects",
        default=0.5,
        max=1.0,
    )


class OBJECT_OT_AutoDecimate(Operator):
    bl_idname = "object.juraji_auto_decimate"
    bl_label = "Apply decimation"
    bl_description = "Decimate the current selected objects"
    bl_options = {'REGISTER', 'UNDO'}

    @staticmethod
    def decimate_object(obj: Object, repeat_n_times: int, decimate_ratio: float):
        # Apply "Decimate" modifier N times
        for _ in range(0, repeat_n_times):
            md = obj.modifiers.new(f"Auto Decimate by {decimate_ratio}", "DECIMATE")
            md.show_viewport = False
            md.ratio = decimate_ratio
            bpy.ops.object.modifier_apply(modifier=md.name)

    @classmethod
    def poll(cls, context):
        return mode_is_object(context) and selected_objects_all_is_mesh(context)

    def execute(self, context):
        # noinspection PyUnresolvedReferences
        props: AutoDecimateProperties = context.scene.juraji_auto_decimate

        batch_run_on_selected_objects(
            context,
            lambda o: self.decimate_object(
                o,
                props.repeat_n_times,
                props.decimate_ratio
            ),
        )

        self.report({'INFO'}, "Decimation applied")

        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class VIEW3D_PT_AutoDecimate(Panel):
    bl_category = "Juraji's Tools"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_context = "objectmode"
    bl_label = "Auto Decimate"

    @classmethod
    def poll(cls, context):
        return mode_is_object(context)

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False

        # noinspection PyUnresolvedReferences
        props: AutoDecimateProperties = context.scene.juraji_auto_decimate

        layout.prop(props, "decimate_ratio")
        layout.prop(props, "repeat_n_times")

        layout.operator(operator="object.juraji_auto_decimate")


def register():
    bpy.utils.register_class(OBJECT_OT_AutoDecimate)
    bpy.utils.register_class(VIEW3D_PT_AutoDecimate)
    bpy.utils.register_class(AutoDecimateProperties)

    bpy.types.Scene.juraji_auto_decimate = PointerProperty(type=AutoDecimateProperties)


def unregister():
    bpy.utils.unregister_class(OBJECT_OT_AutoDecimate)
    bpy.utils.unregister_class(VIEW3D_PT_AutoDecimate)
    bpy.utils.unregister_class(AutoDecimateProperties)

    # noinspection PyUnresolvedReferences
    del bpy.types.Scene.juraji_auto_decimate
