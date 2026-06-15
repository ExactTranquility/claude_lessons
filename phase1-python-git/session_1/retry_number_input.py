

def get_integer(prompt: str, min_val: int, max_val: int) -> int:
    
    while True:
        user_input = input(prompt)
        
        try:
            user_input = int(user_input)
        except ValueError:
            print("Unfortunately that is not a number, please try again.")
            continue
            
        if user_input < min_val or user_input > max_val:
            print(f"That number is out of range, please choose a number between {min_val} and {max_val}")
            continue
            
        return user_input


def main() -> None:
    print(get_integer("Please enter a number between 0 and 120: ", 0, 120))

if __name__ == "__main__":
    main() 
