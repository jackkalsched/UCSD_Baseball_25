install.library(baseballr)
library(tidyverse)
install.packages("baseballr")
library(baseballr)
library(dplyr)
library(stringr)


# retrieve the most recent season in the library
current_season <- most_recent_ncaa_baseball_season()
print(paste("Current NCAA Baseball Season:", current_season))

## testing different dataframes in baseballr
baseballr::load_ncaa_baseball_pbp(current_season)
teams <- baseballr::load_ncaa_baseball_teams() %>% filter(year == 2024)

# more testing (UCSD team_id = 112)
teams %>% filter(str_detect(team_name, "UC San Diego"))

pbp <- baseballr::load_ncaa_baseball_pbp(2023)




