
# SETUP
# install devtools
install.packages("devtools")
# load devtools
library(devtools)
# install arcdiagram
# devtools::install_github('arcdiagram', username='gastonstat')
devtools::install_github('gastonstat/arcdiagram')

# RUN DIAGRAM
# load arcdiagram
library(igraph)
library(arcdiagram)
library(dplyr)
# location of 'gml' file
mis_file = "/home/nejc/PycharmProjects/tripadvisor-scraper/masters/analyser/arcdiagram_slo_19.gml"

mis_file = "/home/nejc/PycharmProjects/tripadvisor-scraper/masters/analyser/arcdiagram_slo_20.gml"

#mis_file = "/home/nejc/PycharmProjects/tripadvisor-scraper/masters/analyser/lesmiserables.gml"
# read 'gml' file
mis_graph = read.graph(mis_file, format="gml")

# get edgelist
edgelist = get.edgelist(mis_graph)
# get vertex labels
vlabels = get.vertex.attribute(mis_graph, "label")
# get vertex groups
vgroups = get.vertex.attribute(mis_graph, "group")
# get vertex fill color
vfill = get.vertex.attribute(mis_graph, "fill")
# get vertex border color
vborders = get.vertex.attribute(mis_graph, "border")
# get vertex degree
degrees = degree(mis_graph)
# get edges value
values = get.edge.attribute(mis_graph, "value")

# load reshape
library(reshape)
# data frame with vgroups, degree, vlabels and ind
x = data.frame(vgroups, degrees, vlabels, ind=1:vcount(mis_graph))
# arranging by vgroups and degrees
y = arrange(x, desc(vgroups), desc(degrees))
# get ordering 'ind'
new_ord = y$ind

# plot arc diagram
#labels=vlabels
arcplot(edgelist, ordering=new_ord, labels=vlabels, cex.labels=0.8,
        show.nodes=TRUE, col.nodes=vborders, bg.nodes=vfill,
        cex.nodes = log(degrees)+2.0, pch.nodes=21,
        lwd.nodes = 3, line=+0.1,
        col.arcs = hsv(0, 0, 0.3, 0.25), lwd.arcs = 2.0 * sqrt(values))
  
