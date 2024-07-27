ONTOLOGY_REASON_PROMPT = """Please determine whether the input triple is consistent within the same ontological framework with a set of known triples in the knowledge graph, which means the entities are consistent in entity type.
A set of known triples are:
{fewshot_triples}
The triple to be determined is:
{test_triple}
Please return 'Y' if the input triple is consistent within the same ontological framework, otherwise return 'N'. Do not say anything else except your determination.
"""

CLOSE_PATH_REASON_PROMPT = """Please determine whether the relation in the input can be reliably inferred, given a set of reasoning paths between two entities of known triples of the knowledge graph.
A set of reasoning paths are:
{reasoning_paths}
The relation to be inferred is:
{test_triple}
Please return 'Y' if there is sufficient evidence from the reasoning paths to infer the relation, otherwise return 'N'. Do not say anything else except your determination.
"""

OPEN_PATH_REASON_PROMPT = """Please determine whether the relation in the input can be reliably inferred, given a set of known triples including two entities of the knowledge graph.
A set of known triples are:
{known_triples}
The relation to be inferred is:
{test_triple}
Please return 'Y' if there is sufficient evidence from the known triples to infer the relation, otherwise return 'N'. Do not say anything else except your determination.
"""

EXPLAINING_PROMPT = """Please explain why the test triple can be reliably inferred based on the provided reasoning evidence. If it cannot be directly inferred from the evidence, provide a detailed justification for its correctness, including potential reasons. 
The reasoning evidence is:
{reasoning_evidence}
The test triple to be explained is:
{test_triple}
Please provide a detailed explanation justifying why.
"""
