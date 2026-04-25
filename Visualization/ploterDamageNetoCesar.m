% read data from Python and plot
clc;
clear;


Geo = {'Neto', 'Cesar_1', 'Cesar_2'};
geo = Geo{3};        % <--- choose your geometry

Lr = {0.6325 , 0.8 , 1.0 , 0};
lr = Lr{4};          % <--- choose your characteristic length 

Conditions = {'4000CP', '2000CP'};  %CP = collocation points
condition = Conditions{1};  % <--- choose your condition


if string(geo) == "Neto"
    
    load('Neto_nodes.mat');
    load('Neto_connectivity.mat');
    load('Neto_D.mat');
    load('Neto_displacement.mat');
    load('Neto_pred.mat');
    load('Neto_pred_2000.mat');
    
    nodes         = Neto_nodes;
    connectivity  = Neto_connectivity;
    displace      = Neto_displacement;
    D_True        = squeeze(Neto_D);
    stp           = 50;
    if string(condition) == "2000CP"
        pred      = Neto_pred_2000;
    else
        pred      = Neto_pred;
    end
        
        
        
elseif string(geo) == "Cesar_1" %coarse
    load('Cesar1_nodes.mat');
    load('Cesar1_connectivity.mat');
    load('Cesar1_D.mat');
    load('Cesar1_displacement.mat');
    load('Cesar1_pred_local.mat');
    load('Cesar1_pred_Nonlocal_Lr6325.mat');
    load('Cesar1_pred_Nonlocal_Lr8.mat');
    load('Cesar1_pred_Nonlocal_Lr1.mat');

    nodes         = Cesar1_nodes;
    connectivity  = Cesar1_connectivity;
    displace      = Cesar1_displacement;
    D_True        = squeeze(Cesar1_D);
    stp           = 157;
    if lr == 0.6325
        pred  = Cesar1_pred_Nonlocal_Lr6325;
    elseif lr == 0.8
        pred  = Cesar1_pred_Nonlocal_Lr8;
    elseif lr == 1.0
        pred  = Cesar1_pred_Nonlocal_Lr1;
    elseif lr == 0
        pred  = Cesar1_pred_local;
    end
    
elseif string(geo) == "Cesar_2"  %fine
    load('Cesar2_nodes.mat');
    load('Cesar2_connectivity.mat');
    load('Cesar2_D.mat');
    load('Cesar2_displacement.mat');
    load('Cesar2_pred_local.mat');
    load('Cesar2_pred_Nonlocal_Lr6325.mat');
    load('Cesar2_pred_Nonlocal_Lr8.mat');
    load('Cesar2_pred_Nonlocal_Lr1.mat');

    nodes         = Cesar2_nodes;
    connectivity  = Cesar2_connectivity;
    displace      = Cesar2_displacement;
    D_True        = squeeze(Cesar2_D);
    stp           = 157;
    if lr == 0.6325
        pred  = Cesar2_pred_Nonlocal_Lr6325;
    elseif lr == 0.8
        pred  = Cesar2_pred_Nonlocal_Lr8;
    elseif lr == 1.0
        pred  = Cesar2_pred_Nonlocal_Lr1;
    elseif lr == 0
        pred  = Cesar2_pred_local;
    end

