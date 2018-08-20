#
# Copyright 2018 rn9dfj3
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import bpy
import bmesh
import bgl
import blf
import math
import bpy_extras.view3d_utils
from bpy.props import IntProperty, BoolProperty, PointerProperty, FloatProperty, CollectionProperty, FloatVectorProperty, EnumProperty


bl_info = {
    "name": "Quicker",
    "author": "rn9dfj3",
    "version": (0, 0),
    "blender": (2, 79, 0),
    "location": "3D View > Object Mode > Tools > Create",
    "description": "Draw curve quick!",
    "warning": "",
    "support": "COMMUNITY",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Add Curve"
}
PI = math.pi
PI_H = PI * 0.5
PEN = "pen"
STAR = "star"
RECT = "rect"
CIRCLE = "circle"

def draw_pen_px(self, context):
    if len(self.strokes)<1:
        return
        
    bgl.glEnable(bgl.GL_BLEND)
    
    width = context.scene.quicker_props.bevel_depth
    rad = 5 * context.scene.tool_settings.curve_paint_settings.radius_max * width * 10
    sqr = rad * math.sqrt(2)*0.5
    pre = [stroke for stroke in self.strokes]
    a = []
    a.append(self.strokes[0])
    a.extend(pre)
    pre = a
    
    bgl.glLineWidth(1)    
    bgl.glColor4f(0.75, 0.75, 0.75, 1.0)    

    bgl.glBegin(bgl.GL_LINE_STRIP)    
    for n, stroke in enumerate(self.strokes):# Size line
        x, y = stroke["mouse"]
        pres = stroke["pressure"]        
        p = pre[n]
        px, py = p["mouse"]
        ang = math.atan2(y -py, x - px)
        pos = ang + PI_H
                
        x = x + math.cos(pos) * rad * pres
        y = y + math.sin(pos) * rad * pres
        bgl.glVertex2i(int(x), int(y))        
    bgl.glEnd()
    
    bgl.glBegin(bgl.GL_LINE_STRIP)    
    for n, stroke in enumerate(self.strokes):# Size line
        x, y = stroke["mouse"]
        pres = stroke["pressure"]        
        p = pre[n]
        px, py = p["mouse"]
        ang = math.atan2(y -py, x - px)
        neg = ang - PI_H
                
        x = x + math.cos(neg) * rad * pres
        y = y + math.sin(neg) * rad * pres
        bgl.glVertex2i(int(x), int(y))        
    bgl.glEnd()

    # restore opengl defaults
    bgl.glLineWidth(1)
    bgl.glDisable(bgl.GL_BLEND)
    bgl.glColor4f(0.0, 0.0, 0.0, 1.0)

def draw_star_px(self, context):
    if len(self.strokes)<2:
        return
        
    bgl.glEnable(bgl.GL_BLEND)
    
    #width = context.scene.quicker_props.bevel_depth
    #rad = 5 * context.scene.tool_settings.curve_paint_settings.radius_max * width * 10
    #sqr = rad * math.sqrt(2)*0.5
    #pre = [stroke for stroke in self.strokes]
    #a = []
    #a.append(self.strokes[0])
    #a.extend(pre)
    #pre = a
    
    bgl.glLineWidth(1)    
    bgl.glColor4f(0.75, 0.75, 0.75, 1.0)    

    bgl.glBegin(bgl.GL_LINE_STRIP)
    sx, sy = self.strokes[0]["mouse"]
    ex, ey = self.strokes[-1]["mouse"]
    o = math.atan2(ey-sy, ex-sx)
    
    m = 5.0
    for n in range(int(m)+1):
        ang = 2 * PI/m * n
        #bgl.glVertex2i(int(sx), int(sy))
        #ex, ey = self.strokes[-1]["mouse"]                                
        rad = math.sqrt((ex-sx) ** 2 + (ey-sy) ** 2)
        x = rad * math.cos(ang + o) + sx
        y = rad * math.sin(ang + o) + sy        
        bgl.glVertex2i(int(x), int(y))
    bgl.glEnd()
    

    # restore opengl defaults
    bgl.glLineWidth(1)
    bgl.glDisable(bgl.GL_BLEND)
    bgl.glColor4f(0.0, 0.0, 0.0, 1.0)
    
def draw_rect_px(self, context):
    if len(self.strokes)<2:
        return
        
    bgl.glEnable(bgl.GL_BLEND)
    
    #width = context.scene.quicker_props.bevel_depth
    #rad = 5 * context.scene.tool_settings.curve_paint_settings.radius_max * width * 10
    #sqr = rad * math.sqrt(2)*0.5
    #pre = [stroke for stroke in self.strokes]
    #a = []
    #a.append(self.strokes[0])
    #a.extend(pre)
    #pre = a
    
    bgl.glLineWidth(1)    
    bgl.glColor4f(0.75, 0.75, 0.75, 1.0)    

    bgl.glBegin(bgl.GL_LINE_STRIP)
    sx, sy = self.strokes[0]["mouse"]
    ex, ey = self.strokes[-1]["mouse"]
#    o = math.atan2(ey-sy, ex-sx)
#    
#    m = 5.0
#    for n in range(int(m)+1):
#        ang = 2 * PI/m * n
#        #bgl.glVertex2i(int(sx), int(sy))
#        #ex, ey = self.strokes[-1]["mouse"]                                
#        rad = math.sqrt((ex-sx) ** 2 + (ey-sy) ** 2)
#        x = rad * math.cos(ang + o) + sx
#        y = rad * math.sin(ang + o) + sy        
#        bgl.glVertex2i(int(x), int(y))
    bgl.glVertex2i(int(sx), int(sy))
    bgl.glVertex2i(int(sx), int(ey))
    bgl.glVertex2i(int(ex), int(ey))
    bgl.glVertex2i(int(ex), int(sy))
    bgl.glVertex2i(int(sx), int(sy))
        
