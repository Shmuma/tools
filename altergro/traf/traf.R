# Script downloads and calculates total traffic for the current day from 8:00 to midnight

library (methods)
library (bitops)

source("getTrafData.R")
source("parseTrafData.R")
source("getToday.R")


if (!file.exists("auth.txt")) {
  print ("No auth.txt file found! You need to copy auth.txt.sample to auth.txt and edit it!")
  return
}

# read password file
auth <- read.csv("auth.txt", header=T)
# download used traffic
html_data <- getTrafData(login=auth$Login, pass=auth$Password)
# parse traffic table
traf_data <- parseTrafData(html_data)

format_size <- function(msg, bytes) {
  sprintf("%-12s%.1f", msg, bytes / 1024)
}

msg <- paste("",
             format_size("Night in:", traf_data$night_in),
             format_size("Night out:", traf_data$night_out),
             format_size("Night:", traf_data$night),
             "",
             format_size("Day in:", traf_data$day_in),
             format_size("Day out:", traf_data$day_out),
             format_size("Day:", traf_data$day),
             sep="\n")
write(msg, file="")
