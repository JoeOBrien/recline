import argparse

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('integers', metavar='N', type=int, nargs='+',
                   help='An integer for the accumulator')
parser.add_argument('--sum', dest='accumulate', action='store_const',
                   const=sum, default=max,
                   help='Sum the integers (default: find the max)')

def main():
    args = parser.parse_args()
    print args.accumulate(args.integers)

if __name__ == "__main__":
    main()
