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
            email="qualilearn@qualilearn.com",
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
            education_level='Academics',
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
                ('Sets & Venn Diagrams', 'Understanding sets, subsets, and visualising with Venn diagrams.', 'https://www.youtube.com/embed/kn83BA7cRNM', 'Academics'),
                ('Quadratic Equations', 'Solving second-degree equations using factoring and formulas.', 'https://www.youtube.com/embed/i7idZShXly8', 'Academics'),
                ('Matrices & Determinants', 'Operations on matrices and finding determinants.', 'https://www.youtube.com/embed/gJgZkH7D-G4', 'Academics'),
                ('Logarithms', 'Laws of logarithms and solving logarithmic equations.', 'https://www.youtube.com/embed/zT1c-1t9wR8', 'Academics'),
                ('Trigonometry Basics', 'Sine, Cosine, and Tangent relationships in triangles.', 'https://www.youtube.com/embed/PUB0TaZ7bhA', 'Academics'),
                ('Circle Geometry', 'Theorems relating to circles, chords, and tangents.', 'https://www.youtube.com/embed/74RcUjxErCg', 'Academics'),
                ('Calculus: Integration', 'Master integration and anti-derivatives.', 'https://www.youtube.com/embed/6WUjbJEeJwM', 'Academics'),
                ('Linear Programming', 'Optimization using linear inequalities and graphing.', 'https://www.youtube.com/embed/BzzqxBaLsh0', 'Academics'),
                ('Statistics: Mean & Median', 'Calculating measures of central tendency for datasets.', 'https://www.youtube.com/embed/5C9LMSzZ2Ok', 'Academics'),
                ('Probability Basics', 'Understanding chance and calculating basic probabilities.', 'https://www.youtube.com/embed/uzkc-qNVoOk', 'Academics'),
                ('Surds & Radicals', 'Simplifying and performing operations on surds.', 'https://www.youtube.com/embed/v9Xz_w-Y8w8', 'Academics'),
                ('Simultaneous Equations', 'Solving systems of equations with two variables.', 'https://www.youtube.com/embed/mGwP08_0mAc', 'Academics')
            ],
            'ha': [
                ('Lissafin Quadratic', 'Kwarewa wajen amfani da dabarun quadratic.', 'https://www.youtube.com/embed/i7idZShXly8', 'Academics'),
                ('Trigonometry na Farko', 'Fahimtar zane-zanen sine da cosine.', 'https://www.youtube.com/embed/PUB0TaZ7bhA', 'Academics'),
                ('Calculus na Diferensheshin', 'Gabatarwa ga derivative da dokokin differentiation.', 'https://www.youtube.com/embed/9vKqVkMQHKk', 'Academics'),
                ('Siffofin Da\'ira (Circle Geometry)', 'Koyi game da chords, tangents, da angles a cikin da\'ira.', 'https://www.youtube.com/embed/74RcUjxErCg', 'Academics'),
                ('Calculus na Integration', 'Kwarewa wajen yin amfani da dabarun integration.', 'https://www.youtube.com/embed/6WUjbJEeJwM', 'Academics')
            ],
            'yo': [
                ('Àlàyé Quadratic', 'Mọ̀ nípa quadratic formula x = [-b ± √(b² - 4ac)] / 2a.', 'https://www.youtube.com/embed/i7idZShXly8', 'Academics'),
                ('Ìmọ̀ Trigonometry', 'Mọ̀ nípa Sine, Cosine, àti Tangent rules.', 'https://www.youtube.com/embed/PUB0TaZ7bhA', 'Academics'),
                ('Ìmọ̀ Circle Geometry', 'Kọ́ nípa chords, tangents àti angles nínú circle.', 'https://www.youtube.com/embed/74RcUjxErCg', 'Academics'),
                ('Ìmọ̀ Integration', 'Kọ́ nípa integration àti anti-derivatives.', 'https://www.youtube.com/embed/6WUjbJEeJwM', 'Academics')
            ],
            'ig': [
                ('Equation Quadratic', 'Mụta otú e si eji quadratic formula eme ihe.', 'https://www.youtube.com/embed/i7idZShXly8', 'Academics'),
                ('Ihe Ndị Dị n’ime Trigonometry', 'Mụta maka Sine, Cosine, na Tangent rules.', 'https://www.youtube.com/embed/PUB0TaZ7bhA', 'Academics'),
                ('Mmụta Circle Geometry', 'Mụta maka chords, tangents na angles n’ime circle.', 'https://www.youtube.com/embed/74RcUjxErCg', 'Academics'),
                ('Mmụta Integration', 'Mụta maka integration na anti-derivatives.', 'https://www.youtube.com/embed/6WUjbJEeJwM', 'Academics')
            ],
            'pi': [
                ('Quadratic Equation', 'Master that x = [-b ± √(b² - 4ac)] / 2a formula.', 'https://www.youtube.com/embed/i7idZShXly8', 'Academics'),
                ('Trigonometry Flow', 'Understand Sine, Cosine, and Tangent rules sharp-sharp.', 'https://www.youtube.com/embed/PUB0TaZ7bhA', 'Academics'),
                ('Circle Geometry Level', 'Master chords, tangents, and angles inside circle.', 'https://www.youtube.com/embed/74RcUjxErCg', 'Academics'),
                ('Calculus: Integration Level', 'Master integration and anti-derivatives.', 'https://www.youtube.com/embed/6WUjbJEeJwM', 'Academics')
            ]
        }

        # --- English Topics ---
        english_topics = {
            'en': [
                ('English Grammar: Tenses', 'Mastering the 12 English tenses and sentence structure.', 'https://www.youtube.com/embed/kYJv8Z16o3k', 'Academics'),
                ('Elements of Literature', 'Exploring Plot, Theme, and Characterization in African Literature.', 'https://www.youtube.com/embed/Pxao6AG88Lw', 'Academics'),
                ('Summary Writing Skills', 'How to extract main points and write concise summaries.', 'https://www.youtube.com/embed/bhtz7RSaKlc', 'Academics'),
                ('Parts of Speech', 'Overview of Nouns, Verbs, Adjectives and more.', 'https://www.youtube.com/embed/01_pXpA674A', 'Academics'),
                ('Punctuation Marks', 'Mastering commas, full stops, and semicolons.', 'https://www.youtube.com/embed/LdCoUz71S_Y', 'Academics'),
                ('Essay Writing', 'Techniques for narrative, descriptive and argumentative essays.', 'https://www.youtube.com/embed/0TshwzD3IHY', 'Academics'),
                ('Oral English', 'Understanding vowel sounds and pronunciation.', 'https://www.youtube.com/embed/0_R_KjP_M_0', 'Academics'),
                ('Common Errors', 'Fixing common mistakes in English sentence structure.', 'https://www.youtube.com/embed/2_Y_Z_K_Q_0', 'Academics')
            ],
            'ha': [
                ('Adabin Turanci', 'Gano Makasudin Labari, Jigo, da Halayen mutane a adabin Afirka.', 'https://www.youtube.com/embed/Pxao6AG88Lw', 'Academics')
            ],
            'yo': [
            ],
            'ig': [
            ],
            'pi': [
            ]
        }

        # --- Biology Topics ---
        biology_topics = {
            'en': [
                ('Cell Structure & Function', 'Detailed look at organelles and the building blocks of life.', 'https://www.youtube.com/embed/URUJD5NEXC8', 'Academics'),
                ('Photosynthesis', 'The chemical process of light conversion in green plants.', 'https://www.youtube.com/embed/SXP6u7m6YFk', 'Academics'),
                ('Genetics & Heredity', 'How DNA and RNA control inheritance across generations.', 'https://www.youtube.com/embed/2reevjoVn6c', 'Academics'),
                ('Respiratory System', 'Understanding how oxygen and carbon dioxide exchange in humans.', 'https://www.youtube.com/embed/f9ONXd_-anM', 'Academics'),
                ('Circulatory System', 'How the heart and blood vessels transport nutrients.', 'https://www.youtube.com/embed/9-XoM21uUCg', 'Academics'),
                ('Nervous System', 'Understanding the brain, spinal cord, and nerves.', 'https://www.youtube.com/embed/qPix_X-9t7E', 'Academics'),
                ('Ecology Basics', 'Interactions between organisms and their environment.', 'https://www.youtube.com/embed/GIn7PYCPutg', 'Academics'),
                ('Digestive System', 'The journey of food through the human body.', 'https://www.youtube.com/embed/Og5xAdC8OKE', 'Academics'),
                ('Excretory System', 'How the body removes waste products.', 'https://www.youtube.com/embed/2_8_V_K_N_0', 'Academics')
            ],
            'ha': [
            ],
            'yo': [
            ],
            'ig': [
            ],
            'pi': [
            ]
        }

        # --- Physics Topics ---
        physics_topics = {
            'en': [
                ('Newton\'s Laws of Motion', 'Understanding how forces affect objects in motion.', 'https://www.youtube.com/embed/g550H4e5FCY', 'Academics'),
                ('Work, Energy & Power', 'Master the fundamental concepts of physical energy.', 'https://www.youtube.com/embed/2WS1sG9fhOk', 'Academics'),
                ('Pressure in Liquids', 'Hydraulics and pressure distribution in fluids.', 'https://www.youtube.com/embed/0B0Xv2fS9_U', 'Academics'),
                ('Electricity Basics', 'Introduction to circuits, voltage, and current.', 'https://www.youtube.com/embed/mc979OhitAg', 'Academics'),
                ('Light: Reflection', 'Laws of reflection and mirror images.', 'https://www.youtube.com/embed/dwP_Z_K_V_0', 'Academics'),
                ('Simple Harmonic Motion', 'Oscillations and wave behavior.', 'https://www.youtube.com/embed/t_L_M_S_H_M', 'Academics'),
                ('Heat & Temperature', 'Thermal properties and heat transfer.', 'https://www.youtube.com/embed/k_N_O_T_H_E', 'Academics'),
                ('Radioactivity', 'Understanding nuclear decay and isotopes.', 'https://www.youtube.com/embed/r_A_D_I_O_A', 'Academics'),
                ('Waves Properties', 'Amplitude, frequency, and wavelength.', 'https://www.youtube.com/embed/w_A_V_E_S_P', 'Academics')
            ]
        }

        # --- Chemistry Topics ---
        chemistry_topics = {
            'en': [
                ('Atomic Structure', 'Detailed study of protons, neutrons, and electrons.', 'https://www.youtube.com/embed/OH-aSu-rWgk', 'Academics'),
                ('Chemical Bonding', 'How atoms join together to form molecules.', 'https://www.youtube.com/embed/QXT4OVM4vXI', 'Academics'),
                ('Acids, Bases and Salts', 'Understanding chemical properties of substances.', 'https://www.youtube.com/embed/ANi709MYnWg', 'Academics'),
                ('The Periodic Table', 'Organisation of elements and their properties.', 'https://www.youtube.com/embed/0RRVV4Diomg', 'Academics'),
                ('Stoichiometry', 'Calculating reactants and products in reactions.', 'https://www.youtube.com/embed/S_T_O_I_C_H', 'Academics'),
                ('Organic: Alkanes', 'Introduction to hydrocarbons and bonding.', 'https://www.youtube.com/embed/O_R_G_A_N_I', 'Academics'),
                ('Redox Reactions', 'Understanding oxidation and reduction.', 'https://www.youtube.com/embed/R_E_D_O_X_R', 'Academics'),
                ('Reaction Rates', 'Factors affecting how fast chemicals react.', 'https://www.youtube.com/embed/R_A_T_E_S_R', 'Academics'),
                ('Chemical Equilibrium', 'Reversible reactions and steady states.', 'https://www.youtube.com/embed/E_Q_U_I_L_I', 'Academics')
            ]
        }

        basic_science_topics = {
            'en': [
                ('Matter and Its Properties', 'States of matter, physical and chemical changes.', 'https://www.youtube.com/embed/S_T_A_T_E_S', 'Academics'),
                ('Living vs Non-Living', 'Characteristics of life and biological classification.', 'https://www.youtube.com/embed/L_I_V_I_N_G', 'Academics'),
                ('Simple Machines', 'Levers, pulleys, and inclined planes for work efficiency.', 'https://www.youtube.com/embed/M_A_C_H_I_N', 'Academics'),
                ('Safety Measures', 'First aid basics and lab safety protocols.', 'https://www.youtube.com/embed/S_A_F_E_T_Y', 'Academics'),
                ('Environmental Care', 'Pollution control and recycling practices.', 'https://www.youtube.com/embed/E_N_V_I_R_O', 'Academics')
            ]
        }

        social_studies_topics = {
            'en': [
                ('The Family Unit', 'Roles, types, and importance of family in society.', 'https://www.youtube.com/embed/F_A_M_I_L_Y', 'Academics'),
                ('Civic Rights', 'Understanding your rights and duties as a citizen.', 'https://www.youtube.com/embed/R_I_G_H_T_S', 'Academics'),
                ('Cultural Diversity', 'Exploring heritage, traditions, and national unity.', 'https://www.youtube.com/embed/C_U_L_T_U_R', 'Academics'),
                ('Social Problems', 'Addressing drug abuse, crime, and social inequality.', 'https://www.youtube.com/embed/I_S_S_U_E_S', 'Academics'),
                ('Interpersonal Relations', 'Communication skills and conflict resolution.', 'https://www.youtube.com/embed/R_E_L_A_T_E', 'Academics')
            ]
        }
        commerce_topics = {
            'en': [
                ('Scope of Commerce', 'Introduction to Trade and Aids to Trade.', 'https://www.youtube.com/embed/7z-r5O-S9qI', 'Academics'),
                ('Occupation', 'Classification of jobs and professional tracks.', 'https://www.youtube.com/embed/kn83BA7cRNM', 'Academics'),
                ('Insurance Basics', 'Risk management and indemnification.', 'https://www.youtube.com/embed/I_N_S_U_R_A', 'Academics'),
                ('Banking Systems', 'Commercial and Central banking functions.', 'https://www.youtube.com/embed/B_A_N_K_I_N', 'Academics'),
                ('Marketing Principles', 'Product, Price, Place, and Promotion.', 'https://www.youtube.com/embed/M_A_R_K_E_T', 'Academics'),
                ('International Trade', 'Import, Export, and Balance of Payments.', 'https://www.youtube.com/embed/T_R_A_D_E_I', 'Academics'),
                ('Consumer Protection', 'Rights and responsibilities of buyers.', 'https://www.youtube.com/embed/C_O_N_S_U_M', 'Academics')
            ]
        }

        agric_topics = {
            'en': [
                ('Introduction to Agriculture', 'Importance and branches of agricultural science.', 'https://www.youtube.com/embed/R2_1cMh2gM0', 'Academics'),
                ('Animal Husbandry', 'Principles of rearing livestock and animal health.', 'https://www.youtube.com/embed/f9ONXd_-anM', 'Academics'),
                ('Soil Conservation', 'Techniques to prevent erosion and maintain fertility.', 'https://www.youtube.com/embed/S_O_I_L_C_O', 'Academics'),
                ('Crop Pests', 'Identifying and controlling agricultural pests.', 'https://www.youtube.com/embed/P_E_S_T_S_C', 'Academics'),
                ('Irrigation Systems', 'Artificial methods of supplying water to crops.', 'https://www.youtube.com/embed/I_R_R_I_G_A', 'Academics'),
                ('Farm Mechanization', 'Use of machinery in modern agriculture.', 'https://www.youtube.com/embed/M_E_C_H_A_N', 'Academics'),
                ('Agricultural Economics', 'Marketing and finance in farming.', 'https://www.youtube.com/embed/E_C_O_N_O_M', 'Academics')
            ]
        }

        geography_topics = {
            'en': [
                ('Introduction to Geography', 'The solar system and the earth\'s structure.', 'https://www.youtube.com/embed/R9K-J0l0L44', 'Academics'),
                ('Map Reading', 'Mastering scale, bearings and relief representation.', 'https://www.youtube.com/embed/74RcUjxErCg', 'Academics'),
                ('Weather & Climate', 'Difference between atmospheric conditions.', 'https://www.youtube.com/embed/W_E_A_T_H_E', 'Academics'),
                ('Environmental Hazards', 'Dealing with floods, erosion, and pollution.', 'https://www.youtube.com/embed/H_A_Z_A_R_D', 'Academics'),
                ('Population Study', 'Distribution and migration patterns.', 'https://www.youtube.com/embed/P_O_P_U_L_A', 'Academics'),
                ('Industrial Geography', 'Location of industries and resources.', 'https://www.youtube.com/embed/I_N_D_U_S_T', 'Academics'),
                ('Earth Structure', 'Crust, Mantle, and Core layers.', 'https://www.youtube.com/embed/C_O_R_E_L_A', 'Academics')
            ]
        }

        social_studies_topics = {
            'en': [
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
                db.session.add(LearningMaterial(title=title, content=content, resource_url=url, subject='Biology', language=lang, material_type='video_link', education_level='Academics'))
                topic = Topic(name=title, subject='Biology', education_level='Academics')
                db.session.add(topic); db.session.flush()
                db.session.add(TopicVideo(topic_id=topic.id, video_url=url, video_title=title))
            
            # Seed Physics
            for title, content, url, level in physics_topics.get(lang, physics_topics['en']):
                db.session.add(LearningMaterial(title=title, content=content, resource_url=url, subject='Physics', language=lang, material_type='video_link', education_level='Academics'))
                topic = Topic(name=title, subject='Physics', education_level='Academics')
                db.session.add(topic); db.session.flush()
                db.session.add(TopicVideo(topic_id=topic.id, video_url=url, video_title=title))
            
            # Seed Chemistry
            for title, content, url, level in chemistry_topics.get(lang, chemistry_topics['en']):
                db.session.add(LearningMaterial(title=title, content=content, resource_url=url, subject='Chemistry', language=lang, material_type='video_link', education_level='Academics'))
                topic = Topic(name=title, subject='Chemistry', education_level='Academics')
                db.session.add(topic); db.session.flush()
                db.session.add(TopicVideo(topic_id=topic.id, video_url=url, video_title=title))

            for title, content, url, level in basic_science_topics.get(lang, basic_science_topics['en']):
                db.session.add(LearningMaterial(title=title, content=content, resource_url=url, subject='Science', language=lang, material_type='video_link', education_level=level))
                topic = Topic(name=title, subject='Science', education_level=level)
                db.session.add(topic); db.session.flush()
                db.session.add(TopicVideo(topic_id=topic.id, video_url=url, video_title=title))


            for title, content, url, level in commerce_topics.get(lang, commerce_topics['en']):
                db.session.add(LearningMaterial(title=title, content=content, resource_url=url, subject='Commerce', language=lang, material_type='video_link', education_level=level))
                topic = Topic(name=title, subject='Commerce', education_level=level)
                db.session.add(topic); db.session.flush()
                db.session.add(TopicVideo(topic_id=topic.id, video_url=url, video_title=title))

            for title, content, url, level in agric_topics.get(lang, agric_topics['en']):
                db.session.add(LearningMaterial(title=title, content=content, resource_url=url, subject='Agricultural Science', language=lang, material_type='video_link', education_level=level))
                topic = Topic(name=title, subject='Agricultural Science', education_level=level)
                db.session.add(topic); db.session.flush()
                db.session.add(TopicVideo(topic_id=topic.id, video_url=url, video_title=title))

            for title, content, url, level in geography_topics.get(lang, geography_topics['en']):
                db.session.add(LearningMaterial(title=title, content=content, resource_url=url, subject='Geography', language=lang, material_type='video_link', education_level=level))
                topic = Topic(name=title, subject='Geography', education_level=level)
                db.session.add(topic); db.session.flush()
                db.session.add(TopicVideo(topic_id=topic.id, video_url=url, video_title=title))

            for title, content, url, level in social_studies_topics.get(lang, social_studies_topics['en']):
                db.session.add(LearningMaterial(title=title, content=content, resource_url=url, subject='Social Studies', language=lang, material_type='video_link', education_level=level))
                topic = Topic(name=title, subject='Social Studies', education_level=level)
                db.session.add(topic); db.session.flush()
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
            ('Third Person', 'Story told using "he", "she", or "they".', 'English'),

            # Biology (50)
            ('Organelle', 'Specialized structure within a cell (e.g. Mitochondria).', 'Biology'),
            ('Ribosome', 'Site of protein synthesis.', 'Biology'),
            ('Lysosome', 'Contains digestive enzymes to break down waste.', 'Biology'),
            ('Vacuole', 'Storage sac for water, nutrients, or waste.', 'Biology'),
            ('Cytoplasm', 'Jelly-like substance filling the cell.', 'Biology'),
            ('Cell Membrane', 'Semi-permeable outer layer of a cell.', 'Biology'),
            ('Cell Wall', 'Rigid outer layer found in plant cells.', 'Biology'),
            ('Nucleus', 'Control center of the cell containing DNA.', 'Biology'),
            ('DNA', 'Carrier of genetic information.', 'Biology'),
            ('RNA', 'Molecule that translates DNA into proteins.', 'Biology'),
            ('ATP', 'Primary energy carrier in cells.', 'Biology'),
            ('Glucose', 'A simple sugar used for energy.', 'Biology'),
            ('Enzyme', 'Biological catalyst that speeds up reactions.', 'Biology'),
            ('Catalyst', 'Substance that increases reaction rate.', 'Biology'),
            ('Substrate', 'Reactant upon which an enzyme acts.', 'Biology'),
            ('Hormone', 'Chemical messenger in the body.', 'Biology'),
            ('Homeostasis', 'Maintenance of a stable internal environment.', 'Biology'),
            ('Neuron', 'Nerve cell that transmits electrical signals.', 'Biology'),
            ('Synapse', 'Gap between two neurons.', 'Biology'),
            ('Cerebrum', 'Largest part of the brain for conscious thought.', 'Biology'),
            ('Cerebellum', 'Part of brain for balance and coordination.', 'Biology'),
            ('Heart', 'Muscular organ that pumps blood.', 'Biology'),
            ('Atrium', 'Upper chamber of the heart.', 'Biology'),
            ('Ventricle', 'Lower chamber of the heart.', 'Biology'),
            ('Artery', 'Blood vessel carrying blood away from heart.', 'Biology'),
            ('Vein', 'Blood vessel carrying blood toward heart.', 'Biology'),
            ('Capillary', 'Smallest blood vessel for nutrient exchange.', 'Biology'),
            ('Alveoli', 'Air sacs in lungs for gas exchange.', 'Biology'),
            ('Nephron', 'Functional unit of the kidney.', 'Biology'),
            ('Liver', 'Organ that detoxifies and produces bile.', 'Biology'),
            ('Stomach', 'Muscular sac for chemical digestion.', 'Biology'),
            ('Small Intestine', 'Primary site of nutrient absorption.', 'Biology'),
            ('Large Intestine', 'Site of water absorption.', 'Biology'),
            ('Metabolism', 'Sum of all chemical reactions in the body.', 'Biology'),
            ('Antibody', 'Protein produced to fight pathogens.', 'Biology'),
            ('Antigen', 'Substance that triggers immune response.', 'Biology'),
            ('Pathogen', 'Disease-causing organism.', 'Biology'),
            ('Bacteria', 'Single-celled prokaryotic organisms.', 'Biology'),
            ('Virus', 'Non-living agent that infects cells.', 'Biology'),
            ('Evolution', 'Change in inherited traits over generations.', 'Biology'),
            ('Natural Selection', 'Survival of the fittest.', 'Biology'),
            ('Species', 'Group of organisms that can interbreed.', 'Biology'),
            ('Habitat', 'Natural home of an organism.', 'Biology'),
            ('Niche', 'Role of an organism in its ecosystem.', 'Biology'),
            ('Food Web', 'Interconnected food chains.', 'Biology'),
            ('Producers', 'Organisms that make their own food.', 'Biology'),
            ('Consumers', 'Organisms that eat other organisms.', 'Biology'),
            ('Decomposers', 'Break down dead organic matter.', 'Biology'),
            ('Taxonomy', 'Science of classifying organisms.', 'Biology'),
            ('Kingdom', 'Broadest category of biological classification.', 'Biology'),

            # Physics (50)
            ('Scalar', 'Quantity with magnitude only.', 'Physics'),
            ('Vector', 'Quantity with magnitude and direction.', 'Physics'),
            ('Displacement', 'Change in position in a specific direction.', 'Physics'),
            ('Velocity', 'Rate of change of displacement.', 'Physics'),
            ('Acceleration', 'Rate of change of velocity.', 'Physics'),
            ('Force', 'Push or pull on an object (Newton).', 'Physics'),
            ('Mass', 'Amount of matter in an object (kg).', 'Physics'),
            ('Weight', 'Force of gravity on an object.', 'Physics'),
            ('Friction', 'Force opposing motion between surfaces.', 'Physics'),
            ('Gravity', 'Force of attraction between masses.', 'Physics'),
            ('Work', 'Force applied over a distance (Joule).', 'Physics'),
            ('Energy', 'Ability to do work.', 'Physics'),
            ('Power', 'Rate at which work is done (Watt).', 'Physics'),
            ('Kinetic Energy', 'Energy of motion.', 'Physics'),
            ('Potential Energy', 'Stored energy based on position.', 'Physics'),
            ('Momentum', 'Product of mass and velocity.', 'Physics'),
            ('Impulse', 'Change in momentum.', 'Physics'),
            ('Pressure', 'Force per unit area (Pascal).', 'Physics'),
            ('Density', 'Mass per unit volume.', 'Physics'),
            ('Buoyancy', 'Upward force exerted by a fluid.', 'Physics'),
            ('Temperature', 'Measure of average kinetic energy.', 'Physics'),
            ('Heat', 'Transfer of energy due to temp difference.', 'Physics'),
            ('Entropy', 'Measure of disorder in a system.', 'Physics'),
            ('Wave', 'Disturbance that transfers energy.', 'Physics'),
            ('Frequency', 'Waves per second (Hertz).', 'Physics'),
            ('Wavelength', 'Distance between wave peaks.', 'Physics'),
            ('Amplitude', 'Maximum displacement from equilibrium.', 'Physics'),
            ('Reflection', 'Bouncing of waves off a surface.', 'Physics'),
            ('Refraction', 'Bending of waves through different media.', 'Physics'),
            ('Induction', 'Production of current by changing magnetic field.', 'Physics'),
            ('Resistance', 'Opposition to current flow (Ohm).', 'Physics'),
            ('Voltage', 'Potential difference (Volt).', 'Physics'),
            ('Current', 'Flow of charge (Ampere).', 'Physics'),
            ('Capacitance', 'Ability to store charge.', 'Physics'),
            ('Magnetism', 'Force exerted by magnets.', 'Physics'),
            ('Photon', 'Particle of light.', 'Physics'),
            ('Isotope', 'Same protons, different neutrons.', 'Physics'),
            ('Fission', 'Splitting of a heavy nucleus.', 'Physics'),
            ('Fusion', 'Joining of light nuclei.', 'Physics'),
            ('Relativity', 'Einstein\'s theory of space and time.', 'Physics'),
            ('Inertia', 'Resistance to change in motion.', 'Physics'),
            ('Torque', 'Rotational force.', 'Physics'),
            ('Circuit', 'Path for electrical current.', 'Physics'),
            ('Conductor', 'Material allowing easy charge flow.', 'Physics'),
            ('Insulator', 'Material resisting charge flow.', 'Physics'),
            ('Semiconductor', 'Material with partial conductivity.', 'Physics'),
            ('Transverse Wave', 'Oscillation perpendicular to propagation.', 'Physics'),
            ('Longitudinal Wave', 'Oscillation parallel to propagation.', 'Physics'),
            ('Doppler Effect', 'Change in frequency due to motion.', 'Physics'),
            ('Superconductivity', 'Zero resistance at low temperatures.', 'Physics'),

            # Chemistry (50)
            ('Atom', 'Smallest unit of an element.', 'Chemistry'),
            ('Element', 'Substance made of one type of atom.', 'Chemistry'),
            ('Compound', 'Two or more elements chemically combined.', 'Chemistry'),
            ('Mixture', 'Physical combination of substances.', 'Chemistry'),
            ('Proton', 'Positive particle in nucleus.', 'Chemistry'),
            ('Neutron', 'Neutral particle in nucleus.', 'Chemistry'),
            ('Electron', 'Negative particle orbiting nucleus.', 'Chemistry'),
            ('Valency', 'Combining power of an atom.', 'Chemistry'),
            ('Ionic Bond', 'Transfer of electrons between atoms.', 'Chemistry'),
            ('Covalent Bond', 'Sharing of electrons between atoms.', 'Chemistry'),
            ('Molecule', 'Group of atoms bonded together.', 'Chemistry'),
            ('pH', 'Measure of acidity or alkalinity.', 'Chemistry'),
            ('Acid', 'Proton donor (pH < 7).', 'Chemistry'),
            ('Base', 'Proton acceptor (pH > 7).', 'Chemistry'),
            ('Salt', 'Product of acid-base neutralization.', 'Chemistry'),
            ('Oxidation', 'Loss of electrons.', 'Chemistry'),
            ('Reduction', 'Gain of electrons.', 'Chemistry'),
            ('Catalyst', 'Speeds up reaction without being consumed.', 'Chemistry'),
            ('Exothermic', 'Reaction that releases heat.', 'Chemistry'),
            ('Endothermic', 'Reaction that absorbs heat.', 'Chemistry'),
            ('Mole', 'SI unit for amount of substance.', 'Chemistry'),
            ('Solute', 'Substance being dissolved.', 'Chemistry'),
            ('Solvent', 'Substance doing the dissolving.', 'Chemistry'),
            ('Solution', 'Homogeneous mixture.', 'Chemistry'),
            ('Titration', 'Method to find concentration of solution.', 'Chemistry'),
            ('Isotopes', 'Atoms with different neutron counts.', 'Chemistry'),
            ('Allotropes', 'Different forms of the same element.', 'Chemistry'),
            ('Hydrocarbon', 'Compound of hydrogen and carbon.', 'Chemistry'),
            ('Alkane', 'Saturated hydrocarbon (single bonds).', 'Chemistry'),
            ('Alkene', 'Unsaturated hydrocarbon (double bond).', 'Chemistry'),
            ('Polymer', 'Large molecule made of repeating units.', 'Chemistry'),
            ('Electrolysis', 'Chemical change caused by electricity.', 'Chemistry'),
            ('Anode', 'Positive electrode.', 'Chemistry'),
            ('Cathode', 'Negative electrode.', 'Chemistry'),
            ('Diffusion', 'Spreading of particles.', 'Chemistry'),
            ('Sublimation', 'Solid to gas change directly.', 'Chemistry'),
            ('Distillation', 'Separation based on boiling points.', 'Chemistry'),
            ('Chromatography', 'Separation based on solubility.', 'Chemistry'),
            ('Noble Gases', 'Unreactive group 18 elements.', 'Chemistry'),
            ('Halogens', 'Reactive group 17 elements.', 'Chemistry'),
            ('Alkali Metals', 'Highly reactive group 1 elements.', 'Chemistry'),
            ('Atomic Number', 'Number of protons.', 'Chemistry'),
            ('Mass Number', 'Protons + Neutrons.', 'Chemistry'),
            ('Avogadro Constant', '6.022 x 10^23 molecules per mole.', 'Chemistry'),
            ('Equilibrium', 'Forward and backward rates are equal.', 'Chemistry'),
            ('Indicator', 'Changes color at specific pH.', 'Chemistry'),
            ('Boyle\'s Law', 'P1V1 = P2V2 at constant temp.', 'Chemistry'),
            ('Charles\'s Law', 'V1/T1 = V2/T2 at constant pressure.', 'Chemistry'),
            ('Concentration', 'Amount of solute per volume.', 'Chemistry'),
            ('Saturated Solution', 'Contains max dissolved solute.', 'Chemistry'),

            # Agricultural Science (50)
            ('Agronomy', 'Science of soil management and crop production.', 'Agricultural Science'),
            ('Fertility', 'Ability of soil to sustain plant growth.', 'Agricultural Science'),
            ('Nitrogen', 'Essential nutrient for leaf growth.', 'Agricultural Science'),
            ('Phosphorus', 'Essential nutrient for root development.', 'Agricultural Science'),
            ('Potassium', 'Essential nutrient for overall plant health.', 'Agricultural Science'),
            ('Compost', 'Decomposed organic matter used as fertilizer.', 'Agricultural Science'),
            ('Tillage', 'Preparation of soil by mechanical agitation.', 'Agricultural Science'),
            ('Irrigation', 'Artificial supply of water to land.', 'Agricultural Science'),
            ('Pesticide', 'Chemical used to kill pests.', 'Agricultural Science'),
            ('Herbicide', 'Chemical used to kill weeds.', 'Agricultural Science'),
            ('Harvesting', 'Gathering of ripe crops.', 'Agricultural Science'),
            ('Livestock', 'Domesticated animals raised for food/work.', 'Agricultural Science'),
            ('Poultry', 'Birds raised for meat or eggs.', 'Agricultural Science'),
            ('Breeding', 'Producing offspring with desired traits.', 'Agricultural Science'),
            ('Silage', 'Fermented, high-moisture stored fodder.', 'Agricultural Science'),
            ('Agro-forestry', 'Combining agriculture and forestry.', 'Agricultural Science'),
            ('Erosion', 'Wearing away of topsoil.', 'Agricultural Science'),
            ('Mulching', 'Covering soil to retain moisture.', 'Agricultural Science'),
            ('Pruning', 'Cutting away dead or overgrown branches.', 'Agricultural Science'),
            ('Thinning', 'Removing some plants to allow others room.', 'Agricultural Science'),
            ('Fallowing', 'Leaving land unplanted to recover.', 'Agricultural Science'),
            ('Crop Rotation', 'Growing different crops in sequence.', 'Agricultural Science'),
            ('Monoculture', 'Growing only one type of crop.', 'Agricultural Science'),
            ('Organic Farming', 'Farming without synthetic chemicals.', 'Agricultural Science'),
            ('Greenhouse', 'Structure for growing plants in controlled heat.', 'Agricultural Science'),
            ('Hydroponics', 'Growing plants in water without soil.', 'Agricultural Science'),
            ('Aquaculture', 'Rearing aquatic animals.', 'Agricultural Science'),
            ('Apiculture', 'Bee keeping.', 'Agricultural Science'),
            ('Floriculture', 'Growing flowers.', 'Agricultural Science'),
            ('Horticulture', 'Garden cultivation and management.', 'Agricultural Science'),
            ('Pedology', 'Study of soil.', 'Agricultural Science'),
            ('Leaching', 'Loss of nutrients by water drainage.', 'Agricultural Science'),
            ('NPK', 'Common fertilizer (Nitrogen, Phosphorus, Potassium).', 'Agricultural Science'),
            ('Photosynthesis', 'Plants making food using light.', 'Agricultural Science'),
            ('Transpiration', 'Loss of water vapor from plants.', 'Agricultural Science'),
            ('Germination', 'Growth of a plant from a seed.', 'Agricultural Science'),
            ('Pollination', 'Transfer of pollen for fertilization.', 'Agricultural Science'),
            ('Hybrid', 'Offspring of two different varieties.', 'Agricultural Science'),
            ('Pathogen', 'Organism causing crop disease.', 'Agricultural Science'),
            ('Ruminant', 'Animal with four-chambered stomach (e.g. Cow).', 'Agricultural Science'),
            ('Draft Animal', 'Animal used for pulling heavy loads.', 'Agricultural Science'),
            ('Extension Officer', 'Teacher of modern farming techniques.', 'Agricultural Science'),
            ('Subsistence Farming', 'Farming only for family needs.', 'Agricultural Science'),
            ('Commercial Farming', 'Farming for sale and profit.', 'Agricultural Science'),
            ('Land Tenure', 'System of land ownership.', 'Agricultural Science'),
            ('Mechanization', 'Using machines for farm tasks.', 'Agricultural Science'),
            ('Post-Harvest Loss', 'Loss of crop after gathering.', 'Agricultural Science'),
            ('Soil Profile', 'Vertical section of soil layers.', 'Agricultural Science'),
            ('Texture', 'Relative proportions of sand, silt, and clay.', 'Agricultural Science'),
            ('Drainage', 'Removal of excess water from soil.', 'Agricultural Science'),

            # Geography (50)
            ('Latitude', 'Horizontal lines measuring distance from Equator.', 'Geography'),
            ('Longitude', 'Vertical lines measuring distance from Meridian.', 'Geography'),
            ('Equator', 'Imaginary line dividing North/South (0°).', 'Geography'),
            ('Meridian', 'Imaginary line dividing East/West (0°).', 'Geography'),
            ('Continent', 'One of Earth\'s seven large landmasses.', 'Geography'),
            ('Island', 'Land surrounded by water on all sides.', 'Geography'),
            ('Plateau', 'Highland with a flat top.', 'Geography'),
            ('Canyon', 'Deep valley with steep sides.', 'Geography'),
            ('Delta', 'Landform at the mouth of a river.', 'Geography'),
            ('Estuary', 'Where river meets the sea.', 'Geography'),
            ('Basin', 'Area drained by a river system.', 'Geography'),
            ('Lake', 'Large body of water surrounded by land.', 'Geography'),
            ('Erosion', 'Wearing away of land by wind/water.', 'Geography'),
            ('Fault', 'Fracture in Earth\'s crust.', 'Geography'),
            ('Fold', 'Bending of rock layers.', 'Geography'),
            ('Volcano', 'Vent in crust releasing magma.', 'Geography'),
            ('Earthquake', 'Sudden shaking of the ground.', 'Geography'),
            ('Crust', 'Outermost layer of Earth.', 'Geography'),
            ('Mantle', 'Layer below the crust.', 'Geography'),
            ('Core', 'Hottest, innermost layer of Earth.', 'Geography'),
            ('Atmosphere', 'Envelope of gases surrounding Earth.', 'Geography'),
            ('Climate', 'Long-term weather patterns.', 'Geography'),
            ('Weather', 'Short-term atmospheric conditions.', 'Geography'),
            ('Precipitation', 'Rain, snow, sleet, or hail.', 'Geography'),
            ('Humidity', 'Amount of water vapor in air.', 'Geography'),
            ('Wind', 'Movement of air from high to low pressure.', 'Geography'),
            ('Ecosystem', 'Community of living and non-living things.', 'Geography'),
            ('Biome', 'Large regional ecosystem (e.g. Desert).', 'Geography'),
            ('Urbanization', 'Growth of cities.', 'Geography'),
            ('Migration', 'Movement of people from one place to another.', 'Geography'),
            ('Population Density', 'People per unit area.', 'Geography'),
            ('Gully Erosion', 'Deep channels carved by running water.', 'Geography'),
            ('Sustainability', 'Using resources without depleting them.', 'Geography'),
            ('Cartography', 'Science of map making.', 'Geography'),
            ('Scale', 'Ratio of map distance to real distance.', 'Geography'),
            ('Legend', 'Key explaining map symbols.', 'Geography'),
            ('Relief', 'Variation in elevation of land.', 'Geography'),
            ('Topography', 'Physical features of an area.', 'Geography'),
            ('Orbit', 'Path of Earth around the Sun.', 'Geography'),
            ('Rotation', 'Spinning of Earth on its axis.', 'Geography'),
            ('Revolution', 'Earth\'s movement around the Sun.', 'Geography'),
            ('Season', 'Division of year marked by weather changes.', 'Geography'),
            ('Resource', 'Something useful from the environment.', 'Geography'),
            ('Renewable', 'Resource that can be replaced (e.g. Solar).', 'Geography'),
            ('Non-renewable', 'Resource that cannot be replaced (e.g. Oil).', 'Geography'),
            ('Pollution', 'Harmful materials in the environment.', 'Geography'),
            ('Deforestation', 'Clearing of forests.', 'Geography'),
            ('Irrigation', 'Artificial watering of land.', 'Geography'),
            ('Glacier', 'Slow moving mass of ice.', 'Geography'),
            ('Tide', 'Rising and falling of the sea.', 'Geography'),

            # Commerce (50)
            ('Trade', 'Exchange of goods and services.', 'Commerce'),
            ('Retail', 'Selling in small quantities to consumers.', 'Commerce'),
            ('Wholesale', 'Selling in bulk to retailers.', 'Commerce'),
            ('Barter', 'Exchange of goods without money.', 'Commerce'),
            ('Currency', 'System of money in use.', 'Commerce'),
            ('Bank', 'Financial institution for deposits/loans.', 'Commerce'),
            ('Credit', 'Ability to obtain goods before payment.', 'Commerce'),
            ('Asset', 'Something of value owned.', 'Commerce'),
            ('Liability', 'Money owed to others.', 'Commerce'),
            ('Capital', 'Money or wealth used to start business.', 'Commerce'),
            ('Profit', 'Revenue minus expenses.', 'Commerce'),
            ('Budget', 'Financial plan for a period.', 'Commerce'),
            ('Tax', 'Mandatory payment to government.', 'Commerce'),
            ('Insurance', 'Protection against financial loss.', 'Commerce'),
            ('Policy', 'Insurance contract.', 'Commerce'),
            ('Indemnity', 'Compensation for loss/damage.', 'Commerce'),
            ('Marketing', 'Promoting and selling products.', 'Commerce'),
            ('Branding', 'Creating a unique name/image.', 'Commerce'),
            ('Logistics', 'Management of flow of goods.', 'Commerce'),
            ('Warehouse', 'Storage facility for goods.', 'Commerce'),
            ('Inventory', 'List of goods in stock.', 'Commerce'),
            ('Dividend', 'Share of profit paid to stockholders.', 'Commerce'),
            ('Investment', 'Allocating money for future gain.', 'Commerce'),
            ('Demand', 'Consumer desire to buy.', 'Commerce'),
            ('Supply', 'Amount of product available.', 'Commerce'),
            ('Monopoly', 'Market with only one seller.', 'Commerce'),
            ('Oligopoly', 'Market with few large sellers.', 'Commerce'),
            ('Entrepreneur', 'Person who starts a business.', 'Commerce'),
            ('E-commerce', 'Buying and selling online.', 'Commerce'),
            ('Balance Sheet', 'Financial statement of assets/liabilities.', 'Commerce'),
            ('Invoicing', 'Requesting payment for goods.', 'Commerce'),
            ('Bookkeeping', 'Recording of financial transactions.', 'Commerce'),
            ('Audit', 'Official inspection of accounts.', 'Commerce'),
            ('Tariff', 'Tax on imported goods.', 'Commerce'),
            ('Subsidy', 'Government grant to support business.', 'Commerce'),
            ('Partnership', 'Business owned by two or more people.', 'Commerce'),
            ('Corporation', 'Company recognized as legal entity.', 'Commerce'),
            ('Niche Market', 'Small, specialized market segment.', 'Commerce'),
            ('Outsourcing', 'Hiring external firm for tasks.', 'Commerce'),
            ('Inflation', 'General rise in prices.', 'Commerce'),
            ('Deflation', 'General fall in prices.', 'Commerce'),
            ('GDP', 'Total value of goods produced in country.', 'Commerce'),
            ('Interest Rate', 'Cost of borrowing money.', 'Commerce'),
            ('Merger', 'Combining two companies into one.', 'Commerce'),
            ('Acquisition', 'One company buying another.', 'Commerce'),
            ('Franchise', 'License to use business name/system.', 'Commerce'),
            ('Debt', 'Money that is owed.', 'Commerce'),
            ('Broker', 'Agent who arranges transactions.', 'Commerce'),
            ('Commodity', 'Basic good used in commerce.', 'Commerce'),
            ('Markup', 'Amount added to cost price for profit.', 'Commerce'),

            # Social Studies (50)
            ('Society', 'Group of people living together.', 'Social Studies'),
            ('Community', 'People with common interests or location.', 'Social Studies'),
            ('Family', 'Basic unit of society.', 'Social Studies'),
            ('Culture', 'Way of life of a group.', 'Social Studies'),
            ('Tradition', 'Customs passed down through generations.', 'Social Studies'),
            ('Values', 'Beliefs about what is important.', 'Social Studies'),
            ('Norms', 'Expected behaviors in society.', 'Social Studies'),
            ('Integrity', 'Quality of being honest and moral.', 'Social Studies'),
            ('Citizenship', 'Status of being a member of a country.', 'Social Studies'),
            ('Rights', 'Legal or moral entitlements.', 'Social Studies'),
            ('Duties', 'Responsibilities of a citizen.', 'Social Studies'),
            ('Constitution', 'Highest law of a land.', 'Social Studies'),
            ('Democracy', 'Government by the people.', 'Social Studies'),
            ('Federalism', 'Power shared between central/state gov.', 'Social Studies'),
            ('Diversity', 'Variety of cultures/backgrounds.', 'Social Studies'),
            ('Socialization', 'Process of learning societal norms.', 'Social Studies'),
            ('Education', 'Process of teaching and learning.', 'Social Studies'),
            ('Conflict', 'Disagreement or struggle.', 'Social Studies'),
            ('Resolution', 'Finding a solution to a problem.', 'Social Studies'),
            ('Poverty', 'State of being extremely poor.', 'Social Studies'),
            ('Health', 'State of physical/mental well-being.', 'Social Studies'),
            ('Environment', 'Surroundings where people live.', 'Social Studies'),
            ('Population', 'Total number of people in an area.', 'Social Studies'),
            ('Census', 'Official count of population.', 'Social Studies'),
            ('Migration', 'Moving from one place to another.', 'Social Studies'),
            ('Human Rights', 'Basic rights for all humans.', 'Social Studies'),
            ('Equality', 'Being equal in status/rights.', 'Social Studies'),
            ('Justice', 'Fairness in behavior or treatment.', 'Social Studies'),
            ('Civics', 'Study of rights and duties of citizens.', 'Social Studies'),
            ('Cooperation', 'Working together for a common goal.', 'Social Studies'),
            ('Leadership', 'Ability to lead or guide others.', 'Social Studies'),
            ('Heroism', 'Great bravery or courage.', 'Social Studies'),
            ('Patriotism', 'Love and devotion to one\'s country.', 'Social Studies'),
            ('Tolerance', 'Respecting differences in others.', 'Social Studies'),
            ('Prejudice', 'Preconceived opinion not based on reason.', 'Social Studies'),
            ('Stereotype', 'Fixed image of a type of person.', 'Social Studies'),
            ('Discrimination', 'Unfair treatment based on group.', 'Social Studies'),
            ('Drugs', 'Substances affecting body/mind.', 'Social Studies'),
            ('Crime', 'Action that breaks the law.', 'Social Studies'),
            ('Corruption', 'Dishonest or illegal behavior.', 'Social Studies'),
            ('Media', 'Means of mass communication.', 'Social Studies'),
            ('Technology', 'Application of scientific knowledge.', 'Social Studies'),
            ('Globalization', 'World becoming more interconnected.', 'Social Studies'),
            ('Peace', 'Freedom from disturbance or war.', 'Social Studies'),
            ('Security', 'Being free from danger or threat.', 'Social Studies'),
            ('Discipline', 'Quality of being orderly.', 'Social Studies'),
            ('Honesty', 'Quality of being truthful.', 'Social Studies'),
            ('Empathy', 'Ability to understand others\' feelings.', 'Social Studies'),
            ('Ethics', 'Principles of right and wrong.', 'Social Studies'),
            ('Loyalty', 'Being faithful to a cause or person.', 'Social Studies'),
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
                db.session.add(Flashcard(front=front, back=back, subject=subject, language=lang, education_level=level))

        # Assessments
        for lang in languages:
            for sub in ['Mathematics', 'Science', 'English']:
                asm = AssessmentTemplate(title=f"{sub} Mastery Test ({lang.upper()})", subject=sub, time_limit=15)
                db.session.add(asm)
                db.session.flush()
                if sub == 'Mathematics':
                    db.session.add_all([
                        Question(assessment_id=asm.id, text='Solve for x: 2x + 5 = 15', option_a='2', option_b='5', option_c='10', option_d='7', correct_option='B'),
                        Question(assessment_id=asm.id, text='What is the square root of 144?', option_a='12', option_b='14', option_c='10', option_d='16', correct_option='A')
                    ])

        # Past Questions Seeding
        pq_data = [
            ('Mathematics', 2023, 'Algebra', 'Solve for y: 3y - 9 = 0', '1', '3', '9', '0', 'B', '3y = 9 => y = 3', 'Academics'),
            ('Science', 2023, 'Biology', 'Which organ pumps blood?', 'Lungs', 'Heart', 'Liver', 'Brain', 'B', 'The heart is the primary pump.', 'Academics')
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
