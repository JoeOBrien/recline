import argparse
parser = argparse.ArgumentParser(description = 'Square a number')
parser.add_argument("square", help="display a square of a given number",
                    type=int)
def main():
    args = parser.parse_args()
    return args.square**2

if __name__ == "__main__":
    main()