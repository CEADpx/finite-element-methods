# Repository instructions

This repository contains a graduate finite element methods book and associated
computational and course material.

## General principles

- Preserve mathematical notation and terminology already established in the book.
- Do not silently change mathematical content, equations, theorem statements,
  or derivations.
- If a mathematical inconsistency is suspected, report it instead of correcting
  it without instruction.
- Prefer simple, readable code over unnecessary abstractions.
- FEniCSx is the primary finite element software used by this project.
- Python examples should be reproducible and deterministic when practical.
- Reusable code belongs in src/fem_utils/.
- Chapter-specific demonstration code may remain in notebooks or examples.
- Do not duplicate large code blocks when a shared implementation is appropriate.
- Do not add dependencies unless they are needed.
- Do not select or change software or content licenses without explicit instruction.

## Book

- The Quarto project root is book/.
- Mathematical notation belongs in book/latex/macros.tex.
- PDF presentation settings belong in book/latex/preamble.tex.
- Chapter sources belong in book/chapters/.
- Keep substantive mathematical exposition in the chapter text.
- Code supports the exposition and must not replace mathematical derivations.
- Use Quarto cross references for equations, figures, tables, definitions,
  examples, and theorems.
- Use citations through book/references.bib.
- Do not invent references.
- Keep executable computations compatible with Quarto and Jupyter.
- The project uses execute: freeze: auto. Do not remove this without instruction.

## Validation

After changes affecting the book, run:

quarto render book

if Quarto is installed.

After changes affecting Python utilities or examples, run the relevant tests.

Report missing dependencies clearly instead of silently working around them.
