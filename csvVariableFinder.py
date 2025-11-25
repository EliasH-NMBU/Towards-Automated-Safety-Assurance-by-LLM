import csv
import re

def load_and_validate_csv(path):
    with open(path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        return list(reader)

def extract_variables_from_ltl(ltl_expression):
    # Remove typical PTL operators and syntax
    cleaned = re.sub(r'\b(H|O|Y|Z|S|U|F|G|X|R)\b', ' ', ltl_expression)  # remove LTL operators
    cleaned = re.sub(r'[\|\&\!\(\)\=\>\<\+\-\*/0-9:\[\]\.,]', ' ', cleaned)  # remove logic and math symbols
    cleaned = re.sub(r'\b(TRUE|FALSE|if|then|else|in|when|until|always|eventually|before|after|for)\b', ' ', cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r'\s+', ' ', cleaned)  # normalize spaces
    
    # Extract variable-like tokens (words starting with letters/underscores)
    variables = re.findall(r'\b[a-zA-Z_][a-zA-Z0-9_]*\b', cleaned)
    return variables

def main():
    path = "lungFiles/lungVentilatorReq.csv"
    CSVDATA = load_and_validate_csv(path)
    
    all_vars = set()
    for row in CSVDATA:
        ltl_expr = row.get("LTL", "")
        if not ltl_expr.strip():
            continue
        vars_in_expr = extract_variables_from_ltl(ltl_expr)
        all_vars.update(vars_in_expr)
    
    print("✅ Extracted variables from LTL column:")
    for v in sorted(all_vars):
        print(v)
    
    print(f"\nTotal unique variables: {len(all_vars)}")

if __name__ == "__main__":
    main()
