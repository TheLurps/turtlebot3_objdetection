data = uptimeyolov21fpspurged;

data = transpose(table2array(data));

plot([1:1:length(data)], data)

set(gcf, 'Color', 'w');

ylabel({'Average system load in last minute [1]'});

xlabel({'Process runtime [s]'});

title({'Darknet YOLOv2 Tiny'});

%export_fig cloud_load.pdf