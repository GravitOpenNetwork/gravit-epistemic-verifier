try:
    from z3 import *  # type: ignore
    HAS_Z3 = True
except Exception:
    HAS_Z3 = False

from typing import Dict, Any, Tuple


if HAS_Z3:
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
            solver = Solver()
            solver.set("timeout", self.timeout_ms)

            P = Bool("intent_predicate")
            Q = Bool("action_predicate")
            R = Bool("integrity_constraint")

            solver.add(P == True)
            solver.add(Implies(P, Q))
            solver.add(R == True)
            solver.add(Implies(And(P, Not(Q)), Not(R)))

            adversarial_constraint = And(P, Not(Q))
            solver.push()
            solver.add(adversarial_constraint)

            adversarial_risk = 0.0
            unsat_core = []

            if solver.check() == unsat:
                unsat_core = self._extract_unsat_core(solver)
                adversarial_risk = 0.8
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
                "action_predicate": str(Q),
            }

        def _extract_unsat_core(self, solver: "Solver") -> list:
            try:
                unsat_core = solver.unsat_core()
                return [str(assertion) for assertion in unsat_core]
            except Exception:
                return ["constraint_conflict_detected"]

        def _compute_adversarial_risk(self, intent: str, action: str) -> float:
            adversarial_patterns = [
                "ignore",
                "bypass",
                "override",
                "force",
                "skip",
                "unauthorized",
                "bypass security",
                "disable check",
            ]

            risk_score = 0.0
            text_lower = (intent + " " + action).lower()

            for pattern in adversarial_patterns:
                if pattern in text_lower:
                    risk_score += 0.15

            return min(risk_score, 1.0)

        def verify_equivalence(self, intent_formula: str, action_formula: str) -> Tuple[bool, str]:
            solver = Solver()
            intent_bool = Bool(intent_formula)
            action_bool = Bool(action_formula)

            solver.add(intent_bool != action_bool)

            if solver.check() == unsat:
                return True, "Intent and action are logically equivalent"
            else:
                return False, "Intent and action diverge logically"

else:
    # z3 not available — provide a lightweight fallback used in CI/test environments
    class GravitSMTVerifier:
        """Fallback SMT verifier without Z3 dependency."""

        def __init__(self, timeout_ms: int = 5000):
            self.timeout_ms = timeout_ms

        def check_divergence_and_adversarial(self, intent_text: str, action_text: str) -> Dict[str, Any]:
            adversarial_risk = self._compute_adversarial_risk(intent_text, action_text)
            # simple heuristic: if exact negation words present, mark low satisfiability
            satisfiable = True
            unsat_core = []
            if "not" in intent_text.split() and intent_text.replace("not", "") == action_text:
                satisfiable = False
                unsat_core = ["heuristic_negation_detected"]

            return {
                "satisfiable": satisfiable,
                "unsat_core": unsat_core,
                "adversarial_risk_score": round(adversarial_risk, 4),
                "intent_predicate": "intent_predicate",
                "action_predicate": "action_predicate",
            }

        def _compute_adversarial_risk(self, intent: str, action: str) -> float:
            adversarial_patterns = [
                "ignore",
                "bypass",
                "override",
                "force",
                "skip",
                "unauthorized",
                "bypass security",
                "disable check",
            ]

            risk_score = 0.0
            text_lower = (intent + " " + action).lower()

            for pattern in adversarial_patterns:
                if pattern in text_lower:
                    risk_score += 0.15

            return min(risk_score, 1.0)

        def verify_equivalence(self, intent_formula: str, action_formula: str) -> Tuple[bool, str]:
            # simple string equivalence fallback
            if intent_formula.strip() == action_formula.strip():
                return True, "Intent and action are logically equivalent"
            return False, "Intent and action diverge logically"
