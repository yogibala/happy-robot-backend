from typing import Dict, Union

# Configuration for Objective 1
MAX_NEGOTIATION_ROUNDS: int = 3
AUTO_ACCEPT_THRESHOLD: float = 0.10  # Accept if within 10% of rate
COUNTER_OFFER_MARGIN: float = 0.03  # Counter with a 3% increase


def negotiate(
    load_rate: float, carrier_offer: float, round_number: int
) -> Dict[str, Union[str, float, None]]:

    # 1. Enforce max rounds
    if round_number > MAX_NEGOTIATION_ROUNDS:
        return {
            "decision": "reject",
            "reason": "Maximum negotiation rounds reached. Please contact a sales rep.",
        }
    margin = 0.05 + (0.02 * round_number) - load_rate
    # 2. Evaluation Logic
    max_accept_rate = load_rate * (1 + margin)

    if carrier_offer <= max_accept_rate:
        return {
            "decision": "accept",
            "final_rate": carrier_offer,
            "reason": "Offer is within our acceptable range.",
        }

    # 3. Counter-Offer Logic (if not the final round)
    if round_number < MAX_NEGOTIATION_ROUNDS:
        counter_rate = load_rate * (1 + (COUNTER_OFFER_MARGIN * round_number))
        return {
            "decision": "counter",
            "counter_rate": round(counter_rate, 2),
            "reason": f"Round {round_number}: We can do better than {carrier_offer}.",
        }

    return {"decision": "reject", "reason": "Final round reached without agreement."}
