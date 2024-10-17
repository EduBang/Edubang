
from proto import proto
from math import *



with proto("Vectors") as Vectors:
    @Vectors
    def get_unit_vector(self, pos1, pos2):
        dif_x = pos2[0] - pos1[0]
        dif_y = pos2[1] - pos1[1]
        distance = sqrt(dif_x ** 2 + dif_y ** 2)
        
        if distance == 0:
            return (0, 0)
        
        x_v_unit = dif_x / distance
        y_v_unit = dif_y / distance
        return (x_v_unit, y_v_unit)
