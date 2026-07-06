"""grades.py — a small reusable module. Import it: `from grades import letter_grade`."""


def letter_grade(score: float) -> str:
    """Return A/B/C/D/F by 90/80/70/60 cutoffs."""
    for cutoff, letter in [(90, "A"), (80, "B"), (70, "C"), (60, "D")]:
        if score >= cutoff:
            return letter
    return "F"


def class_average(scores: list[float]) -> float:
    """Return the mean of scores."""
    return sum(scores) / len(scores)


if __name__ == "__main__":
    # Runs only when you execute `python3 grades.py`, not when imported.
    print(letter_grade(85), class_average([91, 58, 73]))
