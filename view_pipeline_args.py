with open("pipeline.py", "r", encoding="utf-8") as f:
    for line in f:
        if "add_argument" in line:
            print(line.strip())
