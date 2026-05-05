import random
from app import create_app, db
from app.models.assessment import PastQuestion

def seed_50_questions():
    app = create_app('development')
    with app.app_context():
        # Core 5 Subjects
        subjects = ['Mathematics', 'English', 'Biology', 'Physics', 'Chemistry']
        languages = ['en', 'ha', 'yo', 'ig', 'pi']
        
        # Templates for subjects
        templates = {
            'Mathematics': [
                ("Solve for x: {a}x + {b} = {c}", "x = {res}", ["{res}", "{res1}", "{res2}", "{res3}"], "Algebra"),
                ("What is the square root of {a_sq}?", "{a}", ["{a}", "{a1}", "{a2}", "{a3}"], "Arithmetic"),
                ("If a triangle has angles {a} and {b}, what is the third angle?", "{res}", ["{res}", "{res1}", "{res2}", "{res3}"], "Geometry"),
                ("Calculate the area of a circle with radius {a}.", "{res_sq}π", ["{res_sq}π", "{res1}π", "{res2}π", "{res3}π"], "Geometry"),
                ("What is the value of {a} squared plus {b} squared?", "{res}", ["{res}", "{res1}", "{res2}", "{res3}"], "Arithmetic")
            ],
            'Physics': [
                ("A force of {a}N acts on a mass of {b}kg. What is the acceleration?", "{res}m/s²", ["{res}m/s²", "{res1}m/s²", "{res2}m/s²", "{res3}m/s²"], "Mechanics"),
                ("Calculate the work done when a force of {a}N moves an object {b}m.", "{res}J", ["{res}J", "{res1}J", "{res2}J", "{res3}J"], "Energy"),
                ("What is the pressure of {a}N acting on {b}m² area?", "{res}Pa", ["{res}Pa", "{res1}Pa", "{res2}Pa", "{res3}Pa"], "Mechanics"),
                ("Find the potential energy of {a}kg at {b}m height (g=10).", "{res}J", ["{res}J", "{res1}J", "{res2}J", "{res3}J"], "Energy"),
                ("What is the frequency of a wave with period {a} seconds?", "{res}Hz", ["{res}Hz", "{res1}Hz", "{res2}Hz", "{res3}Hz"], "Waves")
            ],
            'Chemistry': [
                ("How many protons are in an atom with atomic number {a}?", "{a}", ["{a}", "{a1}", "{a2}", "{a3}"], "Atomic Structure"),
                ("What is the mass number of an element with {a} protons and {b} neutrons?", "{res}", ["{res}", "{res1}", "{res2}", "{res3}"], "Atomic Structure"),
                ("An isotope has {a} protons and {b} neutrons. What is its symbol?", "Element-{res}", ["Element-{res}", "Element-{res1}", "Element-{res2}", "Element-{res3}"], "Atomic Structure"),
                ("A solution has pH {a}. It is considered:", "{res_type}", ["Acidic", "Basic", "Neutral", "Alkaline"], "Acids & Bases"),
                ("What is the valence electron count for an atom in Group {a}?", "{a}", ["{a}", "{a1}", "{a2}", "{a3}"], "Periodic Table")
            ],
            'Biology': [
                ("The powerhouse of the cell is the:", "Mitochondria", ["Mitochondria", "Nucleus", "Ribosome", "Vacuole"], "Cell Biology"),
                ("Which organ is primarily responsible for filtering blood?", "Kidney", ["Kidney", "Heart", "Liver", "Lungs"], "Human Systems"),
                ("Photosynthesis primarily occurs in which part of the plant?", "Leaf", ["Leaf", "Root", "Stem", "Flower"], "Botany"),
                ("How many chambers does a human heart have?", "4", ["4", "2", "3", "1"], "Human Systems"),
                ("What is the primary gas produced by plants during the day?", "Oxygen", ["Oxygen", "Carbon Dioxide", "Nitrogen", "Argon"], "Ecology")
            ],
            'English': [
                ("Choose the correct tense: I ___ to school yesterday.", "went", ["went", "go", "going", "gone"], "Grammar"),
                ("What is the synonym of 'Quick'?", "Fast", ["Fast", "Slow", "Heavy", "Quiet"], "Vocabulary"),
                ("The plural of 'Child' is:", "Children", ["Children", "Childs", "Childrens", "Childes"], "Grammar"),
                ("Which of these is a Metaphor?", "Life is a journey", ["Life is a journey", "As brave as a lion", "Boom!", "Alas!"], "Literature"),
                ("Identify the Noun in: 'The happy dog barked.'", "Dog", ["Dog", "Happy", "Barked", "The"], "Grammar")
            ]
        }

        print("Deleting old past questions...")
        db.session.query(PastQuestion).delete()
        db.session.commit()

        for sub in subjects:
            print(f"Generating 50 questions for {sub}...")
            for i in range(50):
                tpl_data = random.choice(templates[sub])
                tpl, ans_tpl, opts_tpl, topic = tpl_data
                
                # Randomize variables
                a = random.randint(1, 20)
                b = random.randint(1, 20)
                a_sq = a * a
                c = a * random.randint(2, 5) + b
                
                # Calc math results
                if sub == 'Mathematics':
                    if 'x +' in tpl: res = (c - b) // a
                    elif 'square root' in tpl: res = a
                    elif 'triangle' in tpl: res = 180 - a - b
                    elif 'circle' in tpl: res = a * a
                    else: res = a*a + b*b
                elif sub == 'Physics':
                    if 'force' in tpl: res = a // b if b != 0 else a
                    elif 'work' in tpl: res = a * b
                    elif 'pressure' in tpl: res = a // b if b != 0 else a
                    elif 'potential' in tpl: res = a * b * 10
                    else: res = 1 // a if a != 0 else 1
                elif sub == 'Chemistry':
                    if 'pH' in tpl: res_type = "Acidic" if a < 7 else ("Basic" if a > 7 else "Neutral")
                    res = a + b
                else:
                    res = a # dummy
                
                # Format text
                text = tpl.format(a=a, b=b, c=c, a_sq=a_sq, res=res, res_sq=res, res_type=res_type if 'res_type' in locals() else '')
                correct_val = ans_tpl.format(res=res, a=a, res_sq=res, res_type=res_type if 'res_type' in locals() else '')
                
                # Options
                final_options = []
                for o_tpl in opts_tpl:
                    val = o_tpl.format(res=res, a=a, a1=a+1, a2=a+2, a3=a+3, 
                                      res1=res+5, res2=res-2, res3=res*2, res_sq=res)
                    final_options.append(val)
                
                # Ensure unique options
                final_options = list(set(final_options))
                while len(final_options) < 4:
                    final_options.append(f"Option {len(final_options) + 1}")
                
                random.shuffle(final_options)
                correct_letter = 'A'
                for idx, opt in enumerate(final_options):
                    if opt == correct_val:
                        correct_letter = chr(65 + idx)
                
                # Add for all languages
                for lang in languages:
                    q = PastQuestion(
                        subject=sub,
                        year=random.randint(2015, 2024),
                        topic=topic,
                        question_text=text,
                        option_a=final_options[0],
                        option_b=final_options[1],
                        option_c=final_options[2],
                        option_d=final_options[3],
                        correct_answer=correct_letter,
                        explanation=f"This is a standard {sub} problem based on {topic} principles.",
                        language=lang,
                        education_level='Academics'
                    )
                    db.session.add(q)
            
            db.session.commit()
            print(f"Completed {sub}")

        print("Total questions in DB:", db.session.query(PastQuestion).count())

if __name__ == '__main__':
    seed_50_questions()
