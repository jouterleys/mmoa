library(v3dR)
library(tidyr)
library(purrr)
library(dplyr)
library(here)
library(fst)


rm(list = ls())

# Build a function to do something on each dataframe
loopV3DR <- function(full_filepath) {
  
  df <- v3dR(full_filepath)
  
  print(paste(full_filepath," Complete"))
  
  return(df)
}

openAndGroom <- function() {
  # Define path to data folder
  #resultsPath <- here('data')
  resultsPath <- choose.dir()
  resultsPath
  
  # Create list of subjects based on subject folders
  subList <- list.dirs(resultsPath, recursive=FALSE)
  subList
  
  #subList <- subList[1]
  
  # Build dataframe containing all subject data
  # Creates list of all txt files from within the results folder
  df <- list.files(file.path(subList), pattern = "*.txt", full.names = TRUE) %>% map_df(~loopV3DR(.))
  #df <- list.files(file.path(resultsPath), pattern = "*.txt", full.names = TRUE) %>% map_df(~loopV3DR(.))
  
  df <- data.frame(df)
  
  # clean up names and create signal_side
  # tidyr 1.3.0
  df <- df %>% separate_wider_delim(c3d_name, delim = "_", names = c("subject", "action", "trial"))
  df <- df %>% separate_wider_delim(trial, delim = ".", names = c("trial"), too_many = "drop")
  df <- df %>% mutate(signal_names = toupper(signal_names))
  df <- df %>% separate_wider_delim(signal_names, names = c("signal_side", "signal_names"), delim = "_", too_many = "merge")
  
  # tidyr < 1.3.0
  #df <- df %>% separate(c3d_name, c("subject", "action","trial"),'\\_')
  #df <- df %>% separate_wider_delim(trial, c("trial"), extra = "drop", fill = "right")
  #df <- df %>% separate(signal_names, c("signal_side", "signal_names"), '\\_', extra = "merge", fill = "right")
  
  # create factors
  df$subject <- factor(df$subject)
  df$trial <- factor(df$trial)
  df$action <- factor(df$action)
  df$signal_side <- factor(df$signal_side)
  df$signal_names <- factor(df$signal_names)
  df$signal_types <- factor(df$signal_types)
  df$signal_folder <- factor(df$signal_folder)
  df$signal_components <- factor(df$signal_components)
  df$instance <- factor(df$instance)
  #df$item <- factor(df$item)

  
  return(df)
  
}


#Actual data to df

df <- openAndGroom()

write.fst(df, path = here('chkpts',paste(format(Sys.time(), "%F-%H%M%S"),'Ortho-Phase-2.fst', sep = "-")))
