"""
haliscore — LLM Hallucination Test Suite

A curated set of trap prompts designed to test whether large language models
hallucinate (confidently assert false information) or correctly acknowledge
they don't know.  Comes with a scoring system to rank models.

Usage:
    haliscore list              # show all test prompts
    haliscore run               # interactive mode — score a model yourself
    haliscore score <file>      # score pre-collected responses from a JSON file
"""

__version__ = "0.1.0"
__author__ = "ylaing"
