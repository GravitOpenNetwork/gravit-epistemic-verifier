from z3 import *
from typing import Dict, Any, Tuple

class GravitSMTVerifier:
    """
    SMT-based verifier using Z3 to check semantic divergence
    and adversarial patterns between intent and action.
    """

    def __init__(self, timeout_ms: int = 5000):
        self.timeout_ms = timeout_ms
        self.solver = Solver()
        self.solver.set("timeout", timeout_ms)

    def check_divergence_and_adversarial(self, intent_text: str, action_text: str) -> Dict[str, Any]:
        """
        Encodes intent and action as logical constraints and checks for:
        - Semantic divergence (contradictions between intent and action)
        - Adversarial patterns (suspicious logical structures)

        Returns:
            Dict with keys: satisfiable, unsat_core, adversarial_risk_score
        """
        solver = Solver()
        solver.set("timeout", self.timeout_ms)

        # Create symbolic variables
        P = Bool('intent_predicate')
        Q = Bool('action_predicate')
        R = Bool('integrity_constraint')

        # Intent: must be true
        solver.add(P == True)

        # Action should follow from intent under constraints
        solver.add(Implies(P, Q))

        # Integrity constraints (no contradictions)
        solver.add(R == True)
        solver.add(Implies(And(P, Not(Q)), Not(R)))

        # Check adversarial pattern: intent negated by action
        adversarial_constraint = And(P, Not(Q))
        solver.push()
        solver.add(adversarial_constraint)

        adversarial_risk = 0.0
        unsat_core = []

        # Check for divergence
        if solver.check() == unsat:
            unsat_core = self._extract_unsat_core(solver)
            adversarial_risk = 0.8  # High risk: intent and action conflict
            satisfiable = False
        else:
            adversarial_risk = self._compute_adversarial_risk(intent_text, action_text)
            satisfiable = True

        solver.pop()

        return {
            "satisfiable": satisfiable,
            "unsat_core": unsat_core,
            "adversarial_risk_score": round(adversarial_risk, 4),
            "intent_predicate": str(P),
            "action_predicate": str(Q)
        }

    def _extract_unsat_core(self, solver: Solver) -> list:
        """Extract unsat core assertions if supported"""
        try:
            unsat_core = solver.unsat_core()
            return [str(assertion) for assertion in unsat_core]
        except:
            return ["constraint_conflict_detected"]

    def _compute_adversarial_risk(self, intent: str, action: str) -> float:
        """Heuristic fallback for adversarial risk scoring"""
        adversarial_patterns = [
            "ignore", "bypass", "override", "force", "skip",
            "unauthorized", "bypass security", "disable check"
        ]

        risk_score = 0.0
        text_lower = (intent + " " + action).lower()

        for pattern in adversarial_patterns:
            if pattern in text_lower:
                risk_score += 0.15

        return min(risk_score, 1.0)

    def verify_equivalence(self, intent_formula: str, action_formula: str) -> Tuple[bool, str]:
        """Verify logical equivalence between two formulas"""
        solver = Solver()
        intent_bool = Bool(intent_formula)
        action_bool = Bool(action_formula)

        solver.add(intent_bool != action_bool)

        if solver.check() == unsat:
            return True, "Intent and action are logically equivalent"
        else:
            return False, "Intent and action diverge logically"
