#Create radial build of stellarator from an existing VMEC input file 

import argparse
import numpy as np
import matplotlib.pyplot as plt
import csv
import math
from RZ_convert import * 
from Radial_from_VMEC_working import *

VMEC_MOD("input.ncsx_c09r00_fixed","RZ_new.csv")
