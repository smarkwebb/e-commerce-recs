import math
import numpy as np


def get_purchase_history(history_path):
    with open(history_path) as file:
        raw_data = file.readlines()

    summary = [item for item in raw_data[0].split()]
    del raw_data[0]
    purchase_history = raw_data

    return purchase_history, summary


def process_history_pairs(purchase_history):
    customers_items = []

    for element in purchase_history:
        pair = element.split()
        customers_items.append(pair)

    return customers_items


def customer_item_vectors(customers_items, summary):
    total_customers = int(summary[0])
    total_items = int(summary[1])

    vectors_dict = {}

    for item in range(1, total_items + 1):
        vectors_dict[item] = np.zeros(total_customers)

    for customer, item in customers_items:
        customer_index = int(customer) - 1
        item_index = int(item)

        if item_index in vectors_dict:
            vectors_dict[item_index][customer_index] = 1

    return vectors_dict


def compute_angles(vectors_dict):
    items_angles = []

    for item1, vector1 in vectors_dict.items():
        for item2, vector2 in vectors_dict.items():
            if item1 == item2:
                continue

            norm_vector1 = np.linalg.norm(vector1)
            norm_vector2 = np.linalg.norm(vector2)

            if norm_vector1 == 0 or norm_vector2 == 0:
                continue

            dot_product = np.dot(vector1, vector2)
            cos_theta = dot_product / (norm_vector1 * norm_vector2)
            cos_theta = max(-1, min(1, cos_theta))
            theta = math.degrees(math.acos(cos_theta))

            if theta <= 0:
                continue

            items_angle_pair = [item1, item2, theta]
            items_angles.append(items_angle_pair)

    return items_angles


def get_queries(queries_path):
    with open(queries_path) as file:
        raw_data = file.readlines()

    queries = raw_data

    return queries


def process_queries_carts(queries):
    shopping_carts = []

    for query in queries:
        current_cart = query.split()
        shopping_carts.append(current_cart)

    return shopping_carts


def get_positive_entries(vectors_dict):
    positive_entries = 0

    for item, vector in vectors_dict.items():
        for element in vector:
            if element == 1:
                positive_entries += 1

    return positive_entries


def get_average_angle(items_angles):
    sum = 0

    for item1, item2, angle in items_angles:
        sum += angle

    average_angle = sum / len(items_angles)

    return average_angle


def cart_output_format(current_cart):
    string = ""

    for item in current_cart:
        string = string + item + " "

    return string


def find_suggestions(items_angles, current_item, current_cart):
    suggestions = []

    for item1, item2, angle in items_angles:
        unique_item = 0

        if item1 == item2:
            continue

        if item1 == int(current_item):
            unique_item = item2

        if item2 == int(current_item):
            unique_item = item1

        if unique_item == 0:
            continue

        if str(unique_item) in current_cart:
            continue

        suggestions.append([unique_item, angle])

    return suggestions


def sort_suggestions(suggestions):
    suggestions.sort(key=lambda x: x[1])

    unique_suggestions = []

    for suggestion in suggestions:
        item, angle = suggestion
        in_unique = False
        current_angle = 0

        for unique_suggestion in unique_suggestions:
            unique_item, unique_angle = unique_suggestion

            if item == unique_item:
                in_unique = True
                current_item = unique_item
                current_angle = unique_angle

        if not in_unique:
            unique_suggestions.append(suggestion)
            continue

        if angle > current_angle:
            for unique_suggestion in unique_suggestions:
                unique_item, unique_angle = suggestion

                if unique_item == current_item:
                    unique_angle = current_angle

    return unique_suggestions


def suggestion_output_format(all_suggestions):
    outputted_items = []
    string = ""

    for suggestion in all_suggestions:
        item, angle = suggestion

        if item not in outputted_items:
            if angle < 90:
                string = string + str(item) + " "
                outputted_items.append(item)

    return string


purchase_history, summary = get_purchase_history("history.txt")
customers_items = process_history_pairs(purchase_history)
vectors_dict = customer_item_vectors(customers_items, summary)
items_angles = compute_angles(vectors_dict)
queries = get_queries("queries.txt")
shopping_carts = process_queries_carts(queries)
positive_entries = get_positive_entries(vectors_dict)
average_angle = get_average_angle(items_angles)

print("Positive entries:", positive_entries)
print("Average angle:", round(average_angle, 2))

for current_cart in shopping_carts:
    print("Shopping cart:", cart_output_format(current_cart))
    all_suggestions = []

    for current_item in current_cart:
        suggestions = find_suggestions(items_angles, current_item, current_cart)
        suggestions = sort_suggestions(suggestions)
        item, angle = suggestions[0]

        if angle < 90:
            print(f"Item: {current_item}; match {item}; angle: {angle:.2f}")
            all_suggestions.append([item, angle])
        else:
            print(f"Item: {current_item} no match")

    all_suggestions = sort_suggestions(all_suggestions)
    print(f"Recommend: {suggestion_output_format(all_suggestions)}")
