from app import create_app, db
from app.models.flashcard import Flashcard

def seed_flashcards():
    app = create_app('development')
    with app.app_context():
        languages = ['en', 'ha', 'yo', 'ig', 'pi']
        
        # Math Flashcards (50)
        math_flash = [
            ('Algebraic Expression', 'A mathematical phrase that contains numbers, variables, and operators.'),
            ('Hypotenuse', 'The longest side of a right-angled triangle, opposite the right angle.'),
            ('Quadratic Equation', 'An equation where the highest power of the variable is two (x^2).'),
            ('Mean', 'The average of a set of numbers.'),
            ('Median', 'The middle value in a list of numbers ordered from least to greatest.'),
            ('Mode', 'The number that appears most frequently in a data set.'),
            ('Integer', 'A whole number that can be positive, negative, or zero.'),
            ('Prime Number', 'A number greater than 1 with only two factors: 1 and itself.'),
            ('Factorial', 'The product of all positive integers up to a given number (n!).'),
            ('Circumference', 'The distance around the outside of a circle (2*π*r).'),
            ('Diameter', 'A straight line passing from side to side through the center of a circle.'),
            ('Isosceles Triangle', 'A triangle with at least two equal sides.'),
            ('Equilateral Triangle', 'A triangle where all three sides are equal.'),
            ('Scalene Triangle', 'A triangle where all three sides have different lengths.'),
            ('Parallel Lines', 'Two lines that never meet, no matter how long they are drawn.'),
            ('Perpendicular Lines', 'Lines that meet at a 90-degree angle.'),
            ('Numerator', 'The top number in a fraction.'),
            ('Denominator', 'The bottom number in a fraction.'),
            ('Ratio', 'A comparison of two quantities by division.'),
            ('Percentage', 'A number or ratio expressed as a fraction of 100.'),
            ('Probability', 'The likelihood of a specific event occurring.'),
            ('Square Root', 'A value that, when multiplied by itself, gives the original number.'),
            ('Exponent', 'The number of times a base is multiplied by itself.'),
            ('Variable', 'A symbol (usually a letter) representing an unknown value.'),
            ('Coefficient', 'A number multiplied by a variable.'),
            ('Polygon', 'A closed 2D shape with straight sides.'),
            ('Hexagon', 'A polygon with six sides.'),
            ('Decagon', 'A polygon with ten sides.'),
            ('Obtuse Angle', 'An angle between 90 and 180 degrees.'),
            ('Acute Angle', 'An angle less than 90 degrees.'),
            ('Reflex Angle', 'An angle between 180 and 360 degrees.'),
            ('Pythagoras Theorem', 'a^2 + b^2 = c^2 for right-angled triangles.'),
            ('Area of Circle', 'π multiplied by the radius squared (πr^2).'),
            ('Volume of Cylinder', 'πr^2 multiplied by the height (h).'),
            ('Tangent', 'A line that touches a circle at exactly one point.'),
            ('Translation', 'Moving a shape without rotating or resizing it.'),
            ('Rotation', 'Turning a shape around a fixed center point.'),
            ('Reflection', 'Flipping a shape over a line like a mirror.'),
            ('Congruent', 'Exactly equal in size and shape.'),
            ('Similar', 'Same shape but different size.'),
            ('Derivative', 'The rate of change of a function with respect to a variable.'),
            ('Integral', 'The area under a curve in calculus.'),
            ('Matrix', 'A rectangular array of numbers arranged in rows and columns.'),
            ('Vector', 'A quantity having both magnitude and direction.'),
            ('Sine (sin)', 'Ratio of opposite side over hypotenuse.'),
            ('Cosine (cos)', 'Ratio of adjacent side over hypotenuse.'),
            ('Tangent (tan)', 'Ratio of opposite side over adjacent side.'),
            ('Binary System', 'A base-2 number system using only 0 and 1.'),
            ('HCF', 'Highest Common Factor of two or more numbers.'),
            ('LCM', 'Lowest Common Multiple of two or more numbers.')
        ]

        # English Flashcards (50)
        eng_flash = [
            ('Noun', 'A word that represents a person, place, thing, or idea.'),
            ('Verb', 'A word that expresses an action or state of being.'),
            ('Adjective', 'A word that describes or modifies a noun.'),
            ('Adverb', 'A word that modifies a verb, adjective, or another adverb.'),
            ('Pronoun', 'A word used in place of a noun (e.g., He, She, They).'),
            ('Preposition', 'A word showing the relationship of a noun to another word.'),
            ('Conjunction', 'A word used to connect words or sentences (e.g., and, but).'),
            ('Interjection', 'A word or phrase used to express strong emotion.'),
            ('Simile', 'A comparison using "like" or "as".'),
            ('Metaphor', 'A direct comparison without using "like" or "as".'),
            ('Personification', 'Giving human qualities to non-human things.'),
            ('Hyperbole', 'An extreme exaggeration used for emphasis.'),
            ('Alliteration', 'The repetition of initial consonant sounds.'),
            ('Onomatopoeia', 'Words that sound like the noise they describe.'),
            ('Oxymoron', 'A phrase combining two contradictory terms (e.g., jumbo shrimp).'),
            ('Pun', 'A joke exploring different meanings of a word.'),
            ('Irony', 'When the opposite of what is expected happens.'),
            ('Synonym', 'A word that means the same as another word.'),
            ('Antonym', 'A word that means the opposite of another word.'),
            ('Homophone', 'Words that sound the same but have different meanings and spellings.'),
            ('Subject', 'The person or thing that is doing the action in a sentence.'),
            ('Object', 'The person or thing receiving the action.'),
            ('Clause', 'A group of words containing a subject and a verb.'),
            ('Phrase', 'A group of words without both a subject and a verb.'),
            ('Suffix', 'A letter or group of letters added to the end of a word.'),
            ('Prefix', 'A letter or group of letters added to the beginning of a word.'),
            ('Tense', 'The time when an action takes place (Past, Present, Future).'),
            ('Active Voice', 'When the subject performs the action.'),
            ('Passive Voice', 'When the subject receives the action.'),
            ('Gerund', 'A verb ending in "-ing" that acts as a noun.'),
            ('Infinitive', 'The base form of a verb preceded by "to".'),
            ('Dialogue', 'A conversation between two or more characters.'),
            ('Monologue', 'A long speech by a single character.'),
            ('Protagonist', 'The main character in a story.'),
            ('Antagonist', 'The character or force in conflict with the hero.'),
            ('Climax', 'The most intense or important point of a story.'),
            ('Foreshadowing', 'Hints about what will happen later in the story.'),
            ('Flashback', 'A scene that interrupts the present to show past events.'),
            ('Setting', 'The time and place where a story occurs.'),
            ('Theme', 'The central message or meaning of a literary work.'),
            ('Plagiarism', 'Taking someone else\'s work or ideas as your own.'),
            ('Bibliography', 'A list of sources used in a research paper.'),
            ('Context Clues', 'Hints in a sentence that help you find a word\'s meaning.'),
            ('Inference', 'A conclusion reached based on evidence and reasoning.'),
            ('Expository Writing', 'Writing that explains or informs.'),
            ('Persuasive Writing', 'Writing intended to convince the reader.'),
            ('Narrative Writing', 'Writing that tells a story.'),
            ('Etymology', 'The study of the origin of words.'),
            ('Idiom', 'An expression whose meaning is not literal.'),
            ('Paradox', 'A statement that seems contradictory but may be true.')
        ]

        # Science Flashcards (50)
        sci_flash = [
            ('Photosynthesis', 'The process by which plants use sunlight to make food.'),
            ('Atmosphere', 'The layer of gases surrounding the Earth.'),
            ('Atom', 'The smallest unit of a chemical element.'),
            ('Electron', 'A negatively charged subatomic particle.'),
            ('Proton', 'A positively charged particle found in the nucleus.'),
            ('Neutron', 'A particle with no charge found in the nucleus.'),
            ('Element', 'A substance made of only one type of atom.'),
            ('Compound', 'A substance formed by two or more elements.'),
            ('Molecule', 'Two or more atoms bonded together.'),
            ('Solid', 'A state of matter with fixed shape and volume.'),
            ('Liquid', 'A state of matter with fixed volume but no fixed shape.'),
            ('Gas', 'A state of matter with no fixed shape or volume.'),
            ('Plasma', 'A hot, ionized gas state of matter.'),
            ('Gravity', 'The force that pulls objects toward each other.'),
            ('Friction', 'A force that resists motion between surfaces.'),
            ('Energy', 'The ability to do work.'),
            ('Kinetic Energy', 'The energy of a moving object.'),
            ('Potential Energy', 'Stored energy based on position.'),
            ('Refraction', 'The bending of light as it passes through different media.'),
            ('Reflection', 'Light bouncing off a surface.'),
            ('Conduction', 'Heat transfer through direct contact.'),
            ('Convection', 'Heat transfer through fluid movement.'),
            ('Radiation', 'Energy transfer through electromagnetic waves.'),
            ('Cell', 'The basic unit of life.'),
            ('Nucleus', 'The control center of a cell containing DNA.'),
            ('Mitochondria', 'The powerhouse of the cell producing energy.'),
            ('Chlorophyll', 'The green pigment in plants used for photosynthesis.'),
            ('Metamorphosis', 'A biological process of transformation in animals.'),
            ('DNA', 'The molecule that carries genetic information.'),
            ('Habitat', 'The natural home or environment of an organism.'),
            ('Ecosystem', 'A community of living and non-living things.'),
            ('Pollination', 'Transfer of pollen from male to female plant parts.'),
            ('Evaporation', 'Change of liquid into gas due to heat.'),
            ('Condensation', 'Change of gas into liquid due to cooling.'),
            ('Precipitation', 'Water falling from clouds (rain, snow, etc.).'),
            ('Tectonics', 'Large-scale movements of the Earth\'s crust.'),
            ('Eclipse', 'Obscuring of light from one celestial body by another.'),
            ('Galaxy', 'A massive system of stars, gas, and dust.'),
            ('Inertia', 'An object\'s resistance to change in motion.'),
            ('Velocity', 'Speed in a specific direction.'),
            ('Acids', 'Substances with a pH less than 7.'),
            ('Bases', 'Substances with a pH greater than 7.'),
            ('Neutral', 'A substance with a pH of exactly 7 (e.g., pure water).'),
            ('Insulator', 'A material that resists the flow of electricity.'),
            ('Conductor', 'A material that allows electricity to flow easily.'),
            ('Ohm\'s Law', 'V = I * R (Voltage = Current * Resistance).'),
            ('Circuit', 'A complete path for electrical current.'),
            ('Magnetism', 'The force exerted by magnets when they attract or repel.'),
            ('Volume', 'The amount of space an object occupies.'),
            ('Density', 'Mass divided by volume (M/V).')
        ]

        # Bulk Insert
        for lang in languages:
            map_data = [
                ('Mathematics', math_flash),
                ('English', eng_flash),
                ('Science', sci_flash)
            ]
            
            for subject, pool in map_data:
                for front, back in pool:
                    db.session.add(Flashcard(
                        subject=subject,
                        front=front,
                        back=back,
                        language=lang,
                        user_id=1 # Shared for all
                    ))
        
        db.session.commit()
        print(f"Bulk seeded 150 unique flashcards for all {len(languages)} languages (Total: 750 cards).")

if __name__ == '__main__':
    seed_flashcards()
