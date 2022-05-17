from csv import reader


def import_csv(path):
    terrain_map = []

    with open(path) as map:
        layout = reader(map, delimiter = ',')

        for row in layout:
            terrain_map.append(list(row))

        return terrain_map
