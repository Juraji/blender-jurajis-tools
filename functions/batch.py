"""
Batch functions
"""
from typing import Callable
import bpy

from bpy.types import Context, Object


def batch_run_on_selected_objects(context: Context, op: Callable[[Object], None]):
    """
    Run [op] on all selected objects in the given context.
    :param context:
    :param op:
    :return:
    """
    # Copy current selection and deselect everything
    selected_objects = context.selected_objects
    bpy.ops.object.select_all(action='DESELECT')

    # Iterate through all selected objects
    for obj in selected_objects:
        # Select this object and set it as active
        context.view_layer.objects.active = obj
        obj.select_set(True)

        # Call [fn], given the current object
        op(obj)

        # Deselect object
        obj.select_set(False)

    # Unhide and Re-select the original selected objects
    for obj in selected_objects:
        obj.select_set(True)
