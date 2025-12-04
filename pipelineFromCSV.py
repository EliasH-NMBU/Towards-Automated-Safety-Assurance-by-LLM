from openai import OpenAI
import csvHandler
import nuXmvHandler
import pandas as pd

MODEL = "gpt-5-chat-latest"
NUM_ITERATIONS = 10
TEMPERATURE = 0
EQUIVALENCE_HANDLER = nuXmvHandler.check_equivalence_lungV
FILEPATH = "lungFiles/lungVentilatorReq.csv"   # or .xlsx
VARIABLELIST = csvHandler.get_lung_ventilator_variable_table_info()

client = OpenAI()


# ============================================================
# Load CSV or XLSX file
# ============================================================
def load_ptltl_dataset(filepath):
    if filepath.endswith(".xlsx"):
        df = pd.read_excel(filepath)
    elif filepath.endswith(".csv"):
        df = pd.read_csv(filepath, sep=';')
    else:
        raise ValueError("File must be .csv or .xlsx")

    if "LTL" not in df.columns:
        raise ValueError("Your file must contain a column named 'LTL'")

    return df["LTL"].dropna().tolist()


# ============================================================
# Perform the NL → ptLTL round-trip cycle
# ============================================================
def run_cycle_with_given_ptltl(client, ptltl_base):

    # ============================================================
    # Step 2 — Convert ptLTL → natural language
    # ============================================================
    step2_prompt = (
        "Convert the following ptLTL requirement into natural language.\n"
        "Write a natural-language description that sounds like a real engineering requirement.\n"
        "Use robots, planes, cars, automation, drones, medical devices etc.\n"
        "Do not mention temporal logic. Keep the variable names exactly.\n"
        "Do not use markdown formatting. No bold, italics, lists, commas, semicolons.\n\n"
        f"Formula:\n{ptltl_base}"
    )

    step2 = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You convert temporal logic into natural language."},
            {"role": "user", "content": step2_prompt}
        ],
        max_completion_tokens=512,
        temperature=TEMPERATURE
    )

    nl_description = step2.choices[0].message.content.strip()

    # ============================================================
    # Step 3 — NL → ptLTL (regenerated)
    # ============================================================
    step3_prompt = (
        "Translate the following natural-language requirement into a plain-text "
        "past-time LTL (ptLTL) formula.\n\n"

        "The formula must use ONLY the variables:\n"
        "{VARIABLELIST}\n\n"

        "Use only ptLTL operators:\n"
        "- H φ (Historically)\n"
        "- O φ (Once)\n"
        "- Y φ (Yesterday)\n"
        "- φ S ψ (Since)\n\n"

        "Constraints:\n"
        "- Provide only the formula, no explanation.\n"
        "- Produce exactly ONE ptLTL formula.\n"
        "- Must be syntactically valid.\n"
        "- Strictly output only the formula.\n\n"

        f"Requirement:\n{nl_description}"
    )

    step3 = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You translate natural language back into ptLTL."},
            {"role": "user", "content": step3_prompt}
        ],
        max_completion_tokens=512,
        temperature=TEMPERATURE
    )

    ptltl_regen = step3.choices[0].message.content.strip()

    # ============================================================
    # Step 4 — Equivalence check
    # ============================================================
    equivalence = EQUIVALENCE_HANDLER(ptltl_base, ptltl_regen)

    if equivalence is not True and equivalence is not False:
        return None  # indicates failure → retry

    return ptltl_base, nl_description, ptltl_regen, equivalence


# ============================================================
# MAIN EXECUTION LOOP
# ============================================================
if __name__ == "__main__":

    # Path to your file

    ptltl_list = load_ptltl_dataset(FILEPATH)
    total_rows = len(ptltl_list)

    results = []
    true_count = 0
    iteration = 0

    while iteration < NUM_ITERATIONS:

        print(f"\n=== Iteration {iteration+1}/{NUM_ITERATIONS} ===")

        # Select a ptLTL at random from the dataset
        import random
        ptltl_base = random.choice(ptltl_list)

        cycleData = run_cycle_with_given_ptltl(client, ptltl_base)

        if not cycleData:
            print("⚠️  Skipping iteration due to GPT/NuXMV failure.")
            continue

        ptltl_1, nl_desc, ptltl_2, equivalence = cycleData

        if equivalence is True:
            true_count += 1

        # Clean NL for CSV
        nl_desc_clean = nl_desc.replace("\n", " ").replace(",", ";")

        results.append({
            "Summary": f"{true_count}/{iteration+1}",
            "ID": nl_desc_clean,
            "ptLTL": ptltl_1,
            "Generated ptLTL": ptltl_2,
            "Equivalence Check": equivalence
        })

        iteration += 1

    # Save results
    csvHandler.save_results_to_csv(results, temperature=str(TEMPERATURE))
