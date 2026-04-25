function D_nodes = CalculateNodalValue(D_Integ)


% shape(D_Integ) is  (steps,element,integPoint)

steps   = size(D_Integ, 1);
NumElem = size(D_Integ, 2);


% --- 2x2 Gauss point locations (ξ,η) ---
g = 1/sqrt(3);
gp_coords = [ -g -g;   % GP1
    g -g;   % GP2
    g  g;   % GP3
    -g  g];  % GP4

% --- Build interpolation matrix (GP → Corners) ---
N = zeros(4,4);
for a = 1:4
    xi  = gp_coords(a,1);
    eta = gp_coords(a,2);
    % Shape functions of 4-node quad
    N1 = 0.25*(1 - xi).*(1 - eta);
    N2 = 0.25*(1 + xi).*(1 - eta);
    N3 = 0.25*(1 + xi).*(1 + eta);
    N4 = 0.25*(1 - xi).*(1 + eta);
    N(a,:) = [N1 N2 N3 N4];
end

% Extrapolation matrix: from GP values to corner nodal values
E = inv(N);

% --- Extrapolate each element ---
D_nodes = zeros(steps,NumElem,4);

for s = 1:steps
    for e = 1:NumElem
        gp_vals = squeeze(D_Integ(s,e,:));        % (4x1)
        corner_vals = E * gp_vals;      % (4x1)
        D_nodes(s,e,:) = corner_vals;
    end
end

end
