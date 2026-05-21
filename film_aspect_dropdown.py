# ─────────────────────────────────────────────────────────────────────────────
#  CHANGES IN v2.0
#   • Added category filters for faster preset browsing:
#     Film, TV/Broadcast, Social Media, Devices, and All.
#   • Added 88 aspect ratio presets across film, broadcast,
#     social platforms, photography, print, and modern devices.
#   • Added Resolution Scale % control (10–400%) with live
#     preview of final output dimensions before applying.
#   • Added Rotate 90° button to instantly swap width/height.
#   • Added current resolution readout showing active render
#     size, aspect ratio, and scale percentage.
#   • Apply button now automatically sets pixel aspect to 1:1.
#   • Live preview, rotate, and apply actions.
# ─────────────────────────────────────────────────────────────────────────────

import bpy
from bpy.props import EnumProperty, IntProperty

bl_info = {
    "name"       : "Film Aspect Ratio",
    "author"     : "Vighnaharta Pathare",
    "version"    : (2, 0),
    "blender"    : (4, 0, 0),
    "location"   : "Output Properties → Film Aspect Ratios  |  Render Properties → Aspect Scale",
    "description": "Aspect ratio & resolution presets for film, TV, social media, and devices",
    "category"   : "Render",
}

# ─────────────────────────────────────────────────────────────────────────────
#  PRESET DATA
#  "KEY": ("Display Name", width, height, "CATEGORY")
#  Categories (must match _CATEGORY_ITEMS identifiers exactly):
#    FILM   TV   SOCIAL   DEVICE
# ─────────────────────────────────────────────────────────────────────────────
BUILTIN_PRESETS = {

    # ── Classic & Silent Film ─────────────────────────────────────────────────
    "SILENT_133"      : ("Silent Film 1.33:1",                   1440,  1080, "FILM"),
    "ACADEMY_137"     : ("Academy Film 1.37:1",                  1480,  1080, "FILM"),
    "VISTA_133"       : ("VistaVision 1.33:1",                   1440,  1080, "FILM"),
    "CLASSIC_4_3"     : ("Classic TV 4:3",                       1440,  1080, "TV"),

    # ── Widescreen / Flat Cinema ──────────────────────────────────────────────
    "EURO_166"        : ("European Widescreen 1.66:1",           1792,  1080, "FILM"),
    "FLAT_185"        : ("Cinema Flat 1.85:1",                   1920,  1038, "FILM"),
    "UNIVISIUM_200"   : ("Univisium 2.00:1",                     1920,   960, "FILM"),

    # ── Super 35 / Spherical Anamorphic ───────────────────────────────────────
    "SUPER35_237"     : ("Super 35  2.37:1",                     1920,   810, "FILM"),
    "SCOPE_235"       : ("CinemaScope Classic 2.35:1",           1920,   817, "FILM"),
    "SCOPE_239"       : ("CinemaScope 2.39:1",                   1920,   804, "FILM"),
    "SCOPE_240"       : ("CinemaScope 2.40:1",                   1920,   800, "FILM"),
    "PANAVISION_276"  : ("Ultra Panavision 2.76:1",              1920,   696, "FILM"),
    "CINERAMA_289"    : ("Cinerama 2.89:1",                      1920,   665, "FILM"),

    # ── DCI Digital Cinema ────────────────────────────────────────────────────
    "DCI_2K"          : ("DCI 2K Container",                     2048,  1080, "FILM"),
    "DCI_2K_FLAT"     : ("DCI 2K Flat 1.85:1",                  1998,  1080, "FILM"),
    "DCI_2K_SCOPE"    : ("DCI 2K Scope 2.39:1",                 2048,   858, "FILM"),
    "DCI_4K"          : ("DCI 4K Container",                     4096,  2160, "FILM"),
    "DCI_4K_FLAT"     : ("DCI 4K Flat 1.85:1",                  3996,  2160, "FILM"),
    "DCI_4K_SCOPE"    : ("DCI 4K Scope 2.39:1",                 4096,  1716, "FILM"),
    "DCI_4K_FULL"     : ("DCI 4K Full Container",                4096,  3072, "FILM"),

    # ── IMAX ──────────────────────────────────────────────────────────────────
    "IMAX_136"        : ("IMAX 15/70 Film 1.36:1",               4096,  3012, "FILM"),
    "IMAX_143"        : ("IMAX 70mm  1.43:1",                    2048,  1432, "FILM"),
    "IMAX_190"        : ("Digital IMAX  1.90:1",                 1920,  1010, "FILM"),
    "IMAX_169"        : ("IMAX Laser  16:9",                     3840,  2160, "FILM"),

    # ── Photography / Print ───────────────────────────────────────────────────
    "PHOTO_3_2"       : ("Photography 3:2  (DSLR)",             1620,  1080, "FILM"),
    "PHOTO_4_3"       : ("Photography 4:3  (MFT)",              1440,  1080, "FILM"),
    "PHOTO_5_4"       : ("Photography 5:4  (Large Format)",     1350,  1080, "FILM"),
    "PHOTO_1_1"       : ("Photography 1:1  (Medium Format)",    1080,  1080, "FILM"),
    "PRINT_A4_L"      : ("Print A4 Landscape  (300 DPI)",       2480,  1754, "FILM"),
    "PRINT_A4_P"      : ("Print A4 Portrait  (300 DPI)",        1754,  2480, "FILM"),
    "PRINT_A3_L"      : ("Print A3 Landscape  (300 DPI)",       3508,  2480, "FILM"),

    # ── TV & Broadcast ────────────────────────────────────────────────────────
    "SD_NTSC"         : ("SD NTSC  4:3  (480i)",                  720,   480, "TV"),
    "SD_PAL"          : ("SD PAL  4:3  (576i)",                   720,   576, "TV"),
    "HD_720"          : ("HD 720p  16:9",                        1280,   720, "TV"),
    "HD_169"          : ("HD 1080p  16:9",                       1920,  1080, "TV"),
    "UHD_4K"          : ("4K UHD  16:9",                        3840,  2160, "TV"),
    "UHD_8K"          : ("8K UHD  16:9",                        7680,  4320, "TV"),
    "BROADCAST_21_9"  : ("Broadcast UltraWide  21:9",           2560,  1080, "TV"),
    "DCINEMA_2K"      : ("Digital Cinema 2K  (Broadcast)",      2048,  1080, "TV"),

    # ── Social Media ──────────────────────────────────────────────────────────
    "SQUARE_1_1"      : ("Square 1:1",                          1080,  1080, "SOCIAL"),
    "VERTICAL_916"    : ("Vertical 9:16  (Stories / Reels)",    1080,  1920, "SOCIAL"),
    "VERTICAL_45"     : ("Vertical 4:5  (Instagram Portrait)",  1080,  1350, "SOCIAL"),
    "VERTICAL_23"     : ("Vertical 2:3  (Pinterest)",           1080,  1620, "SOCIAL"),
    "YOUTUBE_THUMB"   : ("YouTube Thumbnail  16:9",             1280,   720, "SOCIAL"),
    "YOUTUBE_BANNER"  : ("YouTube Channel Art  2560×1440",      2560,  1440, "SOCIAL"),
    "TWITTER_POST"    : ("Twitter / X Post  16:9",              1600,   900, "SOCIAL"),
    "TWITTER_CARD"    : ("Twitter Summary Card  2:1",           1200,   600, "SOCIAL"),
    "LINKEDIN_POST"   : ("LinkedIn Post  1.91:1",               1200,   627, "SOCIAL"),
    "LINKEDIN_COVER"  : ("LinkedIn Cover  4:1",                 1584,   396, "SOCIAL"),
    "FB_POST"         : ("Facebook Post  1.91:1",               1200,   630, "SOCIAL"),
    "FB_COVER"        : ("Facebook Cover  2.7:1",                820,   312, "SOCIAL"),
    "FB_STORY"        : ("Facebook Story  9:16",                1080,  1920, "SOCIAL"),
    "INSTA_LANDSCAPE" : ("Instagram Landscape  1.91:1",         1080,   566, "SOCIAL"),
    "PINTEREST_PIN"   : ("Pinterest Pin  2:3",                   735,  1102, "SOCIAL"),
    "TIKTOK_COVER"    : ("TikTok Cover  9:16",                  1080,  1920, "SOCIAL"),
    "SNAPCHAT"        : ("Snapchat  9:16",                      1080,  1920, "SOCIAL"),
    "THREADS_POST"    : ("Threads Post  1:1",                   1080,  1080, "SOCIAL"),

    # ── Monitors & Laptops ────────────────────────────────────────────────────
    "LAPTOP_16_10"    : ("Laptop 16:10  (MacBook / ThinkPad)",  1920,  1200, "DEVICE"),
    "LAPTOP_16_9"     : ("Laptop 16:9  (1080p)",                1920,  1080, "DEVICE"),
    "DESKTOP_QHD"     : ("Desktop QHD  2560×1440",              2560,  1440, "DEVICE"),
    "DESKTOP_WQHD"    : ("Desktop WQHD  3440×1440",             3440,  1440, "DEVICE"),
    "DESKTOP_4K"      : ("Desktop 4K  3840×2160",               3840,  2160, "DEVICE"),
    "DESKTOP_5K"      : ("Desktop 5K  5120×2880",               5120,  2880, "DEVICE"),
    "DESKTOP_6K"      : ("Desktop 6K  6016×3384",               6016,  3384, "DEVICE"),
    "SUPERWIDE_32_9"  : ("Super UltraWide 32:9  5120×1440",     5120,  1440, "DEVICE"),
    "MACBOOK_RETINA"  : ("MacBook Retina  2560×1600",           2560,  1600, "DEVICE"),
    "IMAC_5K"         : ("iMac 5K  5120×2880",                  5120,  2880, "DEVICE"),
    "STUDIO_DISPLAY"  : ("Apple Studio Display  5K",            5120,  2880, "DEVICE"),
    "PRO_DISPLAY_XDR" : ("Pro Display XDR  6K",                 6016,  3384, "DEVICE"),

    # ── Mobile / Phones ───────────────────────────────────────────────────────
    "ANDROID_FHD"     : ("Android FHD  1080×1920",              1080,  1920, "DEVICE"),
    "ANDROID_19_9"    : ("Android 19:9  1080×2280",             1080,  2280, "DEVICE"),
    "ANDROID_20_9"    : ("Android 20:9  1080×2400",             1080,  2400, "DEVICE"),
    "IPHONE_SE"       : ("iPhone SE  2:3  750×1334",             750,  1334, "DEVICE"),
    "IPHONE_X"        : ("iPhone X / 11 Pro  1125×2436",        1125,  2436, "DEVICE"),
    "IPHONE_12"       : ("iPhone 12 / 13 / 14  1170×2532",      1170,  2532, "DEVICE"),
    "IPHONE_15"       : ("iPhone 15 / 16  1179×2556",           1179,  2556, "DEVICE"),
    "IPHONE_15_MAX"   : ("iPhone 15/16 Pro Max  1290×2796",     1290,  2796, "DEVICE"),
    "GALAXY_S24"      : ("Samsung Galaxy S24  1080×2340",       1080,  2340, "DEVICE"),
    "PIXEL_8"         : ("Google Pixel 8  1080×2400",           1080,  2400, "DEVICE"),

    # ── Tablets ───────────────────────────────────────────────────────────────
    "IPAD_MINI"       : ("iPad mini  4:3  2266×1488",           2266,  1488, "DEVICE"),
    "IPAD_4_3"        : ("iPad 10th gen  2360×1640",            2360,  1640, "DEVICE"),
    "IPAD_PRO_11"     : ("iPad Pro 11\"  2388×1668",            2388,  1668, "DEVICE"),
    "IPAD_PRO_129"    : ("iPad Pro 12.9\"  2732×2048",          2732,  2048, "DEVICE"),
    "SAMSUNG_TAB"     : ("Samsung Tab S9  2560×1600",           2560,  1600, "DEVICE"),

}

