import networkx as nx
import json
from collections import Counter

def loadData():
    with open ("units_set16.json", "r") as f:
        units = json.load(f)
    with open ("traits_nohero_set16.json", "r") as h:
        traits = json.load(h)
    # with open ("traits_set16.json", "r") as g:
    #     traits = json.load(g)
    return units, traits

# pretty print from Gemini
def pretty_print_comp(comp, G, trait_data):
    """
    comp: List of unit names (e.g., ["Jinx", "Vi"])
    G: The NetworkX graph containing unit data
    trait_data: The dictionary of trait breakpoints
    """
    print("="*40)
    print(f" FINAL COMPOSITION ({len(comp)} Units)")
    print("="*40)

    # --- SECTION 1: THE UNITS ---
    # Sort by Cost (asc) then Name
    # We retrieve the full node data using G.nodes[name]
    unit_details = [G.nodes[u] for u in comp]
    unit_details.sort(key=lambda x: (x['cost'], x['name']))
    
    total_cost = 0
    print(f"{'COST':<6} {'ROLE':<10} {'NAME':<15} {'TRAITS'}")
    print("-" * 60)
    
    all_traits = []
    
    for u in unit_details:
        total_cost += u['cost']
        # Join traits with a comma for display
        traits_str = ", ".join(u['traits'])
        print(f" {u['cost']:<5} {u['role']:<10} {u['name']:<15} {traits_str}")
        
        # Collect traits for the next section
        all_traits.extend(u['traits'])

    print("-" * 60)
    print(f"Total Gold Cost: {total_cost}")
    print("\n")

    # --- SECTION 2: THE SYNERGIES ---
    print(f" ACTIVE SYNERGIES")
    print("-" * 40)
    
    # 1. Count how many of each trait we have
    trait_counts = Counter(all_traits)
    
    active_traits = []
    
    # 2. Check against the breakpoints in trait_data
    for trait, count in trait_counts.items():
        if trait in trait_data:
            breakpoints = trait_data[trait] # e.g. {'2': 1, '4': 3}
            
            # Find the highest active breakpoint
            current_style = 0
            next_breakpoint = None
            
            # Sort breakpoints numerically (2, 4, 6...)
            sorted_bps = sorted([int(k) for k in breakpoints.keys()])
            
            for bp in sorted_bps:
                if count >= bp:
                    # We met this breakpoint, look up its style (1=Bronze, 3=Gold, etc)
                    current_style = breakpoints[str(bp)]
                else:
                    # We haven't met this one yet, it's our "next goal"
                    if next_breakpoint is None:
                        next_breakpoint = bp
            
            # Only add to list if we have at least the first tier active
            if current_style > 0:
                active_traits.append({
                    "name": trait,
                    "count": count,
                    "style": current_style,
                    "next": next_breakpoint
                })

    # 3. Sort by Style (Prismatic > Gold > Silver > Bronze) then Count
    active_traits.sort(key=lambda x: (x['style'], x['count']), reverse=True)
    
    # Map style IDs to readable names (Standard Riot API values)
    style_map = {1: "Bronze", 2: "Silver", 3: "Gold", 4: "Prismatic"}
    
    if not active_traits:
        print(" (No active traits)")
    else:
        for t in active_traits:
            tier_name = style_map.get(t['style'], "Active")
            next_text = f"/ {t['next']}" if t['next'] else " (MAX)"
            
            # Format: [Gold] Sniper: 4 / 6
            print(f" [{tier_name:<9}] {t['name']:<15}: {t['count']}{next_text}")
            
    print("="*40)