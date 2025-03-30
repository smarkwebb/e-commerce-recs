import numpy as np
import math


def get_pairs(path):
    with open(path) as f:
        raw = f.readlines()
        pairs = []

        for element in raw:
            pair = element.split()
            pairs.append(pair)

        return pairs


def build_history(pairs):
    header = pairs[0]
    num_customers = int(header[0])
    num_items = int(header[1])
    del pairs[0]
    history = {}

    for item in range(1, num_items + 1):
        history[item] = np.zeros(num_customers)

    for pair in pairs:
        customer_index = int(pair[0]) - 1
        item_index = int(pair[1])

        if item_index in history:
            history[item_index][customer_index] = 1

    return history


def compute_angles(history):
    angles = []

    for key1 in history:
        for key2 in history:
            v1 = history[key1]
            v2 = history[key2]

            norm_v1 = np.linalg.norm(v1)
            norm_v2 = np.linalg.norm(v2)

            if norm_v1 == 0 or norm_v2 == 0:
                continue

            dot_product = np.dot(v1, v2)
            cos_theta = dot_product / (norm_v1 * norm_v2)
            theta = math.degrees(math.acos(cos_theta))

            angle = [key1, key2, theta]
            angles.append(angle)


pairs = get_pairs("history.txt")
history = build_history(pairs)
compute_angles(history)