# ─────────────────────────────────────────────────────────────────────────────
#  CATEGORY DEFINITIONS  (static — safe for string default)
# ─────────────────────────────────────────────────────────────────────────────
_CATEGORY_ITEMS = [
    ("ALL",    "All",           "Show every preset"),
    ("FILM",   "Film",          "Film, cinema, IMAX, photography, and print"),
    ("TV",     "TV / Broadcast","Television and broadcast standards"),
    ("SOCIAL", "Social Media",  "Social media, vertical, and web formats"),
    ("DEVICE", "Devices",       "Monitors, laptops, mobile, tablets"),
]

_filtered_items = []

def _rebuild_items(cat_filter: str) -> None:
    """Repopulate _filtered_items for the given category."""
    global _filtered_items
    items = []
    for key, (name, x, y, cat) in BUILTIN_PRESETS.items():
        if cat_filter == "ALL" or cat == cat_filter:
            tip = f"{x} × {y}  ({_ratio_str(x, y)})"
            items.append((key, name, tip))
    if not items:
        items.append(("NONE", "— No presets —", ""))
    _filtered_items = items


def _get_aspect_items(self, context):
    return _filtered_items if _filtered_items else [("NONE", "— No presets —", "")]


def _on_category_update(self, context):
    _rebuild_items(self.aspect_category)
    for window in context.window_manager.windows:
        for area in window.screen.areas:
            if area.type == 'PROPERTIES':
                for region in area.regions:
                    if region.type == 'WINDOW':
                        region.tag_redraw()


