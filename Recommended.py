import numpy as np
import math


def read_history(path):
    with open(path) as f:
        raw = f.readlines()
        pairs = []

        for element in raw:
            pair = element.split()
            pairs.append(pair)

        return pairs


def read_queries(path):
    with open(path) as f:
        raw = f.readlines()
        item_ids = []

        for query in raw:
            item_id = query.split()
            item_ids.append(item_id)

        return item_ids


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

            if not np.array_equal(v1, v2):
                norm_v1 = np.linalg.norm(v1)
                norm_v2 = np.linalg.norm(v2)

                if norm_v1 == 0 or norm_v2 == 0:
                    continue

                cos_theta = np.dot(v1, v2) / (norm_v1 * norm_v2)
                cos_theta = max(-1, min(1, cos_theta))
                theta = math.degrees(math.acos(cos_theta))

                if theta != 0:
                    angle = [key1, key2, theta]
                    angles.append(angle)

    return angles


def get_positive_entries(history):
    pos_entries = 0

    for key in history:
        if history[key].size > 0:
            pos_entries += 1

    return pos_entries


def get_average_angle(angles):
    sum = 0

    for angle in angles:
        sum += angle[2]

    return sum / len(angles)


# Reading the transaction history
pairs = read_history("history.txt")
history = build_history(pairs)
pos_entries = get_positive_entries(history)

# Precomputing item-to-item angles
angles = compute_angles(history)
average_angle = get_average_angle(angles)

# Output
print(f"Positive entries: {pos_entries}")
print(f"Average angle: {average_angle:.2f}")

queries = read_queries("queries.txt")
print(queries)
