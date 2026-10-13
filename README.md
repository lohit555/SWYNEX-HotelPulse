# HotelPulse

### AI-Powered Complaint Classification & Prioritization

HotelPulse is an AI-powered prototype that helps hotel customer-support teams classify guest complaints and prioritize issues requiring attention.

Internship: Swynex Technologies
Task 1 - AI Problem Design (Completed)
Task 2 - Model or API Integration (Completed)

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

A manageable subset will be used for the prototype. Since the dataset does not provide verified complaint-category labels, a smaller sample will be manually labeled for evaluation. Hotel reviews will serve as proxies for complaints, not actual hotel support tickets.

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

The prototype will be evaluated using a held-out, manually labeled sample of reviews.

- Macro-F1, precision, and recall: Measure classification performance.
- Confusion matrix: Identify commonly misclassified categories.
- Priority review: Compare predicted priorities with reference assessments using the documented scoring rubric.
- Functional tests: Check input handling, output validity, sorting, and API error handling.

Performance results will be reported after testing.

## 8. Success Criteria

- Correctly identifies relevant complaint categories.
- Produces valid and explainable priority scores.
- Allows staff to view and sort complaints.
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
- Summary: Construction noise disrupted the guest's sleep.
- Recommended next step: Assign to the duty manager for prompt review and
  guest follow-up.

AI output can vary slightly. Priority is a decision-support recommendation,
not an automated final decision.
