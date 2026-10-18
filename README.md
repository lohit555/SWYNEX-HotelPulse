
# HotelPulse

### AI-Powered Complaint Classification & Prioritization

HotelPulse is an AI-powered prototype that helps hotel customer-support teams classify guest complaints and prioritize issues requiring attention.

Internship: Swynex Technologies
- Task 1 - AI Problem Design (Completed)
- Task 2 - Model or API Integration (Completed)
- Task 3 - Intelligent Feature (Completed)

## 1. Problem Statement

Hotels receive guest feedback about cleanliness, service, facilities, food, and other issues. Manually reviewing large volumes of feedback can be time-consuming.

HotelPulse aims to automate complaint classification and provide explainable priority scores to help staff review important issues first.

## 2. Intended User

Hotel customer-support staff and hotel operations teams who review guest feedback and decide which issues need attention.

## 3. AI Use Case

Primary task: Text classification - identify complaint categories from hotel review text.

Supporting feature: Assign a priority score from 0 - 100 and a priority level (Low, Medium, High, or Critical).

Initial categories include:
- Cleanliness
- Staff/Service
- Room/Facilities
- Food/Dining
- Location
- Noise
- Value/Billing

The system supports staff decision-making; human staff remain responsible for final decisions.

## 4. Dataset

Dataset: https://www.kaggle.com/datasets/jiashenliu/515k-hotel-reviews-data-in-europe

This dataset contains approximately 515,000 hotel reviews, including positive and negative review text and reviewer ratings.

A manually labeled evaluation set of 24 hotel feedback examples is used to evaluate the Task 3 prototype. Since the original dataset does not provide verified complaint-category labels, the examples are labeled with expected categories, complaint status, and severity for evaluation. Hotel reviews serve as proxies for complaints, not actual hotel support tickets.

Dataset Attribution: A 2,000-review sample was extracted from the original Kaggle dataset for exploratory purposes. The Kaggle page lists the dataset under the CC0: Public Domain licence and acknowledges Booking.com as the source of the scraped reviews. The sample's sentiment labels are not ground-truth labels for HotelPulse's complaint categories or priority scores.

## 5. Proposed Approach

- Use an existing AI model/API to classify reviews into predefined categories.
- Calculate priority scores using a documented rubric based on issue severity, safety implications, financial impact, urgency, and multiple or unresolved issues.
- Display the categories, priority scores, and supporting explanations in a simple interface.
- Allow staff to review and sort cases by priority.

## 6. Constraints

- Limited internship timeline and API usage budget.
- Public reviews may not represent actual support tickets.
- Model predictions and priority scores may be inaccurate.
- Human review is required before taking action.
- API keys must be stored securely and excluded from the repository.

## 7. Evaluation Approach

The prototype is evaluated using a manually labeled sample of hotel feedback examples.

- Category accuracy: Measures whether the predicted category matches the expected category.
- Complaint detection accuracy: Measures whether the system correctly identifies complaint versus non-complaint feedback.
- Severity accuracy: Measures whether the predicted severity matches the expected severity.
- Failure analysis: Identifies incorrect predictions and opportunities for prompt refinement.
- Functional tests: Check input handling, output validity, and API error handling.

Performance results are reported in Section 12.

## 8. Success Criteria

- Correctly identifies relevant complaint categories.
- Produces valid and explainable priority scores.
- Allows staff to review individual analyses and priority recommendations.
- Demonstrates measurable classification performance on labeled test examples.

## 9. Task 2 Prototype

The working prototype is a Streamlit web app that sends guest feedback to the
Groq API for structured AI classification. It then applies a transparent,
documented scoring rubric to calculate the priority score. The app includes:

- Sample guest reviews for a quick demonstration.
- AI-generated category, summary, explanation, and risk indicators.
- A 0-100 priority gauge with a score breakdown.
- A recommended next step based on transparent rules.
- A five-item in-session recent-analysis queue.
- A hotel-lobby visual background with high-contrast interface controls.

## 10. Tech Stack

- Python - application logic and priority-scoring rubric.
- Streamlit - interactive web interface.
- Groq API - structured AI classification of guest feedback.
- openai/gpt-oss-120b - model used through the Groq API.
- python-dotenv - local environment-variable and API-key loading.
- HTML/CSS - custom dashboard styling and priority gauge presentation.

