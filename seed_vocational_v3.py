from app import create_app, db
from app.models.learning import VocationalContent

def seed_vocational_v3():
    app = create_app('development')
    with app.app_context():
        # Clear existing to avoid duplicates if preferred, or just add new
        # We will just add more variety
        
        new_skills = [
            # Technology
            {
                "title": "Solar Energy Installation",
                "description": "Learn how to design and install solar power systems for homes and businesses. Covering panels, inverters, and battery storage.",
                "category": "Technology",
                "language": "en",
                "resource_url": "https://www.youtube.com/embed/jj17UHQrcFY"
            },
            {
                "title": "Graphic Design & Branding",
                "description": "Master the art of visual communication. Learn logo design, typography, and color theory using professional tools.",
                "category": "Technology",
                "language": "en",
                "resource_url": "https://www.youtube.com/embed/GQS7wPujL2k"
            },
            
            # Construction / Engineering
            {
                "title": "Modern Plumbing & Piping",
                "description": "Learn professional plumbing techniques for modern residential buildings, including drainage systems and water supply.",
                "category": "Construction",
                "language": "en",
                "resource_url": "https://www.youtube.com/embed/bbqZ12QhoY4"
            },
            {
                "title": "Mobile Phone Repair",
                "description": "Comprehensive guide to diagnosing and fixing hardware and software issues in modern smartphones.",
                "category": "Technology",
                "language": "en",
                "resource_url": "https://www.youtube.com/embed/4NPbLi6OOCY"
            },
            
            # Fashion
            {
                "title": "Advanced Fashion Tailoring",
                "description": "Take your tailoring skills to the next level with advanced cutting and sewing techniques for professional outfits.",
                "category": "Fashion",
                "language": "en",
                "resource_url": "https://www.youtube.com/embed/Njv1-GBMXt4"
            },
            
            # Culinary
            {
                "title": "Professional Pastry & Baking",
                "description": "Master the art of baking. Learn to make professional-grade pastries, cakes, and bread.",
                "category": "Culinary",
                "language": "en",
                "resource_url": "https://www.youtube.com/embed/wLtVgLt7dBA"
            }
        ]

        for s_data in new_skills:
            # Check if already exists to avoid duplicates
            exists = VocationalContent.query.filter_by(title=s_data["title"], language=s_data["language"]).first()
            if not exists:
                skill = VocationalContent(**s_data)
                db.session.add(skill)
                print(f"Added: {s_data['title']}")
            else:
                print(f"Skipped (exists): {s_data['title']}")
        
        db.session.commit()
        print("Vocational V3 Seeding Complete.")

if __name__ == '__main__':
    seed_vocational_v3()
