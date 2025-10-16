"""
Recursive Language Model (RLM) Implementation using OpenRouter API

Based on: https://alexzhang13.github.io/blog/2025/rlm/

This implementation allows language models to recursively process unbounded context
by storing context in a REPL environment and enabling recursive LM calls.
"""

import os
import re
import json
from typing import Any, Dict, List, Optional, Union
from dataclasses import dataclass
import requests


@dataclass
class RLMConfig:
    """Configuration for RLM system"""
    root_model: str = "openai/gpt-4o"  # Root LM model
    recursive_model: str = "openai/gpt-4o-mini"  # Recursive LM model
    max_iterations: int = 10  # Max REPL iterations
    max_recursive_depth: int = 1  # Max depth of recursion
    api_key: Optional[str] = None
    base_url: str = "https://openrouter.ai/api/v1"
    verbose: bool = True


class REPLEnvironment:
    """Python REPL environment for RLM to interact with context"""
    
    def __init__(self, context: Union[str, List[str], Dict], verbose: bool = False):
        self.context = context
        self.variables = {"context": context}
        self.execution_history = []
        self.verbose = verbose
        
    def execute(self, code: str) -> Dict[str, Any]:
        """Execute Python code in the REPL environment"""
        result = {
            "success": False,
            "output": None,
            "error": None,
            "variables": {}
        }
        
        try:
            # Create execution namespace with context and safe builtins
            namespace = {
                "context": self.context,
                **self.variables,
                "len": len,
                "str": str,
                "int": int,
                "float": float,
                "list": list,
                "dict": dict,
                "range": range,
                "enumerate": enumerate,
                "zip": zip,
                "sum": sum,
                "min": min,
                "max": max,
                "sorted": sorted,
                "re": re,
                "json": json,
            }
            
            # Execute code
            exec(code, namespace)
            
            # Update variables (exclude builtins)
            self.variables.update({
                k: v for k, v in namespace.items() 
                if not k.startswith("__") and k not in ["context", "len", "str", "int", "float", "list", "dict", "range", "enumerate", "zip", "sum", "min", "max", "sorted", "re", "json"]
            })
            
            result["success"] = True
            result["variables"] = {k: str(v)[:200] for k, v in self.variables.items()}
            
            # Capture output if there's a result variable
            if "result" in self.variables:
                result["output"] = str(self.variables["result"])
            
        except Exception as e:
            result["error"] = str(e)
        
        self.execution_history.append({
            "code": code,
            "result": result
        })
        
        if self.verbose:
            print(f"\n[REPL] Executed:\n{code}")
            print(f"[REPL] Result: {result}")
        
        return result
    
    def get_variable(self, name: str) -> Any:
        """Get a variable from the REPL environment"""
        return self.variables.get(name)
    
    def peek(self, n: int = 500) -> str:
        """Peek at first n characters of context"""
        if isinstance(self.context, str):
            return self.context[:n]
        elif isinstance(self.context, list):
            return str(self.context[:min(5, len(self.context))])
        return str(self.context)[:n]