#        mouse = (sx, sy)
#        loc = bpy_extras.view3d_utils.region_2d_to_location_3d(context.region, context.space_data.region_3d, mouse, self.cursor)
#        strokes.append({"name":"", "location":loc, "mouse":mouse, "pressure":1, "pen_flip":False, "time":0, "is_start":False, "size":0})            
#        mouse = (sx, ey)
#        loc = bpy_extras.view3d_utils.region_2d_to_location_3d(context.region, context.space_data.region_3d, mouse, self.cursor)
#        strokes.append({"name":"", "location":loc, "mouse":mouse, "pressure":1, "pen_flip":False, "time":0, "is_start":False, "size":0})            
#        mouse = (ex, ey)
#        loc = bpy_extras.view3d_utils.region_2d_to_location_3d(context.region, context.space_data.region_3d, mouse, self.cursor)
#        strokes.append({"name":"", "location":loc, "mouse":mouse, "pressure":1, "pen_flip":False, "time":0, "is_start":False, "size":0})            
#        mouse = (ex, sy)
#        loc = bpy_extras.view3d_utils.region_2d_to_location_3d(context.region, context.space_data.region_3d, mouse, self.cursor)
#        strokes.append({"name":"", "location":loc, "mouse":mouse, "pressure":1, "pen_flip":False, "time":0, "is_start":False, "size":0})                    
    bgl.glEnd()
    

    # restore opengl defaults
    bgl.glLineWidth(1)
    bgl.glDisable(bgl.GL_BLEND)
    bgl.glColor4f(0.0, 0.0, 0.0, 1.0)
    
class QuickerProps(bpy.types.PropertyGroup):
    running = BoolProperty(options={'HIDDEN'})
    #def get_mode():
    #    return [("pen","Pen","Use Pen", "GREASEPENCIL"), ("basic","Basic","Make Basic shape", "LINE_DATA")]
    #mode = EnumProperty(get_mode())
    mode_items = [
        (PEN, "Pen", "Freehand pen","GREASEPENCIL", 0),
        (STAR, "Star", "Star","SOLO_ON", 1),
        (RECT, "Rect", "Rectangle","MESH_PLANE", 2),
        (CIRCLE, "Circle", "Circle","MESH_CIRCLE", 3)



        #("camera", "Camera", "Camera","CAMERA_DATA", 2)
    ]
    mode = EnumProperty(items=mode_items, name="", description="Draw mode", default="pen")
    color = FloatVectorProperty(name="Color", description="Color of curve", subtype='COLOR', min=0.0, max=1.0, default=(0.8, 0.8, 0.8))
    bevel_depth = FloatProperty(name = "Width", description="Width of curve", min=0.0, default=0.1, unit="LENGTH")
    #curve = PointerProperty(type=bpy.types.CurveMapping, name="Curve")
    #def brush_items(self, context):
    #    if not "Quicker" in bpy.data.brushes.keys():
    #        bpy.data.brushes.new("Quicker")
    #    #brush = bpy.context.blend_data.brushes["Quicker"]
    #    return [("Quicker", "Quicker", "Brush for Quicker")]    
    #brush = EnumProperty(items=brush_items)
    fill = BoolProperty(name="Fill", description="Whether curve is fill or not")
    star_num = IntProperty(name="Number", description="Corner number of star", min=2, default=5)        
    star_depth = FloatProperty(name = "Depth", description="Corner depth of star", min=0.0, default=0.5, max=1.0, subtype="FACTOR")
    pen_smooth = FloatProperty(name="Smooth", description="How smooth curve is", default=0.1, min=0.0, max=10.0)
    shadeless = BoolProperty(name="Shadelss", description="Whether curve have shadelss material or not", default=True)
    
class DrawCurve(bpy.types.Operator):

    bl_idname = "curve.quicker_draw_curve"
    bl_label = "Draw Curve Object"
    bl_description = "Draw Curve Object"
    bl_options = {'REGISTER', 'UNDO'}
    #strokes = CollectionProperty(type=bpy.types.OperatorStrokeElement, options={'HIDDEN'})
    cursor = FloatVectorProperty(options={'HIDDEN'})
    #running = BoolProperty(options={'HIDDEN'})
    #f = FloatProperty(name="Smooth", default=0.1, min=0.0, options={'HIDDEN'})
#    smooth = FloatProperty(name="Smooth", default=0.1, min=0.0, options={'HIDDEN'})
    mani = BoolProperty(options={'HIDDEN'})
    outline = BoolProperty(options={'HIDDEN'})
    
    strokes = []
    _handle = None
    #mouses = []
    
    def execute(self, context):
        props = context.scene.quicker_props

        #context.object.location.x = self.value / 100.0
        #strokes = [{"name":stroke.name, "location":stroke.location, "mouse":stroke.mouse, "pressure":stroke.pressure, "pen_flip":stroke.pen_flip, "time":stroke.time, "is_start":stroke.is_start, "size":stroke.size} for stroke in self.strokes]
        #bpy.ops.curve.draw(error_threshold=self.smooth, fit_method='REFIT', corner_angle=1.22173, use_cyclic=False, stroke=strokes)
        #bpy.ops.object.editmode_toggle()
        if bpy.ops.object.mode_set.poll():        
            bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.curve.primitive_bezier_curve_add(enter_editmode=True, view_align=True)
        bpy.ops.curve.select_all(action='SELECT')
        bpy.ops.curve.delete(type='VERT')
        context.object.data.dimensions = '2D'
        if not props.fill:
            context.object.data.fill_mode = 'NONE'

        #context.object.data.fill_mode = 'NONE'
        context.object.data.bevel_depth = props.bevel_depth
        context.object.data.resolution_u = 24
        mat = bpy.data.materials.new('Material')
        context.object.data.materials.append(mat)
        mat.use_shadeless = props.shadeless
        mat.diffuse_color = props.color
        context.space_data.cursor_location = self.cursor
#                bpy.types.SpaceView3D.draw_handler_remove(self._handle, 'WINDOW')
        strokes = [{"name":"", "location":stroke["location"], "mouse":stroke["mouse"], "pressure":stroke["pressure"], "pen_flip":False, "time":0, "is_start":False, "size":0} for stroke in self.strokes]
        if bpy.ops.curve.draw.poll() and len(strokes)>0:
            #bpy.ops.curve.draw(error_threshold=self.smooth, fit_method='REFIT', corner_angle=1.22173, use_cyclic=False, stroke=strokes)
            bpy.ops.curve.draw(error_threshold=props.pen_smooth,stroke=strokes, use_cyclic=props.fill)            
#        bpy.ops.object.editmode_toggle()               
        self.strokes = []
#        if props.fill:
#            bpy.ops.curve.cyclic_toggle()
            
