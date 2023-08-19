import os
import sys

parent_dir = os.path.dirname(os.path.realpath(__file__))
parent_dir_1 = os.path.dirname(os.path.realpath(parent_dir))
parent_dir_2 = os.path.dirname(os.path.realpath(parent_dir_1))
base_dir = os.path.dirname(os.path.realpath(parent_dir_2))

sys.path.append(base_dir)

from openai_key import openai_key

api_key = openai_key