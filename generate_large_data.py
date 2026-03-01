reviews = [
    "The product quality is excellent and I am very happy with the service.",
    "Delivery was slow and the packaging was bad.",
    "The quality is amazing and works perfectly.",
    "There was an error in billing and the support was poor.",
    "Very good experience and great customer service.",
    "Bad support and slow response from the team."
]

TOTAL_REVIEWS = 100000   
with open("data/large_text.txt", "w", encoding="utf-8") as f:
    for i in range(TOTAL_REVIEWS):
        review = reviews[i % len(reviews)]
        f.write(review + "\n")

print(f"{TOTAL_REVIEWS} reviews generated successfully!")