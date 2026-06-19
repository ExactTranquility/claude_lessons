## DONE
# clean_text
# word_count

## Add
# get_clean_input
# get_non_empty

def clean_text(text: str) -> str:
    return " ".join(text.split())


def word_count(text: str) -> int:
    return len(text.split())


def get_clean_input(prompt: str) -> str:
    return clean_text(input(prompt))


def get_non_empty(prompt: str) -> str:
    while True:
        user_input = get_clean_input(prompt)

        if clean_text(user_input):
            return user_input
        else:
            print("Entry cannot be empty")