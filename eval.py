import asyncio
import json
import os
from datetime import datetime
from agent import run_agent

# Test cases: question, expected keywords that MUST appear in the answer
TEST_CASES = [
    {
        "id": "tc_01",
        "question": "What is the total sales amount for the Laptop product across all months?",
        "expected_keywords": ["laptop", "326000"],  # sum of all laptop sales
        "description": "Total sales for one product"
    },
    {
        "id": "tc_02", 
        "question": "Which month had the highest total sales amount?",
        "expected_keywords": ["june"],
        "description": "Best month by sales"
    },
    {
        "id": "tc_03",
        "question": "Which sales rep has the most total units sold?",
        "expected_keywords": ["bob"],  # Bob: 40+35+21+55 = 151 units
        "description": "Top sales rep by units"
    },
    {
        "id": "tc_04",
        "question": "What is the average sales amount per transaction?",
        "expected_keywords": ["35"],  # rough average around 35000
        "description": "Average transaction value"
    },
    {
        "id": "tc_05",
        "question": "Which region had the highest total sales?",
        "expected_keywords": ["north", "south"],  # north or south are close
        "description": "Top region by sales"
    },
]

def score_response(response: str, expected_keywords: list) -> float:
    """
    Score a response from 0.0 to 1.0.
    Score = percentage of expected keywords found in the response.
    """
    response_lower = response.lower()
    found = sum(1 for kw in expected_keywords if kw.lower() in response_lower)
    return found / len(expected_keywords)

async def run_evals(system_prompt_label: str = "default") -> dict:
    """Run all test cases and return scores."""
    
    print(f"\n🧪 Running Evals [{system_prompt_label}]")
    print("=" * 60)
    
    results = []
    total_score = 0
    
    for tc in TEST_CASES:
        print(f"\n📌 Test: {tc['description']}")
        print(f"   Q: {tc['question']}")
        
        response = await run_agent(tc["question"], verbose=False)
        score = score_response(response, tc["expected_keywords"])
        total_score += score
        
        status = "✅" if score >= 0.5 else "❌"
        print(f"   {status} Score: {score:.2f} | Keywords found: {[kw for kw in tc['expected_keywords'] if kw.lower() in response.lower()]}")
        
        results.append({
            "id": tc["id"],
            "description": tc["description"],
            "score": score,
            "response_snippet": response[:200]
        })
    
    average = total_score / len(TEST_CASES)
    
    summary = {
        "label": system_prompt_label,
        "timestamp": datetime.now().isoformat(),
        "average_score": round(average, 3),
        "results": results
    }
    
    print(f"\n📊 Average Score: {average:.2f} / 1.00")
    
    # Save results
    os.makedirs("results", exist_ok=True)
    filepath = f"results/eval_{system_prompt_label}_{datetime.now().strftime('%H%M%S')}.json"
    with open(filepath, "w") as f:
        json.dump(summary, f, indent=2)
    print(f"💾 Saved to {filepath}")
    
    return summary


if __name__ == "__main__":
    asyncio.run(run_evals("baseline"))