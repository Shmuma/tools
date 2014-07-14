# return today's date as data frame
getToday <- function() {
  date <- Sys.Date()
  d <- strsplit(format(date), "-")
  data.frame(year=d[[1]][1], month=d[[1]][2], day=d[[1]][3], date=date)
}