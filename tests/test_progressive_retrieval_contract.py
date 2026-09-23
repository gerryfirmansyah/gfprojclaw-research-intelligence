from pathlib import Path
s=Path("docs/j16/progressive-retrieval-contract-v0.md").read_text()
required=["operational batch boundary","Provider reported → Retrieved → Deduplicated → Screened","exact member set","NOT_RETRIEVED","Machine screening is advisory","HUMAN scientific judgment remains authoritative","scientific_decision=false"]
for x in required:
    assert x in s,x
print("PROGRESSIVE_RETRIEVAL_CONTRACT_PASS")