#        bpy.ops.curve.draw(error_threshold=0.0, use_cyclic=True, stroke=strokes)            
#        #bpy.context.scene.tool_settings.curve_paint_settings.curve_type = 'POLY'
        if props.fill and not bpy.context.scene.tool_settings.curve_paint_settings.curve_type == 'BEZIER':
            bpy.ops.curve.cyclic_toggle()

        if bpy.ops.object.editmode_toggle.poll():
            bpy.ops.object.editmode_toggle()               

        return {'FINISHED'}
    def finish_draw(self, context):
        props = context.scene.quicker_props
        bpy.types.SpaceView3D.draw_handler_remove(self._handle, 'WINDOW')
        context.space_data.show_manipulator = self.mani
        props.running = False                
        context.space_data.show_outline_selected = self.outline
    def add_draw(self, context, event):
        mouse = (event.mouse_region_x, event.mouse_region_y)
        loc = bpy_extras.view3d_utils.region_2d_to_location_3d(bpy.context.region, bpy.context.space_data.region_3d, mouse, self.cursor)
        #brush = bpy.context.blend_data.brushes[props.brush]
        ##layout.template_curve_mapping(brush, "curve")
        #for curve in brush.curve.curves:
        #    pres = curve.evaluate(event.pressure)
        #pres = max(0, min(pres, 1.0) )                
        stroke = {"mouse" : mouse, "pressure" : event.pressure, "location": loc}
        self.strokes.append(stroke)
    
    def modal(self, context, event):
        #props = context.scene.quicker_props
        context.area.tag_redraw()
        props = context.scene.quicker_props
        
        #if context.area.type:#Update render
#        self.report({"INFO"},context.region.type)       
#        if event.type == "LEFTMOUSE":
#            if props.running and event.value == 'RELEASE':
#                props.running = False
#        if event.type in ('RIGHTMOUSE', 'ESC') or not context.region.type == "WINDOW":
#            props.running = False
#            context.space_data.cursor_location = self.cursor
#            bpy.ops.object.editmode_toggle()
#            bpy.types.SpaceView3D.draw_handler_remove(self._handle, 'WINDOW')            
#            return {'CANCELLED'}
#        if not props.running:# Confirm            
#            context.space_data.cursor_location = self.cursor
#            bpy.types.SpaceView3D.draw_handler_remove(self._handle, 'WINDOW')
#            strokes = [{"name":stroke.name, "location":stroke.location, "mouse":stroke.mouse, "pressure":stroke.pressure, "pen_flip":stroke.pen_flip, "time":stroke.time, "is_start":stroke.is_start, "size":stroke.size} for stroke in self.strokes]
#            if bpy.ops.curve.draw.poll() and len(strokes)>0:
#                bpy.ops.curve.draw(error_threshold=self.smooth, fit_method='REFIT', corner_angle=1.22173, use_cyclic=False, stroke=strokes)
#            bpy.ops.object.editmode_toggle()               
#            return self.execute(context)
#            return {'FINISHED'}
        if event.type in ("LEFTMOUSE", "RIGHTMOUSE", "MIDDLEMOUSE"):
            x = event.mouse_region_x
            y = event.mouse_region_y
            w = context.region.width
            h = context.region.height
            if event.value == 'PRESS' and (x < 0 or w < x or y < 0 or h <y):                
                #bpy.types.SpaceView3D.draw_handler_remove(self._handle, 'WINDOW')
                #context.space_data.show_manipulator = self.mani
                #props.running = False
                self.finish_draw(context)
#                return {'CANCELLED'}
                return {'FINISHED'}            
        if event.type == "RIGHTMOUSE":
            if event.value == 'PRESS':
                #bpy.types.SpaceView3D.draw_handler_remove(self._handle, 'WINDOW')
                #props.running = False
                #context.space_data.show_manipulator = self.mani
                self.finish_draw(context)
                return {'FINISHED'}
        if event.type == "LEFTMOUSE":
            if event.value == 'PRESS':
                #if bpy.ops.object.mode_set.poll():
                self.add_draw(context, event)                
            if event.value == 'RELEASE':
                self.add_draw(context, event)                
                self.execute(context)
        if event.type == "MOUSEMOVE":# Draw stroke
            if event.value == 'PRESS' and not (event.ctrl or event.alt or event.shift):
                #stroke = self.strokes.add()
                #stroke.mouse = (event.mouse_region_x, event.mouse_region_y)
                #stroke.pressure = event.pressure
#                mouse = (event.mouse_region_x, event.mouse_region_y)
#                loc = bpy_extras.view3d_utils.region_2d_to_location_3d(bpy.context.region, bpy.context.space_data.region_3d, mouse, self.cursor)
                #brush = bpy.context.blend_data.brushes[props.brush]
                ##layout.template_curve_mapping(brush, "curve")
                #for curve in brush.curve.curves:
                #    pres = curve.evaluate(event.pressure)
                #pres = max(0, min(pres, 1.0) )                
#                stroke = {"mouse" : mouse, "pressure" : event.pressure, "location": loc}
#                self.strokes.append(stroke)
                self.add_draw(context, event)
        return {'PASS_THROUGH'}

    def invoke(self, context, event):
        props = context.scene.quicker_props
        if context.area.type == 'VIEW_3D' and not props.running:
#            context.scene.tool_settings.curve_paint_settings.use_pressure_radius = True          
            self.cursor = context.space_data.cursor_location
            args = (self, context)                   
            self._handle = bpy.types.SpaceView3D.draw_handler_add(draw_pen_px, args, 'WINDOW', 'POST_PIXEL')
            context.window_manager.modal_handler_add(self)                
            self.strokes = []
            props.running = True
            self.mani = context.space_data.show_manipulator
            context.space_data.show_manipulator = False
            self.outline = context.space_data.show_outline_selected
            context.space_data.show_outline_selected = False
            
