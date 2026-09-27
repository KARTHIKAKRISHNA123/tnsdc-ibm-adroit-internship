# # =============================================================
# HANDS-ON 2 — MCP TOOL REGISTRY & DISCOVERY
# =============================================================

print("\n=== MCP TOOL DISCOVERY ===\n")

# -------------------------------------------------------------
# STEP 1: Define MCP Tools
# -------------------------------------------------------------

def get_policy(policy_id):
    return f"Policy Details for {policy_id}"

def claim_status(claim_id):
    return f"Claim Status for {claim_id}"

def calculate_premium(age):
    if age < 30:
        return 5000
    elif age < 50:
        return 8000
    else:
        return 12000


# -------------------------------------------------------------
# STEP 2: Simulate MCP Server Tool Registry
# -------------------------------------------------------------

tool_registry = {
    "get_policy": get_policy,
    "claim_status": claim_status,
    "calculate_premium": calculate_premium
}

# -------------------------------------------------------------
# STEP 3: MCP Client Discovers Available Tools
# -------------------------------------------------------------

print("Tools discovered from MCP Server:\n")

for tool_name in tool_registry:
    print("•", tool_name)

# -------------------------------------------------------------
# STEP 4: MCP Client Calls a Tool
# -------------------------------------------------------------

selected_tool = "claim_status"

print("\nClient selected tool:", selected_tool)

result = tool_registry[selected_tool]("C1001")

print("Tool Result:", result)

# -------------------------------------------------------------
# STEP 5: Call Another Tool
# -------------------------------------------------------------

selected_tool = "calculate_premium"

print("\nClient selected tool:", selected_tool)

result = tool_registry[selected_tool](35)

print("Tool Result:", result)