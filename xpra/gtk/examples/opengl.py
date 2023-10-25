#!/usr/bin/env python3
# This file is part of Xpra.
# Copyright (C) 2013-2020 Antoine Martin <antoine@xpra.org>


def main(argv=()):
    from xpra.log import Logger
    log = Logger("opengl")
    from xpra.platform import program_context
    with program_context("opengl", "OpenGL"):
        try:
            from xpra.os_util import is_X11
            from xpra.client.gl.window import get_gl_client_window_module, test_gl_client_window
            if is_X11():
                from xpra.x11.gtk3.display_source import init_gdk_display_source
                init_gdk_display_source()
            if "-v" in argv or "--verbose" in argv:
                log.enable_debug()
            opengl_props, gl_client_window_module = get_gl_client_window_module("force")
            log("do_run_glcheck() opengl_props=%s, gl_client_window_module=%s", opengl_props, gl_client_window_module)
            gl_client_window_class = gl_client_window_module.GLClientWindow
            pixel_depth = 0
            log("do_run_glcheck() gl_client_window_class=%s, pixel_depth=%s", gl_client_window_class, pixel_depth)
            #if pixel_depth not in (0, 16, 24, 30) and pixel_depth<32:
            #    pixel_depth = 0
            draw_result = test_gl_client_window(gl_client_window_class, pixel_depth=pixel_depth, show=True)
            success = draw_result.pop("success", False)
            opengl_props.update(draw_result)
            if not success:
                opengl_props["safe"] = False
            return 0
        except Exception:
            log("do_run_glcheck(..)", exc_info=True)
            return 1

if __name__ == "__main__":
    import sys
    r = main(sys.argv)
    sys.exit(r)
