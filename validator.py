ALLOWED_TOOLS = ["nmap", "gobuster", "zap"]

def is_safe_command(cmd: str):
    blocked = ["rm", "shutdown", "|", ";", "&&", "sudo", "mkfs"]
    return not any(b in cmd for b in blocked)


def validate_plan(plan):
    if not isinstance(plan, list):
        return False, "Plan is not a list"

    for item in plan:
        if "tool" not in item or "args" not in item:
            return False, "Invalid schema"

        if item["tool"] not in ALLOWED_TOOLS:
            return False, f"Tool not allowed: {item['tool']}"

        if not is_safe_command(item["args"]):
            return False, f"Unsafe command: {item['args']}"

    return True, "OK"