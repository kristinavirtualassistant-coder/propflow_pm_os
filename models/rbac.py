from typing import Dict, List

ROLE_PORTAL_PERMISSIONS: Dict[str, List[str]] = {
    "ADMIN": ["LEAD_GEN", "PM_ADMIN", "OWNER", "TENANT", "VENDOR"],
    "LANDLORD": ["OWNER"],
    "TENANT": ["TENANT"],
    "VENDOR": ["VENDOR"],
    "LEAD_GEN_USER": ["LEAD_GEN", "PM_ADMIN"]
}

class RBACController:
    """Enforces multi-tenant portal access boundaries."""

    @staticmethod
    def can_access_portal(role: str, portal_key: str) -> bool:
        allowed_portals = ROLE_PORTAL_PERMISSIONS.get(role.upper(), [])
        return portal_key.upper() in allowed_portals

if __name__ == "__main__":
    print("[RBAC Check] ADMIN -> TENANT Portal:", RBACController.can_access_portal("ADMIN", "TENANT"))
    print("[RBAC Check] TENANT -> PM_ADMIN Portal:", RBACController.can_access_portal("TENANT", "PM_ADMIN"))
