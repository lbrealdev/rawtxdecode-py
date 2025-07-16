import sys


def main():
    args = sys.argv[1]

    if not args:
        print("Usage: main.py <raw-transaction-hash>")
        sys.exit(1)
    
    print(args)


if __name__ == '__main__':
    main()