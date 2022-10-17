from itertools import combinations_with_replacement
import numpy as np


class Polyomino:
    def __init__(self, shape, orientation=None):
        height, width = shape
        self.orientation = orientation

        if orientation == "L" or orientation == "R":
            self.height = width
            self.width = height
        else:
            self.width = width
            self.height = height

    def is_rectangular_polyomino(self):
        return self.orientation is None

    def is_valid_position(self, size, position):
        return (
                position[0] + self.height <= size[0] and
                position[1] + self.width <= size[1]
        )

    def assume_position(self, position, mask):
        assert self.is_valid_position(mask.shape, position)
        if self.is_rectangular_polyomino():
            if (mask[
                position[0]: position[0] + self.height,
                position[1]: position[1] + self.width
                ]).any():
                raise ValueError("invalid position -- overlapping")
            else:
                mask[
                position[0]: position[0] + self.height,
                position[1]: position[1] + self.width
                ] = True
        else:
            if self.orientation == "U":
                # assert |_|
                if (
                        mask[position[0]: position[0] + self.height: position[1]].any() or  # |
                        mask[position[0] + self.height - 1, position[1]: position[1] + self.width].any() or  # _
                        mask[position[0]: position[0] + self.height, position[1] + self.width - 1].any()  # |
                ):
                    raise ValueError("invalid position -- overlapping")
                else:
                    mask[position[0]: position[0] + self.height: position[1]] = True
                    mask[position[0] + self.height - 1, position[1]: position[1] + self.width] = True
                    mask[position[0]: position[0] + self.height, position[1] + self.width - 1] = True
            elif self.orientation == "D":
                # assert |^|
                if (
                        mask[position[0]: position[0] + self.height, position[1]].any() or  # |
                        mask[position[0], position[1]: position[1] + self.width - 1].any() or  # _
                        mask[position[0]: position[0] + self.height, position[1] + self.width - 1].any()  # |
                ):
                    raise ValueError("invalid position -- overlapping")
                else:
                    mask[position[0]: position[0] + self.height, position[1]] = True
                    mask[position[0], position[1]: position[1] + self.width - 1] = True
                    mask[position[0]: position[0] + self.height, position[1] + self.width - 1] = True
                pass
            elif self.orientation == "L":
                # assert =|
                if (
                        mask[position[0], position[1]: position[1] + self.width].any() or
                        mask[position[0]: position[0] + self.height, position[1] + self.width - 1].any() or  # _
                        mask[position[0] + self.height - 1, position[1]: position[1] + self.width].any()  # |
                ):
                    raise ValueError("invalid position -- overlapping")
                else:
                    mask[position[0], position[1]: position[1] + self.width] = True
                    mask[position[0]: position[0] + self.height, position[1] + self.width - 1] = True
                    mask[position[0] + self.height - 1, position[1]: position[1] + self.width] = True
            elif self.orientation == "R":
                # assert |=
                if (
                        mask[position[0], position[1]: position[1] + self.width - 1].any() or  # |
                        mask[position[0]: position[0] + self.height, position[1]].any() or  # _
                        mask[position[0] + self.height - 1, position[1]: position[1] + self.width].any()  # |
                ):
                    raise ValueError("invalid position -- overlapping")
                else:
                    mask[position[0], position[1]: position[1] + self.width] = True
                    mask[position[0]: position[0] + self.height, position[1]] = True
                    mask[position[0] + self.height - 1, position[1]: position[1] + self.width] = True

        # self.position = position

    def deassume_position(self, mask):
        """
        Set mask back to False; reset position
        """
        raise NotImplemented("This can reduce space by O(table_size)")


def get_configuration_for_index(i, rect_polyominos, pi_polyominos):
    fixed_pi_polyominos = pi_polyominos
    return rect_polyominos, fixed_pi_polyominos


def main(
        size: tuple,
        rect_polyominos,
        pi_polyominos,
):
    # 1. get explicit shape for pi_polyominos
    #   therefore get the fixed set of polyominos
    # For each such set, consider each possible configuration
    # For each possible configuration, determine whether it is valid
    # If valid is found, return
    #
    pi_polyominos_num = sum([pi_polyomino[1] for pi_polyomino in pi_polyominos])
    pi_polyominos_orientations = ["L", "R", "U", "D"]

    for configuration in combinations_with_replacement(pi_polyominos_orientations, pi_polyominos_num):

        polyominos = []
        for (polyomino, polyomino_count) in rect_polyominos:
            for _ in range(polyomino_count):
                polyominos.append(Polyomino(polyomino))
        for (pi_polyomino, pi_polyomino_count) in pi_polyominos:
            for i in range(pi_polyomino_count):
                polyominos.append(Polyomino(pi_polyomino, orientation=configuration[i]))

        if configuration_fits(size, polyominos):
            return True
    return False


def configuration_fits(size, polyominos):
    table_mask = np.zeros(size).astype(bool)
    return configuration_fits_(0, size, polyominos, table_mask)


def configuration_fits_(i, size, polyominos, table_mask):
    if i == len(polyominos):
        return True

    polyomino = polyominos[i]
    for pos_i in range(size[0]):
        for pos_j in range(size[1]):
            if polyomino.is_valid_position(size, (pos_i, pos_j)):
                prev_mask = table_mask.copy()

                try:
                    polyomino.assume_position((pos_i, pos_j), table_mask)
                    if configuration_fits_(i + 1, size, polyominos, table_mask):
                        return True
                except ValueError:
                    pass

                # backtracking
                # polyomino.deassume_position(table_mask)
                table_mask = prev_mask
    return False


if __name__ == "__main__":
    assert main(
        (4, 6),
        [((2, 2), 2)],
        [((3, 4), 1), ((2, 3), 1)],
    ) == True
    assert main(
        (6, 4),
        [((2, 2), 2)],
        [((3, 4), 1), ((2, 3), 1)],
    ) == True
    assert main(
        (3, 3),
        [((1, 1), 4)],
        [((2, 3), 1)],
    ) == True
    assert main(
        (5, 5),
        [((2, 2), 1)],
        [((2, 3), 2), ((2, 3), 1), ((3, 2), 1)],
    ) == False
    assert main(
        (5, 5),
        [((1, 1), 2), ((3, 3), 1), ((2, 2), 1)],
        [((2, 3), 2)],
    ) == True
    assert main(
        (5, 5),
        [((1, 1), 2), ((4, 4), 1), ((2, 2), 1)],
        [((2, 3), 2)],
    ) == False
    assert main(
        (5, 5),
        [((1, 1), 5)],
        [],
    ) == True
