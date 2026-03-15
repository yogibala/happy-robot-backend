from typing import Dict, Union

MAX_NEGOTIATION_ROUNDS: int = 3
ACCEPTANCE_MARGIN: float = 0.15
COUNTER_MARGIN: float = 0.05


def negotiate(
    load_rate: float,
    carrier_offer: float,
    round_number: int
) -> Dict[str, Union[str, float]]:

    max_accept_rate: float = load_rate * (1 + ACCEPTANCE_MARGIN)

    if carrier_offer <= max_accept_rate:
        return {
            "decision": "accept",
            "final_rate": carrier_offer
        }

    if round_number >= MAX_NEGOTIATION_ROUNDS:
        return {
            "decision": "reject",
            "reason": "Max negotiation rounds reached"
        }

    counter_rate: float = load_rate * (1 + COUNTER_MARGIN)

    return {
        "decision": "counter",
        "counter_rate": round(counter_rate, 2)
    }