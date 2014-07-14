library (XML)

parseTrafData <- function(html) {
  locale <- Sys.getlocale("LC_MESSAGES")
  Sys.setlocale(locale="C")
  
  date <- getToday()
  
  orig <- readHTMLTable(html)$inet_week
  
  dates <- strptime(orig[,1], "%d.%m.%Y %a %H:%M")
  in_bytes <- as.numeric(gsub(" ", "", orig[,2]))
  out_bytes <- as.numeric(gsub(" ", "", orig[,3]))
  
  df <- data.frame(date=dates, in_bytes=in_bytes, out_bytes=out_bytes)
  
  Sys.setlocale(locale=locale)
  
  # Filter NAs
  df <- df[!is.na(df$date),]
  date_str <- paste (date$year, date$month, date$day, sep="-")
  daynight_ts <- strptime(c(paste(date_str, "8:00"),
                            paste(date_str, "0:00")),
                          "%Y-%m-%d %H:%M")
  night_df <- df[df$date < daynight_ts[1] & df$date >= daynight_ts[2],]
  day_df <- df[df$date >= daynight_ts[1],]

#  print (night_df)
#  print (day_df)
  
  night_in <- sum(night_df[,2])
  night_out <- sum(night_df[,3])
  
  day_in <- sum(day_df[,2])
  day_out <- sum(day_df[,3])
  
  data.frame(night_in=night_in, night_out=night_out,
             day_in=day_in, day_out=day_out,
             day=day_in+day_out, night=night_in+night_out)
}
