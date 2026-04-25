% read data from Python and plot
clc;
clear;

load('DN_nodes.mat');
load('DN_connectivity.mat');
load('DN_D.mat');
load('DN_displacement.mat');
load('DN_pred_nonlocal.mat');

nodes           = DN_nodes;
connectivity    = DN_connectivity;
displace        = DN_displacement;
pred_nonloacl   = DN_pred_nonlocal;
D_pred_nonlocal = squeeze(pred_nonloacl(:, 7, :, :));
D_FE            = squeeze(DN_D);

displacement = zeros(1, size(displace,2));
for i = 1:size(displace,2)
    displacement(i) = displace{i};
end

node_coords = nodes(:,2:4);  % (x,y,z)
conn = connectivity(:,2:end);

% corner nodes
corner_idx = [1 :8];

% faces defined by corner nodes only
faces = [1 2 3 4;   % bottom
    5 6 7 8;   % top
    1 2 6 5;   % side
    2 3 7 6;
    3 4 8 7;
    4 1 5 8];

stp = 65;
k   = 130;   %334
while k < size(displacement,2)
    
    figure;
    hold on;
    axis equal;
    %xlabel('X'); ylabel('Y'); zlabel('Z');
    axis off
    %grid on;
    colormap(jet); %turbo
    
    values_av = averaging_C3D20R(D_pred_nonlocal ,connectivity);
    values = squeeze(values_av(k, :,:));
    
    for e = 1:size(conn,1)
        elem_nodes = conn(e,:);                   % 20 node indices
        corner_nodes = elem_nodes(corner_idx);    % 8 corner nodes
        
        coords = node_coords(corner_nodes,:);     % (8×3)
        values_elemnt = values(e,:)';      % 8 values
        %order = [1 2 3 4 5 6 7 8]';   % based on Abaqus Integration points numbering
        order = [1 2 4 3 5 6 8 7]'; 
        values_elemnt = values_elemnt(order,: );
        
        for f = 1:size(faces,1)
            patch('Vertices',coords, ...
                'Faces',faces(f,:), ...
                'FaceVertexCData',values_elemnt, ...
                'FaceColor','interp', ...
                'EdgeColor','k', ...
                'FaceAlpha',1);
        end
    end
    
    %title(sprintf('U = %f mm', displacement(k)));

    colorbar;
    c = colorbar;
    c.Position(1) = c.Position(1) - 0.05;  
    c.Position(3) = 0.02; 
    c.Label.FontSize = 15;
    c.LineWidth = 1.7;
    c.FontSize = 40;
    c.FontName = 'Times New Roman';
    c.Ruler.Exponent = 0;
    c.Ticks = linspace(min(caxis), max(caxis), 5);
    ticks = c.Ticks;
    ticks(end) = max(caxis);
    c.Ticks = ticks;
    %view([-1 0 -1]) 
    view(2); 
    camorbit(-60,0,'camera') 
    k = k + stp;
end
