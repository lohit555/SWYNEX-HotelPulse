# HotelPulse

### AI-Powered Complaint Classification & Prioritization

HotelPulse is an AI-powered prototype that helps hotel customer-support teams classify guest complaints and prioritize issues requiring attention.

Internship: Swynex Technologies  
Status: Task 1 - AI Use Case Definition

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

- Macro-F1, precision, and recall:** Measure classification performance.
- Confusion matrix: Identify commonly misclassified categories.
- Priority review: Compare predicted priorities with reference assessments using the documented scoring rubric.
- Functional tests: Check input handling, output validity, sorting, and API error handling.

Performance results will be reported after testing.

## 8. Success Criteria

- Correctly identifies relevant complaint categories.
- Produces valid and explainable priority scores.
- Allows staff to view and sort complaints.
- Demonstrates measurable classification performance on labeled test examples.
