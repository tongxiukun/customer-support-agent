from agents.schemas import SynthesisResult, SafetyVerdict
from safety.dual_llm import dual_validate
from safety.output_guard import check_grounding

class SafetyAgent:
    def review(self, syn_res: SynthesisResult, source_chunks) -> SafetyVerdict:
        dual_check = dual_validate(syn_res.answer)
        if not dual_check["ok"]:
            return SafetyVerdict(approved=False, feedback=dual_check["reason"])
        grounded_ok, msg = check_grounding(syn_res.answer, source_chunks)
        if not grounded_ok:
            return SafetyVerdict(approved=False, feedback=msg)
        return SafetyVerdict(approved=True, final_answer=syn_res.answer)