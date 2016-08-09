import csv

def handle_uploaded_file(f):
    with open('media/raw_urls.csv', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

def csv_reader(filename, list):
    """Open and read a csv file"""
    with open(filename, encoding="utf-8") as csvfile:
        read_csv = csv.reader(csvfile)
        for row in read_csv:
            list.append(row)

def filter(raw_urls, keywords, bad_urls, good_urls):
    """Check each raw url whether it's good or bad"""
    for url in raw_urls:
        if url[2] == "200 OK" and int(url[3]) >= 3:
            for keyword in keywords:
                if keyword in url[0]:
                    bad_urls.append(url)
                    break
            if url not in bad_urls:
                good_urls.append(url)
        else:
            bad_urls.append(url)

def save_csv(filename, list):
    """Save raw urls into a CSV file"""
    with open(filename, 'w', newline='', encoding="utf-8") as output:
        writer = csv.writer(output, delimiter=',')
        for url in list:
            writer.writerows([url])