# ─────────────────────────────────────────────────────────────────────────────
#  HELPERS
# ─────────────────────────────────────────────────────────────────────────────

def _gcd(a, b):
    while b:
        a, b = b, a % b
    return a


def _ratio_str(w, h):
    """'16:9', '1.85:1', etc."""
    g = _gcd(w, h)
    rw, rh = w // g, h // g
    if max(rw, rh) <= 60:
        return f"{rw}:{rh}"
    return f"{w / h:.2f}:1"


def _preview_res(context):
    """Return (w, h) that Apply would set, or (None, None)."""
    scene = context.scene
    key   = getattr(scene, "aspect_dropdown", None)
    scale = getattr(scene, "aspect_scale",    100)
    if not key or key == "NONE":
        return None, None
    data = BUILTIN_PRESETS.get(key)
    if not data:
        return None, None
    _, x, y, _ = data
    f = scale / 100.0
    return max(2, round(x * f)), max(2, round(y * f))


# ─────────────────────────────────────────────────────────────────────────────
#  OPERATORS
# ─────────────────────────────────────────────────────────────────────────────

class RENDER_OT_apply_aspect(bpy.types.Operator):
    """Apply the selected aspect ratio to the render resolution"""
    bl_idname  = "render.apply_aspect"
    bl_label   = "Apply Preset"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        pw, ph = _preview_res(context)
        if pw is None:
            self.report({'WARNING'}, "Select a valid preset first.")
            return {'CANCELLED'}
        r = context.scene.render
        r.resolution_x   = pw
        r.resolution_y   = ph
        r.pixel_aspect_x = 1
        r.pixel_aspect_y = 1
        self.report({'INFO'}, f"Resolution → {pw} × {ph}  ({_ratio_str(pw, ph)})")
        return {'FINISHED'}


