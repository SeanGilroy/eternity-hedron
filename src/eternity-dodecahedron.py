import bpy
import bmesh
import os
import sys
import time
import mathutils
import operator
from math import pi, radians, sin, cos, acos, tan, atan, sqrt
import math
from contextlib import contextmanager

#Hides select Blender console output 
@contextmanager
def suppress_stdout():
    with open(os.devnull, "w") as devnull:
        old_stdout = sys.stdout
        sys.stdout = devnull
        try:  
            yield
        finally:
            sys.stdout = old_stdout

            
#######################################
## Clear previously Generated Design ##
#######################################

for collection in bpy.data.collections:
    bpy.data.collections.remove(collection)

for object in bpy.data.objects:
    bpy.data.objects.remove(object)


###################
## Blender Setup ##
###################

bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.scale_length = 1
bpy.context.scene.unit_settings.length_unit = 'MILLIMETERS'
bpy.context.scene.cursor.location =  [0, 0, 0]
bpy.context.scene.cursor.rotation_euler =  [0, 0, 0]
bpy.ops.extensions.userpref_allow_online()
bpy.ops.extensions.package_install(repo_index=0, pkg_id="edit_mesh_tools")
bpy.ops.extensions.package_install(repo_index=0, pkg_id="print3d_toolbox")
#bpy.context.space_data.clip_end = 10000

for collection in ["FRAME", "OUTER"]:
    bpy.context.scene.collection.children.link(bpy.data.collections.new(collection))

start_time = time.time()



######################
##  Parameters ##
######################
phi = ( 1 + sqrt(5) ) / 2
dihedral_angle_dodecahedron = math.acos(-math.sqrt(5)/5)

acrylic_thickness = 2.8
acrylic_tolerance = 0.2
LED_per_meter = 144/1000
LED_per_side = 17
LED_length = LED_per_side/LED_per_meter

frame_thickness = 1.5
frame_height = 10
frame_width = 0

underwire_thickness = 1.5
frame_outer_bottom_thickness = 3 + underwire_thickness

frame_rail_width = 2
frame_sidewall_height = 12

led_strip_width = 12.2
led_strip_height = 2.2
led_acrylic_gap = 5

XXX = led_acrylic_gap/(2*sin(dihedral_angle_dodecahedron/2)) + frame_thickness + frame_thickness/(tan(dihedral_angle_dodecahedron/2))

frame_length = LED_length*(LED_length/(2*tan(2*pi/10)) + XXX)/(LED_length/(2*tan(2*pi/10)))



######################
## dodecahedron ##
######################





edge_scale = frame_length/(sqrt(5)-1)
dodecahedron_vertex = []
dodecahedron_edges = []
dodecahedron_faces = []




# Generate dodecahedron verticies
for i in (1, -1):
    for j in (1, -1):
        for k in (1, -1):
            dodecahedron_vertex.append( [edge_scale*i*1, edge_scale*j*1, edge_scale*k*1] )

for j in (1, -1):
    for k in (1, -1):
        dodecahedron_vertex.append( [0, edge_scale*j/phi, edge_scale*k*phi] )
        
for i in (1, -1):
    for j in (1, -1):
        dodecahedron_vertex.append( [edge_scale*i/phi, edge_scale*j*phi, 0] )
        
for i in (1, -1):
    for k in (1, -1):
        dodecahedron_vertex.append( [edge_scale*i*phi, 0, edge_scale*k/phi] )

# Define dodecahedron edges and faces based on verticies
for path in [[10,  2, 13, 15,  6],
             [ 8,  0, 16,  2, 10],
             [ 8,  4, 14, 12,  0],
             [10,  6, 18,  4,  8],
             [ 2, 16, 17,  3, 13],
             [ 0, 12,  1, 17, 16],
             [ 4, 18, 19,  5, 14],
             [ 6, 15,  7, 19, 18],
             [11,  7, 15,  13, 3],
             [ 9,  5, 19,  7, 11],
             [ 9,  1, 12, 14,  5],
             [11,  3, 17,  1,  9]]:
    for i in range(len(path)):
        dodecahedron_edges.append([path[i], path[(i+1) % len(path)]])
    dodecahedron_faces.append(list(reversed(path)))









frame_mesh = bpy.data.meshes.new("Dodecahedron_LED")
frame_mesh.from_pydata(dodecahedron_vertex, dodecahedron_edges, dodecahedron_faces)
frame_mesh.validate()
frame_mesh.update()


bpy.context.collection.objects.link(bpy.data.objects.new("Dodecahedron_LED", frame_mesh))

bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)

bpy.ops.object.select_all(action='DESELECT')
bpy.context.view_layer.objects.active = bpy.data.objects['Dodecahedron_LED']
bpy.data.objects['Dodecahedron_LED'].select_set(True)


#bpy.ops.transform.resize(value=(phi/2, phi/2, phi/2), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, snap=False, snap_elements={'INCREMENT'}, use_snap_project=False, snap_target='CLOSEST', use_snap_self=True, use_snap_edit=True, use_snap_nonedit=True, use_snap_selectable=False)
bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)






phi = ( 1 + sqrt(5) ) / 2
edge_scale = frame_length/(sqrt(5)-1)
dodecahedron_vertex = []
dodecahedron_edges = []
dodecahedron_faces = []

for i in (1, -1):
    for j in (1, -1):
        for k in (1, -1):
            dodecahedron_vertex.append( [edge_scale*i*1, edge_scale*j*1, edge_scale*k*1] )

for j in (1, -1):
    for k in (1, -1):
        dodecahedron_vertex.append( [0, edge_scale*j/phi, edge_scale*k*phi] )
        
