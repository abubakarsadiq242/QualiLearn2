from app import create_app, db
from app.models.assessment import PastQuestion

def seed_past_questions():
    app = create_app('development')
    with app.app_context():
        questions = [
            # Mathematics
            {
                'subject': 'Mathematics', 'year': 2023, 'topic': 'Algebra',
                'question_text': 'Simplify: 3(x + 2) - 2(x - 1)',
                'option_a': 'x + 4', 'option_b': 'x + 8', 'option_c': '5x + 4', 'option_d': 'x + 7',
                'correct_answer': 'B', 'explanation': '3x + 6 - 2x + 2 = x + 8', 'language': 'en'
            },
            {
                'subject': 'Mathematics', 'year': 2023, 'topic': 'Geometry',
                'question_text': 'What is the sum of angles in a triangle?',
                'option_a': '90', 'option_b': '180', 'option_c': '270', 'option_d': '360',
                'correct_answer': 'B', 'explanation': 'Angle sum property of a triangle is 180 degrees.', 'language': 'en'
            },
            # Science
            {
                'subject': 'Science', 'year': 2023, 'topic': 'Biology',
                'question_text': 'Which part of the cell is known as the powerhouse?',
                'option_a': 'Nucleus', 'option_b': 'Ribosome', 'option_c': 'Mitochondria', 'option_d': 'Cytoplasm',
                'correct_answer': 'C', 'explanation': 'Mitochondria generate most of the chemical energy needed to power the cell.', 'language': 'en'
            },
            # Physics
            {
                'subject': 'Physics', 'year': 2023, 'topic': 'Mechanics',
                'question_text': 'What is the unit of Force?',
                'option_a': 'Joule', 'option_b': 'Watt', 'option_c': 'Newton', 'option_d': 'Pascal',
                'correct_answer': 'C', 'explanation': 'The SI unit of force is the Newton (N).', 'language': 'en'
            },
            # Chemistry
            {
                'subject': 'Chemistry', 'year': 2023, 'topic': 'Atomic Structure',
                'question_text': 'What is the atomic number of Carbon?',
                'option_a': '4', 'option_b': '6', 'option_c': '12', 'option_d': '14',
                'correct_answer': 'B', 'explanation': 'Carbon has 6 protons, hence atomic number 6.', 'language': 'en'
            }
        ]
        
        for q in questions:
            exists = PastQuestion.query.filter_by(question_text=q['question_text']).first()
            if not exists:
                new_q = PastQuestion(**q)
                db.session.add(new_q)
                print(f"Added: {q['subject']} question")
        
        db.session.commit()
        print("Past questions seeded.")

if __name__ == '__main__':
    seed_past_questions()