#            if bpy.ops.object.mode_set.poll():
#                bpy.ops.object.mode_set(mode='OBJECT')
#            context.scene.tool_settings.curve_paint_settings.use_pressure_radius = True
#      
#            bpy.ops.curve.primitive_bezier_curve_add(enter_editmode=True)
#            bpy.ops.curve.select_all(action='SELECT')
#            bpy.ops.curve.delete(type='VERT')
#            context.object.data.dimensions = '2D'
#            context.object.data.fill_mode = 'NONE'
#            context.object.data.bevel_depth = 0.1
#            mat = bpy.data.materials.new('Material')
#            context.object.data.materials.append(mat)
#            mat.use_shadeless = True
#            mat.diffuse_color = (0, 0, 0)
#            self.camera = context.space_data.region_3d.lock_rotation                
#            self.cursor = context.space_data.cursor_location
#            props.running = True
#            args = (self, context)                   
#            self._handle = bpy.types.SpaceView3D.draw_handler_add(draw_callback_px, args, 'WINDOW', 'POST_PIXEL')
#            context.window_manager.modal_handler_add(self)                
            return {'RUNNING_MODAL'}            
#            if not props.running:
#            else:
#                props.running = False
#                return {'FINISHED'}
        else:            
            #props.running = False            
#            return {'FINISHED'}
            #print("Canceld")
            return {'CANCELLED'}

class DrawStar(bpy.types.Operator):
    bl_idname = "curve.quicker_draw_star"
    bl_label = "Draw Star Object"
    bl_description = "Draw Star Object"
    bl_options = {'REGISTER', 'UNDO'}
    cursor = FloatVectorProperty(options={'HIDDEN'})
    smooth = FloatProperty(name="Smooth", default=0.1, min=0.0, options={'HIDDEN'})
    mani = BoolProperty(options={'HIDDEN'})
    outline = BoolProperty(options={'HIDDEN'})    
    strokes = []
    
    _handle = None
    
    def execute(self, context):
        props = context.scene.quicker_props
        if bpy.ops.object.mode_set.poll():        
            bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.curve.primitive_bezier_curve_add(enter_editmode=True, view_align=True)
        bpy.ops.curve.select_all(action='SELECT')
        bpy.ops.curve.delete(type='VERT')
        context.object.data.dimensions = '2D'
        context.object.data.bevel_depth = props.bevel_depth
        context.object.data.resolution_u = 24
        if not props.fill:
            context.object.data.fill_mode = 'NONE'
        mat = bpy.data.materials.new('Material')
        context.object.data.materials.append(mat)
        mat.use_shadeless = props.shadeless
        mat.diffuse_color = props.color
        context.space_data.cursor_location = self.cursor
        
        sx, sy = self.strokes[0]["mouse"]
        ex, ey = self.strokes[-1]["mouse"]
        o = math.atan2(ey-sy, ex-sx)
                
        m = props.star_num
        d = props.star_depth
        strokes = []
        for n in range(int(m)):
            ang = 2 * PI/m * n
            bet = 2 * PI/m * (n+0.5)
            
            #bgl.glVertex2i(int(sx), int(sy))
            #ex, ey = self.strokes[-1]["mouse"]                                
            rad = math.sqrt((ex-sx) ** 2 + (ey-sy) ** 2)
            x = rad * math.cos(ang + o) + sx
            y = rad * math.sin(ang + o) + sy        
            #bgl.glVertex2i(int(x), int(y))
            mouse = (x, y)
            loc = bpy_extras.view3d_utils.region_2d_to_location_3d(context.region, context.space_data.region_3d, mouse, self.cursor)
            strokes.append({"name":"", "location":loc, "mouse":mouse, "pressure":1, "pen_flip":False, "time":0, "is_start":False, "size":0})            
            
            x = d * rad * math.cos(bet + o) + sx
            y = d * rad * math.sin(bet + o) + sy        
            #bgl.glVertex2i(int(x), int(y))
            mouse = (x, y)
            loc = bpy_extras.view3d_utils.region_2d_to_location_3d(context.region, context.space_data.region_3d, mouse, self.cursor)
            strokes.append({"name":"", "location":loc, "mouse":mouse, "pressure":1, "pen_flip":False, "time":0, "is_start":False, "size":0})            

        #strokes = [{"name":"", "location":stroke["location"], "mouse":stroke["mouse"], "pressure":stroke["pressure"], "pen_flip":False, "time":0, "is_start":False, "size":0} for stroke in self.strokes]
        if bpy.ops.curve.draw.poll() and len(strokes)>0:
            #bpy.ops.curve.draw(error_threshold=0.0, fit_method='REFIT', corner_angle=1.22173, use_cyclic=True, stroke=strokes)
            bpy.ops.curve.draw(error_threshold=0.0, use_cyclic=True, stroke=strokes)            
            #bpy.context.scene.tool_settings.curve_paint_settings.curve_type = 'POLY'
            if not bpy.context.scene.tool_settings.curve_paint_settings.curve_type == 'BEZIER':
                bpy.ops.curve.cyclic_toggle()
        #bpy.ops.curve.cyclic_toggle()

        self.strokes = []
        #if props.fill:
        if bpy.ops.object.editmode_toggle.poll():
            bpy.ops.object.editmode_toggle()               

        return {'FINISHED'}
    def finish_draw(self, context):
        props = context.scene.quicker_props
        bpy.types.SpaceView3D.draw_handler_remove(self._handle, 'WINDOW')
        context.space_data.show_manipulator = self.mani
        props.running = False                
        context.space_data.show_outline_selected = self.outline
    def add_draw(self, context, event):
        mouse = (event.mouse_region_x, event.mouse_region_y)
        loc = bpy_extras.view3d_utils.region_2d_to_location_3d(context.region, context.space_data.region_3d, mouse, self.cursor)
        stroke = {"mouse" : mouse, "pressure" : event.pressure, "location": loc}
        self.strokes.append(stroke)
        
    def modal(self, context, event):
        context.area.tag_redraw()
        props = context.scene.quicker_props
        if event.type in ("LEFTMOUSE", "RIGHTMOUSE", "MIDDLEMOUSE"):
            x = event.mouse_region_x
            y = event.mouse_region_y
            w = context.region.width
            h = context.region.height
            if event.value == 'PRESS' and (x < 0 or w < x or y < 0 or h <y):                
                self.finish_draw(context)
                return {'FINISHED'}            
        if event.type == "RIGHTMOUSE":
            if event.value == 'PRESS':
                self.finish_draw(context)
                return {'FINISHED'}
        if event.type == "LEFTMOUSE":
            if event.value == 'PRESS':
                #pass
                self.add_draw(context, event)
            if event.value == 'RELEASE':
                #self.add_draw(context, event)
                self.execute(context)  
        if event.type == "MOUSEMOVE":# Draw stroke
            if event.value == 'PRESS' and not (event.ctrl or event.alt or event.shift):
                #mouse = (event.mouse_region_x, event.mouse_region_y)
                #loc = bpy_extras.view3d_utils.region_2d_to_location_3d(bpy.context.region, bpy.context.space_data.region_3d, mouse, self.cursor)
                #stroke = {"mouse" : mouse, "pressure" : event.pressure, "location": loc}
                #self.strokes.append(stroke)
                self.add_draw(context, event)
        return {'PASS_THROUGH'}

    def invoke(self, context, event):
        props = context.scene.quicker_props
        if context.area.type == 'VIEW_3D' and not props.running:
            context.scene.tool_settings.curve_paint_settings.use_pressure_radius = True          
            self.cursor = context.space_data.cursor_location
            args = (self, context)                   
            self._handle = bpy.types.SpaceView3D.draw_handler_add(draw_star_px, args, 'WINDOW', 'POST_PIXEL')
            context.window_manager.modal_handler_add(self)                
            self.strokes = []
            props.running = True
            self.mani = context.space_data.show_manipulator
            context.space_data.show_manipulator = False
            self.outline = context.space_data.show_outline_selected
            context.space_data.show_outline_selected = False
            return {'RUNNING_MODAL'}            
        else:            
            return {'CANCELLED'}

