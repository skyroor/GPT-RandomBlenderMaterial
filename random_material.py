bl_info = {
    "name": "Random Material",
    "author": "openAI",
    "version": (0, 5, 0),
    "blender": (3, 3, 0),
    "location": "TBA",
    "description": "Creates a random material",
    "category": "Material"}
    
import bpy
from random import random, randint

# create a new material
def create_random_material(name):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True

    # get the material nodes
    nodes = mat.node_tree.nodes

    # remove default nodes
    for node in nodes:
        nodes.remove(node)

    # create new diffuse, glossy, noise, mix, and output nodes
    diffuse = nodes.new(type="ShaderNodeBsdfDiffuse")
    glossy = nodes.new(type="ShaderNodeBsdfGlossy")
    noise = nodes.new(type="ShaderNodeTexNoise")
    mix = nodes.new(type="ShaderNodeMixShader")
    output = nodes.new(type="ShaderNodeOutputMaterial")

    # adjust the diffuse and glossy colors
    diffuse.inputs[0].default_value = (random(), random(), random(), 1)
    glossy.inputs[0].default_value = (random(), random(), random(), 1)

    # set the noise texture inputs to random values between 1 and 10
    noise.inputs[2].default_value = randint(1, 50)
    noise.inputs[3].default_value = randint(1, 10)
    noise.inputs[4].default_value = randint(1, 10)
    noise.inputs[5].default_value = randint(0, 1)
    
    # space the nodes out on the grid
    diffuse.location = (-150, 0)
    glossy.location = (-150, -150)
    noise.location = (-150, 250)
    mix.location = (150, 0)
    output.location = (300, 0)

    # create links between the nodes
    mat.node_tree.links.new(diffuse.outputs[0], mix.inputs[1])
    mat.node_tree.links.new(glossy.outputs[0], mix.inputs[2])
    mat.node_tree.links.new(noise.outputs[0], mix.inputs[0])
    mat.node_tree.links.new(mix.outputs[0], output.inputs[0])

    return mat


# add the material to the active object
def add_material_to_active_object(material):
    obj = bpy.context.active_object
    if obj.data.materials:
        # assign to 1st material slot
        obj.data.materials[0] = material
    else:
        # no slots
        obj.data.materials.append(material)

class AddRandomMaterialOperator(bpy.types.Operator):
    """Add a random material to the active object"""
    bl_idname = "object.add_random_material"
    bl_label = "Add Random Material"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        # create a random material
        mat = create_random_material("Random Material")
        # add the material to the active object
        add_material_to_active_object(mat)
        return {'FINISHED'}
        
addon_keymaps = []
    
def register_hotkey():
    # get the default keymap
    wm = bpy.context.window_manager
    km = wm.keyconfigs.addon.keymaps.new(name="Object Mode", space_type="EMPTY")

    # create a new hotkey
    kmi = km.keymap_items.new("object.add_random_material", "R", "PRESS", shift=True, alt=True)

    # save the hotkey
    addon_keymaps.append((km, kmi))

def unregister_hotkey():
    # remove the hotkey
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()

def register():
    register_hotkey()
    bpy.utils.register_class(AddRandomMaterialOperator)

def unregister():
    unregister_hotkey()
    bpy.utils.unregister_class(AddRandomMaterialOperator)

if __name__ == "__main__":
    register()