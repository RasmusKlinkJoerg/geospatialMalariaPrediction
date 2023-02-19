#--------- Part 1 -------------
install.packages("devtools")
library(devtools)

# Make sure the following packages are installed:
#Depends:	ggplot2
#Imports:	curl, rgdal, raster, sp, xml2, grid, gridExtra, httr, dplyr, stringi, tidyr, methods, stats, utils, rlang
#Suggests:	testthat, knitr, rmarkdown, palettetown, magrittr, tibble, rdhs

#Install some of the packages by running code below, the last one should be a more robust version of malariaAtlas.
devtools::install_github("ropensci/rdhs")
install.packages("ggplot2")
install.packages("raster")
install.packages("xml2")
install.packages("gridExtra")
install.packages("stringi")
install.packages("tidyr")
install.packages("testthat")
install.packages("knitr")
install.packages("rmarkdown")
install.packages("palettetown")
install.packages("rdhs")
install.packages("devtools")
install_github('https://github.com/malaria-atlas-project/malariaAtlas')


#---------- Part 2 ------------
library(malariaAtlas)
library(rdhs)


# Getting data from Tanzania
TANZ_pr_data <- getPR(country = "Tanzania", species = "both") #Load data from Tanzania
#Save the data to csv
complete_path_name = "C:\\Users\\r-kli\\OneDrive\\Dokumenter OneDrive\\MasterThesis\\TANZ.csv"
write.csv(TANZ_pr_data, complete_path_name, row.names=TRUE)
autoplot(TANZ_pr_data, facet=FALSE) #Plot data om a map

# Getting data from all countries
ALL_pr_data <- getPR(country = "ALL", species = "both")
# Getting data from Africa
Africa_pr_data <- getPR(continent = "Africa", species = "both")


# Filling in confidential data from https://dhsprogram.com/
username = "youremail@gmail.com"
projectname = "Your project name"

#When running the command below, make sure to enter 2 for No, when you are prompted:
#"Do you confirm rdhs to write to files outside your R temporary directry? (Enter 1 or 2)"
TANZ_pr_data_plus <- fillDHSCoordinates(TANZ_pr_data, 
							email = username,
                        			project = projectname)
complete_path_name_plus = "C:\\Users\\r-kli\\OneDrive\\Dokumenter OneDrive\\MasterThesis\\TANZ_plus.csv"
write.csv(TANZ_pr_data_plus, complete_path_name_plus, row.names=TRUE)


ALL_pr_data_plus <- fillDHSCoordinates(ALL_pr_data, username, projectname)
write.csv(ALL_pr_data_plus, 
	"C:\\Users\\r-kli\\OneDrive\\Dokumenter OneDrive\\MasterThesis\\ALL_pr_plus.csv", 
	row.names=TRUE)

