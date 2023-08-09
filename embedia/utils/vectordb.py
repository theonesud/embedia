import math


def distance_to_similarity(distance, type):
    # Converts different types of distances to a similarity score between [0,1]
    # Check https://github.com/nmslib/hnswlib/tree/master for more info

    if type == 'l2':
        return 1.0 - distance / math.sqrt(2)

    if type == 'ip':
        if distance > 0:
            return 1.0 - distance
        return -1.0 * distance

    if type == 'cosine':
        return 1.0 - distance

    else:
        raise ValueError(f"Unknown distance type: {type}")
