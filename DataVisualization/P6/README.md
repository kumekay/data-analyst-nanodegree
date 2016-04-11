P6: Make Effective Data Visualization
=====================================

Death in Russia 2011-2014
-------------------------

Summary
-------

There are 2 visualizations of mortality in Russia for four years (2011-2014). First bar plot depicts mortality by gender and age group. There are some moments clear from this visualization:

1.	Women live longer
2.	Children, who survive during first year have very low chances to die in first 25 years.
3.	Structure of death doesn't change significantly during 4 years

Second visualization shows structure of death by causes. Some finding from visualization:

1.	Most important group of causes: Diseases of circulatory system. Atherosclerotic heart Disease is most common cause of death, for both men and women.
2.	Malignant neoplasm are on second place
3.	It's hard to find such reason like 'terrorism', much more people die by other external causes.

Design
------

This Visualization uses data from Russian Fertility and Mortality Database by Center for Demographic. Initital dataset was prepared for visualization with d3 and dimple using python notebook: `raw_data/prepare_data.ipynb` and data saved as several JSON files.

First visualization use bar plot with age group on horizontal axis and total number of death during the year. Bars for different genders have different colors.

Second plot shows number of deaths (summed for 4 years from 2011 to 2014) by cause of death. Causes of death in one group have same background color and placed together. There are no text labels. To see the description uses should put mouse pointer to the rect, to find data. Although it's may be strange on first view, this solution whet curiosity about the data.

Feedback
--------

### Anna Silnova

-	by gender and age graph
	-	better to swap axis. Y axis for Age looks strange
-	by cause of death graph
	-	it is hard to read
	-	May it will be better do not split data by sub categories?

### Maxim Kazansky

-	by gender and age graph

	-	fix maximum to 200k, to easier compare graphs for different years
	-	better labels for group

-	by cause of death graph

	-	it's almost impossible to read labels
	-	hints don't work

### Veronika Vishnevskaya

-	Regarding the first graph, I would switch the axis, because it looks for me conter intuitive. I would set the age on the horizontal axe, just because it is measure related to time, and this would be more usual and understandable way for presenting this information.

-	On the second graph I really like switcher allowing to choose if you want to see female, male or mixed data. What I think can be improved in this one is getting rid of the text inside all little clusters, you cannot read it anyway. Listing only more general reasons would be sufficient enough for the presenting the current mortality situation.

Resources
---------

-	http://www.icd10data.com/ICD10CM/Codes

-	http://demogr.nes.ru/index.php/ru/demogr_indicat/data

-	http://dimplejs.org/advanced_examples_viewer.html?id=advanced_storyboard_control

-	https://github.com/PMSI-AlignAlytics/dimple/wiki/dimple.chart

-	https://github.com/PMSI-AlignAlytics/dimple/wiki/dimple.storyboard

-	https://github.com/PMSI-AlignAlytics/dimple/wiki/dimple.aggregateMethod

-	http://pandas.pydata.org/pandas-docs/stable/10min.html

-	https://docs.python.org/2/library/functions.html

-	https://github.com/PMSI-AlignAlytics/dimple/wiki/dimple.color

-	http://bl.ocks.org/mbostock/4063269

-	http://bl.ocks.org/mbostock/1696080

-	https://bost.ocks.org/mike/circles/

-	https://bost.ocks.org/mike/join/

-	http://bl.ocks.org/aaizemberg/78bd3dade9593896a59d

-	http://jnnnnn.github.io/category-colors-constrained.html

-	http://stackoverflow.com/questions/20847161/colors-on-d3-js

-	https://bl.ocks.org/mbostock/1345853

-	http://bl.ocks.org/mbostock/4063582

-	https://github.com/mbostock/d3/wiki/Treemap-Layout

-	https://github.com/mbostock/d3/wiki/Requests#d3_json

-	http://www.icd10data.com/Search.aspx

-	https://css-tricks.com/snippets/css/simple-and-nice-blockquote-styling/

-	https://devcenter.heroku.com/articles/static-sites-ruby

-	https://github.com/Caged/d3-tip
