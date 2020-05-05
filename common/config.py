RESOURCEPATH = "../../resources/"   # 开发使用相对路径

# RESOURCEPATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'resources/')  # 打包路径选择
import os
import sys

# RESOURCEPATH = os.path.join(sys._MEIPASS, 'resources/')   # 单一文件资源路径选择

TOOLNAME = "综合工具"
LOGOPATH = "img/didilogo.ico"

"""
资源统一配置
"""


def get_resource_path():
    return RESOURCEPATH


def get_tool_name():
    return TOOLNAME


def get_logo_path():
    return LOGOPATH