for i in (1, -1):
    for j in (1, -1):
        dodecahedron_vertex.append( [edge_scale*i/phi, edge_scale*j*phi, 0] )
        
for i in (1, -1):
    for k in (1, -1):
        dodecahedron_vertex.append( [edge_scale*i*phi, 0, edge_scale*k/phi] )

for path in [[10,  2, 13, 15,  6],
             [ 8,  0, 16,  2, 10],
             [ 8,  4, 14, 12,  0],
             [10,  6, 18,  4,  8],
             [ 2, 16, 17,  3, 13],
             [ 0, 12,  1, 17, 16],
             [ 4, 18, 19,  5, 14],
             [ 6, 15,  7, 19, 18],
             [11,  7, 15,  13, 3],
             [ 9,  5, 19,  7, 11],
             [ 9,  1, 12, 14,  5],
             [11,  3, 17,  1,  9]]:
    for i in range(len(path)):
        dodecahedron_edges.append([path[i], path[(i+1) % len(path)]])
    dodecahedron_faces.append(list(reversed(path)))









frame_mesh = bpy.data.meshes.new("Dodecahedron")
frame_mesh.from_pydata(dodecahedron_vertex, dodecahedron_edges, dodecahedron_faces)
frame_mesh.validate()
frame_mesh.update()

bpy.context.collection.objects.link(bpy.data.objects.new("Dodecahedron", frame_mesh))

bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)

bpy.ops.object.select_all(action='DESELECT')
bpy.context.view_layer.objects.active = bpy.data.objects['Dodecahedron']
bpy.data.objects['Dodecahedron'].select_set(True)

bpy.ops.object.mode_set(mode = 'EDIT')
bpy.ops.mesh.select_all(action='DESELECT')

edge_piece_locations = []
grid_mesh = bmesh.from_edit_mesh(bpy.context.object.data)

grid_mesh.faces.ensure_lookup_table()
face_angle = grid_mesh.faces[0].edges[0].calc_face_angle()
face_angle=108*pi/180
#print("face angle", face_angle)


for face in grid_mesh.faces:
    face.select = True

    bpy.ops.mesh.inset(thickness=led_acrylic_gap/(2*sin(dihedral_angle_dodecahedron/2)) + frame_thickness+ frame_thickness/(tan(dihedral_angle_dodecahedron/2)), use_select_inset=True)
    bpy.ops.mesh.delete(type='FACE')
    
    last_vert = []
    
    for i in range(len(face.edges)):
        if face.edges[i].verts[1].index in last_vert:
            last_vert.append(face.edges[i].verts[0].index)
            
            vertex_order = [face.edges[i].verts[0].index, face.edges[i].verts[1].index]
            face.edges[i].verts[0].index = vertex_order[1]
            face.edges[i].verts[1].index = vertex_order[0]
            
            flip = 1

        else:
            last_vert.append(face.edges[i].verts[1].index)

            flip = -1

        edge_piece_locations.append([
                                     (face.edges[i].verts[1].co + face.edges[i].verts[0].co)/2,
                                     face.normal,
                                     (face.edges[i].verts[1].co - face.edges[i].verts[0].co),
                                     face.calc_center_median() - (face.edges[i].verts[1].co + face.edges[i].verts[0].co)/2,
                                     face.calc_center_median(),
                                     1
                                      ])
        frame_length = face.edges[i].calc_length()

print("frame length", frame_length)
bpy.ops.object.mode_set(mode = 'OBJECT')


#############################
## frame.inside Creation   ##
#############################


# Inside Lip Negative
bpy.ops.mesh.primitive_cube_add(size=1, enter_editmode=False, align='WORLD', location=(0, frame_height-frame_thickness/2, -frame_thickness/2), scale=(frame_length + 4.5*tan(face_angle-pi/2), frame_height, 2*frame_thickness))
bpy.context.object.name = "frame.inside.lip_negative"

# Acrylic Negative
bpy.ops.mesh.primitive_cube_add(size=1, enter_editmode=False, align='WORLD', location=(0, frame_height/2, acrylic_thickness/2), scale=(frame_length + 4.5*tan(face_angle-pi/2), frame_height, acrylic_thickness+acrylic_tolerance))
bpy.context.object.name = "frame.inside.acrylic_negative"

#Rail that connects to Outer Frame

bpy.ops.mesh.primitive_cube_add(size=1, enter_editmode=False, align='WORLD', location=(0, frame_rail_width/2, -3), scale=(frame_length + 4.5*tan(face_angle-pi/2), frame_rail_width-.2, 6))
bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
bpy.ops.transform.rotate(value=-0.553575, orient_axis='X', orient_type='GLOBAL', orient_matrix=((4.93038e-32, 1, 2.22045e-16), (2.22045e-16, 4.93038e-32, 1), (1, 2.22045e-16, 4.93038e-32)), orient_matrix_type='VIEW', mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, snap=False, snap_elements={'INCREMENT'}, use_snap_project=False, snap_target='CLOSEST', use_snap_self=False, use_snap_edit=True, use_snap_nonedit=True, use_snap_selectable=False)



XXX = led_acrylic_gap/(2*sin(dihedral_angle_dodecahedron/2)) + frame_thickness + frame_thickness/(tan(dihedral_angle_dodecahedron/2))
bpy.ops.transform.translate(value=(0, -XXX, 0))

YYY = led_strip_width/2+ frame_rail_width + 3*(0.2)/2
bpy.ops.transform.translate(value=(0, YYY*sin(dihedral_angle_dodecahedron/2), YYY*cos(dihedral_angle_dodecahedron/2)))

