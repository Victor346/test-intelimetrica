import math


# Function used to obtain the mean rating of a list of restaurants
def get_average_rating(list_restaurants):
    total = 0
    for restaurant in list_restaurants:
        total = total + restaurant['rating']
    return total / len(list_restaurants)


# Function used to obtain the standard deviation from a list of restaurants providing the average
def get_standard_deviation(list_restaurants, average):
    sup_sum = 0
    for restaurant in list_restaurants:
        sup_sum = sup_sum + (math.pow(restaurant['rating'] - average, 2))
    sub_result = sup_sum / len(list_restaurants)
    final_result = math.sqrt(sub_result)
    return final_result
