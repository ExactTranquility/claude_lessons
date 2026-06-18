# claude_lessons
- Lesson plan developed personally using current projects I have already created written and reviewed by ChatGPT and Claude


# safe_division.py
- handles safely inputing two floats
- displays whole numbers, or two decimal points rounded for floats
- blocks invalid floats and dividebyzero errors

# file_reader.py
- get safe user input with whitespace stripped
- prompts to retry until the path is valid
    
# retry_number_input.py
- get_integer function loops until valid input
- valid min and max number assigned in parameters
- can be used as a standalone helper module

# week1_tracker.py
- a temporary list creator with retry option if you made a mistake adding or removing an item
- declines duplicate input and blank input
- formats input for blank list

# contact_book.py
- saves and loads a contact book to a local json file for persistant data
- add/delete/find/list contact functions
- rejects blank input when required (e.g. name, menu), optional fields default to "unknown" (e.g. phone_number and email)

# tracker_v2.py
- updates week1_tracker.py
- adds file persistence of the user's list using json
- now calls view_list and save_file anywhere data mutates for easier use by users
- now items are added by names, and deleted by index to reduce typos