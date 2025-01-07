def upscale(matrix, factor):
    new_matrix = []
    for row in matrix:
        new_row = []
        for element in row:
            new_row.extend([element] * factor)
        for _ in range(factor):
            new_matrix.append(new_row)
    return new_matrix

# Exemple d'utilisation
matrix = [1]

upscaled_matrix = upscale(matrix, 2)

for row in upscaled_matrix:
    print(row)