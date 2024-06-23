import os
import json
from src.config import Config
from src.recruitment_post import RecruitmentPost
from src.vector_db import VectorDB

config = Config()
vdb = VectorDB(config)

results = vdb.query("""
# SETTING
You are helping a player of the popular MMORPG, Final Fantasy XIV (FFXIV), find a group that best matches their description.

# TERM DICTIONARY
Below is a list of common terms used by players of FFXIV and their meanings. Some terms are often abbreviated, if a term has an abbreviation it will be provided in parenthesis ().

Static:
A group of players that play the game together on a set weekly schedule.

Raid:
A scenario in FFXIV where player's fight against powerful boss monsters.

Savage:
A raid that is very difficult.

Ultimate:
The most difficult type of raid.

Extreme:
A raid that is moderately difficult.

Normal:
Story mode raid, not meant to be difficult.

Casual (C):
Static focus/mindset. These groups don't take things very seriously and play on a varied/flexible schedule.

Midcore (MC):
Static focus/mindset. These groups take things somewhat seriously and play on a varied/flexible schedule.

Semi-Hardcore (SHC):
Group focus/mindset. These groups take things very seriously and play on a fixed schedule, usually around 12-20 hours a week.

Hardcore (HC):
Group focus/mindset. These groups take things extremely seriously and play on a fixed schedule, usually over 20 hours a week.

Week 1 (W1):
A group whose goal is to complete a new gameplay mode the first week it is released.

World Prog (WP):
A group whose goal is to be the first in the world to complete a new gameplay mode.

Blind:
A group whose goal is to complete a gameplay mode without using outside information (reading guides, etc).

Optimization:
A group whose goal is to complete a gameplay mode as efficiently as possible.

Farm:
A group whose goal is to complete a gameplay mode multiple times to recieve multiple rewards.

Data Center (DC):
A place where game servers are hosted. Players tend try to play on a data center closest to their physical location.

Dynamis:
Data center located in North America.

Aether:
Data center located in North America.

Crystal:
Data center located in North America.

Primal:
Data center located in North America.

Chaos:
Data center located in Europe.

Light:
Data center located in Europe.

Materia:
Data center located in Oceanian.

Elemental:
Data center located in Japan.

Gaia:
Data center located in Japan.

Mana:
Data center located in Japan.

Meteor:
Data center located in Japan.

6.0 / 6.X / 6.0+:
Version number of FFXIV expansion known as Endwalker.

7.0 / 7.X / 7.0+:
Version number of FFXIV expansion known as Dawntrail.

Endwalker:
An expansion to FFXIV, also referred to as 6.0.

Dawntrail:
An expansion to FFXIV, also referred to as 7.0.    

UCOB:
A specific level from the game's ultimate mode. The Unending Coil Of Bahamut (Ultimate).

UWU:
A specific level from the game's ultimate mode. The Weapon's Refrain (Ultimate).

TEA:
A specific level from the game's ultimate mode. The Epic Of Alexander (Ultimate).

DSR:
A specific level from the game's ultimate mode. Dragonsong's Reprise (Ultimate).

TOP:
A specific level from the game's ultimate mode. The Omega Protocol (Ultimate).

P12S:
A specific level from the game's savage mode. Abyssos: The Eighth Circle (Savage).

P11S:
A specific level from the game's savage mode. Abyssos: The Seventh Circle (Savage).

Job:
The specific role of a player in combat. Other RPG games typically refer to this as a "class".

Tank:
Jobs that specialize in taking enemy hits and protecting allies.
PLD, WAR, DRK, GNB

Healer:
Jobs that specialize in healing allies.
WHM, SCH, AST, SGE

Damage Dealer (DPS):
Jobs that specialize in dealing damage to enemies.
MNK, DRG, NIN, SAM, RPR, VIP, BRD, MCH, DNC, BLM, SMN, RDM, PIC, BLU

Regen Healer:
Healer jobs that focus primarly on healing allies.
WHM, AST

Pure Healer:
Alternative name for "Regen Healer".

Shield Healer:
Healer jobs that focus primarly on blocking damage.
SCH, SGE

Barrier Healer:
Alternative name for "Shield Healer".

Melee:
Damage dealer jobs that fight in closer quartered combat.
MNK, DRG, NIN, SAM, RPR, VIP

Physical Ranged:
Damage dealer jobs that use ranged weapons to attack from afar.
BRD, MCH, DNC

Ranged:
Alternative name for "Physical Ranged".

Magical Ranged:
Damage dealer jobs that used magic to attack.
SMN, RDM, PIC, BLU

Caster:
Alternative name for "Magical Ranged".

Paladin (PLD):
Specific tank job.

Warrior (WAR):
Specific tank job.

Dark Knight (DRK):
Specific tank job.

Gunbreaker (GNB):
Specific tank job.

White Mage (WHM):
Specific regen healer job.

Scholar (SCH):
Specific shield healer job.

Astrologian (AST):
Specific regen healer job.

Sage (SGE):
Specific shield healer job.

Monk (MNK):
Specific melee job.

Dragoon (DRG):
Specific melee job.

Ninja (NIN):
Specific melee job.

Samurai (SAM):
Specific melee job.

Reaper (RPR):
Specific melee job.

Viper (VIP):
Specific melee job.

Bard (BRD):
Specific physical ranged job.

Machinist (MCH):
Specific physical ranged job.

Dancer (DNC):
Specific physical ranged job.

Black Mage (BLM):
Specific magical ranged job.

Summoner (SMN):
Specific magical ranged job.

Red Mage (RDM):
Specific magical ranged job.

Pictomancer (PIC):
Specific magical ranged job.

Blue Mage (BLU):
Specific magical ranged job.


# QUERY
```
Show me recruitment posts of mid-core (MC) or semi hard-core (SHC) groups that are looking for a shield healer (NOT pure healer) (SCH/SGE)
for savage and ultimate raids in Dawntrail (7.0). Week one savage clear is ideal. No more than three hours a night and not past 11PM EST unless it's for week one savage.
Particular emphasis on groups that seem like they might be willing to cater to neurodiverse people.
```
""")

for pp in results["documents"]:
    for p in pp:
        print("\n==========\n%s\n==========\n" % p)