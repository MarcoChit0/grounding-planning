from typing import Optional, Tuple
import subprocess


def val(domain_path: str, problem_path: str, plan_path: str) -> Tuple[bool, Optional[str]]:
    """
    Validate a plan using VAL.

    Returns:
        tuple: (is_valid, error_message)
        - is_valid: True if plan is valid, False otherwise
        - error_message: Error message if invalid, None if valid
    """
    command = [
        "validate",
        "-v",
        "-t", "0.001",
        domain_path,
        problem_path,
        plan_path,
    ]

    try:
        result = subprocess.run(command, capture_output=True, text=True, check=False)
    except subprocess.CalledProcessError as e:
        return False, f"Error validating plan: {e.stderr.strip()}"
    except Exception as e:
        return False, f"Error running VAL: {str(e)}"

    content = result.stdout

    if "Error: Bad operator in plan!" in result.stderr:
        return False, "Error: Bad operator in plan."

    if "Error: Error in type-checking!" in result.stderr:
        return False, "Error: Error in type-checking."

    if "Plan failed to execute" in content:
        return False, "Error: Plan failed to execute."

    if "Bad plan description!" in content:
        return False, "Error: Bad plan description."

    if "Goal not satisfied" in content or "Plan invalid" in content:
        return False, "Error: Goal not satisfied."

    if "Plan executed successfully - checking goal" in content and "Plan valid" in content:
        return True, None

    return False, "Error: Unknown validation result."


def validate_plan(domain_path: str, problem_path: str, plan_path: str) -> Tuple[bool, Optional[str]]:
    return val(domain_path, problem_path, plan_path)
