from typing import Dict, Any, List, Tuple

def run_reasoning_engine(state: Dict[str, Any]) -> Tuple[List[str], str]:
    recommendations = set()
    trace_lines = []
    
    soil_carbon = state.get("soil_carbon")
    rainfall = state.get("rainfall")
    land_use = state.get("land_use")
    biodiversity = state.get("biodiversity")
    pollinator_presence = state.get("pollinator_presence")
    
    conditions_met = []
    
    if soil_carbon == "low" and rainfall == "low":
        recommendations.add("Agroforestry")
        trace_lines.append("Low Soil Carbon + Low Rainfall -> Agroforestry")
        
    if soil_carbon == "low":
        recommendations.add("Cover Crops")
        trace_lines.append("Low Soil Carbon -> Cover Crops")
        
    if rainfall == "low":
        recommendations.add("Rainwater Harvesting")
        trace_lines.append("Low Rainfall -> Rainwater Harvesting")
        
    if biodiversity == "low":
        recommendations.add("Native Habitat Restoration")
        trace_lines.append("Low Biodiversity -> Native Habitat Restoration")
        
    if pollinator_presence == "low":
        recommendations.add("Flowering Buffer Strips")
        trace_lines.append("Low Pollinator Presence -> Flowering Buffer Strips")
        
    if land_use == "monoculture":
        recommendations.add("Intercropping")
        trace_lines.append("Monoculture Farming -> Intercropping")
        
    if not trace_lines:
        trace_lines.append("Insufficient critical stress factors for predefined rules, relying on generalized AI reasoning.")
        
    # Formatting output trace as requested
    # Low Soil Carbon + Low Rainfall + Monoculture -> Agroforestry Recommended
    # Wait, the user wants it formatted exactly like:
    # Low Soil Carbon
    # +
    # Low Rainfall
    # +
    # Monoculture
    # ↓
    # Agroforestry Recommended
    
    if trace_lines and not trace_lines[0].startswith("Insufficient"):
        factors = []
        if soil_carbon == "low": factors.append("Low Soil Carbon")
        if rainfall == "low": factors.append("Low Rainfall")
        if land_use == "monoculture": factors.append("Monoculture")
        if biodiversity == "low": factors.append("Low Biodiversity")
        if pollinator_presence == "low": factors.append("Low Pollinator")
        
        reasoning_trace = "\n+\n".join(factors)
        if factors:
            reasoning_trace += "\n↓\n" + "\n".join([f"{r} Recommended" for r in recommendations])
        else:
            reasoning_trace = "No specific rule triggered."
    else:
        reasoning_trace = "No specific rule triggered."
        
    return list(recommendations), reasoning_trace
