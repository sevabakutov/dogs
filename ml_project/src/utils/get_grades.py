def get_grade_types(grades_type: str):
    if grades_type == "-gen":
        return ['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9', 'A10']
    if grades_type == "-hp":
        return ['HP']
    if grades_type == "-all":
        return []
    else:
        return grades_type.split(" ")