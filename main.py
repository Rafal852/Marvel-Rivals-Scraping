from scraper.fetcher import HTMLFetcher
from scraper.parser import HeroesParser
from scraper.parser import TeamUpParser
from scraper.parser import TeamCompParser
from scraper.saver import CSVWriter
import concurrent.futures
from scraper.parser import TeamCompParser  

def scrape_data(season, rank):
    fetcher = HTMLFetcher()
    heroes_parser = HeroesParser()
    teamup_parser = TeamUpParser()
    teamcomp_parser = TeamCompParser()

    url_heroes = "https://rivalstracker.com/heroes"
    url_team_comps = "https://rivalstracker.com/team-comps"

    print(f"Scraping Season: {season}, Rank: {rank}")

    html_heroes = fetcher.fetch_html(url_heroes, season, rank)
    html_team_comps = fetcher.fetch_html(url_team_comps, season, rank)

    heroes_data = heroes_parser.parse_heroes_tab(html_heroes, season, rank)
    teamups_data = teamup_parser.parse_teamups_tab(html_heroes, season, rank)
    team_comps_data = teamcomp_parser.parse_team_comps(html_team_comps, rank)

    return heroes_data, teamups_data, team_comps_data

def main():
    seasons = ["season0", "1"]
    ranks = ["All Ranks", "Bronze", "Silver", "Gold", "Platinum", "Diamond", "Grandmaster", "Celestial", "Eternity", "One Above All"]
    
    all_heroes_data = []
    all_teamups_data = []
    all_team_comps_data = []

    csv_writer = CSVWriter()

    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        futures = {executor.submit(scrape_data, season, rank): (season, rank) for season in seasons for rank in ranks}

        for future in concurrent.futures.as_completed(futures):
            season, rank = futures[future]
            try:
                heroes, teamups, team_comps = future.result()
                all_heroes_data.extend(heroes)
                all_teamups_data.extend(teamups)
                all_team_comps_data.extend(team_comps)
                print(f"Completed scraping Season: {season}, Rank: {rank}")
            except Exception as e:
                print(f"Error in Season: {season}, Rank: {rank}: {e}")

    csv_writer.save_to_csv(
        "heroes_data_all_seasons_ranks.csv",
        all_heroes_data,
        ["Hero", "Role", "Tier", "Win Rate", "WR Change", "Pick Rate", "PR Change", "Ban Rate", "Matches", "Rank", "Season"]
    )
    print("Heroes data saved!")

    csv_writer.save_to_csv(
        "teamups_data_all_seasons_ranks.csv",
        all_teamups_data,
        ["Team", "Tier", "Win Rate", "Pick Rate", "Matches", "Rank", "Season"]
    )
    print("Team-Ups data saved!")

    csv_writer.save_to_csv(
        "team_comps_data_all_seasons_ranks.csv",
        all_team_comps_data,
        ["Duelist", "Strategist", "Vanguard", "Win Rate", "Pick Rate", "Matches", "Rank"]
    )
    print("Team Comps data saved!")

if __name__ == "__main__":
    main()