from bs4 import BeautifulSoup

class HeroesParser:
    def parse_heroes_tab(self, html, season, rank):
        soup = BeautifulSoup(html, "html.parser")
        heroes_data = []

        for row in soup.select("table tbody tr"):
            columns = row.find_all("td")
            if len(columns) >= 7:
                name = columns[0].text.strip()
                tier = columns[1].text.strip()
                win_rate = columns[2].text.strip()
                wr_change = columns[3].text.strip()
                pick_rate = columns[4].text.strip()
                pr_change = columns[5].text.strip()
                ban_rate = columns[6].text.strip()
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

        # Debugging: Print the number of rows found in the table
        rows = soup.select("table tbody tr")
        print(f"Found {len(rows)} team-up rows")

        for row in rows:
            columns = row.find_all("td")
            
            # Ensure there are enough columns for the expected data (at least 4)
            if len(columns) >= 4:
                heroes = [img["alt"].strip() for img in row.select(".heroes_teamups img")]
                
                # Debugging: Print the heroes being extracted
                print(f"Heroes: {heroes}")

                # If no heroes found, continue to the next row
                if not heroes:
                    print("No heroes found in this row, skipping.")
                    continue
                
                # Extract data for the team-up
                team = ", ".join(heroes)
                tier = columns[1].text.strip()
                win_rate = columns[2].text.strip()
                pick_rate = columns[3].text.strip()
                matches = columns[4].text.strip()

                # Debugging: Check the extracted data before adding to list
                print(f"Team: {team}, Tier: {tier}, Win Rate: {win_rate}, Pick Rate: {pick_rate}, Matches: {matches}")

                # Ensure data isn't blank or malformed
                if team and tier and win_rate and pick_rate and matches:
                    teamups_data.append([team, tier, win_rate, pick_rate, matches, rank, season])
                else:
                    print(f"Skipping row with incomplete data: {row}")

        # Debugging: Check how many valid team-ups were found
        print(f"Found {len(teamups_data)} valid team-ups")
        return teamups_data