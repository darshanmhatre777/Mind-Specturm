# Import necessary libraries
import pandas as pd
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QPalette
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

#  Load the preprocessed dataset
# Replace 'your_dataset.csv' with the actual path to your dataset file
dataset = pd.read_excel('Raw data.xlsx')

#  Prepare the dataset for training
# Extract the features (X) and target variable (y)
X = dataset.iloc[:, :-1]  # All columns except the 'Mental_Score'
y = dataset['Mental_Score']

#  Split the dataset into a training and testing set
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

#  Create and train a machine learning model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

#  Get user responses for the 9 questions
user_responses = [4, 4, 4, 4, 6, 6, 6, 0, 0]
#  Predict the user's mental state
predicted_mental_state = model.predict([user_responses])

#  Map the predicted value to the mental state description
mental_state_mapping = {
    0: "Completely Healthy",
    1: "Healthy",
    2: "Above Average",
    3: "Average",
    4: "Below Average",
    5: "Unhealthy",
    6: "Completely Unhealthy"
}

predicted_state_description = mental_state_mapping[predicted_mental_state[0]]

#  Display the predicted mental state to the user
print(f"Predicted Mental State: {predicted_state_description}")

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QComboBox, QPushButton, QMessageBox


# Function to map dropdown responses to numbers
def map_responses_to_numbers(response):
    mapping = {
        "Not at all": 0,
        "Hardly ever": 1,
        "Some of the time": 2,
        "Often": 3,
        "More than half of days": 4,
        "Nearly everyday": 5,
        "Several days": 6
    }
    return mapping.get(response, -1)  # Default to -1 for unknown responses