class RENDER_OT_swap_resolution(bpy.types.Operator):
    """Swap render width and height (rotate canvas 90°)"""
    bl_idname  = "render.swap_resolution"
    bl_label   = "Rotate 90°"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        r = context.scene.render
        r.resolution_x, r.resolution_y = r.resolution_y, r.resolution_x
        self.report({'INFO'}, f"Swapped → {r.resolution_x} × {r.resolution_y}")
        return {'FINISHED'}


# ─────────────────────────────────────────────────────────────────────────────
#  OUTPUT PROPERTIES PANEL  (main panel)
# ─────────────────────────────────────────────────────────────────────────────

class RENDER_PT_aspect_panel(bpy.types.Panel):
    bl_label       = "Film Aspect Ratios"
    bl_idname      = "RENDER_PT_aspect_panel"
    bl_space_type  = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context     = "output"

    def draw(self, context):
        layout = self.layout
        scene  = context.scene
        render = scene.render

        # ── Current resolution readout ────────────────────────
        box = layout.box()
        box.label(text="Current Render Resolution", icon='RENDER_RESULT')
        row = box.row(align=True)
        row.label(
            text=(
                f"{render.resolution_x} × {render.resolution_y}  "
                f"({_ratio_str(render.resolution_x, render.resolution_y)})  "
                f"@ {render.resolution_percentage}%"
            ),
            icon='ARROW_LEFTRIGHT',
        )
        row.operator("render.swap_resolution", text="", icon='FILE_REFRESH')

        layout.separator()

        # ── Category filter ───────────────────────────────────
        layout.label(text="Filter:", icon='FILTER')
        layout.prop(scene, "aspect_category", expand=True)

        layout.separator()

        # ── Preset dropdown ───────────────────────────────────
        layout.label(text="Preset:", icon='PRESET')
        layout.prop(scene, "aspect_dropdown", text="")

        # ── Scale slider ──────────────────────────────────────
        layout.separator()
        row = layout.row(align=True)
        row.label(text="Scale:", icon='FULLSCREEN_ENTER')
        row.prop(scene, "aspect_scale", text="")

        # ── Live preview ──────────────────────────────────────
        pw, ph = _preview_res(context)
        box2 = layout.box()
        if pw:
            box2.label(
                text=f"Will be set to:  {pw} × {ph}  ({_ratio_str(pw, ph)})",
                icon='CHECKMARK',
            )
        else:
            box2.label(text="Select a preset above", icon='INFO')

        # ── Apply button ──────────────────────────────────────
        row = layout.row()
        row.scale_y = 1.4
        row.operator("render.apply_aspect", text="Apply Preset", icon='CHECKMARK')


