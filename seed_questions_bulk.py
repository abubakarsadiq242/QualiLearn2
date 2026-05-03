from app import create_app, db
from app.models.assessment import PastQuestion

def seed_bulk_questions():
    app = create_app('development')
    with app.app_context():
        languages = ['en', 'ha', 'yo', 'ig', 'pi']
        
        # Mathematics (50)
        math_questions = [
            ('Solve for x: 2x + 4 = 10', '3', '6', '2', '5', 'A', 'Linear Algebra'),
            ('What is the square root of 81?', '7', '8', '9', '10', 'C', 'Arithmetic'),
            ('Sum of angles in a triangle?', '90', '180', '270', '360', 'B', 'Geometry'),
            ('Value of Pi rounded to 2 decimal places?', '3.12', '3.14', '3.16', '3.18', 'B', 'Geometry'),
            ('Solve: 5^2 - 4^2', '9', '1', '16', '25', 'A', 'Arithmetic'),
            ('What is 25 percent of 80?', '15', '20', '25', '30', 'B', 'Percentage'),
            ('Slope of line y = 4x - 2', '4', '-2', '2', '1', 'A', 'Coordinate Geometry'),
            ('Number of sides in a hexagon?', '5', '6', '7', '8', 'B', 'Polygons'),
            ('Probability of flipping heads on a coin?', '0.2', '0.5', '0.7', '1.0', 'B', 'Probability'),
            ('Integral of 2x dx?', 'x^2', '2x^2', 'x', '2', 'A', 'Calculus'),
            ('Mean of 2, 4, 6?', '4', '3', '5', '12', 'A', 'Statistics'),
            ('Area of rectangle (L=5, W=4)?', '9', '20', '18', '10', 'B', 'Mensuration'),
            ('Volume of cube with side 3?', '9', '27', '12', '18', 'B', 'Mensuration'),
            ('Solve: 10/2 + 3', '5', '8', '7', '6', 'B', 'Arithmetic'),
            ('Is 17 a prime number?', 'Yes', 'No', 'Depends', 'Idk', 'A', 'Number Theory'),
            ('Pythagorean triple?', '3,4,5', '1,2,3', '2,4,6', '1,1,2', 'A', 'Geometry'),
            ('Value of x if x^2 = 16?', '2', '4', '8', '16', 'B', 'Algebra'),
            ('Exterior angle of hexagon?', '60', '90', '120', '180', 'A', 'Geometry'),
            ('Binary of 4?', '100', '111', '101', '011', 'A', 'Computing'),
            ('Denominator in 3/4?', '3', '4', '0.75', '1', 'B', 'Fractions'),
            ('Hypotenuse of triangle (3,4)?', '5', '6', '7', '8', 'A', 'Geometry'),
            ('Log 100 base 10?', '1', '2', '10', '100', 'B', 'Logarithms'),
            ('Mode of 1, 2, 2, 3?', '1', '2', '3', '2.5', 'B', 'Statistics'),
            ('Complementary angle of 30?', '30', '60', '90', '150', 'B', 'Geometry'),
            ('Equation of circle at origin (r=5)?', 'x+y=25', 'x^2+y^2=5', 'x^2+y^2=25', 'xy=25', 'C', 'Geometry'),
            ('Factorial of 4 (4!)?', '12', '24', '16', '10', 'B', 'Probability'),
            ('Solve: 2(x - 3) = 14', '7', '10', '4', '14', 'B', 'Algebra'),
            ('Interior angle sum of pentagon?', '180', '360', '540', '720', 'C', 'Geometry'),
            ('Derivative of 5x^3?', '15x^2', '5x^2', '15x', '3', 'A', 'Calculus'),
            ('Simple interest on 100, 5%, 2yrs?', '10', '5', '15', '20', 'A', 'Finance'),
            ('Value of tan(45)?', '0', '0.5', '1', 'Infinity', 'C', 'Trigonometry'),
            ('Factors of 6?', '1,2,3,6', '1,6', '2,3', '1,2,3', 'A', 'Arithmetic'),
            ('Solve: 4x < 12', 'x < 3', 'x = 3', 'x > 3', 'x < 4', 'A', 'Inequalities'),
            ('L.C.M of 4 and 6?', '12', '24', '4', '6', 'A', 'Arithmetic'),
            ('H.C.F of 8 and 12?', '2', '4', '8', '12', 'B', 'Arithmetic'),
            ('Gradient of vertical line?', '0', '1', 'Undefined', '90', 'C', 'Geometry'),
            ('Circumference of circle (d=14)?', '22', '44', '66', '88', 'B', 'Geometry'),
            ('Value of cos(0)?', '0', '0.5', '1', '-1', 'C', 'Trigonometry'),
            ('Square of 13?', '139', '169', '144', '156', 'B', 'Arithmetic'),
            ('Distance between (0,0) and (3,4)?', '5', '7', '12', '25', 'A', 'Geometry'),
            ('Scientific notation: 450?', '4.5x10^2', '4.5x10^1', '45x10', '4.5', 'A', 'Science'),
            ('Midpoint of (0,0) and (4,4)?', '(2,2)', '(2,0)', '(0,2)', '(4,4)', 'A', 'Geometry'),
            ('Solution of x + y = 5, x - y = 1?', '(3,2)', '(2,3)', '(4,1)', '(5,0)', 'A', 'Simultaneous'),
            ('What is an Obtuse angle?', '< 90', '90', '> 90 and < 180', '360', 'C', 'Geometry'),
            ('Volume of cylinder (r=1, h=10)?', '10π', '20π', 'π', '10', 'A', 'Mensuration'),
            ('Slope of line x = 5?', '0', '5', 'Undefined', '1', 'C', 'Geometry'),
            ('Probability of 7 on a dice?', '1/6', '0', '1', '7/6', 'B', 'Probability'),
            ('Sum of 1/2 + 1/3?', '2/5', '1/5', '5/6', '1/6', 'C', 'Fractions'),
            ('Cube root of 64?', '4', '8', '16', '32', 'A', 'Arithmetic'),
            ('Diagonal of square side 1?', '1', '2', 'sqrt(2)', '0.5', 'C', 'Geometry')
        ]

        # English (50)
        english_questions = [
            ('Identify the Noun: "The bright sun rose."', 'Bright', 'Sun', 'Rose', 'The', 'B', 'Grammar'),
            ('Synonym for "Begin"?', 'End', 'Stop', 'Start', 'Pause', 'C', 'Vocabulary'),
            ('Antonym for "Fast"?', 'Quick', 'Rapid', 'Slow', 'Active', 'C', 'Vocabulary'),
            ('Plural of "Mouse"?', 'Mouses', 'Mice', 'Meese', 'Mouse', 'B', 'Grammar'),
            ('Past tense of "Go"?', 'Goded', 'Went', 'Gone', 'Going', 'B', 'Grammar'),
            ('Correct spelling?', 'Beautiful', 'Beatiful', 'Beautifull', 'Beatfull', 'A', 'Spelling'),
            ('Figure of speech: "Life is a journey"?', 'Simile', 'Metaphor', 'Pun', 'Irony', 'B', 'Literature'),
            ('Identify the Adjective: "The old man sat."', 'Old', 'Man', 'Sat', 'The', 'A', 'Grammar'),
            ('Opposite of "Heavy"?', 'Weighty', 'Light', 'Big', 'Hard', 'B', 'Vocabulary'),
            ('Plural of "Child"?', 'Childs', 'Children', 'Childrens', 'Childes', 'B', 'Grammar'),
            ('Meaning of "Euphemism"?', 'Harsh word', 'Mild word', 'Big word', 'Small word', 'B', 'Literature'),
            ('Synonym of "Vanish"?', 'Appear', 'Disappear', 'Hide', 'Stay', 'B', 'Vocabulary'),
            ('Identify the Verb: "She laughed loudly."', 'She', 'Laughed', 'Loudly', 'None', 'B', 'Grammar'),
            ('"He runs as fast as light" is a...?', 'Metaphor', 'Simile', 'Hyperbole', 'Oxymoron', 'B', 'Literature'),
            ('Antonym of "Kind"?', 'Nice', 'Cruel', 'Good', 'Careful', 'B', 'Vocabulary'),
            ('Select the interjection:', 'Wow!', 'Run', 'Red', 'Beautiful', 'A', 'Grammar'),
            ('Plural of "Box"?', 'Boxs', 'Boxies', 'Boxes', 'Boxe', 'C', 'Grammar'),
            ('Synonym of "Annual"?', 'Monthly', 'Yearly', 'Daily', 'Weekly', 'B', 'Vocabulary'),
            ('Meaning of "Optimistic"?', 'Positive', 'Negative', 'Sad', 'Angry', 'A', 'Vocabulary'),
            ('Past participle of "Write"?', 'Wrote', 'Written', 'Writing', 'Writes', 'B', 'Grammar'),
            ('Identify the Pronoun: "They are here."', 'They', 'Are', 'Here', 'None', 'A', 'Grammar'),
            ('Meaning of "Idiom"?', 'Literal meaning', 'Non-literal', 'A type of tool', 'A location', 'B', 'Vocabulary'),
            ('A story with animals as characters is a...?', 'Legend', 'History', 'Fable', 'Science', 'C', 'Literature'),
            ('Correct use: "They ___ playing."', 'is', 'am', 'are', 'was', 'C', 'Grammar'),
            ('Antonym of "Cheap"?', 'Easy', 'Expensive', 'Bargain', 'Low', 'B', 'Vocabulary'),
            ('Synonym of "Courage"?', 'Fear', 'Bravery', 'Weakness', 'Shyness', 'B', 'Vocabulary'),
            ('A person who writes books?', 'Baker', 'Author', 'Painter', 'Driver', 'B', 'Vocabulary'),
            ('Meaning of "Hyperbole"?', 'Understatement', 'Exaggeration', 'Truth', 'Lie', 'B', 'Literature'),
            ('Which is a compound word?', 'Sun', 'Sunshine', 'Shine', 'Sky', 'B', 'Grammar'),
            ('Plural of "Sheep"?', 'Sheeps', 'Sheepies', 'Sheep', 'Sheepers', 'C', 'Grammar'),
            ('Meaning of "Ancient"?', 'New', 'Old', 'Future', 'Now', 'B', 'Vocabulary'),
            ('Identify Adverb: "He ran quickly."', 'He', 'Ran', 'Quickly', 'None', 'C', 'Grammar'),
            ('Group of lions is called a...?', 'Pack', 'Flock', 'Pride', 'Swarm', 'C', 'Vocabulary'),
            ('Opposite of "Visible"?', 'Clear', 'Invisible', 'Seen', 'Bright', 'B', 'Vocabulary'),
            ('Who is the Antagonist?', 'Main hero', 'Villian/Opponent', 'Narrator', 'Author', 'B', 'Literature'),
            ('Synonym of "Brisk"?', 'Slow', 'Energetic', 'Lazy', 'Heavy', 'B', 'Vocabulary'),
            ('A word that sounds like what it means?', 'Simile', 'Onomatopoeia', 'Irony', 'Metaphor', 'B', 'Literature'),
            ('Antonym of "Brave"?', 'Fearless', 'Cowardly', 'Strong', 'Bold', 'B', 'Vocabulary'),
            ('Correct punctuation for surprise?', '.', '?', '!', ',', 'C', 'Grammar'),
            ('Identify the Subject: "John read the book."', 'John', 'Read', 'Book', 'The', 'A', 'Grammar'),
            ('Synonym of "Abundant"?', 'Sparse', 'Plentiful', 'Lacking', 'Small', 'B', 'Vocabulary'),
            ('Past tense of "Buy"?', 'Buyed', 'Bought', 'Buying', 'Buys', 'B', 'Grammar'),
            ('Identify Conjunction: "Fish and Chips"', 'Fish', 'And', 'Chips', 'None', 'B', 'Grammar'),
            ('Plural of "Knife"?', 'Knifes', 'Knives', 'Knive', 'Knife', 'B', 'Grammar'),
            ('Synonym of "Diligent"?', 'Lazy', 'Hardworking', 'Smart', 'Quick', 'B', 'Vocabulary'),
            ('Correct spelling?', 'Definitely', 'Definitly', 'Definatly', 'Defenitely', 'A', 'Spelling'),
            ('Identify Preposition: "Under the table"', 'Under', 'The', 'Table', 'None', 'A', 'Grammar'),
            ('Opposite of "Hostile"?', 'Angry', 'Friendly', 'Cold', 'Silent', 'B', 'Vocabulary'),
            ('Synonym of "Sorrow"?', 'Happiness', 'Sadness', 'Joy', 'Laughter', 'B', 'Vocabulary'),
            ('Plural of "Ox"?', 'Oxes', 'Oxen', 'Oxi', 'Ox', 'B', 'Grammar')
        ]

        # Science (50)
        science_questions = [
            ('Powerhouse of the cell?', 'Nucleus', 'Mitochondria', 'Ribosome', 'Wall', 'B', 'Biology'),
            ('Symbol for Oxygen?', 'Ox', 'O', 'O2', 'G', 'B', 'Chemistry'),
            ('Planet known as the Red Planet?', 'Venus', 'Mars', 'Jupiter', 'Saturn', 'B', 'Physics'),
            ('Boiling point of water (C)?', '0', '50', '100', '200', 'C', 'Physics'),
            ('Sun is a...?', 'Planet', 'Star', 'Moon', 'Comet', 'B', 'Physics'),
            ('Human body has how many bones (adult)?', '106', '206', '306', '406', 'B', 'Biology'),
            ('Center of an Atom?', 'Electron', 'Nucleus', 'Orbit', 'Shell', 'B', 'Chemistry'),
            ('Unit of Force?', 'Joule', 'Newton', 'Watt', 'Volt', 'B', 'Physics'),
            ('Gas plants release during photosynthesis?', 'Oxygen', 'Carbon Dioxide', 'Nitrogen', 'Helium', 'A', 'Biology'),
            ('Speed of light is fastest in...?', 'Water', 'Glass', 'Vacuum', 'Air', 'C', 'Physics'),
            ('Largest organ of human body?', 'Heart', 'Brain', 'Skin', 'Liver', 'C', 'Biology'),
            ('Acid found in lemons?', 'Citric', 'Acetic', 'Lactic', 'Sulfuric', 'A', 'Chemistry'),
            ('Closest star to Earth?', 'Alpha Centauri', 'Sirius', 'Sun', 'North Star', 'C', 'Physics'),
            ('Which vitamin comes from sunlight?', 'A', 'B', 'C', 'D', 'D', 'Biology'),
            ('Common salt is...?', 'NaCl', 'KCl', 'H2O', 'CO2', 'A', 'Chemistry'),
            ('Force that keeps us on ground?', 'Friction', 'Gravity', 'Magnetism', 'Normal', 'B', 'Physics'),
            ('Primary source of energy on Earth?', 'Moon', 'Sun', 'Wind', 'Coal', 'B', 'Physics'),
            ('Number of teeth in adult human?', '28', '30', '32', '34', 'C', 'Biology'),
            ('Symbol for Gold?', 'Go', 'Gd', 'Au', 'Ag', 'C', 'Chemistry'),
            ('Instrument to measure temperature?', 'Barometer', 'Thermometer', 'Scale', 'Ruler', 'B', 'Physics'),
            ('Brain of a cell?', 'Nucleus', 'Vacuole', 'Wall', 'Ribosome', 'A', 'Biology'),
            ('Water freezes at (F)?', '0', '32', '100', '212', 'B', 'Physics'),
            ('Hardest natural substance?', 'Gold', 'Iron', 'Diamond', 'Steel', 'C', 'Chemistry'),
            ('Gas we breathe to stay alive?', 'Oxygen', 'Nitrogen', 'Helium', 'CO2', 'A', 'Biology'),
            ('First element in Periodic Table?', 'Helium', 'Oxygen', 'Hydrogen', 'Carbon', 'C', 'Chemistry'),
            ('Study of plants?', 'Zoology', 'Botany', 'Geology', 'Biology', 'B', 'Biology'),
            ('Earth rotation causes...?', 'Seasons', 'Day and Night', 'Years', 'Eclipses', 'B', 'Physics'),
            ('Part of plant that makes food?', 'Root', 'Leaf', 'Stem', 'Flower', 'B', 'Biology'),
            ('What is pH of pure water?', '0', '5', '7', '14', 'C', 'Chemistry'),
            ('Unit of resistance?', 'Ohm', 'Volt', 'Ampere', 'Watt', 'A', 'Physics'),
            ('Main gas in Earth Atmosphere?', 'Oxygen', 'Nitrogen', 'Argon', 'CO2', 'B', 'Physics'),
            ('Sound cannot travel through...?', 'Air', 'Water', 'Vacuum', 'Steel', 'C', 'Physics'),
            ('Smallest unit of life?', 'Atom', 'Cell', 'Organ', 'Tissue', 'B', 'Biology'),
            ('Process of liquid turning to gas?', 'Melting', 'Freezing', 'Evaporation', 'Condensation', 'C', 'Physics'),
            ('Percentage of Oxygen in air?', '21%', '78%', '1%', '50%', 'A', 'Physics'),
            ('Animal that eats both plants and meat?', 'Herbivore', 'Carnivore', 'Omnivore', 'Decomposer', 'C', 'Biology'),
            ('Symbol for Silver?', 'Si', 'Sv', 'Ag', 'Au', 'C', 'Chemistry'),
            ('Device to measure blood pressure?', 'Sphygmomanometer', 'Thermometer', 'ECG', 'Stethoscope', 'A', 'Biology'),
            ('Light travels in _____ lines?', 'Curved', 'Zigzag', 'Straight', 'Circular', 'C', 'Physics'),
            ('Which planet has rings?', 'Mars', 'Jupiter', 'Saturn', 'Earth', 'C', 'Physics'),
            ('Largest planet in solar system?', 'Earth', 'Saturn', 'Jupiter', 'Neptune', 'C', 'Physics'),
            ('Vitamin found in oranges?', 'A', 'B', 'C', 'D', 'C', 'Biology'),
            ('Dry ice is solid _____?', 'Oxygen', 'Nitrogen', 'Carbon Dioxide', 'Water', 'C', 'Chemistry'),
            ('Human blood is what color when oxygenated?', 'Blue', 'Red', 'Green', 'Yellow', 'B', 'Biology'),
            ('Ozone layer protects us from...?', 'Heat', 'Rain', 'UV Radiation', 'Wind', 'C', 'Physics'),
            ('Symbol for Iron?', 'Ir', 'In', 'Fe', 'I', 'C', 'Chemistry'),
            ('Process of iron rusting?', 'Reduction', 'Oxidation', 'Hydration', 'None', 'B', 'Chemistry'),
            ('How many colors in a rainbow?', '5', '6', '7', '8', 'C', 'Physics'),
            ('A magnifying glass is a ____ lens?', 'Concave', 'Convex', 'Flat', 'None', 'B', 'Physics'),
            ('Density of water?', '1 g/cm3', '10 g/cm3', '0.5 g/cm3', 'None', 'A', 'Physics')
        ]

        # Bulk Insert
        for lang in languages:
            # Map subjects to their respective pools
            map_data = [
                ('Mathematics', math_questions),
                ('English', english_questions),
                ('Science', science_questions)
            ]
            
            for subject, pool in map_data:
                for text, oa, ob, oc, od, ans, topic in pool:
                    db.session.add(PastQuestion(
                        subject=subject,
                        year=2024,
                        question_text=text,
                        option_a=oa,
                        option_b=ob,
                        option_c=oc,
                        option_d=od,
                        correct_answer=ans,
                        topic=topic,
                        language=lang
                    ))
        
        db.session.commit()
        print(f"Bulk seeded 150 unique questions for all {len(languages)} languages (Total: 750 questions).")

if __name__ == '__main__':
    seed_bulk_questions()