class DrawRect(bpy.types.Operator):
    bl_idname = "curve.quicker_draw_rect"
    bl_label = "Draw Rect Object"
    bl_description = "Draw Rectangle Object"
    bl_options = {'REGISTER', 'UNDO'}
    cursor = FloatVectorProperty(options={'HIDDEN'})
    smooth = FloatProperty(name="Smooth", default=0.1, min=0.0, options={'HIDDEN'})
    mani = BoolProperty(options={'HIDDEN'})
    outline = BoolProperty(options={'HIDDEN'})    
    strokes = []
    
    _handle = None
    
    def execute(self, context):
        props = context.scene.quicker_props
        if bpy.ops.object.mode_set.poll():        
            bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.curve.primitive_bezier_curve_add(enter_editmode=True, view_align=True)
        bpy.ops.curve.select_all(action='SELECT')
        bpy.ops.curve.delete(type='VERT')
        context.object.data.dimensions = '2D'
        context.object.data.bevel_depth = props.bevel_depth
        context.object.data.resolution_u = 24
        if not props.fill:
            context.object.data.fill_mode = 'NONE'
        mat = bpy.data.materials.new('Material')
        context.object.data.materials.append(mat)
        mat.use_shadeless = props.shadeless
        mat.diffuse_color = props.color
        context.space_data.cursor_location = self.cursor
        
        sx, sy = self.strokes[0]["mouse"]
        ex, ey = self.strokes[-1]["mouse"]
        o = math.atan2(ey-sy, ex-sx)
                
        m = props.star_num
        d = props.star_depth
        strokes = []
        
        mouse = (sx, sy)
        loc = bpy_extras.view3d_utils.region_2d_to_location_3d(context.region, context.space_data.region_3d, mouse, self.cursor)
        strokes.append({"name":"", "location":loc, "mouse":mouse, "pressure":1, "pen_flip":False, "time":0, "is_start":False, "size":0})            
        mouse = (sx, ey)
        loc = bpy_extras.view3d_utils.region_2d_to_location_3d(context.region, context.space_data.region_3d, mouse, self.cursor)
        strokes.append({"name":"", "location":loc, "mouse":mouse, "pressure":1, "pen_flip":False, "time":0, "is_start":False, "size":0})            
        mouse = (ex, ey)
        loc = bpy_extras.view3d_utils.region_2d_to_location_3d(context.region, context.space_data.region_3d, mouse, self.cursor)
        strokes.append({"name":"", "location":loc, "mouse":mouse, "pressure":1, "pen_flip":False, "time":0, "is_start":False, "size":0})            
        mouse = (ex, sy)
        loc = bpy_extras.view3d_utils.region_2d_to_location_3d(context.region, context.space_data.region_3d, mouse, self.cursor)
        strokes.append({"name":"", "location":loc, "mouse":mouse, "pressure":1, "pen_flip":False, "time":0, "is_start":False, "size":0})            
    
        #for n in range(int(m)):
        #    ang = 2 * PI/m * n
        #    bet = 2 * PI/m * (n+0.5)
        #    
        #    #bgl.glVertex2i(int(sx), int(sy))
        #    #ex, ey = self.strokes[-1]["mouse"]                                
        #    rad = math.sqrt((ex-sx) ** 2 + (ey-sy) ** 2)
        #    x = rad * math.cos(ang + o) + sx
        #    y = rad * math.sin(ang + o) + sy        
        #    #bgl.glVertex2i(int(x), int(y))
        #    mouse = (x, y)
        #    loc = bpy_extras.view3d_utils.region_2d_to_location_3d(context.region, context.space_data.region_3d, mouse, self.cursor)
        #    strokes.append({"name":"", "location":loc, "mouse":mouse, "pressure":1, "pen_flip":False, "time":0, "is_start":False, "size":0})            
        #    
        #    x = d * rad * math.cos(bet + o) + sx
        #    y = d * rad * math.sin(bet + o) + sy        
        #    #bgl.glVertex2i(int(x), int(y))
        #    mouse = (x, y)
        #    loc = bpy_extras.view3d_utils.region_2d_to_location_3d(context.region, context.space_data.region_3d, mouse, self.cursor)
        #    strokes.append({"name":"", "location":loc, "mouse":mouse, "pressure":1, "pen_flip":False, "time":0, "is_start":False, "size":0})            

        #strokes = [{"name":"", "location":stroke["location"], "mouse":stroke["mouse"], "pressure":stroke["pressure"], "pen_flip":False, "time":0, "is_start":False, "size":0} for stroke in self.strokes]
        if bpy.ops.curve.draw.poll() and len(strokes)>0:
            #bpy.ops.curve.draw(error_threshold=0.0, fit_method='REFIT', corner_angle=1.22173, use_cyclic=True, stroke=strokes)
            bpy.ops.curve.draw(error_threshold=0.0, use_cyclic=True, stroke=strokes)            
            #bpy.context.scene.tool_settings.curve_paint_settings.curve_type = 'POLY'
            if not bpy.context.scene.tool_settings.curve_paint_settings.curve_type == 'BEZIER':
                bpy.ops.curve.cyclic_toggle()
        #bpy.ops.curve.cyclic_toggle()

        self.strokes = []
        #if props.fill:
        if bpy.ops.object.editmode_toggle.poll():
            bpy.ops.object.editmode_toggle()               

        return {'FINISHED'}
    def finish_draw(self, context):
        props = context.scene.quicker_props
        bpy.types.SpaceView3D.draw_handler_remove(self._handle, 'WINDOW')
        context.space_data.show_manipulator = self.mani
        props.running = False                
        context.space_data.show_outline_selected = self.outline
    def add_draw(self, context, event):
        mouse = (event.mouse_region_x, event.mouse_region_y)
        loc = bpy_extras.view3d_utils.region_2d_to_location_3d(context.region, context.space_data.region_3d, mouse, self.cursor)
        stroke = {"mouse" : mouse, "pressure" : event.pressure, "location": loc}
        self.strokes.append(stroke)
        
    def modal(self, context, event):
        context.area.tag_redraw()
        props = context.scene.quicker_props
        if event.type in ("LEFTMOUSE", "RIGHTMOUSE", "MIDDLEMOUSE"):
            x = event.mouse_region_x
            y = event.mouse_region_y
            w = context.region.width
            h = context.region.height
            if event.value == 'PRESS' and (x < 0 or w < x or y < 0 or h <y):                
                self.finish_draw(context)
                return {'FINISHED'}            
        if event.type == "RIGHTMOUSE":
            if event.value == 'PRESS':
                self.finish_draw(context)
                return {'FINISHED'}
        if event.type == "LEFTMOUSE":
            if event.value == 'PRESS':
                #pass
                self.add_draw(context, event)
            if event.value == 'RELEASE':
                #self.add_draw(context, event)
                self.execute(context)  
        if event.type == "MOUSEMOVE":# Draw stroke
            if event.value == 'PRESS' and not (event.ctrl or event.alt or event.shift):
                #mouse = (event.mouse_region_x, event.mouse_region_y)
                #loc = bpy_extras.view3d_utils.region_2d_to_location_3d(bpy.context.region, bpy.context.space_data.region_3d, mouse, self.cursor)
                #stroke = {"mouse" : mouse, "pressure" : event.pressure, "location": loc}
                #self.strokes.append(stroke)
                self.add_draw(context, event)
        return {'PASS_THROUGH'}

    def invoke(self, context, event):
        props = context.scene.quicker_props
        if context.area.type == 'VIEW_3D' and not props.running:
            context.scene.tool_settings.curve_paint_settings.use_pressure_radius = True          
            self.cursor = context.space_data.cursor_location
            args = (self, context)                   
            self._handle = bpy.types.SpaceView3D.draw_handler_add(draw_rect_px, args, 'WINDOW', 'POST_PIXEL')
            context.window_manager.modal_handler_add(self)                
            self.strokes = []
            props.running = True
            self.mani = context.space_data.show_manipulator
            context.space_data.show_manipulator = False
            self.outline = context.space_data.show_outline_selected
            context.space_data.show_outline_selected = False
            return {'RUNNING_MODAL'}            
        else:            
            return {'CANCELLED'}

