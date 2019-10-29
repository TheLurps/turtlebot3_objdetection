data = table2array(currentyolov21fpspurged);

time = data(:,1);
current = data(:,2);

plot(time, current)

set(gcf, 'Color', 'w');

ylabel({'Current draw [A]'});

xlabel({'Process runtime [s]'});

title({'Darknet YOLOv2 Tiny'});

%export_fig cloud_load.pdf