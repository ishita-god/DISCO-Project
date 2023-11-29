def sort_courses(course_list):
    sorted_courses= []
    def sort_key(course):
        # Split the course name into parts
        parts = course.split()

        # Find the last part that represents the number
        for part in reversed(parts):
            if part.isdigit():
                return int(part)
        return float('inf')

    # Sort the course list using the custom key function
    sorted_courses = sorted(course_list, key=sort_key)
    return sorted_courses

# list1= ['CDC_COURSE 7', 'CDC_COURSE 8', 'CDC_COURSE 2', 'CDC_COURSE 1', 'CDC_COURSE 9', 'CDC_COURSE 4','CDC_COURSE 6','CDC_COURSE 5']
# print(sort_courses(list1))