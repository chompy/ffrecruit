
TANKS = ["PLD", "WAR", "DRK", "GNB"]
SHIELD_HEALERS = ["SCH", "SGE"]
REGEN_HEALDERS = ["WHM", "AST"]
CASTER_DPS = ["BLM", "SMN", "RDM", "PIC"]
RANGED_DPS = ["BRD", "MCH", "DNC"]
MELEE_DPS = ["DRG", "MNK", "SAM", "NIN", "RPR", "VPR"]

ROLE_TO_JOBS_MAP = {
    "tank": TANKS,
    "healer": [*REGEN_HEALDERS, *SHIELD_HEALERS],
    "shield healer": SHIELD_HEALERS,
    "barrier healer": SHIELD_HEALERS,
    "pure healer": REGEN_HEALDERS,
    "regen healer": REGEN_HEALDERS,
    "dps": [*CASTER_DPS, *RANGED_DPS, *MELEE_DPS],
    "melee" : MELEE_DPS,
    "caster": CASTER_DPS,
    "magical ranged": CASTER_DPS,
    "mage": CASTER_DPS,
    "phyiscal ranged": RANGED_DPS,
    "ranged": RANGED_DPS,
    "phys ranged": RANGED_DPS
}

def role_to_jobs(role_name : str) -> list[str]:
    role_name = role_name.lower().strip()
    if role_name in ROLE_TO_JOBS_MAP: return ROLE_TO_JOBS_MAP[role_name]
    return []

def role_list_to_job_list(role_list : list[str]) -> list[str]:
    out = []
    for role in role_list:
        out += role_to_jobs(role)
    out.sort()
    return list(set(out))