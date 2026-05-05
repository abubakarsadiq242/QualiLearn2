import random
from datetime import datetime
from app import create_app, db
from app.models.assessment import PastQuestion
from app.models.flashcard import Flashcard

def seed_final_content():
    app = create_app('development')
    with app.app_context():
        languages = ['en', 'ha', 'yo', 'ig', 'pi']
        subjects = [
            'Mathematics', 'English', 'Biology', 'Physics', 'Chemistry', 
            'Agricultural Science', 'Social Studies', 
            'Commerce', 'Geography', 'Science'
        ]
        
        # 1. QUESTION TEMPLATES
        q_templates = {
            'Mathematics': [
                ("Solve for x: {a}x + {b} = {c}", "{res}", ["{res}", "{res1}", "{res2}", "{res3}"]),
                ("What is the square root of {a2}?", "{a}", ["{a}", "{a_alt1}", "{a_alt2}", "{a_alt3}"]),
                ("If a triangle has angles {a} and {b}, what is the third angle?", "{res}", ["{res}", "{res1}", "{res2}", "{res3}"]),
                ("Calculate the area of a rectangle with length {a} and width {b}.", "{res}", ["{res}", "{res1}", "{res2}", "{res3}"])
            ],
            'Physics': [
                ("A force of {a}N acts on a mass of {b}kg. What is the acceleration?", "{res}m/s²", ["{res}m/s²", "{res1}m/s²", "{res2}m/s²", "{res3}m/s²"]),
                ("What is the unit of {item}?", "{unit}", ["{unit}", "{u1}", "{u2}", "{u3}"]),
                ("Calculate work done: Force={a}N, Distance={b}m.", "{res}J", ["{res}J", "{res1}J", "{res2}J", "{res3}J"]),
                ("The speed of light is approximately:", "3x10^8 m/s", ["3x10^8 m/s", "3x10^6 m/s", "1x10^8 m/s", "3x10^10 m/s"])
            ],
            'Chemistry': [
                ("What is the chemical symbol for {item}?", "{sym}", ["{sym}", "{s1}", "{s2}", "{s3}"]),
                ("What is the atomic number of {item}?", "{num}", ["{num}", "{n1}", "{n2}", "{n3}"]),
                ("A solution with pH {a} is:", "{type}", ["Acidic", "Basic", "Neutral", "None"]),
                ("The most abundant gas in the atmosphere is:", "Nitrogen", ["Nitrogen", "Oxygen", "Argon", "Carbon Dioxide"])
            ],
            'Biology': [
                ("The powerhouse of the cell is the:", "Mitochondria", ["Mitochondria", "Nucleus", "Ribosome", "Vacuole"]),
                ("Which organ is responsible for pumping blood?", "Heart", ["Heart", "Lungs", "Liver", "Brain"]),
                ("Plants make food through a process called:", "Photosynthesis", ["Photosynthesis", "Respiration", "Transpiration", "Digestion"]),
                ("How many bones are in the adult human body?", "206", ["206", "208", "210", "196"])
            ],
            'English': [
                ("Choose the correct synonym for '{word}':", "{syn}", ["{syn}", "{alt1}", "{alt2}", "{alt3}"]),
                ("What is the plural of '{word}'?", "{plural}", ["{plural}", "{alt1}", "{alt2}", "{alt3}"]),
                ("Identify the part of speech: '{word}'", "{part}", ["Noun", "Verb", "Adjective", "Adverb"]),
                ("Choose the correct spelling:", "{word}", ["{word}", "{w1}", "{w2}", "{w3}"])
            ],
            'Agricultural Science': [
                ("The process of removing weeds is called:", "Weeding", ["Weeding", "Mulching", "Pruning", "Thinning"]),
                ("Which of these is a cash crop?", "Cocoa", ["Cocoa", "Maize", "Yam", "Cassava"]),
                ("A tool used for loosening soil is:", "Hoe", ["Hoe", "Cutlass", "Spade", "Rake"]),
                ("The study of soil management and crop production is:", "Agronomy", ["Agronomy", "Biology", "Ecology", "Botany"])
            ],
            'Social Studies': [
                ("The primary agent of socialization is the:", "Family", ["Family", "School", "Church", "Peer group"]),
                ("Integrity means being:", "Honest", ["Honest", "Rich", "Famous", "Strong"]),
                ("Which of these is a social problem?", "Drug abuse", ["Drug abuse", "Reading", "Dancing", "Sports"]),
                ("Human rights are:", "Universal", ["Universal", "Limited", "Optional", "Local"])
            ],
            'Commerce': [
                ("Commerce is the study of:", "Trade and aids to trade", ["Trade and aids to trade", "Production", "Banking", "Accounting"]),
                ("Which of these is an aid to trade?", "Insurance", ["Insurance", "Farming", "Teaching", "Cooking"]),
                ("A wholesaler buys in:", "Bulk", ["Bulk", "Small quantities", "Singles", "Pairs"]),
                ("The exchange of goods for goods is:", "Barter", ["Barter", "Purchase", "Sale", "Credit"])
            ],
            'Geography': [
                ("The largest continent in the world is:", "Asia", ["Asia", "Africa", "North America", "Europe"]),
                ("A map scale of 1:50,000 is a:", "Small scale", ["Small scale", "Large scale", "Linear scale", "None"]),
                ("Igneous rocks are formed from:", "Cooling of magma", ["Cooling of magma", "Pressure", "Erosion", "Sediments"]),
                ("The imaginary line dividing the Earth into North and South is:", "Equator", ["Equator", "Prime Meridian", "Tropic of Cancer", "Axis"])
            ],
            'Science': [
                ("The state of matter with a definite shape is:", "Solid", ["Solid", "Liquid", "Gas", "Plasma"]),
                ("Electric current is measured in:", "Amperes", ["Amperes", "Volts", "Ohms", "Watts"]),
                ("The boiling point of pure water is:", "100°C", ["100°C", "0°C", "50°C", "200°C"]),
                ("An example of a renewable energy source is:", "Solar", ["Solar", "Coal", "Oil", "Natural Gas"])
            ]
        }

        # 2. FLASHCARD TEMPLATES
        f_templates = {
            'Mathematics': [("Pythagoras Theorem", "a² + b² = c²"), ("Area of Circle", "πr²"), ("Quadratic Formula", "x = [-b ± sqrt(b²-4ac)] / 2a")],
            'Physics': [("Newton's 2nd Law", "F = ma"), ("Ohm's Law", "V = IR"), ("Kinetic Energy", "1/2 mv²")],
            'Chemistry': [("Avogadro's Number", "6.022 x 10²³"), ("Ideal Gas Law", "PV = nRT"), ("Periodic Table", "Arrangement of elements by atomic number")],
            'Biology': [("DNA", "Deoxyribonucleic Acid"), ("ATP", "Adenosine Triphosphate"), ("Mitosis", "Cell division resulting in two identical cells")],
            'English': [("Simile", "Comparison using like or as"), ("Metaphor", "Direct comparison"), ("Onomatopoeia", "Word that sounds like its meaning")],
            'Agricultural Science': [("Photosynthesis", "Plants making food from sunlight"), ("Erosion", "Wearing away of soil"), ("Irrigation", "Artificial watering of crops")],
            'Social Studies': [("Values", "Beliefs that guide behavior"), ("Culture", "Way of life of a people"), ("Leadership", "Ability to guide or influence others")],
            'Commerce': [("Asset", "Something of value owned"), ("Liability", "Money owed to others"), ("Equity", "Ownership interest in a business")],
            'Geography': [("Latitude", "Lines running East-West"), ("Longitude", "Lines running North-South"), ("Climate", "Long-term weather patterns")],
            'Science': [("Mass", "Amount of matter in an object"), ("Weight", "Force of gravity on an object"), ("Density", "Mass per unit volume")]
        }

        # 3. SEEDING LOGIC
        for lang in languages:
            print(f"Seeding for language: {lang}")
            for sub in subjects:
                print(f"  Subject: {sub}")
                
                # Questions
                for i in range(50):
                    tpls = q_templates.get(sub, q_templates['Science'])
                    text_tpl, ans_tpl, opts_tpl = random.choice(tpls)
                    
                    # Randomize variables if present
                    a = random.randint(1, 100)
                    b = random.randint(1, 100)
                    c = a + b
                    a2 = a * a
                    word = random.choice(["Happy", "Fast", "Smart", "Large", "Quick"])
                    item = random.choice(["Oxygen", "Gold", "Iron", "Carbon"])
                    sym = "O" if item == "Oxygen" else "Au" if item == "Gold" else "Fe" if item == "Iron" else "C"
                    
                    text = text_tpl.format(a=a, b=b, c=c, a2=a2, word=word, item=item)
                    
                    format_args = {
                        'res': c, 'res1': c+5, 'res2': c-2, 'res3': c*2,
                        'a': a, 'a_alt1': a+2, 'a_alt2': a-1, 'a_alt3': a*2,
                        'word': word, 'alt1': "Option X", 'alt2': "Option Y", 'alt3': "Option Z",
                        'item': item, 'sym': sym, 's1': "S1", 's2': "S2", 's3': "S3",
                        'num': a, 'n1': a+1, 'n2': a+2, 'n3': a+3,
                        'unit': "Unit", 'u1': "U1", 'u2': "U2", 'u3': "U3",
                        'syn': "Synonym", 'plural': word + "s", 'part': "Noun",
                        'w1': "W1", 'w2': "W2", 'w3': "W3",
                        'type': "Acidic"
                    }
                    
                    correct_val = ans_tpl.format(**format_args)
                    
                    # Mix in real answers with some generic ones for high volume
                    options = []
                    for opt in opts_tpl:
                        options.append(opt.format(**format_args))
                    
                    # Ensure correct answer is in options
                    if correct_val not in options:
                        options[0] = correct_val
                    
                    random.shuffle(options)
                    correct_letter = chr(65 + options.index(correct_val))
                    
                    q = PastQuestion(
                        subject=sub,
                        year=random.randint(2015, 2024),
                        topic="General Practice",
                        question_text=text,
                        option_a=options[0],
                        option_b=options[1],
                        option_c=options[2],
                        option_d=options[3],
                        correct_answer=correct_letter,
                        explanation=f"This is a fundamental concept in {sub}.",
                        language=lang,
                    )
                    db.session.add(q)
                
                # Flashcards
                for i in range(50):
                    tpls = f_templates.get(sub, f_templates['Science'])
                    front, back = random.choice(tpls)
                    # Add suffix to ensure uniqueness
                    db.session.add(Flashcard(
                        subject=sub,
                        front=f"{front} ({i+1})",
                        back=back,
                        language=lang,
                        user_id=1
                    ))
                
                db.session.commit()
                print(f"    Added 50 questions and 50 flashcards for {sub} in {lang}")

        print("Comprehensive seeding completed successfully!")

if __name__ == '__main__':
    seed_final_content()
