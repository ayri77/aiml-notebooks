"""Build l12-claims.jsonl: 40 statements a student might make about the
course notes (Lectures 1-6), 20 true and 20 false, each with the
section that settles it. Written by hand from the notes; no model."""
import json

CLAIMS = [  # lecture, section, true statement, false statement
    (1, "2.2",
     "During training a Transformer can score every position of a known "
     "sequence in one pass, because the targets already exist.",
     "During training a Transformer must generate each token before it "
     "can be trained on the next one, just as in generation."),
    (1, "2.5",
     "Mamba carries a compact learned state forward instead of keeping "
     "every earlier position available, as attention does.",
     "Mamba keeps a lossless copy of the whole history, so it remembers "
     "everything attention can."),
    (1, "3.1",
     "A diffusion model is trained by corrupting real images with noise "
     "and learning to estimate a cleaner version.",
     "A diffusion model is trained to add noise to images, and it "
     "generates by adding still more noise."),
    (1, "4.2",
     "DiT replaces the U-Net with Transformer blocks that process image "
     "patches as a sequence, with position information.",
     "DiT discards where each patch was, because flattening the grid "
     "into a sequence removes the spatial arrangement."),
    (2, "1.4",
     "Chinchilla used fewer parameters than Gopher and much more "
     "training text for about the same compute, and performed better.",
     "Chinchilla beat Gopher by having more parameters and less "
     "training text for the same compute."),
    (2, "3.2",
     "Supervised fine-tuning teaches behaviour from supplied target "
     "responses to example requests.",
     "Supervised fine-tuning trains a model only on human rankings of "
     "two answers, with no target responses."),
    (2, "3.4",
     "In Constitutional AI humans choose the principles and an AI "
     "applies them to critique and revise responses.",
     "In Constitutional AI the model writes its own principles, so no "
     "human chooses them."),
    (2, "4.2",
     "Quantization maps weights to a limited set of levels, so nearby "
     "values can share one level.",
     "Quantization deletes decimal digits from the text form of each "
     "weight, which loses no information."),
    (2, "4.3",
     "In distillation the student learns from examples the teacher "
     "produces; the teacher's weights are not copied.",
     "Distillation copies the teacher's weights into a smaller student "
     "model."),
    (3, "3.1",
     "In a Mixture of Experts, a router sends each token through only a "
     "subset of the expert blocks.",
     "In a Mixture of Experts every expert processes every token, and "
     "each expert is a separate chatbot."),
    (3, "4.2",
     "Lowering the temperature makes sampling favour the most likely "
     "tokens more strongly; the order of candidates stays the same.",
     "Raising the temperature changes the order of the candidates, so "
     "the most likely token becomes the least likely."),
    (3, "4.3",
     "Top-p keeps the smallest group of leading tokens whose combined "
     "probability reaches p.",
     "Top-p always keeps exactly p tokens, whatever their "
     "probabilities."),
    (4, "2.1",
     "Zero-shot prompting means giving the task without worked "
     "examples; the model is still trained and instructed.",
     "Zero-shot prompting means the model has had no training at all on "
     "any data."),
    (4, "3.3",
     "Self-Consistency samples several complete attempts and selects "
     "the most frequent final answer.",
     "Self-Consistency asks the model once and repeats that single "
     "answer to make it more consistent."),
    (4, "5.1",
     "Prompt injection is an attempt to make the model treat lower-trust "
     "input, such as a document, as instructions.",
     "Prompt injection only happens when the user types a jailbreak; a "
     "document cannot carry an attack."),
    (4, "3.6",
     "ReAct alternates actions with observations, using each result to "
     "choose the next step.",
     "ReAct plans every action in advance and never looks at tool "
     "results before finishing."),
    (5, "4.1",
     "Pydantic checks data against fields declared in a class, so the "
     "application can read named fields directly.",
     "Using Pydantic makes the model request free, because the check "
     "runs locally."),
    (6, "2.2",
     "A tool's description saying a value must be positive does not "
     "enforce it; bounds in the schema do.",
     "Writing 'positive' in a tool's description is enough to make the "
     "validator reject negative values."),
    (3, "1.2",
     "Time to first token and complete-answer time are different "
     "measurements, and either can be called latency.",
     "Time to first token always equals the time to the complete "
     "answer, so one number describes speed."),
    (2, "1.3",
     "The 2020 scaling laws described next-token loss under the "
     "studied conditions, not an all-purpose score for helpfulness.",
     "The 2020 scaling laws proved that a larger model is more helpful "
     "on every task."),
]

with open("l12-claims.jsonl", "w", encoding="utf-8") as out:
    for i, (lecture, section, true, false) in enumerate(CLAIMS, 1):
        for label, text in (("true", true), ("false", false)):
            out.write(json.dumps({
                "id": f"c{i:02d}-{label[0]}", "lecture": lecture,
                "section": section, "label": label, "claim": text},
                ensure_ascii=False) + "\n")
print("wrote", 2 * len(CLAIMS), "claims")