# ─────────────────────────────────────────────────────────────────────────────
#  RENDER PROPERTIES → FORMAT TAB  sub-panel
#  Gives quick access to the Scale % without leaving the Render tab.
# ─────────────────────────────────────────────────────────────────────────────

class RENDER_PT_aspect_format(bpy.types.Panel):
    bl_label       = "Aspect Ratio Scale"
    bl_idname      = "RENDER_PT_aspect_format"
    bl_space_type  = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context     = "render"          # Render Properties tab
    bl_options     = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        scene  = context.scene
        render = scene.render

        # Quick scale control
        col = layout.column(align=True)
        col.label(text="Preset Scale:", icon='FULLSCREEN_ENTER')
        col.prop(scene, "aspect_scale", text="Scale %", slider=True)

        # Show what Apply would produce
        pw, ph = _preview_res(context)
        if pw:
            col.separator()
            col.label(
                text=f"Preset result:  {pw} × {ph}  ({_ratio_str(pw, ph)})",
                icon='DRIVER_TRANSFORM',
            )

        layout.separator()

        # One-click apply right from the Format tab
        row = layout.row(align=True)
        row.operator("render.apply_aspect",    text="Apply Preset",  icon='CHECKMARK')
        row.operator("render.swap_resolution", text="Rotate 90°",    icon='FILE_REFRESH')

        layout.separator()

        # Also show the native Blender resolution controls for convenience
        col2 = layout.column(align=True)
        col2.label(text="Render Resolution:", icon='RENDER_RESULT')
        col2.prop(render, "resolution_x", text="Width")
        col2.prop(render, "resolution_y", text="Height")
        col2.prop(render, "resolution_percentage", text="Scale %")


# ─────────────────────────────────────────────────────────────────────────────
#  REGISTRATION
# ─────────────────────────────────────────────────────────────────────────────

_CLASSES = (
    RENDER_OT_apply_aspect,
    RENDER_OT_swap_resolution,
    RENDER_PT_aspect_panel,
    RENDER_PT_aspect_format,
)


def _register_props():
    if not hasattr(bpy.types.Scene, "aspect_category"):
        bpy.types.Scene.aspect_category = EnumProperty(
            name        = "Category",
            description = "Filter presets by category",
            items       = _CATEGORY_ITEMS,
            default     = "ALL",
            update      = _on_category_update,   # rebuilds dropdown on change
        )

    # Preset dropdown 
    if not hasattr(bpy.types.Scene, "aspect_dropdown"):
        bpy.types.Scene.aspect_dropdown = EnumProperty(
            name        = "Film Aspect Ratio",
            description = "Choose a resolution preset",
            items       = _get_aspect_items,  
        )

    # Scale %
    if not hasattr(bpy.types.Scene, "aspect_scale"):
        bpy.types.Scene.aspect_scale = IntProperty(
            name        = "Scale",
            description = "Scale the preset resolution before applying (100 = native size)",
            default     = 100,
            min         = 10,
            max         = 400,
            step        = 5,
            subtype     = 'PERCENTAGE',
        )


def _unregister_props():
    for p in ("aspect_category", "aspect_dropdown", "aspect_scale"):
        if hasattr(bpy.types.Scene, p):
            try:
                delattr(bpy.types.Scene, p)
            except Exception:
                pass


def register():
    _rebuild_items("ALL")

    for cls in _CLASSES:
        try:
            bpy.utils.register_class(cls)
        except ValueError:
            bpy.utils.unregister_class(cls)
            bpy.utils.register_class(cls)

    _register_props()


def unregister():
    for cls in reversed(_CLASSES):
        try:
            bpy.utils.unregister_class(cls)
        except RuntimeError:
            pass
    _unregister_props()


if __name__ == "__main__":
    register()
