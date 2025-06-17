import pandas as pd
import requests


df = pd.read_csv("health_prompts.csv")
results = []

for idx, row in df.iterrows():
    prompt = row['prompt']
    try:
        response = requests.post(
            "http://127.0.0.1:8000/retrieve",
            json={"prompt": prompt},
            timeout=10
        )
        if response.status_code == 200:
            result = "success"
        else:
            result = f"fail ({response.status_code})"
    except Exception as e:
        result = f"fail ({str(e)})"
    
    results.append({
        "prompt": prompt,
        "health_ailment": row['health_ailment'],
        "date": row['date'],
        "result": result
    })

results_df = pd.DataFrame(results)
results_df.to_csv("test_results.csv", index=False)

print("Done! Results saved to test_results.csv")