class MentalHealthSurvey(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Mental Health Survey')
        self.setGeometry(100, 100, 600, 400)
        self.user_responses = []

        # Create a layout for the questions and response options
        layout = QVBoxLayout()

        # Define pastel colors
        pastel_green = QColor(173, 216, 230)  # Light Blue
        pastel_pink = QColor(255, 182, 193)  # Light Pink
        pastel_lavender = QColor(230, 230, 250)  # Light Lavender

        # Set the application palette with pastel colors
        palette = QPalette()
        palette.setColor(QPalette.Button, pastel_green)
        palette.setColor(QPalette.ButtonText, Qt.black)
        palette.setColor(QPalette.Window, Qt.white)
        palette.setColor(QPalette.WindowText, Qt.black)
        palette.setColor(QPalette.Text, Qt.black)
        self.setPalette(palette)

        # List of questions
        questions = [
            "How often do you feel left out?",
            "Over the last 2 weeks, how often have you been bothered by feeling nervous, anxious or on edge?",
            "Over the last 2 weeks, how often have you been bothered by becoming easily annoyed or irritable?",
            "Over the last 2 weeks, how often have you been bothered by feeling afraid as if something awful might happen?",
            "Over the last 2 weeks, how often have you been bothered by little interest or pleasure in doing things?",
            "Over the last 2 weeks, how often have you been bothered by feeling down, depressed, or hopeless?",
            "Over the last 2 weeks, how often have you been bothered by poor appetite or overeating?",
            "Over the last 2 weeks, how often have you been bothered by feeling bad about yourself or that you are a failure or have let yourself or your family down?",
            "Over the last 2 weeks, how often have you been bothered by thoughts that you would be better off dead or of hurting yourself in some way?"
        ]


        # Create a label and dropdown for each question
        for i, question in enumerate(questions):
            label = QLabel(question)
            combo_box = QComboBox()
            combo_box.addItems([
                "Not at all", "Hardly ever", "Some of the time", "Often", "More than half of days", "Nearly everyday",
                "Several days"
            ])
            label.setStyleSheet("font-weight: bold; font-size: 12pt; margin-top: 10px;")
            combo_box.setStyleSheet(
                "background-color: #ADD8E6; border: 1px solid #90EE90; font-size: 12pt; font-weight: bold; color: #000;")
            layout.addWidget(label)
            layout.addWidget(combo_box)
            combo_box.currentIndexChanged.connect(self.update_responses)

            # Create a container for the submit button and center it
            submit_container = QWidget()
            submit_layout = QVBoxLayout()
            submit_container.setLayout(submit_layout)

            # Create a submit button
            submit_button = QPushButton("Submit")
            submit_button.setFixedSize(100, 30)  # Set the size of the button
            submit_button.setStyleSheet("background-color: #40E0D0; color: white; border: none; border-radius: 5px;")
            submit_layout.addWidget(submit_button)
            submit_button.clicked.connect(self.calculate_mental_state)

        # Connect the submit_button to the calculate_mental_state function
        submit_button.clicked.connect(self.calculate_mental_state)

        layout.addWidget(submit_container)

        self.setLayout(layout)

    def update_responses(self):
        # Update the user_responses list as the user selects responses
        self.user_responses = [map_responses_to_numbers(combo.currentText()) for combo in self.findChildren(QComboBox)]

    def calculate_mental_state(self):
        if -1 in self.user_responses:
            result_window = QMessageBox()
            result_window.setText("Please answer all the questions.")
            result_window.exec_()
        else:
            # Use the model to predict the mental state
            predicted_state = model.predict([self.user_responses])[0]

            # Map the numeric value to the mental state as specified
            mental_states = {
                0: "Completely Healthy",
                1: "Healthy",
                2: "Above Average",
                3: "Average",
                4: "Below Average",
                5: "Unhealthy",
                6: "Completely Unhealthy"
            }

            mental_state = mental_states[predicted_state]

        # Display the mental state in a new window
        result_window = QMessageBox()
        result_window.setText(f"Your Mental State: {mental_state}")
        result_window.exec_()

        # Define pastel colors for the result window

        pastel_pink = QColor(255, 182, 193)  # Light Pink
        pastel_lavender = QColor(230, 230, 250)  # Light Lavender

        # Set the result window palette with pastel colors
        palette = QPalette()
        palette.setColor(QPalette.Button, pastel_lavender)
        palette.setColor(QPalette.ButtonText, Qt.black)
        palette.setColor(QPalette.Window, pastel_pink)
        palette.setColor(QPalette.WindowText, Qt.black)
        palette.setColor(QPalette.Text, Qt.black)
        result_window.setPalette(palette)

        # Suggestions based on mental state
        if mental_state == "Completely Healthy":
            suggestion = "You are in great mental health! Keep up the good work and maintain a healthy lifestyle."

        elif mental_state == "Healthy":
            suggestion = "You are in good mental health, but remember to manage stress and take care of your mental well-being."

        elif mental_state == "Above Average":
            suggestion = "Your mental health is above average, but it's essential to focus on self-care and stress management."

        elif mental_state == "Average":
            suggestion = "Your mental health is at an average level. Consider seeking support or counseling if needed."

        elif mental_state == "Below Average":
            suggestion = "Your mental health is below average. It's important to talk to a mental health professional for help and support. Consider the following steps:\n\n" \
                         "1. Reach out to a mental health specialist or therapist.\n" \
                         "2. Seek support from friends and family.\n" \
                         "3. Practice relaxation techniques such as meditation or deep breathing.\n" \
                         "4. Stay physically active and maintain a healthy lifestyle.\n" \
                         "5. Contact helpline numbers for immediate assistance.\n" \
                         "Helpline Numbers:\n" \
                         " - National Suicide Prevention Lifeline: +91 033 24637432 \n" \
                         " - Crisis Text Line: Text 'HOME' to 741741"
            result_window.setStyleSheet("color: yellow;")

        elif mental_state == "Unhealthy":
            suggestion = "Your mental health is not in a good state. Reach out to a mental health expert for assistance. Consider the following steps:\n\n" \
                         "1. Consult a mental health professional or therapist for guidance.\n" \
                         "2. Share your feelings and concerns with friends or family.\n" \
                         "3. Engage in stress-reduction activities like yoga or mindfulness.\n" \
                         "4. Maintain a balanced diet and exercise routine.\n" \
                         "5. Contact helpline numbers for immediate support.\n" \
                         "Helpline Numbers:\n" \
                         " - National Suicide Prevention Lifeline: +91 033 24637432 \n" \
                         " - Crisis Text Line: Text 'HOME' to 741741"
            result_window.setStyleSheet("color: orange;")

        elif mental_state == "Completely Unhealthy":
            suggestion = "Your mental health is in a critical condition. Seek immediate help from a mental health specialist. Please take the following actions:\n\n" \
                         "1. Urgently consult a mental health specialist or therapist.\n" \
                         "2. Share your situation with someone you trust for immediate support.\n" \
                         "3. Avoid being alone and stay in a safe environment.\n" \
                         "4. Contact emergency helpline numbers for immediate assistance.\n" \
                         "Helpline Numbers:\n" \
                         " - National Suicide Prevention Lifeline: +91 033 24637432 \n" \
                         " - Crisis Text Line: Text 'HOME' to 741741\n" \
                         " - 988 (Emergency Services)"
            result_window.setStyleSheet("color: red;")

        result_window.setInformativeText(suggestion)
        result_window.exec_()


def main():
    app = QApplication(sys.argv)
    survey = MentalHealthSurvey()
    survey.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
