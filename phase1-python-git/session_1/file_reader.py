

def read_file(path: str) -> str | None:
    try:
        with open(path, 'r') as f:
            return f.read()
    except FileNotFoundError:
        print(f"File not found: {path}")
        return None
        
def main() -> None:
    user_input = read_file("text.txt")
    
    if user_input:
        print(user_input)
    else:
        print("failed")


if __name__ == "__main__":
    main()