ZZZ = led_strip_height + frame_outer_bottom_thickness/3 -0.2
bpy.ops.transform.translate(value=(0, -ZZZ*cos(dihedral_angle_dodecahedron/2), ZZZ*sin(dihedral_angle_dodecahedron/2)))

bpy.context.object.name = "frame.inside.rail"


# Shape Ends into Corner Vertices
bpy.ops.mesh.primitive_cube_add(size=1, enter_editmode=False, align='WORLD', location=(frame_height, frame_height/2, acrylic_thickness/2), scale=(2*frame_height, 2*frame_height, 20+3*frame_thickness+acrylic_thickness))
bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')
bpy.ops.transform.rotate(value=face_angle/2-pi/2, orient_axis='Z', orient_type='GLOBAL', orient_matrix=((1, -0, 0), (-0, 1, -0), (0, -0, 1)), orient_matrix_type='VIEW', mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, snap=False, snap_elements={'INCREMENT'}, use_snap_project=False, snap_target='CLOSEST', use_snap_self=False, use_snap_edit=True, use_snap_nonedit=True, use_snap_selectable=False)
bpy.ops.transform.translate(value=((frame_length + 4.5*tan(face_angle-pi/2))/2, -1, 0), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(True, True, True), mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, snap=False, snap_elements={'INCREMENT'}, use_snap_project=False, snap_target='CLOSEST', use_snap_self=False, use_snap_edit=True, use_snap_nonedit=True, use_snap_selectable=False)
bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')
bpy.context.object.name = "frame.inside.corner_chamfer"
bpy.ops.object.duplicate()
bpy.ops.transform.mirror(orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(True, False, False))


# Main Inner Frame Piece
bpy.ops.mesh.primitive_cube_add(size=1, enter_editmode=False, align='WORLD', location=(0, frame_height/2 - frame_thickness, (2*frame_thickness+acrylic_thickness)/2-frame_thickness), scale=(frame_length + 2*frame_thickness*tan(pi/5), frame_height, 2*frame_thickness+acrylic_thickness))
bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
bpy.context.object.name = "frame.inside"



bpy.ops.object.modifier_add(type='BOOLEAN')
bpy.context.object.modifiers["Boolean"].object = bpy.data.objects["frame.inside.rail"]
bpy.context.object.modifiers["Boolean"].operation = 'UNION'
bpy.ops.object.modifier_apply(modifier="Boolean")

bpy.ops.object.modifier_add(type='BOOLEAN')
bpy.context.object.modifiers["Boolean"].object = bpy.data.objects["frame.inside.lip_negative"]
bpy.ops.object.modifier_apply(modifier="Boolean")

bpy.ops.object.modifier_add(type='BOOLEAN')
bpy.context.object.modifiers["Boolean"].object = bpy.data.objects["frame.inside.acrylic_negative"]
bpy.ops.object.modifier_apply(modifier="Boolean")

bpy.ops.object.modifier_add(type='BOOLEAN')
bpy.context.object.modifiers["Boolean"].object = bpy.data.objects["frame.inside.corner_chamfer"]
bpy.ops.object.modifier_apply(modifier="Boolean")

bpy.ops.object.modifier_add(type='BOOLEAN')
bpy.context.object.modifiers["Boolean"].object = bpy.data.objects["frame.inside.corner_chamfer.001"]
bpy.ops.object.modifier_apply(modifier="Boolean")

bpy.ops.object.select_all(action='DESELECT')

bpy.context.view_layer.objects.active = bpy.data.objects['frame.inside.lip_negative']
bpy.data.objects['frame.inside.lip_negative'].select_set(True)
bpy.data.objects['frame.inside.acrylic_negative'].select_set(True)
bpy.data.objects['frame.inside.rail'].select_set(True)
bpy.data.objects['frame.inside.corner_chamfer'].select_set(True)
bpy.data.objects['frame.inside.corner_chamfer.001'].select_set(True)
bpy.ops.object.delete(use_global=False)



######################
## Frame Placement  ##
######################


