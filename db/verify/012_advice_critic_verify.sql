-- J10 Advice & Critic verification
DO $$
DECLARE
  v_gap uuid := 'edb00111-cf5b-5089-8464-c5f9135a0802';
  v_assessment uuid := '1be6523b-35a0-4715-bfce-9e1374a94b1a';
BEGIN
  IF NOT EXISTS (
    SELECT 1 FROM assessment
    WHERE id = v_assessment AND target_research_object_id = v_gap
      AND assessment_type = 'ADVICE_CRITIC_V1'
  ) THEN RAISE EXCEPTION 'J10 assessment missing or wrong target/type'; END IF;

  IF (SELECT count(*) FROM assessment_dimension WHERE assessment_id = v_assessment) <> 3 THEN
    RAISE EXCEPTION 'J10 requires exactly three canonical dimensions';
  END IF;

  IF EXISTS (SELECT 1 FROM human_decision WHERE assessment_id = v_assessment) THEN
    RAISE EXCEPTION 'J10 must not auto-create/link HumanDecision';
  END IF;

  IF (SELECT current_evolution_state FROM gap_candidate WHERE id = v_gap) <> 'CANDIDATE' THEN
    RAISE EXCEPTION 'J10 must not mutate GapCandidate state';
  END IF;
END $$;
