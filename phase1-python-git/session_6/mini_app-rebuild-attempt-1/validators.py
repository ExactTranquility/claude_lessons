from string_utils import clean_text, get_non_empty

def safe_float(text: str) -> float | None:
    try:
        return float(text)
    except ValueError:
        return None
    

def is_non_empty(text: str) -> bool:
    return bool(clean_text(text))


def get_float(prompt: str) -> float:
    while True:
        user_input = safe_float(get_non_empty(prompt))

        if user_input is not None:
            return user_input
        else:
            print("Invalid number, please try again")


def get_two_float() -> tuple[float, float]:
    float_a = get_float("First number :")
    float_b = get_float("Second Number")

    return float_a, float_b


def format_number(num: float) -> str:
    formatted = f"{num:.2f}"
    if formatted == "0.00":
        return "0"
    return formatted