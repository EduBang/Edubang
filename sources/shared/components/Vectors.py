#Projet : EduBang
#Auteurs : Anaël Pernot-Chevillard, Sacha Fréguin, Néji Lim

from math import sqrt

from proto import proto

with proto("Vectors") as Vectors:
    @Vectors
    def get_distance(self, pos1, pos2) -> float:
        return sqrt(((pos1[0] - pos2[0]) ** 2) + ((pos1[1] - pos2[1]) ** 2))
    
    @Vectors
    def get_unit_vector(self, pos1, pos2) -> tuple[float, float]:
        x_v_unit = y_v_unit = .0
        dif_x: float = pos2[0] - pos1[0]
        dif_y: float = pos2[1] - pos1[1]
        distance: float = sqrt(dif_x ** 2 + dif_y ** 2)
        
        if distance != 0:
            x_v_unit = dif_x / distance
            y_v_unit = dif_y / distance
        
        return (x_v_unit, y_v_unit)

    @Vectors
    def get_unit_vector_mouv(self, pos_init, pos_final) -> tuple[float | int, float | int]:
        unit_vector_mouv: tuple[float, float] = (.0, .0)
        dX, dY = pos_final[0] - pos_init[0], pos_final[1] - pos_init[1]
        if dX != 0 or dY != 0:
            mouv_vector: tuple[float, float] = (dX, dY)
            norm_mouv_vector: float = sqrt(mouv_vector[0] ** 2 + mouv_vector[1] ** 2)
            unit_vector_mouv = (mouv_vector[0] / norm_mouv_vector, mouv_vector[1] / norm_mouv_vector)
        return unit_vector_mouv