## 11. File Structure

```text
SWYNEX-HotelPulse/
├── analyzer.py                     # Groq analysis and priority scoring logic
├── dashboard.py                    # Streamlit web application
├── assets/
│   └── hotel-lobby-background.png  # Dashboard background image
├── requirements.txt                # Python dependencies
├── .env.example                    # API-key placeholder only
├── .gitignore                      # Excludes .env and local virtual environments
└── README.md                       # Project and prototype documentation
```

### Run locally

1. Create and activate a Python virtual environment.
2. Install dependencies: `pip install -r requirements.txt`
3. Copy `.env.example` to `.env` and add a valid `GROQ_API_KEY` locally.
4. Run: `streamlit run dashboard.py`

Never commit `.env` or an API key. The included `.env.example` contains only a
placeholder.

### Example input and output

**Input**

> Loud construction noise outside my room kept me awake until 2 AM.

**Expected prototype output**

- Category: `Noise`
- Likely severity: `serious`
- Priority: `High` (60/100)
- Recommended next step: Assign to the duty manager for prompt review and
  guest follow-up.
- Summary: Construction noise disrupted the guest's sleep.
- Analysis explanation: The AI identified overnight construction noise as a serious comfort issue, classifying it as a High-priority Noise complaint with no safety, urgency, financial, or multiple-issue indicators.

AI output can vary slightly. Priority is a decision-support recommendation,
not an automated final decision.

## 12. Task 3 Prototype Improvement and Evaluation

Task 3 improves the HotelPulse prototype through prompt refinement, model evaluation examples, failure-case analysis, and an interactive web interface.

### Improvements Completed

- Refined the AI prompt to improve complaint categorization and severity classification.
- Created a manually labeled evaluation set containing 24 hotel feedback examples.
- Implemented an evaluation script to compare model predictions against expected labels.
- Reviewed incorrect predictions and refined the prompt to address identified classification issues.
- Retained the Streamlit interface for interactive guest-feedback analysis and priority recommendations.

### Evaluation Method

The evaluation script runs the model against the labeled examples and compares predicted results with the expected labels.

The evaluation measures:

- **Category classification accuracy:** Whether the predicted complaint category matches the expected category.
- **Complaint detection accuracy:** Whether the system correctly identifies complaint versus non-complaint feedback.
- **Severity classification accuracy:** Whether the predicted severity matches the expected severity.
- **Failed predictions:** Whether any examples fail to produce a usable prediction.

### Evaluation Results

The latest evaluation completed successfully on all 24 labeled examples.

| Metric | Result |
|---|---:|
| Category classification accuracy | 100.00% (24/24) |
| Complaint detection accuracy | 100.00% (24/24) |
| Severity classification accuracy | 100.00% (24/24) |
| Failed predictions | 0 |

No incorrect category, complaint-detection, or severity predictions were reported in the latest evaluation run.

**Limitations:** These results apply only to the 24-example evaluation set. The sample is small and manually labeled, so the results do not guarantee equivalent performance on unseen hotel reviews or real-world support tickets.

### Failure-Case Analysis

During an earlier evaluation, the feedback "Room service never answered the phone, and we waited two hours for our order" was classified as Food/Dining instead of Staff/Service.

This highlighted the difficulty of distinguishing service-related failures from food-related complaints when both appear in the same review. The prompt was refined, and the latest evaluation correctly classified all 24 examples.

### Evaluation Files

- `evaluation_examples.json` — labeled evaluation examples and expected outputs.
- `evaluate.py` — runs the model evaluation and compares predictions against expected labels.
- `analyzer.py` — contains the AI prompt, classification logic, and priority-scoring logic.
- `dashboard.py` — provides the interactive Streamlit web interface.
- `evaluation_results.csv` — generated evaluation results, available locally when the evaluation script produces the file.

### Run the Evaluation

After configuring the local environment and installing the project dependencies, run:

```bash
python evaluate.py
```

### Run the Interactive Demo

Start the Streamlit web application:

```bash
streamlit run dashboard.py
```

Enter guest feedback to view the AI-generated classification, explanation, severity indicators, and priority recommendation.
