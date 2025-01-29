from scraper.fetcher import HTMLFetcher
from scraper.parser import HeroesParser
from scraper.parser import TeamUpParser
from scraper.parser import TeamCompParser
from scraper.saver import CSVWriter

from scraper.parser import TeamCompParser  # Import the new parser

# Add TeamCompParser to the function
def main():
    url_heroes = "https://rivalstracker.com/heroes"
    url_team_comps = "https://rivalstracker.com/team-comps"  # URL for Team Comps
    seasons = ["season0", "1"]
    ranks = ["All Ranks", "Bronze", "Silver", "Gold", "Platinum", "Diamond", "Grandmaster", "Celestial", "Eternity", "One Above All"]

    all_heroes_data = []
    all_teamups_data = []
    all_team_comps_data = []  # To store Team Comp data

    fetcher = HTMLFetcher()
    heroes_parser = HeroesParser()
    teamup_parser = TeamUpParser()
    teamcomp_parser = TeamCompParser()  # Initialize the TeamCompParser

    for season in seasons:
        for rank in ranks:
            print(f"Scraping data for Season: {season}, Rank: {rank}")
            html_heroes = fetcher.fetch_html(url_heroes, season, rank)
            html_team_comps = fetcher.fetch_html(url_team_comps, season, rank)

            # Parsing Hero Data
            heroes = heroes_parser.parse_heroes_tab(html_heroes, season, rank)
            all_heroes_data.extend(heroes)

            # Parsing Team-Ups Data
            teamups = teamup_parser.parse_teamups_tab(html_heroes, season, rank)
            all_teamups_data.extend(teamups)

            # Parsing Team Comps Data
            team_comps = teamcomp_parser.parse_team_comps(html_team_comps, rank)
            all_team_comps_data.extend(team_comps)

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

    # Saving Team Comps Data
    csv_writer.save_to_csv(
        "team_comps_data_all_seasons_ranks.csv",
        all_team_comps_data,
        ["Team Comp", "Win Rate", "Pick Rate", "Matches", "Rank"],
    )
    print("Team Comps data saved!")

if __name__ == "__main__":
    main()
	