set term pdfcairo enhanced color size 21cm, 15cm
set output 'network_traffic.pdf'

# 设置图表标题和坐标轴标签
set title "Network Traffic"
#set xlabel "Cache Replacement Policy"
set ylabel "Network Traffic (MB)"
#set xtics font ", 20"
#set ytics font ", 20"

set multiplot layout 2,2 #title "Network Traffic" font ", 15"
set object 1 rectangle behind from graph 0,0 to graph 1,1 fc rgb "#EFEFEF" fillstyle solid noborder

set datafile separator comma
unset border
set grid

set key font ", 15"
set style line 1 lc rgb '#0907BB' lt 1 lw 4 pt 5
set style line 2 lc rgb '#2C6676' lt 1 lw 4 pt 7
set style line 3 lc rgb '#379CB6' lt 1 lw 4 pt 11
set style line 4 lc rgb '#AAAAFF' lt 1 lw 4 pt 2

######################
#    Plot Figure 1   #
######################
set origin 0.02,0.51; set size 0.49, 0.49;

set title "a) twitter ego" offset 0, -22
plot 'twitter_ego.dat' using 0:2:xtic(1) with linespoints linestyle 1 title 'Layer1 CDN',\
                    '' using 0:3:xtic(1) with linespoints linestyle 2 title 'Layer2 CDN',\
                    '' using 0:4:xtic(1) with linespoints linestyle 3 title 'DC layer',\
                    '' using 0:5:xtic(1) with linespoints linestyle 4 title 'Total'

######################
#    Plot Figure 2   #
######################
set origin 0.51,0.51; set size 0.49, 0.49;

set title "b) twitter full"
plot 'twitter_full.dat' using 0:2:xtic(1) with linespoints linestyle 1 title 'Layer1 CDN',\
                    '' using 0:3:xtic(1) with linespoints linestyle 2 title 'Layer2 CDN',\
                    '' using 0:4:xtic(1) with linespoints linestyle 3 title 'DC layer',\
                    '' using 0:5:xtic(1) with linespoints linestyle 4 title 'Total'

######################
#    Plot Figure 3   #
######################
set origin 0.02,0.02; set size 0.49, 0.49;

set title "c) brightkite"
plot 'brightkite.dat' using 0:2:xtic(1) with linespoints linestyle 1 title 'Layer1 CDN',\
                    '' using 0:3:xtic(1) with linespoints linestyle 2 title 'Layer2 CDN',\
                    '' using 0:4:xtic(1) with linespoints linestyle 3 title 'DC layer',\
                    '' using 0:5:xtic(1) with linespoints linestyle 4 title 'Total'

######################
#    Plot Figure 4   #
######################
set origin 0.51,0.02; set size 0.49, 0.49;

set title "d) gowalla"
plot 'gowalla.dat' using 0:2:xtic(1) with linespoints linestyle 1 title 'Layer1 CDN',\
                    '' using 0:3:xtic(1) with linespoints linestyle 2 title 'Layer2 CDN',\
                    '' using 0:4:xtic(1) with linespoints linestyle 3 title 'DC layer',\
                    '' using 0:5:xtic(1) with linespoints linestyle 4 title 'Total'

unset multiplot