import random
from app import create_app, db
from app.models.assessment import PastQuestion

def seed_mass_questions():
    app = create_app('development')
    with app.app_context():
        subjects = ['Mathematics', 'Science', 'English', 'Physics', 'Chemistry']
        
        # Templates for subjects
        templates = {
            'Mathematics': [
                ("Solve for x: {a}x + {b} = {c}", "x = {res}", ["{res}", "{res1}", "{res2}", "{res3}"]),
                ("What is the square root of {a}?", "{res}", ["{res}", "{res1}", "{res2}", "{res3}"]),
                ("If a triangle has angles {a} and {b}, what is the third angle?", "{res}", ["{res}", "{res1}", "{res2}", "{res3}"]),
                ("Calculate the area of a circle with radius {a}.", "{res}π", ["{res}π", "{res1}π", "{res2}π", "{res3}π"])
            ],
            'Physics': [
                ("A force of {a}N acts on a mass of {b}kg. What is the acceleration?", "{res}m/s²", ["{res}", "{res1}", "{res2}", "{res3}"]),
                ("Calculate the work done when a force of {a}N moves an object {b}m.", "{res}J", ["{res}", "{res1}", "{res2}", "{res3}"]),
                ("What is the pressure of {a}N acting on {b}m² area?", "{res}Pa", ["{res}", "{res1}", "{res2}", "{res3}"]),
                ("Find the potential energy of {a}kg at {b}m height (g=10).", "{res}J", ["{res}", "{res1}", "{res2}", "{res3}"])
            ],
            'Chemistry': [
                ("How many protons are in an atom with atomic number {a}?", "{a}", ["{a}", "{a1}", "{a2}", "{a3}"]),
                ("What is the molar mass of an element with {a} protons and {b} neutrons?", "{res}", ["{res}", "{res1}", "{res2}", "{res3}"]),
                ("An isotope of Carbon has {a} neutrons. What is its mass number?", "{res}", ["{res}", "{res1}", "{res2}", "{res3}"]),
                ("A solution has pH {a}. It is considered:", "{res}", ["Acidic", "Basic", "Neutral", "Alkaline"])
            ],
            'Science': [
                ("Which organ is responsible for {a}?", "{res}", ["{res}", "{alt1}", "{alt2}", "{alt3}"]),
                ("Plants use {a} for photosynthesis.", "{res}", ["Sunlight", "Oxygen", "Nitrogen", "Argon"]),
                ("The unit of {a} is {b}.", "{res}", ["True", "False", "Maybe", "None"]),
                ("Water boils at {a} degrees Celsius.", "100", ["100", "50", "0", "200"])
            ],
            'English': [
                ("Choose the correct tense: I {a} to school yesterday.", "went", ["went", "go", "going", "gone"]),
                ("What is the synonym of '{a}'?", "{res}", ["{res}", "{alt1}", "{alt2}", "{alt3}"]),
                ("Identity the figure of speech: 'The wind {a}'", "{res}", ["Personification", "Metaphor", "Simile", "Irony"]),
                ("The plural of '{a}' is:", "{res}", ["{res}", "{alt1}", "{alt2}", "{alt3}"])
            ]
        }
        
        dummy_data = {
            'res': ['10', '20', '30', '40', '50'],
            'alt': ['15', '25', '35', '45', '55']
        }

        for sub in subjects:
            print(f"Generating questions for {sub}...")
            count = 0
            while count < 100:
                tpl, ans_tpl, opts_tpl = random.choice(templates[sub])
                
                # Dynamic generation of numbers/values
                a = random.randint(1, 20)
                b = random.randint(1, 20)
                c = a * random.randint(2, 5) + b
                res = (c - b) // a if sub == 'Mathematics' and 'x' in tpl else random.randint(1, 100)
                
                text = tpl.format(a=a, b=b, c=c, res=res)
                correct_val = ans_tpl.format(res=res, a=a)
                
                # Create 4 unique options
                options = [ans_tpl.format(res=res, a=a), ans_tpl.format(res=res+5, a=a+1), 
                           ans_tpl.format(res=res-2, a=a-1), ans_tpl.format(res=res*2, a=a*2)]
                
                if sub == 'Science' and '{res}' in opts_tpl:
                     options = ["Heart", "Lungs", "Brain", "Liver"]
                elif sub == 'English' and '{res}' in opts_tpl:
                     options = ["Fast", "Slow", "Quick", "Rapid"]
                
                random.shuffle(options)
                correct_letter = 'A'
                for i, o in enumerate(options):
                    if o == correct_val:
                        correct_letter = chr(65 + i)
                
                q = PastQuestion(
                    subject=sub,
                    year=random.randint(2010, 2023),
                    topic="General",
                    question_text=text,
                    option_a=options[0],
                    option_b=options[1],
                    option_c=options[2],
                    option_d=options[3],
                    correct_answer=correct_letter,
                    explanation=f"Based on standard {sub.lower()} principles.",
                    language='en'
                )
                db.session.add(q)
                count += 1
            
            db.session.commit()
            print(f"Finished {sub}")

if __name__ == '__main__':
    seed_mass_questions()
