"""
Scale Converter
"""
import bpy
from bpy.props import PointerProperty
from bpy.types import PropertyGroup, Operator

from . import JurajisToolsPanel
from ..functions.batch import batch_run_on_selected_objects
from ..functions.poll import mode_is_object, selected_objects_has_selection


class ScaleConverterProperties(PropertyGroup):
    current_scale: bpy.props.FloatProperty(
        name="Current scale (1:N)",
        description="The current scale, by 1 over N",
        default=1,
        min=1,
        step=1,
    )
    target_scale: bpy.props.FloatProperty(
        name="Target scale (1:N)",
        description="The target scale, by 1 over N",
        default=1,
        min=1,
        step=1,
    )


class OBJECT_OT_ScaleConverter(Operator):
    bl_idname = "object.juraji_scale_converter"
    bl_label = "Convert scale"
    bl_description = "Convert scale and apply to currently selected objects"
    bl_options = {'REGISTER', 'UNDO'}

    @staticmethod
    def scale_object(scale: float):
        bpy.ops.transform.resize(
            value=(scale, scale, scale),
            orient_type='GLOBAL',
            orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)),
        )
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

    @classmethod
    def poll(cls, context):
        return mode_is_object(context) and selected_objects_has_selection(context)

    def execute(self, context):
        # noinspection PyUnresolvedReferences
        props: ScaleConverterProperties = context.scene.juraji_scale_converter

        scale_factor: float = props.current_scale / props.target_scale

        batch_run_on_selected_objects(
            context,
            lambda o: self.scale_object(scale_factor),
        )

        scale_perc = round(100 * scale_factor, 2)
        self.report({'INFO'}, "Scale converted successfully. "
                              f"Source: 1/{props.current_scale:.1f} to 1/{props.target_scale:.1f}, "
                              f"{scale_perc:.2f}%")

        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class VIEW3D_PT_ScaleConverter(JurajisToolsPanel):
    bl_label = "Scale Converter"

    @classmethod
    def poll(cls, context):
        return mode_is_object(context)

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False

        # noinspection PyUnresolvedReferences
        props: ScaleConverterProperties = context.scene.juraji_scale_converter

        layout.prop(props, "current_scale")
        layout.prop(props, "target_scale")

        layout.operator(operator="object.juraji_scale_converter")


def register():
    bpy.utils.register_class(OBJECT_OT_ScaleConverter)
    bpy.utils.register_class(VIEW3D_PT_ScaleConverter)
    bpy.utils.register_class(ScaleConverterProperties)

    bpy.types.Scene.juraji_scale_converter = PointerProperty(type=ScaleConverterProperties)


def unregister():
    bpy.utils.unregister_class(OBJECT_OT_ScaleConverter)
    bpy.utils.unregister_class(VIEW3D_PT_ScaleConverter)
    bpy.utils.unregister_class(ScaleConverterProperties)

    # noinspection PyUnresolvedReferences
    del bpy.types.Scene.juraji_scale_converter
