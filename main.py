from scraper.fetcher import HTMLFetcher
from scraper.parser import HeroesParser
from scraper.parser import TeamUpParser
from scraper.saver import CSVWriter

def main():
    url = "https://rivalstracker.com/heroes"
    seasons = ["season0", "1"]
    ranks = ["All Ranks", "Bronze", "Silver", "Gold", "Platinum", "Diamond", "Grandmaster", "Celestial", "Eternity", "One Above All"]

    all_heroes_data = []
    all_teamups_data = []

    fetcher = HTMLFetcher()  # Instance of HTMLFetcher
    heroes_parser = HeroesParser()  # Instance of HeroesParser
    teamup_parser = TeamUpParser()# Instance of TeamUpParser

    for season in seasons:
        for rank in ranks:
            print(f"Scraping data for Season: {season}, Rank: {rank}")
            html = fetcher.fetch_html(url, season, rank)

            # Parsing Hero Data
            heroes = heroes_parser.parse_heroes_tab(html, season, rank)
            all_heroes_data.extend(heroes)

            # Parsing Team-Ups Data
            teamups = teamup_parser.parse_teamups_tab(html, season, rank)
            all_teamups_data.extend(teamups)

    csv_writer = CSVWriter()

    # Saving Heroes Data
    csv_writer.save_to_csv(
        "heroes_data_all_seasons_ranks.csv",
        all_heroes_data,
        ["Hero", "Tier", "Win Rate", "WR Change", "Pick Rate", "PR Change", "Ban Rate", "Matches", "Rank", "Season"],
    )
    print("Heroes data saved!")

    # Saving Team-Ups Data
    csv_writer.save_to_csv(
        "teamups_data_all_seasons_ranks.csv",
        all_teamups_data,
        ["Team", "Tier", "Win Rate", "Pick Rate", "Matches", "Rank", "Season"],
    )
    print("Team-Ups data saved!")

if __name__ == "__main__":
    main()