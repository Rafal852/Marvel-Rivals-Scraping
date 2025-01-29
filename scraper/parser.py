from bs4 import BeautifulSoup
import re

def safe_float(value):
    # Handle 'N/A', strip out unwanted characters, and convert to a float
    if 'W' in value:
        value = value.split('%')[0]  # Remove the win count part after %
    return float(value.replace('%', '').replace('N/A', '0').strip()) / 100 if value not in ('N/A', '') else 0


class HeroesParser:
    def parse_heroes_tab(self, html, season, rank):
        soup = BeautifulSoup(html, "html.parser")
        heroes_data = []

        for row in soup.select("table tbody tr"):
            columns = row.find_all("td")
            if len(columns) >= 7:
                name = columns[0].text.strip()
                tier = columns[1].text.strip()
                win_rate = safe_float(columns[2].text.strip())  # Use safe_float to handle 'N/A'
                wr_change = safe_float(columns[3].text.strip())
                pick_rate = safe_float(columns[4].text.strip())
                pr_change = safe_float(columns[5].text.strip())
                ban_rate = safe_float(columns[6].text.strip())
                matches = columns[7].text.strip()

                # Add the rank and season to the data
                heroes_data.append(
                    [name, tier, win_rate, wr_change, pick_rate, pr_change, ban_rate, matches, rank, season]
                )

        return heroes_data

class TeamUpParser:
    def parse_teamups_tab(self, html, season, rank):
        soup = BeautifulSoup(html, 'html.parser')
        teamups_data = []

        rows = soup.select("table tbody tr")
        print(f"Found {len(rows)} team-up rows")

        for row in rows:
            columns = row.find_all("td")
            if len(columns) >= 4:
                heroes = [img["alt"].strip() for img in row.select(".heroes_teamups img")]

                # Skip if no heroes found
                if not heroes:
                    print("No heroes found in this row, skipping.")
                    continue
                
                # Extract data for the team-up
                team = ", ".join(heroes)
                tier = columns[1].text.strip()
                win_rate = safe_float(columns[2].text.strip())
                pick_rate = safe_float(columns[3].text.strip())
                matches = columns[4].text.strip()

                if team and tier and win_rate is not None and pick_rate is not None and matches:
                    teamups_data.append([team, tier, win_rate, pick_rate, matches, rank, season])

        print(f"Found {len(teamups_data)} valid team-ups")
        return teamups_data

class TeamCompParser:
    def parse_team_comps(self, html, rank):
        soup = BeautifulSoup(html, 'html.parser')
        team_comps_data = []

        for row in soup.select("table tbody tr"):
            columns = row.find_all("td")
            if len(columns) >= 4:
                team_comp = columns[0].text.strip()
                components = team_comp.split(", ")  # Split the team comp into components
                # Correctly extract and process win rate and pick rate
                win_rate = safe_float(columns[1].text.strip())  # Convert to float
                pick_rate = safe_float(columns[2].text.strip())  # Convert to float
                matches = columns[3].text.strip()

                if components and win_rate is not None and pick_rate is not None and matches:
                    team_comps_data.append(components + [win_rate, pick_rate, matches, rank])

        return team_comps_data

