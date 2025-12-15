from openai import OpenAI
import spot
import random
import csv
import re
import json


MODEL = "gpt-5-chat-latest"
client = OpenAI()


def load_jsonl(path):
    examples = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            obj = json.loads(line)

            nl = " ".join(obj["logic_sentence"])
            ltl = " ".join(obj["logic_ltl"])

            examples.append({
                "nl": nl.strip(),
                "ltl": ltl.strip()
            })
    return examples


def normalize_ltl(formula: str) -> str:
    f = formula
    replacements = {
        r'\bglobally\b': 'G',
        r'\bfinally\b': 'F',
        r'\buntil\b': 'U',
        r'\bimply\b': '->',
        r'\bequal\b': '<->',
        r'\band\b': '&',
        r'\bor\b': '|',
    }
    for pat, rep in replacements.items():
        f = re.sub(pat, rep, f)
    return " ".join(f.split())



def ltl_equivalent(f1: str, f2: str) -> bool:
    try:
        a1 = spot.translate(f1, 'det')
        a2 = spot.translate(f2, 'det')
        return spot.are_equivalent(a1, a2)
    except Exception as e:
        print("LTL parse error:", e)
        return False



def run_iteration(nl_text, reference_ltl):
    ref_norm = normalize_ltl(reference_ltl)

    prompt = f"""
Convert the requirement into a valid LTL formula using operators:
G, F, X, U, &, |, ->, <->, !.
Use only signals prop_1 ... prop_7.
Output only the formula.

Requirement: {nl_text}
"""

    answer = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You generate valid LTL formulas."},
            {"role": "user", "content": prompt}
        ],
        max_completion_tokens=256,
        temperature=1
    )

    generated = answer.choices[0].message.content.strip()
    gen_norm = normalize_ltl(generated)

    eq = ltl_equivalent(ref_norm, gen_norm)
    return ref_norm, gen_norm, eq



if __name__ == "__main__":

    examples = load_jsonl("lifted_data.jsonl")
    print("Loaded", len(examples), "examples")
    random.shuffle(examples)

    NUM_ITERATIONS = 100
    true_count = 0

    csv_path = "ltl_results.csv"

    with open(csv_path, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        # Header
        writer.writerow([
            "true/total",
            "natural_language",
            "reference_ltl",
            "generated_ltl",
            "equivalent"
        ])

        for i in range(NUM_ITERATIONS):
            ex = examples[i % len(examples)]

            print(f"\n=== Iteration {i+1}/{NUM_ITERATIONS} ===")

            ref_norm, gen_norm, eq = run_iteration(ex["nl"], ex["ltl"])

            if eq:
                true_count += 1

            ratio = f"{true_count}/{i+1}"

            print("NL:", ex["nl"])
            print("Reference:", ref_norm)
            print("Generated:", gen_norm)
            print("Equivalent:", eq)

            # Write CSV row
            writer.writerow([
                ratio,
                ex["nl"],
                ref_norm,
                gen_norm,
                eq
            ])

            # Ensure data is written even if interrupted
            f.flush()

    print("\nFinal Summary:", true_count, "/", NUM_ITERATIONS, "equivalent")
    print("Results saved to:", csv_path)
