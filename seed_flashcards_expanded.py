from app import create_app, db
from app.models.flashcard import Flashcard

def seed_more_flashcards():
    app = create_app('development')
    with app.app_context():
        languages = ['en', 'ha', 'yo', 'ig', 'pi']
        
        # Comprehensive Flashcard Data
        math_cards = [
            ('Polynomial', 'An expression consisting of variables and coefficients.'),
            ('Quadratic Formula', 'x = [-b ± √(b² - 4ac)] / 2a'),
            ('Pythagorean Theorem', 'a² + b² = c² for right-angled triangles.'),
            ('Cosine Rule', 'a² = b² + c² - 2bc cos A'),
            ('Sine Rule', 'a / sin A = b / sin B = c / sin C'),
            ('Differentiation', 'Process of finding the rate of change (derivative).'),
            ('Integration', 'Process of finding the area under a curve (anti-derivative).'),
            ('Logarithm', 'The power to which a base must be raised to produce a given number.'),
            ('Mean', 'The average of a set of numbers.'),
            ('Median', 'The middle value in a sorted list of numbers.'),
            ('Mode', 'The number that occurs most frequently in a set.'),
            ('Standard Deviation', 'Measure of the amount of variation or dispersion.'),
            ('Probability', 'The likelihood of an event occurring (ranges 0 to 1).'),
            ('Circle Circumference', 'C = 2πr'),
            ('Area of a Circle', 'A = πr²'),
            ('Volume of a Sphere', 'V = (4/3)πr³'),
            ('Hypotenuse', 'The longest side of a right-angled triangle.'),
            ('Isosceles Triangle', 'A triangle with two equal sides and angles.'),
            ('Equilateral Triangle', 'A triangle with all sides and angles equal (60°).'),
            ('Tangent', 'A line that touches a circle at exactly one point.'),
            ('Chord', 'A line segment connecting two points on a circle.'),
            ('Diameter', 'A chord that passes through the center of a circle.'),
            ('Prime Number', 'A number divisible only by 1 and itself.'),
            ('Factorial', 'The product of all positive integers up to a number (n!).'),
            ('Matrix', 'A rectangular array of numbers arranged in rows and columns.'),
            ('Vector', 'A quantity having both magnitude and direction.'),
            ('Scalar', 'A quantity having only magnitude, not direction.'),
            ('Simultaneous Equations', 'A set of equations with shared variables solved together.'),
            ('Indices', 'The power or exponent of a number.'),
            ('Sequence', 'An ordered list of numbers following a specific pattern.'),
            ('Arithmetic Progression', 'A sequence where differences between terms are constant.'),
            ('Geometric Progression', 'A sequence where each term is multiplied by a constant.'),
            ('Permutation', 'An arrangement of objects in a specific order.'),
            ('Combination', 'A selection of objects where order does not matter.'),
            ('Percentage', 'A number expressed as a fraction of 100.'),
            ('Ratio', 'A comparison of two quantities by division.'),
            ('Proportion', 'An equation stating that two ratios are equal.'),
            ('Absolute Value', 'The distance of a number from zero, regardless of sign.'),
            ('Variable', 'A symbol representing an unknown value.'),
            ('Coefficient', 'A number used to multiply a variable.'),
            ('Constant', 'A fixed value that does not change.'),
            ('Inequality', 'A mathematical statement using <, >, or ≠.'),
            ('Factorization', 'Breaking down an expression into products of its factors.'),
            ('Gradient', 'The slope of a line (rise over run).'),
            ('Intercept', 'Point where a graph crosses an axis.'),
            ('Parabola', 'The U-shaped curve of a quadratic function.'),
            ('Ellipse', 'An elongated circle-like shape.'),
            ('Asymptote', 'A line that a curve approaches but never touches.'),
            ('Complex Number', 'A number in the form a + bi.'),
            ('Infinity', 'A concept representing something without bound or end.')
        ]

        science_cards = [
            ('Osmosis', 'Movement of water molecules across a semi-permeable membrane.'),
            ('Diffusion', 'Movement of particles from high to low concentration.'),
            ('Mitosis', 'Cell division resulting in two identical daughter cells.'),
            ('Meiosis', 'Cell division resulting in four genetically distinct gametes.'),
            ('Photosynthesis', 'Process of converting light energy into chemical energy.'),
            ('Respiration', 'Process of releasing energy from glucose in cells.'),
            ('Enzyme', 'A biological catalyst that speeds up reactions.'),
            ('DNA', 'Deoxyribonucleic acid, the carrier of genetic information.'),
            ('Gene', 'A segment of DNA that codes for a specific protein.'),
            ('Chromosomes', 'Thread-like structures made of DNA and proteins.'),
            ('Refractory Period', 'Short rest time after a nerve impulse or contraction.'),
            ('Homeostasis', 'Maintenance of a stable internal environment.'),
            ('Newton\'s First Law', 'An object at rest stays at rest unless acted upon.'),
            ('Newton\'s Second Law', 'Force equals mass times acceleration (F=ma).'),
            ('Newton\'s Third Law', 'For every action, there is an equal and opposite reaction.'),
            ('Kinetic Energy', 'The energy an object possesses due to its motion.'),
            ('Potential Energy', 'Stored energy based on an object\'s position.'),
            ('Velocity', 'Speed in a specific direction.'),
            ('Acceleration', 'The rate of change of velocity over time.'),
            ('Momentum', 'The product of an object\'s mass and velocity.'),
            ('Gravity', 'The force that pulls objects toward each other.'),
            ('Electrolysis', 'Breaking down of a substance using electricity.'),
            ('Atom', 'The smallest unit of matter retaining chemical properties.'),
            ('Proton', 'Positively charged particle in the nucleus.'),
            ('Neutron', 'Neutral particle in the nucleus.'),
            ('Electron', 'Negatively charged particle orbiting the nucleus.'),
            ('Atomic Number', 'The number of protons in an atom.'),
            ('Mass Number', 'The total number of protons and neutrons in an atom.'),
            ('Isotope', 'Atoms of the same element with different neutron counts.'),
            ('Valency', 'The combining power of an element.'),
            ('Ionic Bond', 'Bond formed by the transfer of electrons.'),
            ('Covalent Bond', 'Bond formed by the sharing of electrons.'),
            ('Metallic Bond', 'Bond formed by the attraction of metal ions to electrons.'),
            ('pH Scale', 'Measures how acidic or basic a substance is (0-14).'),
            ('Acid', 'A substance that releases hydrogen ions in water (low pH).'),
            ('Base', 'A substance that releases hydroxide ions (high pH).'),
            ('Exothermic', 'A reaction that releases heat to its surroundings.'),
            ('Endothermic', 'A reaction that absorbs heat from its surroundings.'),
            ('Redox Reaction', 'A reaction involving both reduction and oxidation.'),
            ('Catalyst', 'A substance that increases reaction rate without being consumed.'),
            ('Combustion', 'A chemical reaction involving fuel and oxygen (burning).'),
            ('Polymerization', 'Process of joining small molecules into large chains.'),
            ('Hard Water', 'Water containing high levels of calcium and magnesium.'),
            ('Distillation', 'Purifying a liquid by heating and cooling.'),
            ('Corrosion', 'Gradual destruction of metals by chemical reaction.'),
            ('Magnetism', 'Force of attraction or repulsion by magnets.'),
            ('Wave Frequency', 'Number of waves passing a point per second (Hertz).'),
            ('Amplitude', 'The maximum displacement of a wave.'),
            ('Reflection', 'Bouncing back of waves from a surface.'),
            ('Refraction', 'Bending of waves as they enter a different medium.')
        ]

        english_cards = [
            ('Simile', 'Comparison using "like" or "as".'),
            ('Metaphor', 'Direct comparison without using "like" or "as".'),
            ('Personification', 'Giving human qualities to non-human objects.'),
            ('Onomatopoeia', 'Words that imitate sounds (e.g., "buzz", "bang").'),
            ('Alliteration', 'Repetition of initial consonant sounds.'),
            ('Hyperbole', 'Exaggerated statements not meant to be taken literally.'),
            ('Irony', 'Contrast between expectation and reality.'),
            ('Satire', 'Use of humor or riducule to critisize stupidity.'),
            ('Paradox', 'A self-contradictory statement that reveals a truth.'),
            ('Oxymoron', 'Two contradictory terms used together (e.g., "bittersweet").'),
            ('Pun', 'A joke exploiting different meanings of a word.'),
            ('Allegory', 'A story with hidden symbolic meaning.'),
            ('Euphemism', 'A mild word used to replace something harsh.'),
            ('Cliche', 'A phrase that is overused and lacks original thought.'),
            ('Protagonist', 'The main character in a story.'),
            ('Antagonist', 'The character opposing the main character.'),
            ('Foreshadowing', 'Hints given about future events in a story.'),
            ('Climax', 'The most intense part of a plot.'),
            ('Resolution', 'The end of a story where problems are solved.'),
            ('Tone', 'The author\'s attitude toward the subject.'),
            ('Mood', 'The atmosphere or feeling created for the reader.'),
            ('Point of View', 'The perspective from which a story is told.'),
            ('Noun', 'A word representing a person, place, or thing.'),
            ('Verb', 'A word expressing an action or state of being.'),
            ('Adjective', 'A word that describes or modifies a noun.'),
            ('Adverb', 'A word that modifies a verb, adjective, or adverb.'),
            ('Pronoun', 'A word used in place of a noun.'),
            ('Preposition', 'Shows show relationship between a noun and another word.'),
            ('Conjunction', 'A word used to connect sentences or clauses.'),
            ('Interjection', 'A word used to express sudden emotion.'),
            ('Synonym', 'Words with similar meanings.'),
            ('Antonym', 'Words with opposite meanings.'),
            ('Homophone', 'Words that sound same but have different meanings.'),
            ('Clause', 'A group of words containing a subject and a verb.'),
            ('Phrase', 'A group of words without a subject-verb unit.'),
            ('Active Voice', 'When the subject performs the action.'),
            ('Passive Voice', 'When the action is performed on the subject.'),
            ('Idiom', 'An expression whose meaning is not literal.'),
            ('Prefix', 'A group of letters added to the start of a word.'),
            ('Suffix', 'A group of letters added to the end of a word.'),
            ('Root Word', 'The core part of a word to which affixes are added.'),
            ('Main Idea', 'The most important point in a text.'),
            ('Context Clues', 'Information in a text that helps define a word.'),
            ('Dialogue', 'Conversation between characters.'),
            ('Monologue', 'A long speech by a single character.'),
            ('Setting', 'The time and place of a story.'),
            ('Theme', 'The central underlying message of a work.'),
            ('Genre', 'A category or type of literature.'),
            ('First Person', 'Story told using "I" or "we".'),
            ('Third Person', 'Story told using "he", "she", or "they".')
        ]

        # Combine all
        all_new_cards = []
        for front, back in math_cards: all_new_cards.append((front, back, 'Mathematics'))
        for front, back in science_cards: all_new_cards.append((front, back, 'Science'))
        for front, back in english_cards: all_new_cards.append((front, back, 'English'))

        # Clear existing to avoid duplicates if re-seeding
        # db.session.query(Flashcard).delete()
        
        for lang in languages:
            for front, back, subject in all_new_cards:
                db.session.add(Flashcard(front=front, back=back, subject=subject, language=lang))
        
        db.session.commit()
        print(f"Added {len(all_new_cards)} flashcards for each of the {len(languages)} languages.")

if __name__ == '__main__':
    seed_more_flashcards()
