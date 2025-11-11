from src.scrapper import LinkedInScapper

scrapper = LinkedInScapper()

results = scrapper.scrape(["https://www.linkedin.com/in/bushranazir333/"])

print(results)
