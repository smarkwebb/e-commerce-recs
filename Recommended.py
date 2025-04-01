import math
import numpy as np


def get_history(path):
    with open(path) as file:
        history = file.readlines()

    return history


def convert_to_pairs(history):
    pairs = []

    for item in history:
        pair = item.split()
        pairs.append(pair)

    return pairs


def build_history_table(pairs):
    header_data = pairs[0]
    del pairs[0]

    num_customers = int(header_data[0])
    num_items = int(header_data[1])

    history = {}

    for item in range(1, num_items + 1):
        history[item] = np.zeros(num_customers)

    for pair in pairs:
        customer_index = int(pair[0]) - 1
        item_index = int(pair[1])

        if item_index in history:
            history[item_index][customer_index] = 1

    return history


def get_positive_entries():
    pass


def get_queries(path):
    with open(path) as file:
        queries = file.readlines()

    return queries


def convert_to_carts(enquires):
    carts = []

    for item in enquires:
        cart = item.split()
        carts.append(cart)

    return carts


def compute_angles(history_table):
    angles = []

    for key1 in history:
        for key2 in history:
            if key1 == key2:
                continue

            vector1 = history_table[key1]
            vector2 = history_table[key2]

            norm_vector1 = np.linalg.norm(vector1)
            norm_vector2 = np.linalg.norm(vector2)

            if norm_vector1 == 0 or norm_vector2 == 0:
                continue

            dot_product = np.dot(vector1, vector2)
            cos_theta = dot_product / (norm_vector1 * norm_vector2)
            cos_theta = max(-1, min(1, cos_theta))
            theta = math.degrees(math.acos(cos_theta))

            if theta > 0:
                angle = [key1, key2, theta]
                angles.append(angle)

    return angles


def get_average_angle(angles):
    sum = 0

    for angle in angles:
        sum += angle[2]

    return sum / len(angles)


history = get_history("history.txt")
pairs = convert_to_pairs(history)
print(f"PAIRS {pairs}")
history = build_history_table(pairs)
print(f"HISTORY TABLE {history}")
queries = get_queries("queries.txt")
print(f"QUERIES: {queries}")
carts = convert_to_carts(queries)
print(f"CARTS {carts}")
angles = compute_angles(history)
print(f"ANGLES {angles}")

print(f"Positive entries: {get_positive_entries()}")
print(f"Average angle: {get_average_angle(angles)}")
