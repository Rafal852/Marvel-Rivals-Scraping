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

                # Extract Role Icon and Map to Role Name
                role_img = row.select_one("td .role img")
                role = "Unknown"  # Default if not found
                
                if role_img and "src" in role_img.attrs:
                    src = role_img["src"]
                    print(f"Role Image Src for {name}: {src}")  # Debugging line

                    if src.startswith("data:image/png;base64,"):
                        base64_data = src.split(",")[1]  # Extract base64 part
                        
                        # Directly check the base64 string and assign role
                        if "iVBORw0KGgoAAAANSUhEUgAAABoAAAAWCAMAAADpVnyHAAAAKlBMVEUYGidMaXEWGCQXGSUWGCQVGCMXGSUXGSUXGSUWGCUXGSUVFyMXGSUWFhYOTH96AAAADnRSTlP+AF3nRzOZ9sWF1x+wDfagzcwAAAAJcEhZcwAACxMAAAsTAQCanBgAAADZSURBVHicbZJbcsQgDAQbSQjx8P2vmxJ47a0k/KH24BkGyveSuN4N36QqUf9FdQDyL+o03NT+oEukE6aP8EaXec7cB6jIFxIlV6tOQxx/Ud8Exlz0/csHWUoajaien+0zD6qpkPTukmpZbd7oymkvjksDImB9HMY2UWZ6hwZqH+Q5WaWkKKnWJ9exaHmN6SPJQVPSIsS0UqYeslEdIy2msxjdLM4tss9v1WMoxMoUdy+UE2RWs7lQGuuu80Y0hm2bPEV/ECqZDXS+VR6kfWTSHeA3OrXQ32fzA/IpBTzpneDQAAAAAElFTkSuQmCC" in base64_data:
                            role = "Duelist"
                        elif "iVBORw0KGgoAAAANSUhEUgAAABoAAAAWCAMAAADpVnyHAAAAKlBMVEVMaXEXGSUVFyQWGCMXGSUXGSUWFyQXGCUWGCUXGSYXGSUXGSUXGSUYGicV9gYgAAAADXRSTlMA3y4UyO1Fj3z3taBtotKEggAAAAlwSFlzAAALEwAACxMBAJqcGAAAAN9JREFUeJyFke2OBSEIQ1FARD3v/7obZ5z7kc1m+SUpLaWK/FP6Z1tL/UTaq9WItE/IMuLh4G3OM1nnbM7NW2WyFmS7xIDVibK2XDIaZvQNdazQBhkqQeLRqzE3NLHaw0m6VMMZW8guC9Bk4FgVUcumNaCoiDpE1ZZ23dZsuBeSJRJAcR92eRLRyS5THdcD5juPasnYB94zX9lIH7IOZf2K+FaFk9FHwkYCydBvOWl+OEX7ndhr0wHwWpM7stv84/lOAhjH/OOZPX5snk/Z68+lUp+duUR6llNuKuFPl/0HCkcLeZoYNQ0AAAAASUVORK5CYII=" in base64_data:
                            role = "Vanguard"
                        elif "iVBORw0KGgoAAAANSUhEUgAAABoAAAAWCAMAAADpVnyHAAAAJ1BMVEVMaXENEiUWGSYXGSUWGSUXGSUXGSQWGSUXGSUVGCMWGCUWGCQYGiYdhHX4AAAADHRSTlMABB/QWO6jcbVGfo+RjOptAAAACXBIWXMAAAsTAAALEwEAmpwYAAAApElEQVR4nK1RSRIDIQgEUUDl/+9NCQ5xqswtfaQXNoA/ARF/EHCROgCwcr1Ky2hmxruypKUG5iKsiVNOTDuhJTNCmpi44yI8QdKzbz0Js9Ul99IXxWOUGGAl0kmpkC4yVuon1TqR6uxuQxhe0xiH+yRiHntnNZICRTy6cR1EvENL+AE7u5WrkObx/DBLFVYVyVme+6f1e63XE9xK1y+H9f5pt34ADpwIgbSPdPUAAAAASUVORK5CYII=" in base64_data:
                            role = "Strategist"

                tier = columns[1].text.strip()
                win_rate = safe_float(columns[2].text.strip())
                wr_change = safe_float(columns[3].text.strip())
                pick_rate = safe_float(columns[4].text.strip())
                pr_change = safe_float(columns[5].text.strip())
                ban_rate = safe_float(columns[6].text.strip())
                matches = columns[7].text.strip()

                # Append role to data
                heroes_data.append(
                    [name, role, tier, win_rate, wr_change, pick_rate, pr_change, ban_rate, matches, rank, season]
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
