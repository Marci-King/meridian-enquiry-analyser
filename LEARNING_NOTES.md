# Learning Notes

These notes explain the project for someone new to Python.

## 1. How To Run The Project

Open a terminal in the project folder and run:

```bash
python3 meridian_analyser.py
```

The script reads fictional enquiries from `data/enquiries.json`.

It creates two output files:

```text
outputs/analysed_enquiries.json
outputs/daily_summary.md
```

## 2. What Each File Does

- `data/enquiries.json` stores fictional messy customer enquiries.
- `meridian_analyser.py` contains the Python logic that analyses each enquiry.
- `outputs/analysed_enquiries.json` stores the structured result for each enquiry.
- `outputs/daily_summary.md` stores a readable Markdown summary.
- `README.md` explains the project for public viewing.
- `LEARNING_NOTES.md` explains the Python concepts used in the project.
- `EXAMPLE_OUTPUT.md` shows one raw enquiry, one analysed object, and a summary excerpt.

## 3. What The Main Python Concepts Are

`import` brings in code from Python's standard library.

`pathlib` helps create file paths such as `data/enquiries.json`.

`json` reads and writes JSON data.

`re` checks text using regular expressions.

`dataclass` creates a simple structured object without lots of boilerplate code.

`class` groups related data and functions together.

`function` is a named block of reusable code.

`dictionary` stores key-value pairs such as `{"id": "ENQ-001"}`.

`list` stores multiple values in order.

`loop` repeats work for each item in a list.

`if/else` lets the program make decisions.

`Counter` counts repeated values, such as categories.

Writing files means opening a path and saving text or JSON into it.

## 4. Function-By-Function Explanation

`AnalysedEnquiry`

- Receives structured values such as `id`, `category`, and `owner_note`.
- Returns a dataclass object.
- Exists so each analysed enquiry has the same shape.

`MeridianAnalyser.__init__`

- Receives the list of raw enquiries.
- Returns nothing.
- Exists to store the data inside the analyser object.

`classify`

- Receives one enquiry text string.
- Returns one category: `hospitality`, `clinic_consultation`, `send_sports`, or `general`.
- Exists to decide the broad service route.

`detect_interest`

- Receives one enquiry text string.
- Returns an interest area such as `PRP`, `catering`, or `pricing / quote`.
- Exists to make the enquiry easier to route and summarise.

`find_missing_details`

- Receives a category and one enquiry text string.
- Returns a list of missing details.
- Exists to show what a human might need to ask next.

`audit_human_review`

- Receives the category, interest area, and enquiry text.
- Returns a boolean and a reason string.
- Exists to flag messages that need careful human review.

`build_owner_note`

- Receives the category, interest area, missing details, review flag, and review reason.
- Returns the owner, suggested next step, and owner note.
- Exists to prepare a practical handoff note.

`process`

- Receives nothing directly because it uses the enquiries stored in the class.
- Returns a list of `AnalysedEnquiry` objects.
- Exists to run all analysis steps for every enquiry.

`contains_any`

- Receives text and a list of words.
- Returns `True` or `False`.
- Exists to keep simple keyword checks readable.

`load_enquiries`

- Receives a file path.
- Returns a list of dictionaries loaded from JSON.
- Exists to separate file loading from analysis logic.

`write_json_output`

- Receives analysed enquiries and an output path.
- Returns nothing.
- Exists to save structured JSON output.

`write_markdown_summary`

- Receives analysed enquiries and an output path.
- Returns nothing.
- Exists to create a readable daily report.

`format_counter`

- Receives a `Counter`.
- Returns a short text summary.
- Exists to make category and interest breakdowns readable.

`main`

- Receives nothing.
- Returns nothing.
- Exists as the script entry point that runs the whole workflow.

## 5. How The Data Flows

```text
Raw JSON -> analyser -> structured object -> JSON output -> Markdown report
```

In plain English:

1. The script loads raw enquiries from JSON.
2. The analyser classifies and reviews each enquiry.
3. Each result becomes an `AnalysedEnquiry` object.
4. The objects are written to a structured JSON file.
5. The same objects are summarised in a Markdown report.

## 6. Three Beginner Exercises

Exercise A: Add one new fictional enquiry to `data/enquiries.json`.

Exercise B: Add a new human-review trigger for pricing using:

```text
cost|price|how much|quote
```

Exercise C: Change the `daily_summary.md` wording in `write_markdown_summary` and rerun the script.

## 7. Stretch Exercises

- Add CSV output.
- Add unit tests.
- Add a new category.
- Add a command-line argument for the input file.
