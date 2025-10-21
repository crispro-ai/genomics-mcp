#!/usr/bin/env python3
"""
Clinical Genomics Domain Test Runner

Runs tasks through LLM agent and evaluates results.
"""

import json
import yaml
import argparse
from pathlib import Path
from typing import Dict, List, Any
import os
import sys

# Add parent directory to path to import evaluators
sys.path.insert(0, str(Path(__file__).parent.parent))


def load_domain_config(domain: str) -> Dict[str, Any]:
    """Load domain configuration."""
    config_path = Path(f"domains/{domain}/config.yaml")
    with open(config_path) as f:
        return yaml.safe_load(f)


def load_task(task_path: str) -> Dict[str, Any]:
    """Load task JSON."""
    with open(task_path) as f:
        return json.load(f)


def run_agent_on_task(task: Dict[str, Any], model: str = "gpt-4o") -> Dict[str, Any]:
    """
    Run LLM agent on task.
    
    This is a simplified version - you'd integrate with:
    - OpenAI API
    - LangChain/LangGraph for agent loops
    - MCP server connections
    """
    from openai import OpenAI
    
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    
    # Build system prompt
    system_prompt = """You are a clinical genomics AI assistant.
    
Your capabilities:
- Interpret genetic variants using ClinVar and ACMG/AMP guidelines
- Recommend treatments based on genomic profiles
- Match patients to clinical trials
- Analyze drug-gene interactions
- Synthesize evidence from medical literature

Always cite sources and quantify uncertainty."""
    
    # Run agent (simplified - real version would use tools/MCP servers)
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": task["question"]}
        ],
        temperature=0.1  # Low temp for medical accuracy
    )
    
    return {
        "result": response.choices[0].message.content,
        "model": model,
        "usage": {
            "prompt_tokens": response.usage.prompt_tokens,
            "completion_tokens": response.usage.completion_tokens
        }
    }


def evaluate_response(task: Dict[str, Any], agent_response: Dict[str, Any]) -> Dict[str, Any]:
    """
    Evaluate agent response using task evaluators.
    """
    # Import evaluator functions dynamically
    domain = task.get("domain", "clinical_genomics")
    evaluators_module = __import__(f"domains.{domain}.evaluators.functions", fromlist=[""])
    
    results = {
        "task": task.get("id", "unknown"),
        "passed": True,
        "scores": [],
        "errors": []
    }
    
    for evaluator in task.get("evaluators", []):
        try:
            eval_func_name = evaluator["op"].split(".")[-1]
            eval_func = getattr(evaluators_module, eval_func_name)
            
            # Run evaluator
            eval_result = eval_func(
                question=task["question"],
                llm_response=agent_response,
                op_args=evaluator.get("op_args", {})
            )
            
            results["scores"].append({
                "evaluator": eval_func_name,
                "score": eval_result.get("score", 0),
                "passed": eval_result.get("passed", False),
                "feedback": eval_result.get("feedback", "")
            })
            
            if not eval_result.get("passed", False):
                results["passed"] = False
                
        except Exception as e:
            results["errors"].append({
                "evaluator": evaluator["op"],
                "error": str(e)
            })
            results["passed"] = False
    
    return results


def run_tests(domain: str, runs: int = 3, output_dir: str = "results/") -> Dict[str, Any]:
    """
    Run full test suite for domain.
    """
    print(f"🧬 Running tests for domain: {domain}")
    print(f"📊 Pass@{runs} testing (each task runs {runs} times)")
    
    # Load config
    config = load_domain_config(domain)
    tasks = config.get("tasks", [])
    
    # Create output directory
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Run tests
    all_results = []
    pass_at_1_count = 0
    pass_at_k_count = 0
    
    for task_file in tasks:
        task_path = f"domains/{domain}/{task_file}"
        print(f"\n📝 Testing: {task_file}")
        
        task = load_task(task_path)
        task["id"] = Path(task_file).stem
        
        # Run multiple times for Pass@K
        run_results = []
        for run_num in range(runs):
            print(f"  Run {run_num + 1}/{runs}...", end=" ")
            
            try:
                # Run agent
                agent_response = run_agent_on_task(task)
                
                # Evaluate
                eval_result = evaluate_response(task, agent_response)
                eval_result["run"] = run_num + 1
                run_results.append(eval_result)
                
                status = "✅" if eval_result["passed"] else "❌"
                print(status)
                
            except Exception as e:
                print(f"❌ Error: {e}")
                run_results.append({
                    "run": run_num + 1,
                    "passed": False,
                    "error": str(e)
                })
        
        # Calculate Pass@1 and Pass@K
        pass_at_1 = run_results[0]["passed"] if run_results else False
        pass_at_k = any(r["passed"] for r in run_results)
        
        if pass_at_1:
            pass_at_1_count += 1
        if pass_at_k:
            pass_at_k_count += 1
        
        all_results.append({
            "task": task["id"],
            "runs": run_results,
            "pass_at_1": pass_at_1,
            "pass_at_k": pass_at_k
        })
    
    # Calculate overall metrics
    total_tasks = len(tasks)
    summary = {
        "domain": domain,
        "total_tasks": total_tasks,
        "runs_per_task": runs,
        "pass_at_1": round((pass_at_1_count / total_tasks) * 100, 1),
        "pass_at_k": round((pass_at_k_count / total_tasks) * 100, 1),
        "categories": []  # TODO: Group by task category
    }
    
    # Save results
    with open(output_path / "results.json", "w") as f:
        json.dump(all_results, f, indent=2)
    
    with open(output_path / "summary.json", "w") as f:
        json.dump(summary, f, indent=2)
    
    # Print summary
    print("\n" + "="*60)
    print(f"📊 TEST RESULTS SUMMARY")
    print("="*60)
    print(f"Domain: {domain}")
    print(f"Total Tasks: {total_tasks}")
    print(f"Pass@1: {summary['pass_at_1']}%")
    print(f"Pass@{runs}: {summary['pass_at_k']}%")
    print(f"\nTarget Range: 30-70% Pass@1")
    
    if 30 <= summary['pass_at_1'] <= 70:
        print("✅ Pass@1 in target range!")
    elif summary['pass_at_1'] < 30:
        print("⚠️  Pass@1 too low - tasks may be too hard")
    else:
        print("⚠️  Pass@1 too high - tasks may be too easy")
    
    return summary


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run clinical genomics domain tests")
    parser.add_argument("--domain", default="clinical_genomics", help="Domain to test")
    parser.add_argument("--runs", type=int, default=3, help="Number of runs per task (Pass@K)")
    parser.add_argument("--output", default="results/", help="Output directory for results")
    
    args = parser.parse_args()
    
    try:
        summary = run_tests(args.domain, args.runs, args.output)
        
        # Exit with error if not in target range
        if summary['pass_at_1'] < 30 or summary['pass_at_1'] > 70:
            sys.exit(1)
            
    except Exception as e:
        print(f"\n❌ Test run failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

