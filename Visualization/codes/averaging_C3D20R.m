function D_averaged = averaging_C3D20R(Damage , Connectivity)
    % Damage: [nSteps , nElem , 8]
    % connectivity: [nElem , 8]
    % DN_nodes: [nNodes , 3] (only for nNodes)
    % Output: D_averaged [nSteps , nElem , 8]
    connectivity = Connectivity(: , 2:9);
    order = [1 2 4 3 5 6 8 7]'; 
    connectivity = connectivity(:,order);
    
    [nSteps, nElem, ~] = size(Damage);

    D_averaged = zeros(nSteps, nElem, 8);

    for e = 1:nElem
        elemNodes = connectivity(e,:);   % 8 global nodes of element e
        for r = 1:8
            nd = elemNodes(r);           % global node number
            [rows, cols] = find(connectivity(:,:) == nd); % elems & local idx of this node

            % collect values from all elements sharing this node
            vals = zeros(nSteps, numel(rows));
            for k = 1:numel(rows)
                vals(:,k) = Damage(: , rows(k) , cols(k));
            end

            % averaged values for this global node
            D_averaged(:, e, r) = mean(vals, 2);
        end
    end
end