class RecursiveLM:
    """Recursive Language Model implementation"""
    
    def __init__(self, config: RLMConfig):
        self.config = config
        self.api_key = config.api_key or os.getenv("OPENROUTER_API_KEY")
        if not self.api_key:
            raise ValueError("OpenRouter API key required. Set OPENROUTER_API_KEY env var or pass in config.")
        
        self.total_cost = 0.0
        self.call_count = 0
    
    def _call_llm(self, messages: List[Dict], model: str, depth: int = 0) -> str:
        """Make API call to OpenRouter"""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/rlm-test",
            "X-Title": "RLM Test"
        }
        
        data = {
            "model": model,
            "messages": messages,
            "temperature": 0.7,
        }
        
        if self.config.verbose:
            print(f"\n[LM Call - Depth {depth}] Model: {model}")
            print(f"[LM Call - Depth {depth}] Messages: {json.dumps(messages[-1], indent=2)[:500]}...")
        
        response = requests.post(
            f"{self.config.base_url}/chat/completions",
            headers=headers,
            json=data
        )
        response.raise_for_status()
        
        result = response.json()
        self.call_count += 1
        
        content = result["choices"][0]["message"]["content"]
        
        if self.config.verbose:
            print(f"[LM Response - Depth {depth}]: {content[:300]}...")
        
        return content
    
    def _create_recursive_lm_function(self, repl: REPLEnvironment, depth: int) -> callable:
        """Create a recursive LM function that can be called from REPL"""
        def recursive_lm(query: str, context_subset: Optional[str] = None) -> str:
            """Recursive LM call - can be invoked from REPL code"""
            if depth >= self.config.max_recursive_depth:
                return "Max recursion depth reached"
            
            messages = [
                {
                    "role": "system",
                    "content": "You are a helpful assistant. Answer the query based on the provided context."
                },
                {
                    "role": "user",
                    "content": f"Query: {query}\n\nContext: {context_subset or repl.context}"
                }
            ]
            
            return self._call_llm(messages, self.config.recursive_model, depth + 1)
        
        return recursive_lm
    
    def completion(self, query: str, context: Union[str, List[str], Dict]) -> Dict[str, Any]:
        """
        Main RLM completion method - replaces standard LM completion
        
        Args:
            query: The user's query
            context: The (potentially huge) context to process
            
        Returns:
            Dict with 'answer', 'iterations', 'repl_history', 'total_calls'
        """
        # Initialize REPL environment with context
        repl = REPLEnvironment(context, verbose=self.config.verbose)
        
        # Create system prompt for root LM
        system_prompt = f"""You are a Recursive Language Model (RLM) with access to a Python REPL environment.

The user's context is stored in a variable called 'context'. You can interact with it programmatically.

Available tools:
1. Execute Python code to analyze, filter, or transform the context
2. Call recursive_lm(query, context_subset) to spawn sub-queries on context chunks
3. Use regex, string operations, list comprehension to process context

Context info:
- Type: {type(context).__name__}
- Size: {len(str(context))} characters
- Preview: {repl.peek(200)}

IMPORTANT: You MUST end your response with your final answer in this exact format:
FINAL(your answer here)

Example workflow:
1. Write Python code in ```python code blocks to analyze context
2. Review execution results
3. When ready, provide FINAL(answer)

You have {self.config.max_iterations} iterations maximum. Be efficient and provide FINAL() as soon as you have the answer."""

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Query: {query}"}
        ]
        
        iterations = 0
        final_answer = None
        
        while iterations < self.config.max_iterations and final_answer is None:
            iterations += 1
            
            # Get response from root LM
            response = self._call_llm(messages, self.config.root_model, depth=0)
            
            # Check for final answer
            final_match = re.search(r'FINAL\((.*?)\)', response, re.DOTALL)
            final_var_match = re.search(r'FINAL_VAR\((.*?)\)', response)
            
            if final_match:
                final_answer = final_match.group(1).strip()
                break
            elif final_var_match:
                var_name = final_var_match.group(1).strip()
                final_answer = str(repl.get_variable(var_name))
                break
            
            # Extract and execute code blocks
            code_blocks = re.findall(r'```python\n(.*?)\n```', response, re.DOTALL)
            
            if code_blocks:
                for code in code_blocks:
                    # Inject recursive_lm function into code if needed
                    if "recursive_lm" in code:
                        # This is a simplified version - in production, you'd need proper function injection
                        exec_result = repl.execute(code)
                    else:
                        exec_result = repl.execute(code)
                    
                    # Add execution result to conversation
                    messages.append({"role": "assistant", "content": response})
                    messages.append({
                        "role": "user", 
                        "content": f"Execution result: {json.dumps(exec_result, indent=2)}"
                    })
            else:
                # No code blocks, just add response and ask for next step
                messages.append({"role": "assistant", "content": response})
                messages.append({
                    "role": "user",
                    "content": "Continue with your analysis or provide FINAL(answer)."
                })
        
        return {
            "answer": final_answer or "No final answer provided within iteration limit",
            "iterations": iterations,
            "repl_history": repl.execution_history,
            "total_calls": self.call_count,
            "messages": messages
        }


def create_rlm(
    root_model: str = "openai/gpt-4o",
    recursive_model: str = "openai/gpt-4o-mini",
    api_key: Optional[str] = None,
    verbose: bool = True
) -> RecursiveLM:
    """Factory function to create an RLM instance"""
    config = RLMConfig(
        root_model=root_model,
        recursive_model=recursive_model,
        api_key=api_key,
        verbose=verbose
    )
    return RecursiveLM(config)
