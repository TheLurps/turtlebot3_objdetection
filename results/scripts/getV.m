function [avgV, minV, maxV] = getV(data)
data = transpose(table2array(data));
avgV = round(mean(data));
minV = round(min(data));
maxV = round(max(data));

avgV, minV, maxV
end