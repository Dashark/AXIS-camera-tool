# -*- coding: utf-8 -*-
import sys
import os

# sysdict=sys.__dict__
# hasforzen=False
def app_path():
    """Returns the base application path."""
    if hasattr(sys, 'frozen'):
        # Handles PyInstaller\
        # global hasforzen
        # hasforzen=True
        # os.environ['PATH'] = sys._MEIPASS + ";" + os.environ['PATH']
        # return sys._MEIPASS  # 使用pyinstaller打包后的exe目录
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.realpath(sys.argv[0]))
    # return os.path.dirname(__file__)  # 没打包前的py目录

base_dir=app_path()