end
    
    
    
    D_True_nodal = CalculateNodalValue(D_True);
    
    D_pred  = squeeze(pred(:, 7, :, :));
    %D_pred_nodal = CalculateNodalValue(D_pred);
    D_pred_nodal = D_pred; %C
    D_pred_nodal_final = squeeze(D_pred_nodal(end, :, :, :));
    
    
    figure;
    hold on;
    axis equal;
    %colormap(flipud(gray));
    colormap(jet); %turbo
    
    NumElem = size(connectivity,1);
    for i = 1:NumElem
        elemNodes = connectivity(i, 2:5); % Extract node numbers
        x = nodes(elemNodes, 2); % X-coordinates
        y = nodes(elemNodes, 3); % Y-coordinates
        c = zeros(1,4);
        
        for r = 1:4
            nd = elemNodes(r);
            [row, col] = find(connectivity(:, 2:end) == nd);
            sum = 0 ;
            for k=1:size(row,1)
                sum = sum + D_pred_nodal_final(row(k,1), col(k,1));
            end
            c(r) = sum / size(row,1);
        end
        
        % Plot original quarter
        patch(x, y, c, 'EdgeColor', 'k', 'FaceColor', 'interp');
        % Mirror across the y-axis
        patch(-x, y, c, 'EdgeColor', 'k', 'FaceColor', 'interp');
        % Mirror across the x-axis
        patch(x, -y, c, 'EdgeColor', 'k', 'FaceColor', 'interp');
        % Mirror across both axes
        patch(-x, -y, c, 'EdgeColor', 'k', 'FaceColor', 'interp');
    end
    
    colorbar; % Add color legend
    c = colorbar;
    %c.Label.String = 'Damage';
    c.Label.FontSize = 15;
    c.LineWidth = 1.7;
    c.FontSize = 40;
    c.FontName = 'Times New Roman';
    c.Ticks = linspace(min(caxis), max(caxis), 5); % Control tick intervals manually
    
    ticks = c.Ticks;
    ticks(end) = max(caxis);   % replace last tick with caxis max
    c.Ticks = ticks;
    
    fprintf('max Damage = %f\n', max(max(D_pred_nodal_final)));
    
    
    
    
    %---------------------------Plot Damage Error --------------------
    %-------------------------(PINN Compaire to FE) ------------------
    
    displacement = zeros(1, size(displace,2));
    for i = 1:size(displace,2)
        displacement(i) = displace{i};
    end
    
    
    j = 20;
    while j <= size(displacement, 2)
        
        figure;
        hold on;
        axis equal;
        colormap(jet); %turbo
        
        
        %error_damage = squeeze(D_True_nodal(j,:,:,:)) - squeeze(D_pred_nodal(j,:,:,:));
        
        error_damage = squeeze(D_pred_nodal(j,:,:,:));
        
        for i = 1:NumElem
            elemNodes = connectivity(i, 2:5); % Extract node numbers
            x = nodes(elemNodes, 2); % X-coordinates
            y = nodes(elemNodes, 3); % Y-coordinates
            c = zeros(1,4);
            
            for r = 1:4
                nd = elemNodes(r);
                [row, col] = find(connectivity(:, 2:5) == nd);
                sum = 0 ;
                for k=1:size(row,1)
                    sum = sum + error_damage(row(k,1), col(k,1));
                end
                c(r) = sum / size(row,1);
            end
            
            % Plot original quarter
            patch(x, y, c, 'EdgeColor', 'k', 'FaceColor', 'interp');
            % Mirror across the y-axis
            patch(-x, y, c, 'EdgeColor', 'k', 'FaceColor', 'interp');
            % Mirror across the x-axis
            patch(x, -y, c, 'EdgeColor', 'k', 'FaceColor', 'interp');
            % Mirror across both axes
            patch(-x, -y, c, 'EdgeColor', 'k', 'FaceColor', 'interp');
        end
        
        %title(sprintf('U = %f  [mm]', displacement(j)),'FontSize', 24, 'FontName', 'Times New Roman');
        colorbar; % Add color legend
        c = colorbar;
        %c.Label.String = 'Damage Error';
        c.Label.FontSize = 15;
        axis off;
        c.LineWidth = 1.7;
        c.FontSize = 40;
        c.FontName = 'Times New Roman';
        c.Ruler.Exponent = 0;
        c.Ticks = linspace(min(caxis), max(caxis), 5);
        
        ticks = c.Ticks;
        ticks(end) = max(caxis);
        ticks(1) = min(caxis);
        c.Ticks = ticks;
        
        
        disp('---------------------------')
        fprintf('U                = %f [mm]\n' , displacement(j));
        fprintf('max Damage Error = %f\n'      , max(error_damage(:)));
        fprintf('max D_True_nodal = %f \n' , max(D_True_nodal(j,:,:,:), [], 'all'));
        fprintf('max D_pred_nodal = %f \n' , max(D_pred_nodal(j,:,:,:), [], 'all'));
        j = j + stp;  
        
    end
    
%path_ploter(D_pred_nodal, nodes, connectivity, displacement , geo);
%ploterMeshDependency(D_pred_nodal, nodes, connectivity)