Malaria data from the Malaria Atlas Project (MAP):

--- Getting the data ---:
Install R, the programming language.
Use the R package described here: https://cran.r-project.org/web/packages/malariaAtlas/index.html.
To download the package and its dependencies run the first part of the R script MAP_data_downloading.R.
To download malaria data run the second part of the R script.

Some data entries are confidential. To get the confidential data you must create an account on the https://dhsprogram.com/
and make a project. Then within the project you can request access to their data.
We have requested data from Sub-Saharan Africa, and then remember to also select [Show GPS datasets] located on the top left
of the list of countries. Then you can click [Select all surveys] on the top right of the country-list. Then after a couple of
days you should have access to the data.

The confidential data can be accessed with the R library with the fillDHSCoordinates method (see the R script).


--- Details about what the data contains ---:
See the report.
