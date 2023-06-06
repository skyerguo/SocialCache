set term pdfcairo enhanced color size 21cm, 15cm
set output 'network_traffic.pdf'

# 设置图表标题和坐标轴标签
set title "Network Traffic"
#set xlabel "Cache Replacement Policy"
set ylabel "Network Traffic (MB)"
#set xtics font ", 20"
#set ytics font ", 20"

set multiplot layout 2,2 title "Network Traffic"

set datafile separator comma
unset border
set grid
# 设置x轴标签和刻度
set xtics mirror rotate by -45 font ", 10"
#set xticlabels ("RAND" 1, "FIFO" 2, "LRU" 3, "LRU-Social" 4, "SocialCache" 5)

######################
#    Plot Figure 1   #
######################
set origin 0.01,0.51; set size 0.49, 0.49;

set title "a) twitter ego"
plot 'twitter_ego.dat' using 0:2:xtic(1) with lines title 'Layer1 CDN',\
                    '' using 0:3:xtic(1) with lines title 'Layer2 CDN',\
                    '' using 0:4:xtic(1) with lines title 'DC layer',\
                    '' using 0:5:xtic(1) with lines title 'Total'
