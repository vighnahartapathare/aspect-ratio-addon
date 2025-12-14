import bpy

bl_info = {
    "name": "Film Aspect Ratio",  # Display name of the add-on in Blender's add-on list
    "author": "Vighnaharta Pathare",
    "version": (1, 0),
    "blender": (5, 0, 0),
    "location": "Output Properties",  # UI tab in Properties editor where the panel appears
    "description": "Film aspect ratios",
    "category": "Render",
}

# Dictionary of aspect ratios
# "INTERNAL_KEY": ("Visible name in UI", x, y)
aspect_ratios = {
# Square formats
    "SQUARE_1_1": ("Square 1:1", 1080, 1080),

# Classic / Standard film and TV
    "CLASSIC_4_3": ("Classic TV 4:3", 1440, 1080),
    "ACADEMY_137": ("Academy Film 1.37", 1480, 1080),

# European / Widescreen cinema
    "EURO_166": ("European Widescreen 1.66", 1792, 1080),
    "FLAT_185": ("Cinema Flat 1.85", 1920, 1038),
    "UNIVISIUM_200": ("Univisium 2.00", 1920, 960),

# CinemaScope / Anamorphic
    "SCOPE_239": ("CinemaScope 2.39", 1920, 804),
    "SCOPE_240": ("CinemaScope 2.40", 1920, 800),

# IMAX
    "IMAX_143": ("IMAX 70mm 1.43", 2048, 1432),
    "IMAX_190": ("Digital IMAX 1.90", 1920, 1010),

# Standard HD / Widescreen
    "HD_169": ("HD 16:9", 1920, 1080),

# Photography / Print
    "PHOTO_3_2": ("Photography 3:2", 1620, 1080),
    "PHOTO_5_4": ("Photography 5:4", 1350, 1080),

# Vertical / Social Media
    "VERTICAL_916": ("Vertical 9:16", 1080, 1920),
    "VERTICAL_45": ("Vertical 4:5", 1080, 1350),

# Devices / Screens
    "LAPTOP_16_10": ("Laptop 16:10", 1920, 1200),
    "LAPTOP_16_9": ("Laptop 16:9", 1920, 1080),
    "DESKTOP_16_9": ("Desktop 16:9", 2560, 1440),
    "DESKTOP_21_9": ("UltraWide Desktop 21:9", 3440, 1440),

# Mobile devices
    "MOBILE_19_9": ("Mobile 19:9", 1080, 2280),
    "MOBILE_20_9": ("Mobile 20:9", 1080, 2400),

# Apple devices
    "IPHONE_19_9": ("iPhone 19:9", 1125, 2436),      # iPhone X, 11 Pro
    "IPHONE_20_9": ("iPhone 20:9", 1170, 2532),     # iPhone 12, 13, 14
    "IPAD_4_3": ("iPad 4:3", 2048, 1536),
    "IPAD_PRO_11": ("iPad Pro 11\" 4:3", 2388, 1668),
    "IPAD_PRO_12_9": ("iPad Pro 12.9\" 4:3", 2732, 2048),
}

# Prepare dropdown items (only name and ratio shown)
def get_aspect_items(self, context):
    items = []
    for key, (name, x, y) in aspect_ratios.items():
        items.append((key, name, ""))  # Label only shows name (no px)
    return items

# Add EnumProperty to Scene
bpy.types.Scene.aspect_dropdown = bpy.props.EnumProperty(
    name="Film Aspect Ratio",
    description="Choose film aspect ratio",
    items=get_aspect_items
)

# Operator to apply selected resolution
class RENDER_OT_apply_aspect(bpy.types.Operator):
    bl_idname = "render.apply_aspect"
    bl_label = "Apply Aspect Ratio"

    def execute(self, context):
        key = context.scene.aspect_dropdown
        _, x, y = aspect_ratios[key]
        scene = context.scene
        scene.render.resolution_x = x
        scene.render.resolution_y = y
        scene.render.pixel_aspect_x = 1
        scene.render.pixel_aspect_y = 1
        self.report({'INFO'}, f"Set resolution to {x}x{y}")
        return {'FINISHED'}

# Panel with dropdown
class RENDER_PT_aspect_panel(bpy.types.Panel):
    bl_label = "Film Aspect Ratios"
    bl_idname = "RENDER_PT_aspect_panel"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "output"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        layout.prop(scene, "aspect_dropdown")  # dropdown
        layout.operator("render.apply_aspect", text="Apply")

# Register / Unregister
def register():
    bpy.utils.register_class(RENDER_OT_apply_aspect)
    bpy.utils.register_class(RENDER_PT_aspect_panel)

def unregister():
    bpy.utils.unregister_class(RENDER_PT_aspect_panel)
    bpy.utils.unregister_class(RENDER_OT_apply_aspect)
    del bpy.types.Scene.aspect_dropdown

if __name__ == "__main__":
    register()