for frame in edge_piece_locations:    
        
    bpy.ops.object.add_named(name = "frame.inside")
    bpy.ops.transform.translate(value=frame[0], orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, snap=False, snap_elements={'INCREMENT'}, use_snap_project=False, snap_target='CLOSEST', use_snap_self=True, use_snap_edit=True, use_snap_nonedit=True, use_snap_selectable=False)
    
    bpy.data.collections['FRAME'].objects.link(bpy.context.selected_objects[-1])
    bpy.context.collection.objects.unlink(bpy.context.selected_objects[-1])
    
    
    local_z = frame[4].normalized()
    if local_z.length == 0:
        local_z = mathutils.Vector((0, 0, 1, 0))
        
    local_y = (frame[4]-frame[3]).normalized()
    if local_y.length == 0:
        local_y = mathutils.Vector((0, 1, 0, 0))
        
    local_x = local_z.cross(local_y).normalized()
    if local_x.length == 0:
        local_x = mathutils.Vector((1, 0, 0, 0))
    
    local_axis = mathutils.Matrix([local_x, -local_y, local_z])
    
    #bpy.context.object.rotation_mode = 'QUATERNION'
    #bpy.context.object.rotation_quaternion = local_x.to_track_quat('X','Y')
    
    
    rotation  = mathutils.Vector((1,0,0)).rotation_difference(local_x)
    
    bpy.context.object.rotation_mode = 'QUATERNION'
    bpy.context.object.rotation_quaternion = bpy.context.object.matrix_world.to_quaternion() @ rotation
    
    
    bpy.context.object.rotation_mode = 'XYZ'
    

    
    rot_local_x = local_y.angle(mathutils.Vector(bpy.context.object.rotation_euler.to_matrix() @ mathutils.Vector((1.0, 0.0, 0.0))))
    rot_local_y = local_y.angle(mathutils.Vector(bpy.context.object.rotation_euler.to_matrix() @ mathutils.Vector((0.0, 1.0, 0.0))))
    rot_local_z = local_z.angle(mathutils.Vector(bpy.context.object.rotation_euler.to_matrix() @ mathutils.Vector((0.0, 0.0, 1.0))))
    
    #print(bpy.context.object.name, mathutils.Vector(bpy.context.object.rotation_euler.to_matrix() @ mathutils.Vector((1.0, 0.0, 0.0))).dot(local_x))
    #print(bpy.context.object.name, mathutils.Vector(bpy.context.object.rotation_euler.to_matrix() @ mathutils.Vector((0.0, 1.0, 0.0))).dot(local_z))
    #print(bpy.context.object.name, mathutils.Vector(bpy.context.object.rotation_euler.to_matrix() @ mathutils.Vector((0.0, 0.0, 1.0))).dot(local_z))
    
    if mathutils.Vector(bpy.context.object.rotation_euler.to_matrix() @ mathutils.Vector((0.0, 1.0, 0.0))).dot(local_z) < 0:
        rot_local_z = -rot_local_z

    bpy.ops.transform.rotate(value=(rot_local_z), orient_axis='X', orient_type='LOCAL')
    
    #bpy.context.scene.cursor.location = bpy.context.object.location
    #bpy.context.scene.cursor.rotation_euler = bpy.context.object.rotation_euler

bpy.ops.object.mode_set(mode = 'OBJECT')






    
bpy.ops.object.select_all(action='DESELECT')

bpy.context.view_layer.objects.active = bpy.data.objects['Dodecahedron']
bpy.data.objects['Dodecahedron'].select_set(True)



bpy.ops.object.modifier_add(type='SOLIDIFY')
bpy.context.object.modifiers["Solidify"].thickness = -acrylic_thickness
bpy.context.object.modifiers["Solidify"].use_even_offset = True
bpy.ops.object.modifier_apply(modifier="Solidify")



########################
## frame.outside Creation   
##     - This is the outside superstructure that will join the acrilic sheets and also house the LEDs
##     - The orgin point is inline with the top of the LED strip
########################

# Vertex Chamfer
bpy.ops.mesh.primitive_cube_add(size=40, enter_editmode=False, align='WORLD', location=(20, 0, 0), scale=(1, 1, 1))
bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')
bpy.ops.transform.translate(value=(0, 0, frame_outer_bottom_thickness + led_strip_height))

# Angle is pentagon angle /6 (180*3 /5 /6 = 18 deg)
bpy.ops.transform.rotate(value=pi/10, orient_axis='Y', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, True, False), mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, snap=False, snap_elements={'INCREMENT'}, use_snap_project=False, snap_target='CLOSEST', use_snap_self=True, use_snap_edit=True, use_snap_nonedit=True, use_snap_selectable=False)


# Angle from here:  https://math.stackexchange.com/questions/4605339/dodecahedron-angle-between-edge-and-face
bpy.ops.transform.rotate(value=acos(sqrt((5-sqrt(5))/10)) - pi/2, orient_axis='Z', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, False, True), mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, snap=False, snap_elements={'INCREMENT'}, use_snap_project=False, snap_target='CLOSEST', use_snap_self=True, use_snap_edit=True, use_snap_nonedit=True, use_snap_selectable=False)

bpy.ops.transform.translate(value=(0.5*(2*tan(0.3648610801294146)*(frame_outer_bottom_thickness + led_strip_height)+LED_length*(LED_length/(2*tan(2*pi/10)) + XXX)/(LED_length/(2*tan(2*pi/10)))), 0, 0))
bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')

bpy.context.object.name = "frame.outside.vertex_chamfer.001"
bpy.ops.object.duplicate()
bpy.ops.transform.mirror(orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(True, False, False))
bpy.ops.object.duplicate()
bpy.ops.transform.mirror(orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, True, False))
bpy.ops.object.duplicate()
bpy.ops.transform.mirror(orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(True, False, False))
#bpy.ops.transform.translate(value=((frame_length+1.3)/2, 0, 4+3/2), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(True, False, False), mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, snap=False, snap_elements={'INCREMENT'}, use_snap_project=False, snap_target='CLOSEST', use_snap_self=True, use_snap_edit=True, use_snap_nonedit=True, use_snap_selectable=False)
#bpy.ops.transform.rotate(value=-0.3648610801294146, orient_axis='Y', orient_type='GLOBAL', orient_matrix=((0.99961, -0.0279216, 3.85335e-08), (0.00136394, 0.0488314, 0.998806), (-0.0278883, -0.998417, 0.0488505)), orient_matrix_type='VIEW', mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, snap=False, snap_elements={'INCREMENT'}, use_snap_project=False, snap_target='CLOSEST', use_snap_self=False, use_snap_edit=True, use_snap_nonedit=True, use_snap_selectable=False)


'''
bpy.ops.object.duplicate_move(OBJECT_OT_duplicate={"linked":False, "mode":'TRANSLATION'}, TRANSFORM_OT_translate={"value":(0, 0, 0), "orient_type":'GLOBAL', "orient_matrix":((0, 0, 0), (0, 0, 0), (0, 0, 0)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, False, False), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_elements":{'INCREMENT'}, "use_snap_project":False, "snap_target":'CLOSEST', "use_snap_self":True, "use_snap_edit":True, "use_snap_nonedit":True, "use_snap_selectable":False, "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "use_duplicated_keyframes":False, "view2d_edge_pan":False, "release_confirm":False, "use_accurate":False, "use_automerge_and_split":False})
bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')
bpy.ops.transform.mirror(orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(True, False, False))
'''



