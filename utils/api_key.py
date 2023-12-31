import os
import sys

parent_dir = os.path.dirname(os.path.realpath(__file__))
parent_dir_1 = os.path.dirname(os.path.realpath(parent_dir))
base_dir = os.path.dirname(os.path.realpath(parent_dir_1))

sys.path.append(base_dir)

from ai_key import ai_key

api_key = ai_key