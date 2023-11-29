import csv
import numpy as np
from hungarian_algo import hungarian_algorithm, ans_calculation
from sorted_courses import sort_courses
from random_generator import random_rows
from itertools import islice

def process_csv():
    with open('faculty_preference.csv', 'r') as file:
        csvreader = csv.reader(file)
        next(csvreader) # Skip the header row
        CDC_list = []
        ELEC_list = []
        prof_list = []
        professor = []
        
        #rows = random_rows(csvreader) #get 30 random rows for differetn test cases
        rows = islice(csvreader, 30)

        for row in rows:
            try: #If there are blank/unreadable rows in faculty_preference
                # Process the element as needed
                name = row[0]
                category = row[1]
                prefs = row[2:]
                professor.append({
                    'name':name,
                    'category':category,
                    'prefs':prefs
                })
                for i in prefs:
                    if 'CDC' in i:
                        CDC_list.append(i)
                    else:
                        ELEC_list.append(i)
                """ Here we append the professor names to the list of profs 
                depending on number of times we can divide it by 0.5, to help 1:1 mapping """
                if category == 'x1':
                    prof_list.append(name)
                elif category == 'x2':
                    prof_list.append(name)
                    prof_list.append(name)
                elif category == 'x3':
                    prof_list.append(name)
                    prof_list.append(name)
                    prof_list.append(name)

            except IndexError as e:
                print(f"Error: {e}. Skipping row.")
                continue
                
    return set(CDC_list), set(ELEC_list), professor, prof_list # Ensure unique courses for our initial data


CDC_set, ELEC_set, professor, prof_list = process_csv()

CDC_list = sort_courses(list(CDC_set) * 2)   # Duplicated so we can treat each course and professor mapping as 1:1
ELEC_list = sort_courses(list(ELEC_set) * 2)  # Duplicated so we can treat each course and professor mapping as 1:1
# Determine the size of the square matrix (maximum length of CDC_set or ELEC_set)
matrix_size = max(len(CDC_list), len(prof_list))

# Initialize square matrices with zeros
CDC_arr = np.full((matrix_size, matrix_size),1000, dtype=int) #initilizing all elements with dummy data
ELEC_arr = np.full((matrix_size, matrix_size),1000,dtype=int) #initilizing all elements with dummy data

# Iterate over each professor
for idx, i in enumerate(prof_list):
    # Find the corresponding professor in the 'professor' list
    prof_info = next((p for p in professor if p['name'] == i), None)
    
    if prof_info:
        # Extract the preferences list for the professor
        prefs = prof_info['prefs']
        cdc_row = []
        elec_row = []

        # Populate CDC_arr
        for k in CDC_list:
            if k in prefs:
                index=prefs.index(k) + 1 #To make sure preference goes from 1.. not 0
                cdc_row.append(index)
            else:
                cdc_row.append(1000)
        
        # Use slicing to ensure the correct length
        CDC_arr[idx, :len(cdc_row)] = cdc_row[:matrix_size]

        for k in ELEC_set:

            if k in prefs:
                index=prefs.index(k) + 1 #To make sure preference goes from 1.. not 0
                elec_row.append(index)
            else:
                elec_row.append(1000)
        
        # Use slicing to ensure the correct length
        ELEC_arr[idx, :len(elec_row)] = elec_row[:matrix_size]

print(CDC_arr)
ans_pos = hungarian_algorithm(CDC_arr.copy())
ans, ans_mat = ans_calculation(CDC_arr, ans_pos)
print(ans_mat)

output = []
for i in range(len(ans_mat)):
    try:
        # Attempt to access the element at the maximum index in CDC_list
        assigned_cdc = CDC_list[np.argmax(ans_mat[i])]

        # Append the tuple to the output list
        output.append((prof_list[i], assigned_cdc))

    except IndexError:
        # Handle the IndexError (e.g., print a message or assign a default value)
        print(f"IndexError occurred for prof_list[{i}]")


print('\n', output)


# course_profs = {}

# # Group tuples by course and store professors in a list
# for prof, course in output:
#     if course not in course_profs:
#         course_profs[course] = [prof]
#     else:
#         course_profs[course].append(prof)

prof_courses = {} 
#output is a list of tuples with each prof assigned to 1 course, but some profs 
#teach two courses so they are compiled

# Group tuples by professor and store courses in a list
for prof, course in output:
    if prof not in prof_courses:
        prof_courses[prof] = [course]
    else:
        prof_courses[prof].append(course)
print(prof_courses)
# Check for professors assigned the same course
profs_left_to_assign=[]
for prof, courses in prof_courses.items():

    if len(set(courses)) < len(courses):
        print(f"Professor {prof} is assigned the same course multiple times: {courses}")
    




#For Testing
with open('CDC_course_list.csv', 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(CDC_list)
    for line in CDC_arr:
        csvwriter.writerow(line)


with open('ELEC_course_list.csv', 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(ELEC_list)
    for line in ELEC_arr:
        csvwriter.writerow(line)


def check_prof_requirements(prof_category, assigned_courses):
    if prof_category == 'x1':
        return 1 - assigned_courses
    elif prof_category == 'x2':
        return 2 - assigned_courses
    elif prof_category == 'x3':
        return 3 - assigned_courses
    else:
        return 0  # Default case, no requirement
def proffs_left():
    prof_left = {}
    for prof, courses in prof_courses.items():
        category = next((p['category'] for p in professor if p['name'] == prof), None)
        requirements_left = check_prof_requirements(category, len(courses))
        if requirements_left > 0:
            prof_left[prof] = requirements_left

    print("Professors left to assign:")
    print(prof_left)