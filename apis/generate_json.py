import json

def generate_json(num_lines):
    data = []

    for i in range(1, num_lines + 1):
        entry = {
            "id": i,
            "name": "Name {}".format(i),
            "age": 20 + (i % 10),
            "city": "City {}".format(i)
        }
        data.append(entry)

    with open("data.json", "w") as json_file:
        json.dump(data, json_file, indent=4)

if __name__ == "__main__":
    num_lines = int(input("Enter the number of lines for the JSON file: "))
    generate_json(num_lines)
    print(f"{num_lines} lines of JSON data have been generated and saved to 'data.json'.")