# End Caps
bpy.ops.mesh.primitive_circle_add(vertices=3, radius=(led_strip_width + 6*frame_rail_width)/sqrt(3)-0.01, enter_editmode=False, align='WORLD', location=(0, 0, 0), rotation=(0, 0, 0.523599), scale=(1, 1, 1))
bpy.ops.object.mode_set(mode = 'EDIT')
bpy.ops.mesh.edge_face_add()
bpy.ops.transform.resize(value=(1/3, 1, 1), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(True, True, True), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, snap=False, snap_elements={'INCREMENT'}, use_snap_project=False, snap_target='CLOSEST', use_snap_self=True, use_snap_edit=True, use_snap_nonedit=True, use_snap_selectable=False)

bpy.ops.object.mode_set(mode = 'OBJECT')

bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')
bpy.ops.transform.translate(value=((frame_length+1.3)/2-0.01, 0, 4+3/2+underwire_thickness), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(True, False, False), mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, snap=False, snap_elements={'INCREMENT'}, use_snap_project=False, snap_target='CLOSEST', use_snap_self=True, use_snap_edit=True, use_snap_nonedit=True, use_snap_selectable=False)


# NOTE: Angle is half the icosohedron dihedral angle
bpy.ops.transform.rotate(value=-0.3648610801294146, orient_axis='Y', orient_type='GLOBAL', orient_matrix=((0.99961, -0.0279216, 3.85335e-08), (0.00136394, 0.0488314, 0.998806), (-0.0278883, -0.998417, 0.0488505)), orient_matrix_type='VIEW', mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, snap=False, snap_elements={'INCREMENT'}, use_snap_project=False, snap_target='CLOSEST', use_snap_self=False, use_snap_edit=True, use_snap_nonedit=True, use_snap_selectable=False)

bpy.ops.object.modifier_add(type='SOLIDIFY')
bpy.context.object.modifiers["Solidify"].thickness = 3/cos(-0.3648610801294146)-0.01
bpy.ops.object.modifier_apply(modifier="Solidify")

bpy.context.object.name = "frame.outside.endcap"
bpy.ops.object.duplicate_move(OBJECT_OT_duplicate={"linked":False, "mode":'TRANSLATION'}, TRANSFORM_OT_translate={"value":(0, 0, 0), "orient_type":'GLOBAL', "orient_matrix":((0, 0, 0), (0, 0, 0), (0, 0, 0)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, False, False), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_elements":{'INCREMENT'}, "use_snap_project":False, "snap_target":'CLOSEST', "use_snap_self":True, "use_snap_edit":True, "use_snap_nonedit":True, "use_snap_selectable":False, "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "use_duplicated_keyframes":False, "view2d_edge_pan":False, "release_confirm":False, "use_accurate":False, "use_automerge_and_split":False})
bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')
bpy.ops.transform.mirror(orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(True, False, False))


# Frame Groove Sidewall chamfer
bpy.ops.mesh.primitive_cube_add(size=1, enter_editmode=False, align='WORLD', location=(0, 10, -10), scale=(frame_length+1.3, 20, 20))
bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')
bpy.ops.transform.rotate(value=pi/2-dihedral_angle_dodecahedron/2, orient_axis='X', orient_type='VIEW', orient_matrix=((4.93038e-32, 1, 2.22045e-16), (2.22045e-16, 4.93038e-32, 1), (1, 2.22045e-16, 4.93038e-32)), orient_matrix_type='VIEW', mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, snap=False, snap_elements={'INCREMENT'}, use_snap_project=False, snap_target='CLOSEST', use_snap_self=True, use_snap_edit=True, use_snap_nonedit=True, use_snap_selectable=False)
bpy.ops.transform.translate(value=(0, sin(pi/2-dihedral_angle_dodecahedron/2)*(acrylic_thickness+acrylic_tolerance+frame_thickness), cos(pi/2-dihedral_angle_dodecahedron/2)*(acrylic_thickness+acrylic_tolerance+frame_thickness)), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, False, True), mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, snap=False, snap_elements={'INCREMENT'}, use_snap_project=False, snap_target='CLOSEST', use_snap_self=True, use_snap_edit=True, use_snap_nonedit=True, use_snap_selectable=False)
bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')
bpy.context.object.name = "frame.outside.chamfer"


# Sidewalls that constrain the frame rails
bpy.ops.mesh.primitive_cube_add(size=1, enter_editmode=False, align='WORLD', location=(0, (-3*frame_rail_width + led_strip_width + 6*frame_rail_width)/2 , -frame_sidewall_height/2 + led_strip_height + frame_outer_bottom_thickness), scale=(2*tan(0.3648610801294146)*(frame_outer_bottom_thickness + led_strip_height)+LED_length*(LED_length/(2*tan(2*pi/10)) + XXX)/(LED_length/(2*tan(2*pi/10))), 3*frame_rail_width, frame_sidewall_height))
bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')
bpy.context.object.name = "frame.outside.sidewall"

bpy.ops.object.modifier_add(type='BOOLEAN')
bpy.context.object.modifiers["Boolean"].object = bpy.data.objects["frame.outside.chamfer"]
bpy.ops.object.modifier_apply(modifier="Boolean")


bpy.ops.object.duplicate()
bpy.ops.transform.mirror(orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, True, False))