class DrawCircle(bpy.types.Operator):
    bl_idname = "curve.quicker_draw_circle"
    bl_label = "Draw Circle Object"
    bl_description = "Draw Circle Object"
    bl_options = {'REGISTER', 'UNDO'}
    cursor = FloatVectorProperty(options={'HIDDEN'})
    smooth = FloatProperty(name="Smooth", default=0.1, min=0.0, options={'HIDDEN'})
    mani = BoolProperty(options={'HIDDEN'})
    outline = BoolProperty(options={'HIDDEN'})    
    strokes = []
    
    _handle = None
    
    def execute(self, context):
        props = context.scene.quicker_props
        if bpy.ops.object.mode_set.poll():
            bpy.ops.object.mode_set(mode='OBJECT')
#        bpy.ops.curve.primitive_bezier_curve_add(enter_editmode=True, view_align=True)

        sx, sy = self.strokes[0]["mouse"]
        ex, ey = self.strokes[-1]["mouse"]
        mouse = (sx, sy)
        ori = bpy_extras.view3d_utils.region_2d_to_location_3d(context.region, context.space_data.region_3d, mouse, self.cursor)
        #strokes.append({"name":"", "location":loc, "mouse":mouse, "pressure":1, "pen_flip":False, "time":0, "is_start":False, "size":0})            
        
        #dis = mat.sqrt( (ex-sx)**2 + (ey-sy)**2 )
        mouse = (ex, ey)
        rad = bpy_extras.view3d_utils.region_2d_to_location_3d(context.region, context.space_data.region_3d, mouse, self.cursor)
        #(rad - ori).magnitude
        bpy.ops.curve.primitive_bezier_circle_add(radius=(rad - ori).magnitude, view_align=True, location=ori)
        #bpy.ops.curve.select_all(action='SELECT')
        #bpy.ops.curve.delete(type='VERT')
        context.object.data.dimensions = '2D'
        context.object.data.bevel_depth = props.bevel_depth
        context.object.data.resolution_u = 24
        if not props.fill:
            context.object.data.fill_mode = 'NONE'
        mat = bpy.data.materials.new('Material')
        context.object.data.materials.append(mat)
        mat.use_shadeless = props.shadeless
        mat.diffuse_color = props.color
        context.space_data.cursor_location = self.cursor
        
        #sx, sy = self.strokes[0]["mouse"]
        #ex, ey = self.strokes[-1]["mouse"]
        #o = math.atan2(ey-sy, ex-sx)
        #        
        #m = props.star_num
        #d = props.star_depth
        #strokes = []
        #
        #mouse = (sx, sy)
        #loc = bpy_extras.view3d_utils.region_2d_to_location_3d(context.region, context.space_data.region_3d, mouse, self.cursor)
        #strokes.append({"name":"", "location":loc, "mouse":mouse, "pressure":1, "pen_flip":False, "time":0, "is_start":False, "size":0})            
        #mouse = (sx, ey)
        #loc = bpy_extras.view3d_utils.region_2d_to_location_3d(context.region, context.space_data.region_3d, mouse, self.cursor)
        #strokes.append({"name":"", "location":loc, "mouse":mouse, "pressure":1, "pen_flip":False, "time":0, "is_start":False, "size":0})            
        #mouse = (ex, ey)
        #loc = bpy_extras.view3d_utils.region_2d_to_location_3d(context.region, context.space_data.region_3d, mouse, self.cursor)
        #strokes.append({"name":"", "location":loc, "mouse":mouse, "pressure":1, "pen_flip":False, "time":0, "is_start":False, "size":0})            
        #mouse = (ex, sy)
        #loc = bpy_extras.view3d_utils.region_2d_to_location_3d(context.region, context.space_data.region_3d, mouse, self.cursor)
        #strokes.append({"name":"", "location":loc, "mouse":mouse, "pressure":1, "pen_flip":False, "time":0, "is_start":False, "size":0})            
    
        #for n in range(int(m)):
        #    ang = 2 * PI/m * n
        #    bet = 2 * PI/m * (n+0.5)
        #    
        #    #bgl.glVertex2i(int(sx), int(sy))
        #    #ex, ey = self.strokes[-1]["mouse"]                                
        #    rad = math.sqrt((ex-sx) ** 2 + (ey-sy) ** 2)
        #    x = rad * math.cos(ang + o) + sx
        #    y = rad * math.sin(ang + o) + sy        
        #    #bgl.glVertex2i(int(x), int(y))
        #    mouse = (x, y)
        #    loc = bpy_extras.view3d_utils.region_2d_to_location_3d(context.region, context.space_data.region_3d, mouse, self.cursor)
        #    strokes.append({"name":"", "location":loc, "mouse":mouse, "pressure":1, "pen_flip":False, "time":0, "is_start":False, "size":0})            
        #    
        #    x = d * rad * math.cos(bet + o) + sx
        #    y = d * rad * math.sin(bet + o) + sy        
        #    #bgl.glVertex2i(int(x), int(y))
        #    mouse = (x, y)
        #    loc = bpy_extras.view3d_utils.region_2d_to_location_3d(context.region, context.space_data.region_3d, mouse, self.cursor)
        #    strokes.append({"name":"", "location":loc, "mouse":mouse, "pressure":1, "pen_flip":False, "time":0, "is_start":False, "size":0})            
        #
        ##strokes = [{"name":"", "location":stroke["location"], "mouse":stroke["mouse"], "pressure":stroke["pressure"], "pen_flip":False, "time":0, "is_start":False, "size":0} for stroke in self.strokes]
        #if bpy.ops.curve.draw.poll() and len(strokes)>0:
        #    #bpy.ops.curve.draw(error_threshold=0.0, fit_method='REFIT', corner_angle=1.22173, use_cyclic=True, stroke=strokes)
        #    bpy.ops.curve.draw(error_threshold=0.0, use_cyclic=True, stroke=strokes)            
        #    #bpy.context.scene.tool_settings.curve_paint_settings.curve_type = 'POLY'
        #    if not bpy.context.scene.tool_settings.curve_paint_settings.curve_type == 'BEZIER':
        #        bpy.ops.curve.cyclic_toggle()
        ##bpy.ops.curve.cyclic_toggle()
        #
        self.strokes = []
        #if props.fill:
        #if bpy.ops.object.editmode_toggle.poll():
        #    bpy.ops.object.editmode_toggle()               

        return {'FINISHED'}
    def finish_draw(self, context):
        props = context.scene.quicker_props
        bpy.types.SpaceView3D.draw_handler_remove(self._handle, 'WINDOW')
        context.space_data.show_manipulator = self.mani
        props.running = False                
        context.space_data.show_outline_selected = self.outline
    def add_draw(self, context, event):
        mouse = (event.mouse_region_x, event.mouse_region_y)
        loc = bpy_extras.view3d_utils.region_2d_to_location_3d(context.region, context.space_data.region_3d, mouse, self.cursor)
        stroke = {"mouse" : mouse, "pressure" : event.pressure, "location": loc}
        self.strokes.append(stroke)
        
    def modal(self, context, event):
        context.area.tag_redraw()
        props = context.scene.quicker_props
        if event.type in ("LEFTMOUSE", "RIGHTMOUSE", "MIDDLEMOUSE"):
            x = event.mouse_region_x
            y = event.mouse_region_y
            w = context.region.width
            h = context.region.height
            if event.value == 'PRESS' and (x < 0 or w < x or y < 0 or h <y):                
                self.finish_draw(context)
                return {'FINISHED'}            
        if event.type == "RIGHTMOUSE":
            if event.value == 'PRESS':
                self.finish_draw(context)
                return {'FINISHED'}
        if event.type == "LEFTMOUSE":
            if event.value == 'PRESS':
                #pass
                self.add_draw(context, event)
            if event.value == 'RELEASE':
                #self.add_draw(context, event)
                self.execute(context)  
        if event.type == "MOUSEMOVE":# Draw stroke
            if event.value == 'PRESS' and not (event.ctrl or event.alt or event.shift):
                #mouse = (event.mouse_region_x, event.mouse_region_y)
                #loc = bpy_extras.view3d_utils.region_2d_to_location_3d(bpy.context.region, bpy.context.space_data.region_3d, mouse, self.cursor)
                #stroke = {"mouse" : mouse, "pressure" : event.pressure, "location": loc}
                #self.strokes.append(stroke)
                self.add_draw(context, event)
        return {'PASS_THROUGH'}

    def invoke(self, context, event):
        props = context.scene.quicker_props
        if context.area.type == 'VIEW_3D' and not props.running:
            context.scene.tool_settings.curve_paint_settings.use_pressure_radius = True          
            self.cursor = context.space_data.cursor_location
            args = (self, context)                   
            self._handle = bpy.types.SpaceView3D.draw_handler_add(draw_star_px, args, 'WINDOW', 'POST_PIXEL')
            context.window_manager.modal_handler_add(self)                
            self.strokes = []
            props.running = True
            self.mani = context.space_data.show_manipulator
            context.space_data.show_manipulator = False
            self.outline = context.space_data.show_outline_selected
            context.space_data.show_outline_selected = False
            return {'RUNNING_MODAL'}            
        else:            
            return {'CANCELLED'}

