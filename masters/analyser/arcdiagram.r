# install devtools
install.packages("devtools")
# load devtools
library(devtools)
# install arcdiagram
# devtools::install_github('arcdiagram', username='gastonstat')
devtools::install_github('gastonstat/arcdiagram')
# load arcdiagram
library(igraph)

library(arcdiagram)
library(dplyr)
# location of 'gml' file
mis_file = "/home/nejc/PycharmProjects/tripadvisor-scraper/masters/analyser/lesmiserables.gml"
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
arcplot(edgelist, ordering=new_ord, labels=vlabels, cex.labels=0.8,
        show.nodes=TRUE, col.nodes=vborders, bg.nodes=vfill,
        cex.nodes = log(degrees)+0.5, pch.nodes=21,
        lwd.nodes = 2, line=-0.5,
        col.arcs = hsv(0, 0, 0.2, 0.25), lwd.arcs = 1.5 * values)

















install.packages("igraph")

library(arcdiagram)
library(igraph)

# create a star graph with 10 nodes
star_graph = graph.star(10, mode="out")

# extract edgelist
star_edges = get.edgelist(star_graph)

# inspect star_edges
star_edges

# plot 1: default arc diagram
arcplot(star_edges)

# plot 2: show nodes as circles, in decreasing order
arcplot(star_edges, show.nodes=TRUE, sorted=TRUE, decreasing=TRUE, las=1)

# plot 3: different ordering, arc widths, arc colors, and node sizes
set.seed(120)
arcplot(star_edges, ordering=sample(1:10), labels=paste("node",1:10,sep="-"),
        lwd.arcs=4*runif(10,.5,2), col.arcs=hsv(runif(9,0.6,0.8),alpha=0.4),
        show.nodes=TRUE, pch.nodes=21, cex.nodes=runif(10,1,3), 
        col.nodes="gray80", bg.nodes="gray90", lwd.nodes=2)

# plot 4: same as plot 3 but vertically oriented
set.seed(120)
op = par(mar = c(0.5, 5, 0.5, 3))
arcplot(star_edges, ordering=sample(1:10), horizontal=FALSE,
        labels=paste("node",1:10,sep="-"),
        lwd.arcs=4*runif(10,.5,2), col.arcs=hsv(runif(9,0.6,0.8),alpha=0.4),
        show.nodes=TRUE, pch.nodes=21, cex.nodes=runif(10,1,3), 
        col.nodes="gray80", bg.nodes="gray90", lwd.nodes=2)
par(op)
