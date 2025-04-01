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


def cart_output(cart):
    output = ""

    for item in cart:
        output = output + item + " "

    return output


def find_item_match(angles, target, cart):
    min_angle = 10000
    match_item = 0
    recommended = []

    for index in angles:
        angle = index[2]

        if angle < min_angle:
            item1 = index[0]
            item2 = index[1]

            if item1 == item2:
                continue

            if str(item1) == target:
                cur_item = item2
            elif str(item2) == target:
                cur_item = item1
            else:
                continue

            if str(cur_item) in cart:
                continue

            min_angle = angle
            match_item = cur_item

    return [match_item, min_angle, recommended]


def compute_angles(history):
    angles = []

    for key1 in history:
        for key2 in history:
            if key1 == key2:
                continue

            vector1 = history[key1]
            vector2 = history[key2]

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
history = build_history_table(pairs)
queries = get_queries("queries.txt")
carts = convert_to_carts(queries)
angles = compute_angles(history)

# Output to user
print(f"Positive entries: {get_positive_entries()}")
print(f"Average angle: {round(get_average_angle(angles), 2)}")

for cart in carts:
    print(f"Shopping cart: {cart_output(cart)}")

    for item in cart:
        match = find_item_match(angles, item, cart)

        if match[1] < 90:
            print(f"Item: {item}; match: {match[0]}; angle: {round(match[1], 2)}")
        else:
            print(f"Item: {item} no match")