class OBJECT_PT_Quicker(bpy.types.Panel):
    bl_label = "Quicker"
    bl_space_type = "VIEW_3D"
    bl_region_type = 'TOOLS'
    bl_category = "Create"
    bl_context = "objectmode"
    
    def draw(self, context):
        layout = self.layout
        props = context.scene.quicker_props
        layout.enabled = not props.running
        
        layout.prop(props, "mode")        

        if props.mode == PEN:
            layout.operator(DrawCurve.bl_idname, text="Draw", icon="PLAY")                        
        if props.mode == STAR:
            layout.operator(DrawStar.bl_idname, text="Draw", icon="PLAY")
            
        if props.mode == RECT:
            layout.operator(DrawRect.bl_idname, text="Draw", icon="PLAY")            
        if props.mode == CIRCLE:
            layout.operator(DrawCircle.bl_idname, text="Draw", icon="PLAY")
        
        #view = context.space_data
        #layout.column().prop(context.space_data, "cursor_location", text="Cursor")

#context.scene.tool_settings.curve_paint_settings.curve_type = 'BEZIER'

        #layout.separator()

        #layout.label(text="Shape")        
        
        
        #layout.operator_context = 'INVOKE_DEFAULT'
        #layout.prop(props, "color")
        
        #if props.mode in ("pen", "basic"):
            #layout.label(text="Color")
            #layout.template_curve_mapping(props, "curve", type='VECTOR', levels=False, brush=False, use_negative_slope=False)
        col = layout.column(align=True)
            
        if props.mode == PEN:
            pass
            col.prop(context.scene.tool_settings.curve_paint_settings, "use_pressure_radius")
            col.prop(props, "pen_smooth")        
            
            #col = layout.column()
            #col.operator_context = 'INVOKE_DEFAULT'
            #col.separator()
            #col.operator(DrawCurve.bl_idname, text="Draw", icon="PLAY")
