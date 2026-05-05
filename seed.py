from app import create_app, db, bcrypt
from app.models.user import User
from app.models.learning import LearningMaterial, VocationalContent
from app.models.assessment import PastQuestion, AssessmentTemplate, Question, Result
from app.models.flashcard import Flashcard
from datetime import date, timedelta
import os

def seed_data():
    app = create_app('development')
    with app.app_context():
        print("Dropping all tables...")
        db.drop_all()
        print("Creating all tables...")
        db.create_all()

        # Create Users
        admin_pass = bcrypt.generate_password_hash('admin123').decode('utf-8')
        student_pass = bcrypt.generate_password_hash('student123').decode('utf-8')
        
        admin = User(
            first_name="Admin",
            last_name="User",
            email="admin@qualilearn.com",
            password_hash=admin_pass,
            role="admin",
            language="en"
        )
        
        student = User(
            first_name="Sadiq",
            last_name="Abubakar",
            email="student@qualilearn.com",
            password_hash=student_pass,
            role="student",
            education_level="SSS 2",
            language="en",
            overall_progress=45,
            study_time=125, # 2h 5m
            assessments_passed=3,
            current_streak=5,
            last_activity_date=date.today() - timedelta(days=0)
        )
        
        db.session.add(admin)
        db.session.add(student)
        db.session.commit()

        # Add some results for the student
        res1 = Result(user_id=student.id, assessment_id=1, score=85, total_questions=10)
        res2 = Result(user_id=student.id, assessment_id=2, score=45, total_questions=10)
        res3 = Result(user_id=student.id, assessment_id=3, score=92, total_questions=12)
        db.session.add_all([res1, res2, res3])
        db.session.commit()

        # Subjects and Languages
        subjects = ['Mathematics', 'Science', 'English', 'Social Studies']
        languages = ['en', 'ha', 'yo', 'ig', 'pi']
        
        # --- Mathematics Topics ---
        math_topics = {
            'en': [
                ('Algebraic Expressions', 'Learn to simplify complex algebraic expressions with practical examples.', 'https://www.youtube.com/embed/vDqOoI-4Z6M', 'JSS'),
                ('Quadratic Equations', 'Master the quadratic formula and solving for x step by step.', 'https://www.youtube.com/embed/i7idZShXly8', 'SSS'),
                ('Trigonometry Basics', 'Understanding Sine, Cosine, and Tangent in right-angled triangles.', 'https://www.youtube.com/embed/PUB0TaZ7bhA', 'SSS'),
                ('Circle Geometry', 'Theorems involving chords, tangents and angles in a circle.', 'https://www.youtube.com/embed/74RcUjxErCg', 'SSS'),
                ('Calculus: Differentiation', 'Introduction to derivatives and fundamental rules of differentiation.', 'https://www.youtube.com/embed/9vKqVkMQHKk', 'SSS'),
                ('Calculus: Integration', 'Mastering the anti-derivative and basic integration techniques.', 'https://www.youtube.com/embed/6WUjbJEeJwM', 'SSS'),
                ('Statistics: Data Handling', 'Learn about Mean, Median, Mode and Frequency tables.', 'https://www.youtube.com/embed/kn83BA7cRNM', 'JSS'),
                ('Probability Theory', 'Introductory concepts to calculating the likelihood of events.', 'https://www.youtube.com/embed/KzfWUEJjG18', 'JSS')
            ],
            'ha': [
                ('Lissafin Algebra', 'Koyi yadda ake sauƙaƙa lissafin algebra.', 'https://www.youtube.com/embed/vDqOoI-4Z6M', 'JSS'),
                ('Lissafin Quadratic', 'Kwarewa wajen amfani da dabarun quadratic.', 'https://www.youtube.com/embed/i7idZShXly8', 'SSS'),
                ('Trigonometry na Farko', 'Fahimtar zane-zanen sine da cosine.', 'https://www.youtube.com/embed/PUB0TaZ7bhA', 'SSS'),
                ('Kiɗiddiga (Statistics)', 'Ma\'aunin kididdiga don rukunin bayanai.', 'https://www.youtube.com/embed/kn83BA7cRNM', 'JSS'),
                ('Calculus na Diferensheshin', 'Gabatarwa ga derivative da dokokin differentiation.', 'https://www.youtube.com/embed/9vKqVkMQHKk', 'SSS'),
                ('Siffofin Da\'ira (Circle Geometry)', 'Koyi game da chords, tangents, da angles a cikin da\'ira.', 'https://www.youtube.com/embed/74RcUjxErCg', 'SSS'),
                ('Lissafin Probability', 'Koyi yadda ake lissafin yiwuwar abubuwa su faru.', 'https://www.youtube.com/embed/KzfWUEJjG18', 'JSS'),
                ('Calculus na Integration', 'Kwarewa wajen yin amfani da dabarun integration.', 'https://www.youtube.com/embed/6WUjbJEeJwM', 'SSS')
            ],
            'yo': [
                ('Àlàyé Algebra', 'Kọ́ bí a ṣe n dín àwọn algebra expressions kù.', 'https://www.youtube.com/embed/vDqOoI-4Z6M', 'JSS'),
                ('Àlàyé Quadratic', 'Mọ̀ nípa quadratic formula x = [-b ± √(b² - 4ac)] / 2a.', 'https://www.youtube.com/embed/i7idZShXly8', 'SSS'),
                ('Ìmọ̀ Trigonometry', 'Mọ̀ nípa Sine, Cosine, àti Tangent rules.', 'https://www.youtube.com/embed/PUB0TaZ7bhA', 'SSS'),
                ('Mọ̀ nípa Statistics', 'Kọ́ nípa Mean, Median, àti Mode fun data sets.', 'https://www.youtube.com/embed/kn83BA7cRNM', 'JSS'),
                ('Ìmọ̀ Circle Geometry', 'Kọ́ nípa chords, tangents àti angles nínú circle.', 'https://www.youtube.com/embed/74RcUjxErCg', 'SSS'),
                ('Ìmọ̀ Integration', 'Kọ́ nípa integration àti anti-derivatives.', 'https://www.youtube.com/embed/6WUjbJEeJwM', 'SSS')
            ],
            'ig': [
                ('Nkọwa Algebra', 'Mụta otú e si eme ka algebra expression dị mfe.', 'https://www.youtube.com/embed/vDqOoI-4Z6M', 'JSS'),
                ('Equation Quadratic', 'Mụta otú e si eji quadratic formula eme ihe.', 'https://www.youtube.com/embed/i7idZShXly8', 'SSS'),
                ('Ihe Ndị Dị n’ime Trigonometry', 'Mụta maka Sine, Cosine, na Tangent rules.', 'https://www.youtube.com/embed/PUB0TaZ7bhA', 'SSS'),
                ('Statistics na Data', 'Mụta maka Mean, Median, na Mode maka data sets.', 'https://www.youtube.com/embed/kn83BA7cRNM', 'JSS'),
                ('Mmụta Circle Geometry', 'Mụta maka chords, tangents na angles n’ime circle.', 'https://www.youtube.com/embed/74RcUjxErCg', 'SSS'),
                ('Mmụta Integration', 'Mụta maka integration na anti-derivatives.', 'https://www.youtube.com/embed/6WUjbJEeJwM', 'SSS')
            ],
            'pi': [
                ('Algebra Grammar', 'Learn how to cut algebra expressions down to size.', 'https://www.youtube.com/embed/vDqOoI-4Z6M', 'JSS'),
                ('Quadratic Equation', 'Master that x = [-b ± √(b² - 4ac)] / 2a formula.', 'https://www.youtube.com/embed/i7idZShXly8', 'SSS'),
                ('Trigonometry Flow', 'Understand Sine, Cosine, and Tangent rules sharp-sharp.', 'https://www.youtube.com/embed/PUB0TaZ7bhA', 'SSS'),
                ('Statistics: Data Level', 'Learn Mean, Median, and Mode for set patterns.', 'https://www.youtube.com/embed/kn83BA7cRNM', 'JSS'),
                ('Circle Geometry Level', 'Master chords, tangents, and angles inside circle.', 'https://www.youtube.com/embed/74RcUjxErCg', 'SSS'),
                ('Calculus: Integration Level', 'Master integration and anti-derivatives.', 'https://www.youtube.com/embed/6WUjbJEeJwM', 'SSS')
            ]
        }

        # --- English Topics ---
        english_topics = {
            'en': [
                ('English Grammar: Tenses', 'Mastering Past, Present, and Future tenses for perfect communication.', 'https://www.youtube.com/embed/sCiG6rlk2Bc', 'JSS'),
                ('Composition Writing', 'Learn the secrets to writing high-scoring narrative and descriptive essays.', 'https://www.youtube.com/embed/RFwui6V32nc', 'JSS'),
                ('Elements of Literature', 'Exploring Plot, Theme, and Characterization in African Literature.', 'https://www.youtube.com/embed/Pxao6AG88Lw', 'SSS'),
                ('Summary Writing Skills', 'How to extract main points and write concise summaries.', 'https://www.youtube.com/embed/bhtz7RSaKlc', 'SSS'),
                ('Oral English: Vowels', 'Perfecting pronunciation of English vowel sounds.', 'https://www.youtube.com/embed/uW0Qd86_XfM', 'JSS'),
                ('Concord and Agreement', 'Rules governing the relationship between subjects and verbs.', 'https://www.youtube.com/embed/7_mZInLh-64', 'SSS')
            ],
            'ha': [
                ('Dokokin Turanci: Tenses', 'Kwarewa wajen amfani da Past, Present, da Future tenses.', 'https://www.youtube.com/embed/sCiG6rlk2Bc', 'JSS'),
                ('Dabarun Rubutu', 'Koyi yadda ake rubuta shararren labari da rubutun bayani.', 'https://www.youtube.com/embed/RFwui6V32nc', 'JSS'),
                ('Adabin Turanci', 'Gano Makasudin Labari, Jigo, da Halayen mutane a adabin Afirka.', 'https://www.youtube.com/embed/Pxao6AG88Lw', 'SSS')
            ],
            'yo': [
                ('Èdè Gẹ̀ẹ́sì: Tenses', 'Mọ̀ nípa Past, Present, àti Future tenses.', 'https://www.youtube.com/embed/sCiG6rlk2Bc', 'JSS'),
                ('Ìlànà Ìkọ̀wé', 'Kọ́ bí a ṣe n kọ narrative àti descriptive essays.', 'https://www.youtube.com/embed/RFwui6V32nc', 'JSS')
            ],
            'ig': [
                ('Asụsụ Bekee: Tenses', 'Mụta maka Past, Present, na Future tenses.', 'https://www.youtube.com/embed/sCiG6rlk2Bc', 'JSS'),
                ('Nkà n’Ide Ihe', 'Mụta otú e si ede narrative na descriptive essays.', 'https://www.youtube.com/embed/RFwui6V32nc', 'JSS')
            ],
            'pi': [
                ('English Grammar: Tenses', 'Master how to use Past, Present, and Future tenses.', 'https://www.youtube.com/embed/sCiG6rlk2Bc', 'JSS'),
                ('Composition Writing', 'Learn the code to write correct narrative and descriptive essays.', 'https://www.youtube.com/embed/RFwui6V32nc', 'JSS')
            ]
        }

        # --- Science (Biology) Topics ---
        biology_topics = {
            'en': [
                ('Cell Structure & Function', 'Detailed look at organelles and the building blocks of life.', 'https://www.youtube.com/embed/URUJD5NEXC8', 'JSS'),
                ('Photosynthesis', 'The chemical process of light conversion in green plants.', 'https://www.youtube.com/embed/SXP6u7m6YFk', 'JSS'),
                ('Genetics & Heredity', 'How DNA and RNA control inheritance across generations.', 'https://www.youtube.com/embed/2reevjoVn6c', 'SSS'),
                ('Respiratory System', 'Understanding how oxygen and carbon dioxide exchange in humans.', 'https://www.youtube.com/embed/f9ONXd_-anM', 'JSS')
            ],
            'ha': [
                ('Biology: Cell Structure', 'Koyi game da sassan tantanin halitta da ayyukansu.', 'https://www.youtube.com/embed/URUJD5NEXC8', 'JSS'),
                ('Photosynthesis Process', 'Yadda tsire-tsire ke amfani da haske don samar da abinci.', 'https://www.youtube.com/embed/SXP6u7m6YFk', 'JSS')
            ],
            'yo': [
                ('Ẹ̀kọ́ Biology: Cell', 'Mọ̀ nípa cell structure àti iṣẹ́ rẹ̀.', 'https://www.youtube.com/embed/URUJD5NEXC8', 'JSS')
            ],
            'ig': [
                ('Mmụta Biology: Cell', 'Mụta maka cell structure na ọrụ ya.', 'https://www.youtube.com/embed/URUJD5NEXC8', 'JSS')
            ],
            'pi': [
                ('Cell Structure & Level', 'Better look at how your cells dey work properly.', 'https://www.youtube.com/embed/URUJD5NEXC8', 'JSS')
            ]
        }

        # --- Physics Topics ---
        physics_topics = {
            'en': [
                ('Newton\'s Laws of Motion', 'Understanding how forces affect objects in motion.', 'https://www.youtube.com/embed/g550H4e5FCY', 'SSS'),
                ('Work, Energy & Power', 'Master the fundamental concepts of physical energy.', 'https://www.youtube.com/embed/2WS1sG9fhOk', 'SSS'),
                ('Pressure in Liquids', 'Hydraulics and pressure distribution in fluids.', 'https://www.youtube.com/embed/0B0Xv2fS9_U', 'JSS'),
                ('Electricity Basics', 'Introduction to circuits, voltage, and current.', 'https://www.youtube.com/embed/mc979OhitAg', 'JSS')
            ]
        }

        # --- Chemistry Topics ---
        chemistry_topics = {
            'en': [
                ('Atomic Structure', 'Detailed study of protons, neutrons, and electrons.', 'https://www.youtube.com/embed/OH-aSu-rWgk', 'JSS'),
                ('Chemical Bonding', 'How atoms join together to form molecules.', 'https://www.youtube.com/embed/QXT4OVM4vXI', 'SSS'),
                ('Acids, Bases and Salts', 'Understanding chemical properties of substances.', 'https://www.youtube.com/embed/ANi709MYnWg', 'JSS'),
                ('The Periodic Table', 'Organisation of elements and their properties.', 'https://www.youtube.com/embed/0RRVV4Diomg', 'SSS')
            ]
        }

        from app.models.topics import Topic, TopicVideo

        # Seed all learning materials and topics
        for lang in languages:
            # Seed Math
            for title, content, url, level in math_topics.get(lang, math_topics['en']):
                db.session.add(LearningMaterial(title=title, content=content, resource_url=url, subject='Mathematics', language=lang, material_type='video_link', education_level=level))
                
                # Also create a Topic for this material so it shows up in the grid
                topic = Topic(name=title, subject='Mathematics', education_level=level)
                db.session.add(topic)
                db.session.flush()
                db.session.add(TopicVideo(topic_id=topic.id, video_url=url, video_title=title))

            # Seed English
            for title, content, url, level in english_topics.get(lang, english_topics['en']):
                db.session.add(LearningMaterial(title=title, content=content, resource_url=url, subject='English', language=lang, material_type='video_link', education_level=level))
                
                topic = Topic(name=title, subject='English', education_level=level)
                db.session.add(topic)
                db.session.flush()
                db.session.add(TopicVideo(topic_id=topic.id, video_url=url, video_title=title))

            # Seed Biology
            for title, content, url, level in biology_topics.get(lang, biology_topics['en']):
                subj = 'Biology' if level == 'SSS' else 'Science'
                db.session.add(LearningMaterial(title=title, content=content, resource_url=url, subject=subj, language=lang, material_type='video_link', education_level=level))
                
                topic = Topic(name=title, subject=subj, education_level=level)
                db.session.add(topic)
                db.session.flush()
                db.session.add(TopicVideo(topic_id=topic.id, video_url=url, video_title=title))
            
            # Also add Physics and Chemistry topics
            for title, content, url, level in physics_topics.get(lang, physics_topics['en']):
                subj = 'Physics' if level == 'SSS' else 'Science'
                db.session.add(LearningMaterial(title=title, content=content, resource_url=url, subject=subj, language=lang, material_type='video_link', education_level=level))
                
                topic = Topic(name=title, subject=subj, education_level=level)
                db.session.add(topic)
                db.session.flush()
                db.session.add(TopicVideo(topic_id=topic.id, video_url=url, video_title=title))
            
            for title, content, url, level in chemistry_topics.get(lang, chemistry_topics['en']):
                subj = 'Chemistry' if level == 'SSS' else 'Science'
                db.session.add(LearningMaterial(title=title, content=content, resource_url=url, subject=subj, language=lang, material_type='video_link', education_level=level))
                
                topic = Topic(name=title, subject=subj, education_level=level)
                db.session.add(topic)
                db.session.flush()
                db.session.add(TopicVideo(topic_id=topic.id, video_url=url, video_title=title))

            # Redundant sections removed

        # --- Expanded Flashcards (50 per subject) ---
        flashcards_data = [
            # Mathematics (50)
            ('Polynomial', 'An expression consisting of variables and coefficients.', 'Mathematics'),
            ('Quadratic Formula', 'x = [-b ± √(b² - 4ac)] / 2a', 'Mathematics'),
            ('Pythagorean Theorem', 'a² + b² = c² for right-angled triangles.', 'Mathematics'),
            ('Cosine Rule', 'a² = b² + c² - 2bc cos A', 'Mathematics'),
            ('Sine Rule', 'a / sin A = b / sin B = c / sin C', 'Mathematics'),
            ('Differentiation', 'Process of finding the rate of change (derivative).', 'Mathematics'),
            ('Integration', 'Process of finding the area under a curve (anti-derivative).', 'Mathematics'),
            ('Logarithm', 'The power to which a base must be raised to produce a given number.', 'Mathematics'),
            ('Mean', 'The average of a set of numbers.', 'Mathematics'),
            ('Median', 'The middle value in a sorted list of numbers.', 'Mathematics'),
            ('Mode', 'The number that occurs most frequently in a set.', 'Mathematics'),
            ('Standard Deviation', 'Measure of the amount of variation or dispersion.', 'Mathematics'),
            ('Probability', 'The likelihood of an event occurring (ranges 0 to 1).', 'Mathematics'),
            ('Circle Circumference', 'C = 2πr', 'Mathematics'),
            ('Area of a Circle', 'A = πr²', 'Mathematics'),
            ('Volume of a Sphere', 'V = (4/3)πr³', 'Mathematics'),
            ('Hypotenuse', 'The longest side of a right-angled triangle.', 'Mathematics'),
            ('Isosceles Triangle', 'A triangle with two equal sides and angles.', 'Mathematics'),
            ('Equilateral Triangle', 'A triangle with all sides and angles equal (60°).', 'Mathematics'),
            ('Tangent', 'A line that touches a circle at exactly one point.', 'Mathematics'),
            ('Chord', 'A line segment connecting two points on a circle.', 'Mathematics'),
            ('Diameter', 'A chord that passes through the center of a circle.', 'Mathematics'),
            ('Prime Number', 'A number divisible only by 1 and itself.', 'Mathematics'),
            ('Factorial', 'The product of all positive integers up to a number (n!).', 'Mathematics'),
            ('Matrix', 'A rectangular array of numbers arranged in rows and columns.', 'Mathematics'),
            ('Vector', 'A quantity having both magnitude and direction.', 'Mathematics'),
            ('Scalar', 'A quantity having only magnitude, not direction.', 'Mathematics'),
            ('Simultaneous Equations', 'A set of equations with shared variables solved together.', 'Mathematics'),
            ('Indices', 'The power or exponent of a number.', 'Mathematics'),
            ('Sequence', 'An ordered list of numbers following a specific pattern.', 'Mathematics'),
            ('Arithmetic Progression', 'A sequence where differences between terms are constant.', 'Mathematics'),
            ('Geometric Progression', 'A sequence where each term is multiplied by a constant.', 'Mathematics'),
            ('Permutation', 'An arrangement of objects in a specific order.', 'Mathematics'),
            ('Combination', 'A selection of objects where order does not matter.', 'Mathematics'),
            ('Percentage', 'A number expressed as a fraction of 100.', 'Mathematics'),
            ('Ratio', 'A comparison of two quantities by division.', 'Mathematics'),
            ('Proportion', 'An equation stating that two ratios are equal.', 'Mathematics'),
            ('Absolute Value', 'The distance of a number from zero, regardless of sign.', 'Mathematics'),
            ('Variable', 'A symbol representing an unknown value.', 'Mathematics'),
            ('Coefficient', 'A number used to multiply a variable.', 'Mathematics'),
            ('Constant', 'A fixed value that does not change.', 'Mathematics'),
            ('Inequality', 'A mathematical statement using <, >, or ≠.', 'Mathematics'),
            ('Factorization', 'Breaking down an expression into products of its factors.', 'Mathematics'),
            ('Gradient', 'The slope of a line (rise over run).', 'Mathematics'),
            ('Intercept', 'Point where a graph crosses an axis.', 'Mathematics'),
            ('Parabola', 'The U-shaped curve of a quadratic function.', 'Mathematics'),
            ('Ellipse', 'An elongated circle-like shape.', 'Mathematics'),
            ('Asymptote', 'A line that a curve approaches but never touches.', 'Mathematics'),
            ('Complex Number', 'A number in the form a + bi.', 'Mathematics'),
            ('Infinity', 'A concept representing something without bound or end.', 'Mathematics'),

            # Science (50)
            ('Osmosis', 'Movement of water molecules across a semi-permeable membrane.', 'Science'),
            ('Diffusion', 'Movement of particles from high to low concentration.', 'Science'),
            ('Mitosis', 'Cell division resulting in two identical daughter cells.', 'Science'),
            ('Meiosis', 'Cell division resulting in four genetically distinct gametes.', 'Science'),
            ('Photosynthesis', 'Process of converting light energy into chemical energy.', 'Science'),
            ('Respiration', 'Process of releasing energy from glucose in cells.', 'Science'),
            ('Enzyme', 'A biological catalyst that speeds up reactions.', 'Science'),
            ('DNA', 'Deoxyribonucleic acid, the carrier of genetic information.', 'Science'),
            ('Gene', 'A segment of DNA that codes for a specific protein.', 'Science'),
            ('Chromosomes', 'Thread-like structures made of DNA and proteins.', 'Science'),
            ('Refractory Period', 'Short rest time after a nerve impulse or contraction.', 'Science'),
            ('Homeostasis', 'Maintenance of a stable internal environment.', 'Science'),
            ('Newton\'s First Law', 'An object at rest stays at rest unless acted upon.', 'Science'),
            ('Newton\'s Second Law', 'Force equals mass times acceleration (F=ma).', 'Science'),
            ('Newton\'s Third Law', 'For every action, there is an equal and opposite reaction.', 'Science'),
            ('Kinetic Energy', 'The energy an object possesses due to its motion.', 'Science'),
            ('Potential Energy', 'Stored energy based on an object\'s position.', 'Science'),
            ('Velocity', 'Speed in a specific direction.', 'Science'),
            ('Acceleration', 'The rate of change of velocity over time.', 'Science'),
            ('Momentum', 'The product of an object\'s mass and velocity.', 'Science'),
            ('Gravity', 'The force that pulls objects toward each other.', 'Science'),
            ('Electrolysis', 'Breaking down of a substance using electricity.', 'Science'),
            ('Atom', 'The smallest unit of matter retaining chemical properties.', 'Science'),
            ('Proton', 'Positively charged particle in the nucleus.', 'Science'),
            ('Neutron', 'Neutral particle in the nucleus.', 'Science'),
            ('Electron', 'Negatively charged particle orbiting the nucleus.', 'Science'),
            ('Atomic Number', 'The number of protons in an atom.', 'Science'),
            ('Mass Number', 'The total number of protons and neutrons in an atom.', 'Science'),
            ('Isotope', 'Atoms of the same element with different neutron counts.', 'Science'),
            ('Valency', 'The combining power of an element.', 'Science'),
            ('Ionic Bond', 'Bond formed by the transfer of electrons.', 'Science'),
            ('Covalent Bond', 'Bond formed by the sharing of electrons.', 'Science'),
            ('Metallic Bond', 'Bond formed by the attraction of metal ions to electrons.', 'Science'),
            ('pH Scale', 'Measures how acidic or basic a substance is (0-14).', 'Science'),
            ('Acid', 'A substance that releases hydrogen ions in water (low pH).', 'Science'),
            ('Base', 'A substance that releases hydroxide ions (high pH).', 'Science'),
            ('Exothermic', 'A reaction that releases heat to its surroundings.', 'Science'),
            ('Endothermic', 'A reaction that absorbs heat from its surroundings.', 'Science'),
            ('Redox Reaction', 'A reaction involving both reduction and oxidation.', 'Science'),
            ('Catalyst', 'A substance that increases reaction rate without being consumed.', 'Science'),
            ('Combustion', 'A chemical reaction involving fuel and oxygen (burning).', 'Science'),
            ('Polymerization', 'Process of joining small molecules into large chains.', 'Science'),
            ('Hard Water', 'Water containing high levels of calcium and magnesium.', 'Science'),
            ('Distillation', 'Purifying a liquid by heating and cooling.', 'Science'),
            ('Corrosion', 'Gradual destruction of metals by chemical reaction.', 'Science'),
            ('Magnetism', 'Force of attraction or repulsion by magnets.', 'Science'),
            ('Wave Frequency', 'Number of waves passing a point per second (Hertz).', 'Science'),
            ('Amplitude', 'The maximum displacement of a wave.', 'Science'),
            ('Reflection', 'Bouncing back of waves from a surface.', 'Science'),
            ('Refraction', 'Bending of waves as they enter a different medium.', 'Science'),

            # English (50)
            ('Simile', 'Comparison using "like" or "as".', 'English'),
            ('Metaphor', 'Direct comparison without using "like" or "as".', 'English'),
            ('Personification', 'Giving human qualities to non-human objects.', 'English'),
            ('Onomatopoeia', 'Words that imitate sounds (e.g., "buzz", "bang").', 'English'),
            ('Alliteration', 'Repetition of initial consonant sounds.', 'English'),
            ('Hyperbole', 'Exaggerated statements not meant to be taken literally.', 'English'),
            ('Irony', 'Contrast between expectation and reality.', 'English'),
            ('Satire', 'Use of humor or riducule to critisize stupidity.', 'English'),
            ('Paradox', 'A self-contradictory statement that reveals a truth.', 'English'),
            ('Oxymoron', 'Two contradictory terms used together (e.g., "bittersweet").', 'English'),
            ('Pun', 'A joke exploiting different meanings of a word.', 'English'),
            ('Allegory', 'A story with hidden symbolic meaning.', 'English'),
            ('Euphemism', 'A mild word used to replace something harsh.', 'English'),
            ('Cliche', 'A phrase that is overused and lacks original thought.', 'English'),
            ('Protagonist', 'The main character in a story.', 'English'),
            ('Antagonist', 'The character opposing the main character.', 'English'),
            ('Foreshadowing', 'Hints given about future events in a story.', 'English'),
            ('Climax', 'The most intense part of a plot.', 'English'),
            ('Resolution', 'The end of a story where problems are solved.', 'English'),
            ('Tone', 'The author\'s attitude toward the subject.', 'English'),
            ('Mood', 'The atmosphere or feeling created for the reader.', 'English'),
            ('Point of View', 'The perspective from which a story is told.', 'English'),
            ('Noun', 'A word representing a person, place, or thing.', 'English'),
            ('Verb', 'A word expressing an action or state of being.', 'English'),
            ('Adjective', 'A word that describes or modifies a noun.', 'English'),
            ('Adverb', 'A word that modifies a verb, adjective, or adverb.', 'English'),
            ('Pronoun', 'A word used in place of a noun.', 'English'),
            ('Preposition', 'Shows show relationship between a noun and another word.', 'English'),
            ('Conjunction', 'A word used to connect sentences or clauses.', 'English'),
            ('Interjection', 'A word used to express sudden emotion.', 'English'),
            ('Synonym', 'Words with similar meanings.', 'English'),
            ('Antonym', 'Words with opposite meanings.', 'English'),
            ('Homophone', 'Words that sound same but have different meanings.', 'English'),
            ('Clause', 'A group of words containing a subject and a verb.', 'English'),
            ('Phrase', 'A group of words without a subject-verb unit.', 'English'),
            ('Active Voice', 'When the subject performs the action.', 'English'),
            ('Passive Voice', 'When the action is performed on the subject.', 'English'),
            ('Idiom', 'An expression whose meaning is not literal.', 'English'),
            ('Prefix', 'A group of letters added to the start of a word.', 'English'),
            ('Suffix', 'A group of letters added to the end of a word.', 'English'),
            ('Root Word', 'The core part of a word to which affixes are added.', 'English'),
            ('Main Idea', 'The most important point in a text.', 'English'),
            ('Context Clues', 'Information in a text that helps define a word.', 'English'),
            ('Dialogue', 'Conversation between characters.', 'English'),
            ('Monologue', 'A long speech by a single character.', 'English'),
            ('Setting', 'The time and place of a story.', 'English'),
            ('Theme', 'The central underlying message of a work.', 'English'),
            ('Genre', 'A category or type of literature.', 'English'),
            ('First Person', 'Story told using "I" or "we".', 'English'),
            ('Third Person', 'Story told using "he", "she", or "they".', 'English')
        ]

        # Vocational Content Translations
        voc_data = {
            'en': [
                ('Professional Tailoring', 'Complete guide to measurements, cutting, and stitching for beginners.', 'Fashion', 'https://www.youtube.com/embed/p9JdC_w0MvY'),
                ('Smartphone Hardware Repair', 'Essential tips for screen replacement and fixing internal components.', 'Technology', 'https://www.youtube.com/embed/8kAsX_gXhR0'),
                ('Web Design for Beginners', 'Learn HTML, CSS, and Responsive Design to build professional websites.', 'Technology', 'https://www.youtube.com/embed/mU6anWqZJcc'),
                ('Professional Catering', 'Master the art of professional baking and Nigerian catering basics.', 'Culinary', 'https://www.youtube.com/embed/kYv9y_t9R14'),
                ('Modern Plumbing Basics', 'Introductory guide to household plumbing, pipe fittings, and repairs.', 'Plumbing', 'https://www.youtube.com/embed/Xp4S1GvP2Qk'),
                ('Basic Home Wiring', 'Learn how to safely handle electrical installations and home wiring.', 'Electrical', 'https://www.youtube.com/embed/fA_I2j-hF8A'),
                ('Furniture Crafting', 'Step-by-step guide to building simple household furniture with wood.', 'Carpentry', 'https://www.youtube.com/embed/U3l08mP69Xw'),
                ('Fashion Illustration', 'Master the art of sketching and designing your own fashion collections.', 'Fashion', 'https://www.youtube.com/embed/Pj1C9vI7Xg0')
            ],
            'ha': [
                ('Ɗinkin Kaya na Zamani', 'Cikakken jagora kan aunawa, yanka, da dinkin kaya ga sabon koyo.', 'Fashion', 'https://www.youtube.com/embed/p9JdC_w0MvY'),
                ('Gyaran Wayar Hannu', 'Muhimman bayanai kan canza sikirin da gyaran sassan waya.', 'Technology', 'https://www.youtube.com/embed/8kAsX_gXhR0'),
                ('Koyon Web Design', 'Koyi HTML, CSS, da yadda ake gina yanar gizo.', 'Technology', 'https://www.youtube.com/embed/mU6anWqZJcc'),
                ('Koyon Girki da Cake', 'Kwarewa wajen girkin party da yin cake.', 'Culinary', 'https://www.youtube.com/embed/kYv9y_t9R14')
            ],
            'yo': [
                ('Iṣẹ́ Ríránṣọ', 'Bí a ṣe n yà, tí a sì n ránṣọ ní kíkún fún àwọn tuntun.', 'Fashion', 'https://www.youtube.com/embed/p9JdC_w0MvY'),
                ('Àtúnṣe Fóònù', 'Ìlànà bí a ṣe n tún fóònù ṣe ní kíkún.', 'Technology', 'https://www.youtube.com/embed/8kAsX_gXhR0'),
                ('Web Design Tuntun', 'Kọ́ HTML àti CSS láti ṣí oju-ewé internet.', 'Technology', 'https://www.youtube.com/embed/mU6anWqZJcc')
            ],
            'ig': [
                ('Ịkwa ákwà', 'Otú e si atụle na ịkwa ákwà maka ndị ọhụrụ.', 'Fashion', 'https://www.youtube.com/embed/p9JdC_w0MvY'),
                ('Nzi nhazi Fóònù', 'Otú e si arụzi fóònù ndị mebiri emebi.', 'Technology', 'https://www.youtube.com/embed/8kAsX_gXhR0')
            ],
            'pi': [
                ('Fashion Tailoring Level', 'Complete guide make you know how to cut and sew cloth.', 'Fashion', 'https://www.youtube.com/embed/p9JdC_w0MvY'),
                ('Smartphone Repair Level', 'Better tips for screen replacement and how to fix phones.', 'Technology', 'https://www.youtube.com/embed/8kAsX_gXhR0')
            ]
        }

        for lang in languages:
            for title, desc, cat, url in voc_data.get(lang, voc_data['en']):
                db.session.add(VocationalContent(title=title, description=desc, category=cat, language=lang, resource_url=url))
            
            # Seed Flashcards
            for front, back, subject in flashcards_data:
                # Default academic cards to SS level for now, can be mixed
                level = 'SSS' if subject in ['Physics', 'Chemistry', 'Calculus'] else 'JSS'
                db.session.add(Flashcard(front=front, back=back, subject=subject, language=lang, education_level=level))

        # Assessments
        for title, sub, lvl in [('Mathematics Mastery', 'Mathematics', 'SSS'), ('English Proficiency', 'English', 'JSS'), ('General Science Review', 'Science', 'JSS')]:
            asm = AssessmentTemplate(title=title, subject=sub, time_limit=15)
            db.session.add(asm)
            db.session.flush()
            if sub == 'Mathematics':
                db.session.add_all([
                    Question(assessment_id=asm.id, text='Solve for x: 2x + 5 = 15', option_a='2', option_b='5', option_c='10', option_d='7', correct_option='B'),
                    Question(assessment_id=asm.id, text='What is the square root of 144?', option_a='12', option_b='14', option_c='10', option_d='16', correct_option='A')
                ])

        # Past Questions Seeding
        pq_data = [
            ('Mathematics', 2023, 'Algebra', 'Solve for y: 3y - 9 = 0', '1', '3', '9', '0', 'B', '3y = 9 => y = 3', 'SSS'),
            ('Mathematics', 2022, 'Arithmetic', 'What is 15% of 200?', '20', '30', '40', '15', 'B', '0.15 * 200 = 30', 'JSS'),
            ('English', 2023, 'Grammar', 'Identify the verb: "The cat runs fast."', 'The', 'cat', 'runs', 'fast', 'C', 'Action word is runs', 'JSS'),
            ('Science', 2023, 'Biology', 'Which organ pumps blood?', 'Lungs', 'Heart', 'Liver', 'Brain', 'B', 'The heart is the primary pump.', 'SSS')
        ]
        
        for sub, yr, top, txt, oa, ob, oc, od, ans, exp, lvl in pq_data:
            for lang in languages:
                db.session.add(PastQuestion(
                    subject=sub, year=yr, topic=top, question_text=txt,
                    option_a=oa, option_b=ob, option_c=oc, option_d=od,
                    correct_answer=ans, explanation=exp, language=lang, education_level=lvl
                ))

        db.session.commit()
        print("Database seeded with multilingual support successfully!")

if __name__ == '__main__':
    seed_data()