# Connection Rail Negative for frame.inner
bpy.ops.mesh.primitive_cube_add(size=1, enter_editmode=False, align='WORLD', location=(0, led_strip_width/2+ 3*(frame_rail_width + 0.2)/2, -10/2 + led_strip_height + frame_outer_bottom_thickness/3), scale=(frame_length+1.3, frame_rail_width + 0.2, 10))
bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')
bpy.context.object.name = "frame.outside.rail_channel"
bpy.ops.object.duplicate()
bpy.ops.transform.mirror(orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, True, False))




# Wire Channel Under LED Strip
bpy.ops.mesh.primitive_cube_add(size=1, enter_editmode=False, align='WORLD', location=(0, 0, 2.5 - .5 + underwire_thickness), scale=(2*tan(0.3648610801294146)*(frame_outer_bottom_thickness + led_strip_height)+LED_length*(LED_length/(2*tan(2*pi/10)) + XXX)/(LED_length/(2*tan(2*pi/10))), 2*underwire_thickness, 2*underwire_thickness))
bpy.context.object.name = "frame.outside.wire_channel"


bpy.ops.mesh.primitive_cube_add(size=1, enter_editmode=False, align='WORLD', location=(0, frame_height/2, (2*frame_thickness+acrylic_thickness)/2-acrylic_tolerance), scale=(frame_length + 5*frame_thickness*tan(pi/5), frame_height, 2*frame_thickness+acrylic_thickness))
bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
bpy.ops.transform.translate(value=(0, led_acrylic_gap/2, -led_acrylic_gap*tan(dihedral_angle_dodecahedron/2)/2+frame_thickness/(tan(dihedral_angle_dodecahedron/2))))
bpy.ops.transform.rotate(value=pi/2-dihedral_angle_dodecahedron/2, orient_axis='X')
bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')
bpy.context.object.name = "diffuser.groove_negative.001"
bpy.ops.object.duplicate()
bpy.ops.transform.mirror(orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, True, False))

bpy.ops.mesh.primitive_cube_add(size=1, enter_editmode=False, align='WORLD', location=(0, -frame_height/2 - 0.4, (2*frame_thickness+acrylic_thickness)/2-acrylic_tolerance), scale=(frame_length + 5*frame_thickness*tan(pi/5), frame_height, 2*frame_thickness+acrylic_thickness))
bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
bpy.ops.transform.translate(value=(0, led_acrylic_gap/2, -led_acrylic_gap*tan(dihedral_angle_dodecahedron/2)/2+frame_thickness/(tan(dihedral_angle_dodecahedron/2))))
bpy.ops.transform.rotate(value=pi/2-dihedral_angle_dodecahedron/2, orient_axis='X')
bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')
bpy.context.object.name = "diffuser.groove_negative.003"
bpy.ops.object.duplicate()
bpy.ops.transform.mirror(orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, True, False))



bpy.ops.mesh.primitive_cube_add(size=1, enter_editmode=False, align='WORLD', location=(0, 0, -2), scale=(2*tan(0.3648610801294146)*(frame_outer_bottom_thickness + led_strip_height)+LED_length*(LED_length/(2*tan(2*pi/10)) + XXX)/(LED_length/(2*tan(2*pi/10))), led_acrylic_gap-.8 , 3))
bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
bpy.context.object.name = "diffuser.middle_negative"

bpy.ops.mesh.primitive_cube_add(size=1, enter_editmode=False, align='WORLD', location=(0, 0, -2.3), scale=(2*tan(0.3648610801294146)*(frame_outer_bottom_thickness + led_strip_height)+LED_length*(LED_length/(2*tan(2*pi/10)) + XXX)/(LED_length/(2*tan(2*pi/10))), led_strip_width , 3))
bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
bpy.context.object.name = "diffuser"


bpy.ops.object.modifier_add(type='BOOLEAN')
bpy.context.object.modifiers["Boolean"].object = bpy.data.objects["diffuser.middle_negative"]
bpy.ops.object.modifier_apply(modifier="Boolean")

bpy.ops.object.modifier_add(type='BOOLEAN')
bpy.context.object.modifiers["Boolean"].object = bpy.data.objects["diffuser.groove_negative.001"]
bpy.ops.object.modifier_apply(modifier="Boolean")

bpy.ops.object.modifier_add(type='BOOLEAN')
bpy.context.object.modifiers["Boolean"].object = bpy.data.objects["diffuser.groove_negative.002"]
bpy.ops.object.modifier_apply(modifier="Boolean")

bpy.ops.object.modifier_add(type='BOOLEAN')
bpy.context.object.modifiers["Boolean"].object = bpy.data.objects["diffuser.groove_negative.003"]
bpy.ops.object.modifier_apply(modifier="Boolean")

bpy.ops.object.modifier_add(type='BOOLEAN')
bpy.context.object.modifiers["Boolean"].object = bpy.data.objects["diffuser.groove_negative.004"]
bpy.ops.object.modifier_apply(modifier="Boolean")

bpy.ops.object.modifier_add(type='BOOLEAN')
bpy.context.object.modifiers["Boolean"].object = bpy.data.objects["frame.outside.vertex_chamfer.001"]
bpy.ops.object.modifier_apply(modifier="Boolean")

bpy.ops.object.modifier_add(type='BOOLEAN')
bpy.context.object.modifiers["Boolean"].object = bpy.data.objects["frame.outside.vertex_chamfer.002"]
bpy.ops.object.modifier_apply(modifier="Boolean")

