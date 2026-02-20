from typing import Any

def node_save_draft(state: dict[str, Any]) -> dict[str, Any]:
    """Finalizes the report and sets the compliance status."""
    print("--- SAVING REPORT TO CRM: ✅ APPROVED ---")
    
    # This sends the final success signal back to main.py
    return {"compliance_status": "✅ Approved & Saved to Client File"}