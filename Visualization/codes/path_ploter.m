
function path_ploter(D_pred_nodal, nodes, connectivity, displacement , geo)

x_axis_indices = abs(nodes(:,3)) == 0;
x_nodes = nodes(x_axis_indices, :);
x_nodes = sortrows(x_nodes, 2);
x_el = zeros(size(x_nodes,1),1);

for i =1:size(x_nodes,1)
    for j=1:size(connectivity,1)
        for a=2:size(connectivity,2)
            if connectivity(j, a) == x_nodes(i,1)
                x_el(i,1) = connectivity(j, 1);
            end
        end
    end
end

x_element = unique(x_el);
figure;
d = zeros(size(x_element,1)+1, 1);
steps = size(D_pred_nodal,1);

x_position = x_nodes(1:2:end , 2);

if string(geo) == "Neto"
    indx1 = 20;
    indx2 = 30;
    indx_intg = 4;
else % cesar
    indx1 = 91;
    indx2 = 100;
    indx_intg = 3;
end

for i=indx1:indx2:steps
    for j=1: size(x_element,1)
        indx = x_element(j,1);
        d(j) = D_pred_nodal(i, indx, 2);
    end
    d(j+1) = D_pred_nodal(i, indx, indx_intg); %last node
    hold on
    
    plot( x_position, d,'LineWidth', 3);
    label = sprintf(' u = %.4f mm', displacement(i));
    text(x_position(floor(end/4)), d(floor(end/4))+0.018, label, 'FontSize', 27,'fontname','Times New Roman', 'HorizontalAlignment', 'left');
    
    
end

ylim([0 0.7]);
yticks(0:0.1:0.7);
xlabel('X-Coordinate (mm) ', 'FontSize' , 35 ,'fontname','Times New Roman');
ylabel('Damage', 'FontSize' , 35 ,'fontname','Times New Roman');
ax= gca;
ax.LineWidth = 1.7;
ax.FontSize = 35;
ax.FontName = 'Times New Roman';
box on;

end
