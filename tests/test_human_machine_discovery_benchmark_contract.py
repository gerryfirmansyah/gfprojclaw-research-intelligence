from pathlib import Path
s=Path("docs/j16/human-machine-discovery-benchmark-contract-v0.md").read_text()
required=["QUERY_PARITY","NON_PARITY_COMPARISON","provider_reported_total","human_captured_count","retrieved_count","overlap_count","human_only_count","machine_only_count","exact member lists","NOT_AVAILABLE","limit=10","scientific decision","OpenAlex"]
for x in required:
    assert x in s,x
assert "declare HUMAN wrong" in s
assert "declare machine superior" in s
assert "Research Universe=10" in s
print("HUMAN_MACHINE_DISCOVERY_BENCHMARK_CONTRACT_PASS")
