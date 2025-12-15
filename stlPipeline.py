from openai import OpenAI
import spot
import random
import json

MODEL = "gpt-5-chat-latest"
client = OpenAI()

def normalize_ltl(formula: str) -> str:
    import re
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
    # Normalize dataset formula
    ref_norm = normalize_ltl(reference_ltl)

    # Ask GPT to regenerate LTL from NL
    prompt = f"""
Convert the requirement into a valid LTL formula using operators:
G, F, X, U, &, |, ->, <->, !.
Use only signals prop_1 ... prop_7.
Output only the formula.

Requirement: {nl_text}
"""
    answer = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "system", "content": "You generate valid LTL formulas."},
                  {"role": "user", "content": prompt}],
        max_completion_tokens=256
    )

    generated = answer.choices[0].message.content.strip()
    gen_norm = normalize_ltl(generated)

    # Check equivalence with SPOT
    eq = ltl_equivalent(ref_norm, gen_norm)

    return ref_norm, gen_norm, eq


if __name__ == "__main__":
    # Example dataset entry
    examples = [
        {
            "nl": "If prop_1 is true then eventually prop_2 should become true",
            "ltl": "(prop_1 imply finally prop_2)"
        },
        {
            "nl": "Continue with prop_2 until prop_3 happens, and ensure prop_4 also holds",
            "ltl": "((prop_2 until prop_3) and prop_4)"
        }
    ]

    NUM_ITERATIONS = 5
    true_count = 0

    for i in range(NUM_ITERATIONS):
        ex = random.choice(examples)

        print(f"\n=== Iteration {i+1}/{NUM_ITERATIONS} ===")

        ref_norm, gen_norm, eq = run_iteration(ex["nl"], ex["ltl"])

        print("NL:", ex["nl"])
        print("Reference:", ref_norm)
        print("Generated:", gen_norm)
        print("Equivalent:", eq)

        if eq:
            true_count += 1

    print("\nSummary:", true_count, "/", NUM_ITERATIONS, "equivalent")
