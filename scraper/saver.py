import csv

class CSVWriter:
    def save_to_csv(self, filename, data, headers):
        with open(filename, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(headers)
            writer.writerows(data)