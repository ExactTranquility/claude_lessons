
def safe_float(prompt: str) -> float:
    while True:
        raw = input(prompt)
        try:
            return float(raw)
        except ValueError:
            print("Sorry, that is not a valid number, please try again.")

    
        
def safe_divide(num: float, den: float) -> None | float:
    try:
        return (num / den)
    except ZeroDivisionError:
        print("Denominator cannot be zero")
        return None    


def format_float_2f_non_whole(raw: float) -> str:
    if raw % 1 == 0:
        return str(int(raw))
    return f"{raw:.2f}"
    

def main() -> None:
    while True:
        numerator = safe_float("First number? : ")
        denominator = safe_float("Second number?: ")
    
        quotient = safe_divide(numerator, denominator)
        
        if quotient is not None:
            print(f"Your answer is {format_float_2f_non_whole(quotient)}")
            break
            

if __name__ ==  "__main__":
    main()