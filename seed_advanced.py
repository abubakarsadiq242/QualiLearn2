import random
from app import create_app, db
from app.models.assessment import PastQuestion

def add_advanced_questions():
    app = create_app('development')
    with app.app_context():
        # Physics Advanced
        phys_q = [
            ("What is the terminal velocity of a falling object?", "When drag equals weight", ["Zero", "Infinity", "When drag equals weight", "Constant 9.8m/s"]),
            ("Which law defines Inertia?", "Newton's First Law", ["Newton's First Law", "Newton's Second Law", "Newton's Third Law", "Inverse Square Law"]),
            ("Define Archimedes' Principle.", "Upthrust equals weight of fluid displaced", ["Upthrust equals weight of fluid displaced", "Pressure is constant", "Volume equals mass", "Force equals pressure"])
        ]
        
        # Chemistry Advanced
        chem_q = [
            ("Which element has the highest electronegativity?", "Fluorine", ["Oxygen", "Fluorine", "Chlorine", "Nitrogen"]),
            ("Define a Covalent Bond.", "Sharing of electrons", ["Transfer of electrons", "Sharing of electrons", "Metallic sea", "Van der Waals"]),
            ("What is the shape of a water molecule?", "Bent", ["Linear", "Bent", "Tetrahedral", "Trigonal"])
        ]

        for sub, qs in [('Physics', phys_q), ('Chemistry', chem_q)]:
            for text, correct, opts in qs:
                random.shuffle(opts)
                letter = chr(65 + opts.index(correct))
                q = PastQuestion(
                    subject=sub, year=2024, topic="Advanced",
                    question_text=text, option_a=opts[0], option_b=opts[1], option_c=opts[2], option_d=opts[3],
                    correct_answer=letter, explanation="Advanced scientific concept.", language='en'
                )
                db.session.add(q)
        
        db.session.commit()
        print("Advanced questions added.")

if __name__ == '__main__':
    add_advanced_questions()
