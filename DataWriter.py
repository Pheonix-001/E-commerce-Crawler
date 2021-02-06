import csv

class DataWriter:

    file_name = ''

    def __init__(self, file_name):
        self.file_name = file_name
        

    def writer(self, data):
        f = self.file_name

        with open(f, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["Product Name", "Price", "Rating", "No. of reviews", "Buy link"])
            writer.writerows(data)

