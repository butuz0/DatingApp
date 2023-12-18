from account.models import GroupOfInterests, Interest

INTERESTS = {
    'Sports': ['Basketball', 'Football', 'Tennis', 'Soccer', 'Volleyball',
               'Golf', 'Table Tennis', 'Badminton', 'Swimming', 'Running'],
    'Outdoor Activities': ['Hiking', 'Camping', 'Cycling', 'Skiing', 'Snowboarding',
                           'Surfing', 'Rock Climbing', 'Kayaking', 'Fishing', 'Gardening'],
    'Music': ['Playing Instruments', 'Singing', 'Listening to Pop', 'Rock Music Enthusiast',
              'Jazz Aficionado', 'Classical Music Lover', 'Electronic Dance Music (EDM)',
              'Hip-Hop and Rap Fan', 'Country Music Enthusiast', 'Indie Music Explorer'],
    'Art and Creativity': ['Painting', 'Drawing', 'Photography', 'Sculpting', 'Writing', 'Poetry',
                           'Graphic Design', 'Performing Arts', 'DIY Crafts', 'Film and Cinema'],
    'Books and Literature': ['Fiction Reader', 'Non-fiction Reader', 'Mystery and Thriller',
                             'Science Fiction and Fantasy', 'Historical Fiction', 'Poetry Enthusiast',
                             'Classic Literature', 'Self-Help Books', 'Romance Novels', 'Biography and Autobiography'],
    'Gaming': ['Video Games', 'Board Games', 'Card Games', 'Role-Playing Games (RPG)', 'Strategy Games',
               'Puzzle Games', 'Online Gaming', 'Chess', 'Billiards/Pool', 'Arcade Games'],
    'Fitness and Wellness': ['Yoga', 'Meditation', 'Weightlifting', 'CrossFit', 'Martial Arts',
                             'Pilates', 'Cycling', 'Healthy Cooking', 'Running', 'Zumba'],
    'Travel': ['Backpacking', 'Road Trips', 'Adventure Travel', 'Beach Vacation', 'Cultural Exploration',
               'Food Tourism', 'Historical Sites', 'Nature Retreats', 'City Exploration', 'Camping Trips'],
    'Technology': ['Coding/Programming', 'Tech Gadgets', 'AI and Machine Learning', 'Virtual Reality (VR)',
                   'Augmented Reality (AR)', 'Cybersecurity', 'Robotics', 'Blockchain', 'Mobile App Development',
                   'Internet of Things (IoT)'],
    'Food and Culinary Arts': ['Cooking', 'Baking', 'Food Photography', 'Fine Dining',
                               'Vegetarian/Vegan Lifestyle', 'BBQ and Grilling', 'Dessert Enthusiast',
                               'Food Blogging', 'Coffee Connoisseur', 'Wine Tasting'],
    'Lifestyle': ['Traveling', 'Adventure Seeker', 'Mindfulness Practices', 'Sustainable Living',
                  'Minimalism', 'Fitness Junkie', 'Fashion and Style', 'Socializing and Events',
                  'Pet Lover', 'Home Decor and Interior Design']
}

BACKGROUND_COLORS = ['#F19191', '#F1C17F', '#E3E559', '#AEE559', '#59E57F', '#58DCC8',
                     '#58AADC', '#5858DC', '#A058DC', '#D858DC', '#DC588C']


def fill_interests():
    for group in INTERESTS:
        g, group_created = GroupOfInterests.objects.get_or_create(name=group)
        for interest in INTERESTS[group]:
            i, interest_created = Interest.objects.get_or_create(name=interest, group=g)


def add_background_colors():
    groups = GroupOfInterests.objects.all()
    for group, color in zip(groups, BACKGROUND_COLORS):
        group.background_color = color
        group.save()