bpy.ops.object.modifier_add(type='BOOLEAN')
bpy.context.object.modifiers["Boolean"].object = bpy.data.objects["frame.outside.vertex_chamfer.003"]
bpy.ops.object.modifier_apply(modifier="Boolean")

bpy.ops.object.modifier_add(type='BOOLEAN')
bpy.context.object.modifiers["Boolean"].object = bpy.data.objects["frame.outside.vertex_chamfer.004"]
bpy.ops.object.modifier_apply(modifier="Boolean")









# Primary Body for frame.outside
#not sure if the angle is correct below.  using icosohedron dihedral angle (dual shape of dodecahedron)
bpy.ops.mesh.primitive_cube_add(size=1, enter_editmode=False, align='WORLD', location=(0, 0, frame_outer_bottom_thickness/2 + led_strip_height), scale=(2*tan(0.3648610801294146)*(frame_outer_bottom_thickness + led_strip_height)+LED_length*(LED_length/(2*tan(2*pi/10)) + XXX)/(LED_length/(2*tan(2*pi/10))), led_strip_width + 6*frame_rail_width, frame_outer_bottom_thickness))
bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
bpy.context.object.name = "frame.outside"





bpy.ops.object.modifier_add(type='BOOLEAN')
bpy.context.object.modifiers["Boolean"].object = bpy.data.objects["frame.outside.sidewall"]
bpy.context.object.modifiers["Boolean"].operation = 'UNION'
bpy.ops.object.modifier_apply(modifier="Boolean")

bpy.ops.object.modifier_add(type='BOOLEAN')
bpy.context.object.modifiers["Boolean"].object = bpy.data.objects["frame.outside.sidewall.001"]
bpy.context.object.modifiers["Boolean"].operation = 'UNION'
bpy.ops.object.modifier_apply(modifier="Boolean")

bpy.ops.object.modifier_add(type='BOOLEAN')
bpy.context.object.modifiers["Boolean"].object = bpy.data.objects["frame.outside.vertex_chamfer.001"]
bpy.ops.object.modifier_apply(modifier="Boolean")

bpy.ops.object.modifier_add(type='BOOLEAN')
bpy.context.object.modifiers["Boolean"].object = bpy.data.objects["frame.outside.vertex_chamfer.002"]
bpy.ops.object.modifier_apply(modifier="Boolean")

bpy.ops.object.modifier_add(type='BOOLEAN')
bpy.context.object.modifiers["Boolean"].object = bpy.data.objects["frame.outside.vertex_chamfer.003"]
bpy.ops.object.modifier_apply(modifier="Boolean")

bpy.ops.object.modifier_add(type='BOOLEAN')
bpy.context.object.modifiers["Boolean"].object = bpy.data.objects["frame.outside.vertex_chamfer.004"]
bpy.ops.object.modifier_apply(modifier="Boolean")

'''
bpy.ops.object.modifier_add(type='BOOLEAN')
bpy.context.object.modifiers["Boolean"].object = bpy.data.objects["frame.outside.endcap"]
bpy.context.object.modifiers["Boolean"].operation = 'UNION'
bpy.ops.object.modifier_apply(modifier="Boolean")

bpy.ops.object.modifier_add(type='BOOLEAN')
bpy.context.object.modifiers["Boolean"].object = bpy.data.objects["frame.outside.endcap.001"]
bpy.context.object.modifiers["Boolean"].operation = 'UNION'
bpy.ops.object.modifier_apply(modifier="Boolean")
'''

bpy.ops.object.modifier_add(type='BOOLEAN')
bpy.context.object.modifiers["Boolean"].object = bpy.data.objects["frame.outside.rail_channel"]
bpy.ops.object.modifier_apply(modifier="Boolean")

bpy.ops.object.modifier_add(type='BOOLEAN')
bpy.context.object.modifiers["Boolean"].object = bpy.data.objects["frame.outside.rail_channel.001"]
bpy.ops.object.modifier_apply(modifier="Boolean")

bpy.ops.object.modifier_add(type='BOOLEAN')
bpy.context.object.modifiers["Boolean"].object = bpy.data.objects["frame.outside.wire_channel"]
bpy.ops.object.modifier_apply(modifier="Boolean")




#############
#  Diffuser ?
############


bpy.ops.object.modifier_add(type='BOOLEAN')
bpy.context.object.modifiers["Boolean"].object = bpy.data.objects["diffuser"]
bpy.context.object.modifiers["Boolean"].operation = 'UNION'
bpy.ops.object.modifier_apply(modifier="Boolean")


bpy.ops.object.select_all(action='DESELECT')

bpy.context.view_layer.objects.active = bpy.data.objects['frame.outside.vertex_chamfer.001']
bpy.data.objects['frame.outside.vertex_chamfer.001'].select_set(True)
bpy.data.objects['frame.outside.vertex_chamfer.002'].select_set(True)
bpy.data.objects['frame.outside.vertex_chamfer.003'].select_set(True)
bpy.data.objects['frame.outside.vertex_chamfer.004'].select_set(True)
bpy.data.objects['frame.outside.sidewall'].select_set(True)
bpy.data.objects['frame.outside.sidewall.001'].select_set(True)
bpy.data.objects['frame.outside.chamfer'].select_set(True)
bpy.data.objects['frame.outside.rail_channel'].select_set(True)
bpy.data.objects['frame.outside.rail_channel.001'].select_set(True)
bpy.data.objects['frame.outside.wire_channel'].select_set(True)
bpy.data.objects['frame.outside.endcap'].select_set(True)
bpy.data.objects['frame.outside.endcap.001'].select_set(True)
bpy.ops.object.delete(use_global=False)



