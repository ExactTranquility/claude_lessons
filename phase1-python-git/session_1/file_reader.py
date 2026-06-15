

# Strips whitespace, keeps user formatting
def get_input(prompt: str) -> str:
    while True:
        raw = input(prompt)
        if not raw.strip():
            print("Field cannot be empty, try again.")
            continue
        return raw.strip()


def read_file(path: str) -> str | None:
    try:
        with open(path, 'r') as f:
            return f.read()
    except FileNotFoundError:
        print(f"File not found: {path}")
        return None

        
def main() -> None:
    while True:
        user_input = get_input("What file do you want to see? : ")
        file = read_file(user_input)
    
        if file:
            print(file)
            break
        else:
            print("Reading failed, please try another file name")


if __name__ == "__main__":
    main()
