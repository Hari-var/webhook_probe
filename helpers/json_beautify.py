import json
import ast                                                                                                                                                                                                                                            

def beautify_json(json_string: str) -> str:
    try:
        # Try JSON first
        parsed = json.loads(json_string)
    except json.JSONDecodeError:
        try:
            # Try Python dict string
            parsed = ast.literal_eval(json_string)
        except Exception:
            return json_string

    return json.dumps(parsed, indent=4)

if __name__ == "__main__":
    input_file = input("Enter input file: ")
    output_file = input("Enter output file: ")

    with open(input_file, "r") as f:
        data = f.read()

    with open(output_file, "w") as f:
        f.write(beautify_json(data))