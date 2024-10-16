class Matrix:

    def __init__(self, matrix_name, matrix_dim):
        self.name = matrix_name
        self.dim = matrix_dim

    def set_name(self, name: str):
        self.name = name

    def set_dimensions(self, dimensions: tuple):
        self.dimensions = dimensions

    def get_name(self):
        return self.name

    def get_dimensions(self):
        return self.dim