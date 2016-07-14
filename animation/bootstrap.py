import os
import sys

# Setup the path to known locations of GLFW's DLL on Windows
if sys.platform == 'win32':
    import platform
    bits = platform.architecture()[0][:2]
    os.environ['PATH'] += os.pathsep + r'C:\ProgramData\chocolatey\msvc120-{}\bin'.format(bits)

# Inject support for local font loading into VisPy.
def _get_vispy_font_filename(face, bold, italic):
    return os.path.join(os.path.dirname(__file__), 'data/questrial.ttf')

# Fonts on Mac OSX.
if sys.platform == 'darwin':
    from vispy.util.fonts import _quartz
    _quartz._vispy_fonts = ('Questrial',)
    _quartz._get_vispy_font_filename = _get_vispy_font_filename
    del _quartz

# Fonts on Windows and Linux.
if sys.platform in ['win32', 'linux']:
    from vispy.util.fonts import _freetype
    _freetype._vispy_fonts = ('Questrial',)
    _freetype._get_vispy_font_filename = _get_vispy_font_filename
    del _freetype