#            col.enabled = not props.running
        if props.mode == STAR:
            pass            
            #col = layout.column()            
            #col.separator()
            #col.operator(DrawStar.bl_idname, text="Draw", icon="PLAY")
#            col.enabled = not props.running
            col.prop(props, "star_num")        
            col.prop(props, "star_depth")        
        if props.mode == RECT:
            pass
        if props.mode == CIRCLE:
            pass
            #toolsettings = context.tool_settings.image_paint
            #brush = toolsettings.brush
            
            #brush = bpy.context.blend_data.brushes[props.brush]
            #layout.template_curve_mapping(brush, "curve")
            #layout.template_ID_preview(context, "brush", new="brush.add", rows=2, cols=6)            
            #row = layout.row(align=True)
            #row.operator("brush.curve_preset", icon='SMOOTHCURVE', text="").shape = 'SMOOTH'
            #row.operator("brush.curve_preset", icon='SPHERECURVE', text="").shape = 'ROUND'
            #row.operator("brush.curve_preset", icon='ROOTCURVE', text="").shape = 'ROOT'
            #row.operator("brush.curve_preset", icon='SHARPCURVE', text="").shape = 'SHARP'
            #row.operator("brush.curve_preset", icon='LINCURVE', text="").shape = 'LINE'
            #row.operator("brush.curve_preset", icon='NOCURVE', text="").shape = 'MAX'
        layout.separator()
        #layout.label(text="General")                        
        col = layout.column(align=True)
        
        col.template_color_picker(props, "color", value_slider=True)
        col.prop(props, "color", text="")
        col.prop(props, "fill")
        col.prop(props, "shadeless")

        
        col.separator()
        col.prop(context.scene.tool_settings.curve_paint_settings, "curve_type",text="")                                        
        col.prop(props, "bevel_depth")
        
        
        #layout.label(text="View")                        
        layout.separator()        
        col = layout.column(align=True)
        
        col.prop(context.space_data.region_3d, "lock_rotation", text="Lock View")        

        
        #col = layout.column(align=True)        
        
            
        #if props.mode == "camera":
        #    layout.prop(context.space_data.region_3d, "lock_rotation", text="Lock View")
        #    layout.separator()
        #    layout.operator("view3d.view_persportho", text="Persp/Ortho")
        #
        #    row = layout.row()
        #    col = row.column()
        #    
        #    num = col.operator("view3d.viewnumpad", text="Top")
        #    num.align_active = True
        #    num.type = 'TOP'
        #    
        #    num = col.operator("view3d.viewnumpad", text="Front")
        #    num.align_active = True
        #    num.type = 'FRONT'
        #
        #    num = col.operator("view3d.viewnumpad", text="Bottom")
        #    num.align_active = True
        #    num.type = 'BOTTOM'
        #    
        #    col = row.column()
        #
        #    num = col.operator("view3d.viewnumpad", text="Back")
        #    num.align_active = True
        #    num.type = 'BACK'
        #
        #    num = col.operator("view3d.viewnumpad", text="Right")
        #    num.align_active = True
        #    num.type = 'RIGHT'
        #
        #    num = col.operator("view3d.viewnumpad", text="Left")
        #    num.align_active = True
        #    num.type = 'LEFT'
        #layout.template_reports_banner()
        #layout.template_palette(props, "color", color=False)
        #layout.template_edit_mode_selection()
#class OBJECT_PT_quicker(bpy.types.Panel):
#    bl_label = "Quicker"
#    bl_space_type = "VIEW_3D"
#    bl_region_type = 'UI'
#    #bl_category = "Quicker"
#
#    def draw(self, context):
#        layout = self.layout
#        
#        if isinstance(context.active_object.data, bpy.types.Curve):
#            layout.prop(context.active_object.active_material, "diffuse_color", text="")
#        #props = context.scene.quicker_props
#        #layout.operator_context = 'INVOKE_DEFAULT'
#        #col = layout.column()
#        #col.operator_context = 'INVOKE_DEFAULT'
#        #col.operator(DrawCurve.bl_idname, text="Draw", icon="GREASEPENCIL")
#        #col.enabled = not props.running
#        #layout.prop(context.space_data.region_3d, "lock_rotation", text="Lock View")        
         
def register():
    bpy.utils.register_module(__name__)
    sc = bpy.types.Scene
    sc.quicker_props = PointerProperty(
        name="Property",
        description="Property",
        type=QuickerProps
    )
    #print("")


def unregister():
    del bpy.types.Scene.quicker_props
    bpy.utils.unregister_module(__name__)
    #print("")


if __name__ == "__main__":
    register()