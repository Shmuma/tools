library(RCurl)

# obtains traffic data in raw html for the current day
getTrafData <- function(login, pass) {
  date <- getToday()
  
  handle <- getCurlHandle()
  curlSetOpt(cookieJar="cookies.txt", curl=handle)
  res <- postForm("http://stats.altegrosky.ru/?actm=guest&act=login", login=login, pass=pass, enter="enter",
                  act_="form_login", act="news", id_="0",
                  .encoding="utf-8", curl=handle)
  res2 <- postForm("http://stats.altegrosky.ru/?actm=inet&act=inetstats", day_before=date$day, month_before=date$month, 
                   year_before=date$year, grp="-1", .encoding="utf-8", curl=handle)
#  write(res2, "res2.html")
}
