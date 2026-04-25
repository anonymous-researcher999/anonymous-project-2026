
function ploterMeshDependency(D_pred_nodal, nodes, connectivity)

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
x_position = x_nodes(1:2:end , 2);

i = 491;


for j=1: size(x_element,1)
    indx = x_element(j,1);
    d(j) = D_pred_nodal(i, indx, 2);
end
d(j+1) = D_pred_nodal(i, indx, 3); %last node

plot( x_position, d,'LineWidth', 2.7);
legend('Fine mesh');

ylim([0 0.45]);
yticks(0:0.1:0.45);
xlabel('X-Coordinate (mm) ', 'FontSize' , 35 ,'fontname','Times New Roman');
ylabel('Damage', 'FontSize' , 35 ,'fontname','Times New Roman');
ax= gca;
ax.LineWidth = 1.7;
ax.FontSize = 35;
ax.FontName = 'Times New Roman';
box on;

end