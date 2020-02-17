import ingestor.ingestor

collected_posts = ingestor.collect_posts('NeutralPolitics', 1000)
print(collected_posts.head())

