from math import sqrt

from proto import proto

with proto("Vectors") as Vectors:
    
    @Vectors
    def get_distance(self, corps1, corps2) -> float:
        return sqrt(((corps1.pos[0] - corps2.pos[0]) ** 2) + ((corps1.pos[1] - corps2.pos[1]) ** 2))
    
    @Vectors
    def get_unit_vector(self, pos1, pos2) -> tuple[float, float]:
        dif_x = pos2[0] - pos1[0]
        dif_y = pos2[1] - pos1[1]
        distance = sqrt(dif_x ** 2 + dif_y ** 2)
        
        if distance == 0:
            return (0, 0)
        
        x_v_unit = dif_x / distance
        y_v_unit = dif_y / distance
        return (x_v_unit, y_v_unit)

    @Vectors
    def get_unit_vector_mouv(self, pos_init, pos_final) -> tuple[float | int, float | int]:
        mouv_vector = (pos_final[0] - pos_init[0], pos_final[1] - pos_init[1])
        norm_mouv_vector = sqrt(mouv_vector[0] ** 2 + mouv_vector[1] ** 2)
        if norm_mouv_vector != 0:
            unit_vector_mouv = (mouv_vector[0] / norm_mouv_vector, mouv_vector[1] / norm_mouv_vector)
        else:
            unit_vector_mouv = (0, 0)
        return unit_vector_mouv