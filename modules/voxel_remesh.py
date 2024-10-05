"""
Voxel remesh tools
"""
import bpy

from bpy.props import PointerProperty, FloatProperty
from bpy.types import PropertyGroup, Object, Operator, Panel
from ..functions.batch import batch_run_on_selected_objects
from ..functions.poll import mode_is_object, selected_objects_all_is_mesh


class VoxelRemeshProperties(PropertyGroup):
    voxel_size: FloatProperty(
        name="Voxel Size",
        description="The voxel size to use",
        default=0.005,
        min=0.001,
        precision=3,
    )


class OBJECT_OT_VoxelRemesh(Operator):
    bl_idname = "object.juraji_voxel_remesh"
    bl_label = "Remesh"
    bl_description = "Apply a voxel remesh"
    bl_options = {'REGISTER', 'UNDO'}

    @staticmethod
    def remesh_objects(obj: Object, voxel_size: float):
        md = obj.modifiers.new(f"Remesh {voxel_size}", "REMESH")
        md.show_viewport = False
        md.voxel_size = voxel_size
        bpy.ops.object.modifier_apply(modifier=md.name)

    @classmethod
    def poll(cls, context):
        return mode_is_object(context) and selected_objects_all_is_mesh(context)

    def execute(self, context):
        # noinspection PyUnresolvedReferences
        props: VoxelRemeshProperties = context.scene.juraji_voxel_remesh
        normalized_voxel_size = props.voxel_size * 10

        batch_run_on_selected_objects(
            context,
            lambda o: self.remesh_objects(o, normalized_voxel_size),
        )

        self.report({'INFO'}, "Remesh applied")
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class VIEW3D_PT_VoxelRemesh(Panel):
    bl_category = "Juraji's Tools"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_context = "objectmode"
    bl_label = "Voxel Remesh"

    @classmethod
    def poll(cls, context):
        return mode_is_object(context)

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False

        # noinspection PyUnresolvedReferences
        props: VoxelRemeshProperties = context.scene.juraji_voxel_remesh

        layout.prop(props, "voxel_size")

        layout.operator(operator="object.juraji_voxel_remesh")


def register():
    bpy.utils.register_class(OBJECT_OT_VoxelRemesh)
    bpy.utils.register_class(VIEW3D_PT_VoxelRemesh)
    bpy.utils.register_class(VoxelRemeshProperties)

    bpy.types.Scene.juraji_voxel_remesh = PointerProperty(type=VoxelRemeshProperties)


def unregister():
    bpy.utils.unregister_class(OBJECT_OT_VoxelRemesh)
    bpy.utils.unregister_class(VIEW3D_PT_VoxelRemesh)
    bpy.utils.unregister_class(VoxelRemeshProperties)

    # noinspection PyUnresolvedReferences
    del bpy.types.Scene.juraji_voxel_remesh
