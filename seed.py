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
                ('Algebraic expressions and equations', 'Master variables, coefficients, and solving linear equations.', 'https://www.youtube.com/embed/vDqOoI-4Z6M', 'Academics'),
                ('Quadratic equations', 'Solutions and the quadratic formula.', 'https://www.youtube.com/embed/qeByhTF8WEw', 'Academics'),
                ('Geometry (angles, triangles, circles)', 'Properties of shapes and spatial reasoning.', 'https://www.youtube.com/embed/302eJ3TzJQU', 'Academics'),
                ('Statistics and probability', 'Data analysis and chance calculation.', 'https://www.youtube.com/embed/SkidyDQuupA', 'Academics'),
                ('Trigonometry basics', 'Relationship between angles and side ratios.', 'https://www.youtube.com/embed/PUB0TaZ7bhA', 'Academics')
            ]
        }

        # --- English Topics ---
        english_topics = {
            'en': [
                ('Comprehension and summary', 'Developing reading skills and concise summarizing.', 'https://www.youtube.com/embed/e4HiKR3wmWo', 'Academics'),
                ('Essay writing (formal & informal)', 'Mastering different styles of essay composition.', 'https://www.youtube.com/embed/PgwmAUJx248', 'Academics'),
                ('Parts of speech and grammar rules', 'Essential rules for nouns, verbs, and syntax.', 'https://www.youtube.com/embed/chjmnCSPnbw', 'Academics'),
                ('Sentence structure and punctuation', 'Crafting clear sentences with correct punctuation.', 'https://www.youtube.com/embed/nyYyiYULkM4', 'Academics'),
                ('Vocabulary building and word usage', 'Expanding lexicon and understanding context.', 'https://www.youtube.com/embed/CQSUEKNOc6s', 'Academics')
            ]
        }

        # --- Biology Topics ---
        biology_topics = {
            'en': [
                ('Cell structure and functions', 'The building blocks of life and their organelles.', 'https://www.youtube.com/embed/URUJD5NEXC8', 'Academics'),
                ('Nutrition in plants and animals', 'How organisms obtain and process energy.', 'https://www.youtube.com/embed/waamP1uq1Ck', 'Academics'),
                ('Human body systems', 'Anatomy and physiology of major organ systems.', 'https://www.youtube.com/embed/8Z1C7B98KEY', 'Academics'),
                ('Reproduction in organisms', 'Biological processes for producing offspring.', 'https://www.youtube.com/embed/jt_wm0PuzSQ', 'Academics'),
                ('Ecology and ecosystems', 'Interactions between organisms and their environment.', 'https://www.youtube.com/embed/srpl5YRw-_U', 'Academics')
            ]
        }

        # --- Physics Topics ---
        physics_topics = {
            'en': [
                ('Motion and force', 'Newton’s laws and the relationship between mass and acceleration.', 'https://www.youtube.com/embed/g550H4e5FCY', 'Academics'),
                ('Energy and work', 'Kinetic and potential energy, and the principle of conservation.', 'https://www.youtube.com/embed/_MR1Dp8-F8w', 'Academics'),
                ('Waves and sound', 'Properties of mechanical waves and the physics of acoustics.', 'https://www.youtube.com/embed/XY0RJu4sDHk', 'Academics'),
                ('Electricity and circuits', 'Current, voltage, resistance, and circuit diagrams.', 'https://www.youtube.com/embed/m4jzgqZu-4s', 'Academics'),
                ('Heat and temperature', 'Thermodynamics and thermal properties of matter.', 'https://www.youtube.com/embed/f1eAOygDP5s', 'Academics')
            ]
        }

        # --- Chemistry Topics ---
        chemistry_topics = {
            'en': [
                ('Atomic structure', 'Components of atoms and electronic configuration.', 'https://www.youtube.com/embed/OH-aSu-rWgk', 'Academics'),
                ('Periodic table and elements', 'Classification and properties of chemical elements.', 'https://www.youtube.com/embed/0RRVV4Diomg', 'Academics'),
                ('Chemical bonding', 'Ionic, covalent, and metallic bonds.', 'https://www.youtube.com/embed/7DjsD7Hcd9U', 'Academics'),
                ('Acids, bases, and salts', 'pH scales, neutralization, and salt formation.', 'https://www.youtube.com/embed/ANi709MYnWg', 'Academics'),
                ('Chemical reactions and equations', 'Balancing equations and types of reactions.', 'https://www.youtube.com/embed/Hxd1TNgSuPg', 'Academics')
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

            # Seed Vocational (if needed, keeping it minimal)
            voc_topics = [
                ('Digital Literacy', 'Basic computer skills.', '', 'Vocational'),
                ('Graphic Design', 'Introduction to visual communication.', '', 'Vocational')
            ]
            for title, content, url, level in voc_topics:
                db.session.add(LearningMaterial(title=title, content=content, resource_url=url, subject='Vocational', language=lang, material_type='video_link', education_level=level))
                topic = Topic(name=title, subject='Vocational', education_level=level)
                db.session.add(topic); db.session.flush()
                db.session.add(TopicVideo(topic_id=topic.id, video_url=url, video_title=title))

        # --- Flashcards (50 per subject) ---
        flashcards_data = [
            # Mathematics
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

            # English
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

            # Biology
            ('Osmosis', 'Movement of water molecules across a semi-permeable membrane.', 'Biology'),
            ('Diffusion', 'Movement of particles from high to low concentration.', 'Biology'),
            ('Mitosis', 'Cell division resulting in two identical daughter cells.', 'Biology'),
            ('Meiosis', 'Cell division resulting in four genetically distinct gametes.', 'Biology'),
            ('Photosynthesis', 'Process of converting light energy into chemical energy.', 'Biology'),
            ('Respiration', 'Process of releasing energy from glucose in cells.', 'Biology'),
            ('Enzyme', 'A biological catalyst that speeds up reactions.', 'Biology'),
            ('DNA', 'Deoxyribonucleic acid, the carrier of genetic information.', 'Biology'),
            ('Gene', 'A segment of DNA that codes for a specific protein.', 'Biology'),
            ('Chromosomes', 'Thread-like structures made of DNA and proteins.', 'Biology'),
            ('Refractory Period', 'Short rest time after a nerve impulse or contraction.', 'Biology'),
            ('Homeostasis', 'Maintenance of a stable internal environment.', 'Biology'),
            ('Organelle', 'Specialized structure within a cell (e.g. Mitochondria).', 'Biology'),
            ('Ribosome', 'Site of protein synthesis.', 'Biology'),
            ('Lysosome', 'Contains digestive enzymes to break down waste.', 'Biology'),
            ('Vacuole', 'Storage sac for water, nutrients, or waste.', 'Biology'),
            ('Cytoplasm', 'Jelly-like substance filling the cell.', 'Biology'),
            ('Cell Membrane', 'Semi-permeable outer layer of a cell.', 'Biology'),
            ('Cell Wall', 'Rigid outer layer found in plant cells.', 'Biology'),
            ('Nucleus', 'Control center of the cell containing DNA.', 'Biology'),
            ('RNA', 'Molecule that translates DNA into proteins.', 'Biology'),
            ('ATP', 'Primary energy carrier in cells.', 'Biology'),
            ('Glucose', 'A simple sugar used for energy.', 'Biology'),
            ('Substrate', 'Reactant upon which an enzyme acts.', 'Biology'),
            ('Hormone', 'Chemical messenger in the body.', 'Biology'),
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
            ('Taxonomy', 'Science of classifying organisms.', 'Biology'),

            # Physics
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

            # Chemistry
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
            ('Saturated Solution', 'Contains max dissolved solute.', 'Chemistry')
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
            for sub in ['Mathematics', 'English', 'Biology', 'Physics', 'Chemistry']:
                asm = AssessmentTemplate(title=f"{sub} Mastery Test ({lang.upper()})", subject=sub, time_limit=15)
                db.session.add(asm)
                db.session.flush()
                if sub == 'Mathematics':
                    db.session.add_all([
                        Question(assessment_id=asm.id, text='Solve for x: 2x + 5 = 15', option_a='2', option_b='5', option_c='10', option_d='7', correct_option='B'),
                        Question(assessment_id=asm.id, text='What is the square root of 144?', option_a='12', option_b='14', option_c='10', option_d='16', correct_option='A')
                    ])

        # Past Questions Seeding (50 per subject)
        print("Seeding Past Questions (50 per subject)...")
        pq_templates = {
            'Mathematics': [
                ("Solve for x: {a}x + {b} = {c}", "{res}", ["{res}", "{res1}", "{res2}", "{res3}"], "Algebra"),
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

        import random
        for sub in ['Mathematics', 'English', 'Biology', 'Physics', 'Chemistry']:
            for i in range(50):
                tpl_data = random.choice(pq_templates[sub])
                tpl, ans_tpl, opts_tpl, topic = tpl_data
                a, b = random.randint(1, 20), random.randint(1, 20)
                a_sq, c = a*a, a*random.randint(2, 5)+b
                
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
                    res_type = "Acidic" if a < 7 else ("Basic" if a > 7 else "Neutral")
                    res = a + b
                else: res = a

                text = tpl.format(a=a, b=b, c=c, a_sq=a_sq, res=res, res_sq=res, res_type=res_type if 'res_type' in locals() else '')
                correct_val = ans_tpl.format(res=res, a=a, res_sq=res, res_type=res_type if 'res_type' in locals() else '')
                
                final_options = list(set([o_tpl.format(res=res, a=a, a1=a+1, a2=a+2, a3=a+3, res1=res+5, res2=res-2, res3=res*2, res_sq=res) for o_tpl in opts_tpl]))
                while len(final_options) < 4: final_options.append(f"Option {len(final_options) + 1}")
                random.shuffle(final_options)
                correct_letter = chr(65 + final_options.index(correct_val))

                for lang in languages:
                    db.session.add(PastQuestion(
                        subject=sub, year=random.randint(2015, 2024), topic=topic,
                        question_text=text, option_a=final_options[0], option_b=final_options[1],
                        option_c=final_options[2], option_d=final_options[3],
                        correct_answer=correct_letter, explanation=f"Standard {sub} principles apply.",
                        language=lang, education_level='Academics'
                    ))

        db.session.commit()
        print("Database seeded with core curriculum successfully!")

if __name__ == '__main__':
    seed_data()
