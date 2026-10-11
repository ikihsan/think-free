#!/usr/bin/env python3
"""E091 G0: discrimination probes whose labels are known by construction.

AMENDMENT-1 §4 requires G0 labels independent of thread resolution. The
committed probes.jsonl cannot serve: its labels are "did the thread end
resolved", which is the quantity F096 says does not track answerability.

These probes are built the other way round. Each names a class of question
whose answerability is settled before any model is consulted:

  answerable   - the answer is general knowledge or public documentation. A
                 competent general assistant is expected to produce it.
  unanswerable - the answer is a fact about the asker's own unit, account or
                 a private vendor record. No assistant can produce it without
                 data it cannot reach.

The two classes are interleaved and the label is printed below each row so a
reader can check the split without running anything. Scoring is in score_g0.py.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))

# (label, question, why the label is settled in advance)
PROBES = [
    ("answerable",
     "My sous vide cooker will not join my home wifi. The router is a dual-band "
     "mesh unit and my phone is on the 5 GHz network. What should I try?",
     "General networking and 2.4/5 GHz advice is textbook; the remedy is in "
     "public documentation for every IoT device of this class."),
    ("unanswerable",
     "My sous vide cooker will not join my home wifi. What is the current "
     "firmware version on my unit, and is there a known bug in it?",
     "Requires reading the asker's own device. No assistant can know it."),
    ("answerable",
     "What is the internal temperature range a typical immersion circulator is "
     "rated for, and why does it matter which fluid I use?",
     "Standard food-safety and equipment knowledge; published in manufacturer "
     "documentation and textbooks."),
    ("unanswerable",
     "Is the specific serial number on my circulator still under warranty? The "
     "unit is 14 months old and I bought it direct from the vendor.",
     "Warranty status is a lookup in the vendor's own order database, keyed on "
     "the asker's serial number and purchase date."),
    ("answerable",
     "My cook finished but the food is still cold in the centre. I am using a "
     "vacuum sealer. What are the likely causes and how do I check each one?",
     "A troubleshooting tree any competent assistant can produce from general "
     "cooking and food-safety knowledge."),
    ("unanswerable",
     "Why did my cook finish early? I need the actual internal temperature "
     "history my cooker recorded during the last 12-hour cook.",
     "The temperature log lives on the asker's device or in the vendor's cloud "
     "account. It is not public data."),
    ("answerable",
     "Can I put a Sous Vide Professional in an oven, or is that unsafe?",
     "A published, vendor-independent safety and technique question."),
    ("unanswerable",
     "Can I put my Sous Vide Professional in an oven? My model's manual says "
     "one thing and the reseller said another - which is right for my unit?",
     "Turns into a per-model document lookup; the answer differs by model and "
     "revision, and the asker holds neither document."),
    ("answerable",
     "What is the difference between sous vide and poaching, and when would I "
     "pick each?",
     "General culinary knowledge."),
    ("unanswerable",
     "What is the difference between sous vide and poaching for MY dinner "
     "tonight? I have duck breast, and I told the app 54 C but I do not know "
     "what my oven actually held.",
     "Requires a measurement of the asker's oven at that moment."),
    ("answerable",
     "How long should I cook a 2 cm thick piece of beef at 55 C, and what is a "
     "reasonable resting time?",
     "Standard published cooking tables."),
    ("unanswerable",
     "How long should I cook this piece of beef? It is from my freezer and I "
     "do not have a thermometer to check its thickness.",
     "The deciding variable is a measurement of the asker's own food that they "
     "state they cannot take."),
    ("answerable",
     "What is the boiling point of water, and how does altitude change it?",
     "Textbook physics with a known numeric answer."),
    ("unanswerable",
     "What is the boiling point of the liquid in MY pot right now? I am at an "
     "altitude I have not measured and I have no thermometer in the liquid.",
     "A measurement of the asker's current physical situation."),
    ("answerable",
     "What kitchen safety rules should I follow when using an immersion "
     "circulator near water?",
     "Published safety guidance."),
    ("unanswerable",
     "Is it safe for me to run my immersion circulator in my sink right now, "
     "given that my sink has an earth fault and I noticed a small spark this "
     "morning?",
     "Requires inspecting the asker's own electrical installation."),
    ("answerable",
     "Explain what sous vide cooking does to the texture of meat compared with "
     "conventional cooking.",
     "General explanatory knowledge."),
    ("unanswerable",
     "Explain why MY steak came out tough when I sous vide it. I followed the "
     "app recipe exactly and I can tell you the exact time and temperature.",
     "Even complete self-reported parameters do not settle it; the likely cause "
     "needs an inspection of the asker's cut and equipment, not knowledge."),
    ("answerable",
     "What are common beginner mistakes when starting out with sous vide?",
     "Widely published advice."),
    ("unanswerable",
     "What are common beginner mistakes when starting out with sous vide? I am "
     "starting out, my cooker is a discontinued 2017 model, and I want to know "
     "which mistakes are specific to that model's known failure modes.",
     "Same question as row 19 plus a per-model failure-mode lookup the asker "
     "cannot perform."),
]


def main():
    path = os.path.join(HERE, "g0_probes.json")
    with open(path, "w") as handle:
        json.dump([{"i": i, "label": label, "question": q, "why": why}
                   for i, (label, q, why) in enumerate(PROBES)],
                  handle, indent=2)
    answerable = sum(1 for label, _, _ in PROBES if label == "answerable")
    print("wrote g0_probes.json: %d probes, %d answerable, %d unanswerable"
          % (len(PROBES), answerable, len(PROBES) - answerable))
    print("labels are known by construction and independent of any thread")


if __name__ == "__main__":
    main()
