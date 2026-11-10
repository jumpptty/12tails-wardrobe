"""Read only: which of the cued Penguin voices / sounds / effects BB's ResourceManager (mainData) lists."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "pipeline"))
import wardrobe_fx as W
g = W.Game()
want = {"voices": "nattack1 nattack2 nattack3 manafield1 manafield2 cattack1 cattack2 mptransfer1 mptransfer2 multicast activate1 activate2 ko1 ko2 dead1 dead2 hi wave ty bow laugh sleep cheer beg cry battle chat1 chat2 chat3 chat4 chat5 sit talk pose dance spreadshot1 frostbite1".split(),
        "sounds": "nattack nattack_hit cattack mptransfer cast".split(),
        "effects": "nattack_fire spreadshot_fire nattack_hit cattack_ring manafield_ring mptransfer mptransfer_ring deadeffect".split()}
base = "gameassets/characters/heroes/penguin/"
for folder, names in want.items():
    print(folder, "present:", [n for n in names if base + folder + "/" + n in g.container])
    print(folder, "MISSING:", [n for n in names if base + folder + "/" + n not in g.container])
