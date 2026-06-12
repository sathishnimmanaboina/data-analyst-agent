import asyncio
import json
import sys
from agent import run_agent
from eval import run_evals, TEST_CASES, score_response
import claude_agent_sdk

# Different system prompts to try — each one gives Claude different instructions
PROMPT_VARIANTS = [
    {
        "label": "baseline",
        "prompt": """You are a data analyst agent. You have access to CSV files in the data/ folder.
When asked a question about data, read the file and answer clearly with exact numbers."""
    },
    {
        "label": "step_by_step",
        "prompt": """You are a precise data analyst agent. You have access to CSV files in the data/ folder.

ALWAYS follow these steps:
1. Read the CSV file first
2. List the relevant rows or columns you found
3. Show your calculation step by step
4. State the final answer clearly on its own line starting with "ANSWER:"

Be exact with numbers. Double-check your arithmetic."""
    },
    {
        "label": "calculation_focused",
        "prompt": """You are a data analyst agent specialized in numerical accuracy.

When answering questions:
- Always read the source CSV file first
- Show the exact numbers you are working with
- Show the sum/average/count calculation explicitly  
- Give the final numeric answer prominently
- For rankings, list top 3 not just the winner

Data files are in the data/ folder."""
    },
]


async def run_optimizer():
    """Try each prompt variant, find the best one."""
    
    print("\n⚡ OPTIMIZER — Finding the best system prompt")
    print("=" * 60)
    
    all_results = []
    
    for variant in PROMPT_VARIANTS:
        print(f"\n🔄 Testing variant: [{variant['label']}]")
        
        # Temporarily patch the system prompt in agent.py
        import agent
        original_prompt = agent.SYSTEM_PROMPT
        agent.SYSTEM_PROMPT = variant["prompt"]
        
        # Run evals with this prompt
        result = await run_evals(variant["label"])
        all_results.append(result)
        
        # Restore original
        agent.SYSTEM_PROMPT = original_prompt
    
    # Find the best
    best = max(all_results, key=lambda x: x["average_score"])
    
    print("\n" + "=" * 60)
    print("📈 OPTIMIZATION RESULTS SUMMARY")
    print("=" * 60)
    for r in all_results:
        bar = "█" * int(r["average_score"] * 20)
        print(f"  {r['label']:25s} | {bar:20s} | {r['average_score']:.3f}")
    
    print(f"\n🏆 Best variant: [{best['label']}] with score {best['average_score']:.3f}")
    improvement = best["average_score"] - all_results[0]["average_score"]
    if improvement > 0:
        print(f"📈 Improvement over baseline: +{improvement:.3f} ({improvement*100:.1f}%)")
    else:
        print("ℹ️  Baseline was already the best — no improvement needed.")
    
    # Save full comparison
    comparison = {
        "all_variants": all_results,
        "best_variant": best["label"],
        "best_score": best["average_score"],
        "baseline_score": all_results[0]["average_score"],
        "improvement": round(improvement, 3)
    }
    with open("results/optimizer_comparison.json", "w") as f:
        json.dump(comparison, f, indent=2)
    print("\n💾 Full comparison saved to results/optimizer_comparison.json")


if __name__ == "__main__":
    asyncio.run(run_optimizer())