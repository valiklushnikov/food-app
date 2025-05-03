MINIMAL = 1.2
LOW = 1.375
MODERATE = 1.55
HIGH = 1.725
HIGHEST = 1.9
ACTIVITY_LEVEL_CHOICES = [
    (MINIMAL, 'Minimal'),
    (LOW, 'Low'),
    (MODERATE, 'Moderate'),
    (HIGH, 'High'),
    (HIGHEST, 'Highest'),
]
WEIGHT_LOSS_KCAL = -400
WEIGHT_MAINTENANCE_KCAL = 0
WEIGHT_GAIN_KCAL = 400
GOAL_CHOICES = [
    (WEIGHT_LOSS_KCAL, 'Weight loss'),
    (WEIGHT_MAINTENANCE_KCAL, 'Weight maintenance'),
    (WEIGHT_GAIN_KCAL, 'Weight gain'),
]