#############
# Wire Holes
#############

bpy.ops.mesh.primitive_cylinder_add(vertices=32, radius=7.5, depth=50, enter_editmode=False, align='WORLD', location=(0.5*(2*tan(0.3648610801294146)*(frame_outer_bottom_thickness + led_strip_height)+LED_length*(LED_length/(2*tan(2*pi/10)) + XXX)/(LED_length/(2*tan(2*pi/10)))), 0, frame_outer_bottom_thickness + led_strip_height), scale=(1, 1, 1))
bpy.ops.transform.rotate(value=-0.3648610801294146, orient_axis='Y', orient_type='GLOBAL', orient_matrix=((1, -0, -0), (-0, -1.34359e-07, 1), (-0, -1, -1.34359e-07)), orient_matrix_type='VIEW', mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, snap=False, snap_elements={'INCREMENT'}, use_snap_project=False, snap_target='CLOSEST', use_snap_self=False, use_snap_edit=True, use_snap_nonedit=True, use_snap_selectable=False)
bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')
bpy.context.object.name = "frame.outside.wire_hole.001"

bpy.ops.object.select_all(action='DESELECT')

bpy.context.view_layer.objects.active = bpy.data.objects['frame.outside']

bpy.ops.object.modifier_add(type='BOOLEAN')
bpy.context.object.modifiers["Boolean"].object = bpy.data.objects["frame.outside.wire_hole.001"]
bpy.ops.object.modifier_apply(modifier="Boolean")



##############################
## frame.outside Placement  ##
##############################


bpy.context.view_layer.objects.active = bpy.data.objects['Dodecahedron_LED']
bpy.data.objects['Dodecahedron_LED'].select_set(True)

bpy.ops.object.mode_set(mode = 'EDIT')
bpy.ops.mesh.select_all(action='DESELECT')

edge_piece_locations = []
grid_mesh = bmesh.from_edit_mesh(bpy.context.object.data)

grid_mesh.faces.ensure_lookup_table()


for edge in grid_mesh.edges:
    edge.select = True

    edge_piece_locations.append([
                                 (edge.verts[1].co + edge.verts[0].co)/2,
                                 (edge.verts[1].co - edge.verts[0].co)])
bpy.ops.object.mode_set(mode = 'OBJECT')



for frame in edge_piece_locations:    
        
    bpy.ops.object.add_named(name = "frame.outside")
    bpy.ops.transform.translate(value=frame[0], orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, snap=False, snap_elements={'INCREMENT'}, use_snap_project=False, snap_target='CLOSEST', use_snap_self=True, use_snap_edit=True, use_snap_nonedit=True, use_snap_selectable=False)
    
    bpy.data.collections['OUTER'].objects.link(bpy.context.selected_objects[-1])
    bpy.context.collection.objects.unlink(bpy.context.selected_objects[-1])
    
    local_z = frame[0].normalized()
    if local_z.length == 0:
        local_z = mathutils.Vector((0, 0, 1, 0))
    
    local_x = frame[1].normalized()
    if local_x.length == 0:
        local_x = mathutils.Vector((1, 0, 0, 0))
        
    local_y = local_z.cross(local_x).normalized()
    if local_y.length == 0:
        local_y = mathutils.Vector((0, 1, 0, 0))

    
    local_axis = mathutils.Matrix([local_x, -local_y, local_z])
    
    #bpy.context.object.rotation_mode = 'QUATERNION'
    #bpy.context.object.rotation_quaternion = local_x.to_track_quat('X','Y')
    
    
    rotation  = mathutils.Vector((1,0,0)).rotation_difference(local_x)
    
    bpy.context.object.rotation_mode = 'QUATERNION'
    bpy.context.object.rotation_quaternion = bpy.context.object.matrix_world.to_quaternion() @ rotation
    
    
    bpy.context.object.rotation_mode = 'XYZ'
    

    
    rot_local_x = local_y.angle(mathutils.Vector(bpy.context.object.rotation_euler.to_matrix() @ mathutils.Vector((1.0, 0.0, 0.0))))
    rot_local_y = local_y.angle(mathutils.Vector(bpy.context.object.rotation_euler.to_matrix() @ mathutils.Vector((0.0, 1.0, 0.0))))
    rot_local_z = local_z.angle(mathutils.Vector(bpy.context.object.rotation_euler.to_matrix() @ mathutils.Vector((0.0, 0.0, 1.0))))
    
    #print(bpy.context.object.name, mathutils.Vector(bpy.context.object.rotation_euler.to_matrix() @ mathutils.Vector((1.0, 0.0, 0.0))).dot(local_x))
    #print(bpy.context.object.name, mathutils.Vector(bpy.context.object.rotation_euler.to_matrix() @ mathutils.Vector((0.0, 1.0, 0.0))).dot(local_z))
    #print(bpy.context.object.name, mathutils.Vector(bpy.context.object.rotation_euler.to_matrix() @ mathutils.Vector((0.0, 0.0, 1.0))).dot(local_z))
    
    if mathutils.Vector(bpy.context.object.rotation_euler.to_matrix() @ mathutils.Vector((0.0, 1.0, 0.0))).dot(local_z) < 0:
        rot_local_z = -rot_local_z

    bpy.ops.transform.rotate(value=(rot_local_z), orient_axis='X', orient_type='LOCAL')
    
    #bpy.context.scene.cursor.location = bpy.context.object.location
    #bpy.context.scene.cursor.rotation_euler = bpy.context.object.rotation_euler

bpy.ops.object.mode_set(mode = 'OBJECT')
    
bpy.ops.object.select_all(action='DESELECT')