import numpy as np

class SpaceDecomposition:
    def __init__(self, bounds, dims, num_points, extend=1.2):
        self.bounds = bounds
        self.dims = dims
        self.num_points = num_points
        self.extend = extend

        self.spaces = [[self.bounds] * self.dims]

    def generate_points(self):
        a, b = self.bounds
        # Tạo điểm trong hypercube con
        return np.random.uniform((3*a + b)/4, (a + 3*b)/4, size=(self.num_points, self.dims))

    def decompose(self):
        points = self.generate_points()

        for i in range(self.num_points):
            dim = i % self.dims
            # Sắp xếp điểm dựa trên chiều hiện tại
            sorted_points = points[np.argsort(points[:, dim])]
            slice_point = sorted_points[i // self.dims, dim] # Lấy điểm cắt

            slice_space = self.spaces.pop()
            space_1 = [s if idx != dim else [s[0], slice_point] for idx, s in enumerate(slice_space)]
            space_2 = [s if idx != dim else [slice_point, s[1]] for idx, s in enumerate(slice_space)]

            self.spaces.append(space_1)
            self.spaces.append(space_2)

        return self.spaces
    
    def extension(self):
        self.spaces = self.decompose()

        for space in self.spaces:
            for i in range(self.dims):
                LB, UB = space[i]

                LB = 1/2 * ((1 + self.extend) * LB + (1 - self.extend) * UB)
                UB = 1/2 * ((1 - self.extend) * LB + (1 + self.extend) * UB)

                LB = np.clip(LB, self.bounds[0], self.bounds[1])
                UB = np.clip(UB, self.bounds[0], self.bounds[1])

                space[i] = [LB, UB]

        return self.spaces
