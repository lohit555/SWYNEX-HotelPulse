
# 🏨 HotelPulse

### AI-Powered Complaint Classification & Prioritization

HotelPulse is an AI-powered prototype that helps hotel customer-support teams classify guest complaints and prioritize issues requiring attention.

**Artificial Intelligence Intern:** Swynex Technologies

- Task 1 - AI Problem Design (Completed)
- Task 2 - Model or API Integration (Completed)
- Task 3 - Intelligent Feature (Completed)
- Task 4 - Final AI Application (Completed)

---

## Task 1 - AI Problem Design

### 1. Problem Statement

Hotels receive large volumes of guest feedback about cleanliness, service, facilities, food, and other issues. Manually reviewing this feedback can be time-consuming. HotelPulse aims to automate complaint classification and prioritize issues requiring attention.

### 2. Intended User

Hotel customer-support staff and hotel operations teams who review guest feedback and determine which issues need attention.

### 3. AI Use Case

- **Primary task:** Classify guest feedback into predefined complaint categories.
- **Supporting feature:** Assign a priority score from 0–100 and a priority level: Low, Medium, High, or Critical.

Categories include Cleanliness, Staff/Service, Room/Facilities, Food/Dining, Location, Noise, and Value/Billing.

### 4. Dataset

[515K Hotel Reviews Data in Europe — Kaggle](https://www.kaggle.com/datasets/jiashenliu/515k-hotel-reviews-data-in-europe)

A 2,000-review sample is included for exploratory purposes. Since the original dataset does not provide verified complaint-category or severity labels, a separate manually constructed set of 50 examples is used for evaluation.

The Kaggle page lists the dataset under the CC0: Public Domain licence and acknowledges Booking.com as the source of the scraped reviews. Review sentiment labels are not ground truth for complaint categories or priority scores.

### 5. Proposed Approach

- Use an AI model through an API to classify guest feedback.
- Apply a documented scoring rubric based on severity, safety, financial impact, urgency, and multiple or unresolved issues.
- Display the classification, explanation, priority score, and recommended next step in a web interface.
- Keep human staff responsible for final decisions.

### 6. Constraints

- Limited internship timeline and API usage budget.
- Public reviews may not represent real support tickets.
- AI predictions and priority scores may be inaccurate.
- Human review is required before taking action.
- API keys must remain secure and excluded from version control.

### 7. Evaluation Approach

The prototype is evaluated using manually labeled examples. Metrics include category classification accuracy, complaint detection accuracy, severity accuracy, and failed predictions. Incorrect predictions are reviewed to identify improvement opportunities.

### 8. Success Criteria

- Correctly identify relevant complaint categories.
- Generate priority scores and explanations.
- Provide an interactive interface for reviewing analyses.
- Demonstrate measurable performance on labeled test examples.

---

## Task 2 - Model or API Integration

The working prototype uses Streamlit and the Groq API to analyze guest feedback. The AI returns structured classifications, while application logic calculates the priority score.

### Key Features

- Sample guest reviews for quick testing.
- AI-generated category, summary, explanation, and risk indicators.
- 0–100 priority gauge and score breakdown.
- Recommended next steps based on the analysis.
- Five-item in-session recent-analysis queue.
- Custom hotel-lobby background and dashboard styling.

### Run Locally

1. Create and activate a Python virtual environment.
2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Copy `.env.example` to `.env` and add your `GROQ_API_KEY`.
4. Start the application:

   ```bash
   streamlit run dashboard.py
   ```

Never commit `.env` or API keys.

---

## Task 3 - Intelligent Feature

Task 3 improved classification through prompt refinement, evaluation, and failure-case analysis.

### Improvements

- Refined prompts for complaint categories and severity.
- Expanded the evaluation set from 24 to 50 manually constructed examples to test a wider variety of guest-feedback scenarios and obtain a more informative assessment of model performance.
- Implemented `evaluate.py` to compare predictions with expected labels.
- Reviewed incorrect predictions to identify areas for improvement.
- Retained the interactive dashboard and priority-scoring functionality.

### Evaluation Results

| Metric | Correct Predictions | Accuracy |
|---|---:|---:|
| Category Classification | 47/50 | 94% |
| Complaint Detection | 48/50 | 96% |
| Severity Classification | 44/50 | 88% |
| Failed Predictions | 0/50 | 0 failures |

**Limitations:** The evaluation set is small and manually constructed, and its labels have not been independently validated. These results represent preliminary prototype performance, not guaranteed accuracy on real-world hotel feedback.

### Run Evaluation

```bash
python evaluate.py
```

The generated `evaluation_results.csv` is available locally and excluded from Git.

---

## Task 4 - Final AI Application

### Method

1. The user enters guest feedback in the Streamlit interface.
2. The application sends the text to the Groq API using `openai/gpt-oss-120b`.
3. The model generates a category, summary, severity assessment, and explanation.
4. The application applies its scoring rubric and returns a priority score and level.
5. Hotel staff review the recommendation and decide on the appropriate action.

### Demonstration

**Example input:**

> Loud construction noise outside my room kept me awake until 2 AM.

**Illustrative output:**

- **Category:** Noise
- **Severity:** Serious
- **Priority:** High (60/100)
- **Recommended action:** Refer the issue to the duty manager for review and guest follow-up.

Actual AI output may vary between runs.

### Limitations and Ethical Considerations

- **Accuracy:** Predictions may be incorrect, and severity labels can be subjective.
- **Data limitations:** Public hotel reviews are not equivalent to real support tickets.
- **Privacy:** Avoid unnecessary personal or sensitive information when using an external AI API.
- **Fairness:** Further testing is required across different writing styles, languages, and guest populations.
- **Transparency:** Displayed explanations help staff inspect recommendations but may not perfectly reflect the model's reasoning.
- **Human oversight:** Staff remain accountable for decisions. The system should not independently make consequential decisions about guests.
- **Security:** Store API credentials in environment variables and exclude them from version control.

### Final Outcome

HotelPulse demonstrates an AI-assisted workflow for complaint classification, severity assessment, priority scoring, and interactive review. The 50-example evaluation provides an initial measure of performance, but broader testing with independently labeled data is needed before real-world deployment.

### Example Output

**Input:**

> Loud construction noise outside my room kept me awake until 2 AM.

| Field | Result |
|---|---|
| Category | Noise |
| Severity | Serious |
| Priority Score | 60/100 |
| Priority Level | High |
| Summary | Construction noise disrupted the guest's sleep. |
| Recommended Action | Refer the issue to the duty manager for review and guest follow-up. |

*Note: This is an illustrative example. Actual AI-generated results may vary between runs.*

---

## File Structure

```text
SWYNEX-HotelPulse/
├── assets/
│   └── hotel-lobby-background.png
├── data/
│   └── hotel_reviews_sample.csv
├── analyzer.py
├── dashboard.py
├── evaluate.py
├── evaluation_examples.json
├── prepare_dataset.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## Tech Stack

- **Python** - application logic and priority scoring.
- **Streamlit** - interactive web application.
- **Groq API** - AI-powered guest-feedback classification.
- **`openai/gpt-oss-120b`** - language model.
- **python-dotenv** - environment-variable management.
- **HTML/CSS** - dashboard styling and priority gauge.
- **Pandas** - dataset preparation and evaluation result handling.
