import sys
import pandas as pd

def main():
    day = int(sys.argv[1])
    df = pd.DataFrame({
        "A": [1,2],
        "B": [3,4]
    })
    print("Hello from workshop!")
    print(f"day: {day}")
    df.to_parquet(f"output_day_{day}.parquet")


if __name__ == "__main__":
    main()
