#To randomly select testcases from csv file
import random
def random_rows(course_info):
    all_rows = list(course_info)
    random_rows = random.sample(all_rows, 30)
    return random_rows


# import csv
# import random
# from datetime import datetime   
# # To randomly generate different testcases for algorithm
# # Load the CSV file into a list of dictionaries
# file_path = 'faculty_preference.csv'  # Replace with the actual path to your CSV file

# with open(file_path, 'r') as file:
#     csv_reader = csv.DictReader(file)
#     data = list(csv_reader)

# # Ensure there are at least 30 rows in the dataset
# if len(data) < 30:
#     print("Not enough rows in the dataset.")
# else:
#     # Set a unique random seed using the current timestamp
#     random_seed = int(datetime.timestamp(datetime.now()))

#     # Randomly select 30 unique indices
#     random_indices = random.sample(range(len(data)), 30)

#     # Get the corresponding rows from the dataset
#     random_selection = [data[i] for i in random_indices]

#     # Print or use the randomly selected data as needed
#     for row in random_selection:
#         print(row)