from bpy.types import Context, Object


### Editor modes

def mode_is_object(context: Context):
    """
    Checks of the current editor mode is set to "OBJECT"
    :param context:
    :return:
    """
    return context.mode == 'OBJECT'


### Object

def object_is_mesh(context: Context, obj: Object = None, check_linked=False):
    obj = obj or context.active_object

    if obj is None:
        return False
    if obj.type == 'MESH':
        if check_linked and object_is_linked(context, obj) == True:
            return False
        return True


def object_is_linked(context: Context, obj: Object = None):
    obj = obj or context.active_object

    if obj not in context.editable_objects:
        return True
    else:
        if obj.library or obj.override_library:
            return True


### Selected objects

def selected_objects_has_selection(context: Context):
    return len(context.selected_objects) != 0


def selected_objects_all_is_mesh(context: Context):
    """
    Checks if all selected objects in the given context are of type MESH,
    Note, if no objects are selected, this method returns False.

    :param context:
    :return:
    """
    return (selected_objects_has_selection(context) and
            all(object_is_mesh(context, o) for o in context.selected_objects))
