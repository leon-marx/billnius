import billboard

#years = [str(i) for i in range(1955, 2024, 1)]
years = [str(i) for i in range(2018, 2019, 1)]
months = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]
days = ["01", "08", "15", "22", "29"]

for year in years:
    for month in months:
        for day in days:
            try:
                chart = billboard.ChartData("hot-100", date=f"{year}-{month}-{day}")
                print(f"got charts from {year}-{month}-{day}")
            except ValueError:
                print(f"date skipped since not valid: {year}-{month}-{day}")
            with open (f"./charts/charts_{year}_{month}_{day}.txt", "w") as f:
                f.write("title;artist;peakpos;lastpos;weeks;rank;isnew\n")
                for song in chart:
                    f.write(f"{song.title};{song.artist};{song.peakPos};{song.lastPos};{song.weeks};{song.rank};{song.isNew}\n")
                print(str(chart))
