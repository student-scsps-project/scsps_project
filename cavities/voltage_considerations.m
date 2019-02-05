%% Considerations for RF Voltage
% Aimee Ross
%
% Script to establish lower bound for rf voltage for scSPS based on bucket
% area considerations.
%
% Using equation from S.Y.Lee Section II.2:
% 
% $$A_{B}=16\sqrt{\frac{\beta^2EeV}{2\pi\omega_{0}^{2}h\left|\eta\right|}}a_{b}(\phi_{s})$$
% 

%% Bucket area calculations
% To determine a lower bound on voltage across rf cavity for scSPS
%Can change between injection and extraction energy (change first input
%only)
KE = 26e9; %eV
c=2.998e8; %m/s
e=1.6e-19; %C
m = 0.938e9; %eV
E=KE+m; %eV
gamma = E/m;
beta = sqrt(1-1/gamma^2);
circumference = 6.9e3; %m
R_0 = circumference/(2*pi); %radius of SPS in m
omega_0 = beta*c/R_0; %revolution frequency
h = 11052; %harmonic number based on python cavity calulations (rf freq = 480MHz)
gamma_tr = 22.8; %from https://accelconf.web.cern.ch/AccelConf/IPAC2011/papers/mops012.pdf

eta = 1/gamma_tr^2 - 1/gamma^2; %slippage factor at injection

a_b = @(phi_s) (1-sind(phi_s))/(1+sind(phi_s)); %for phi_s synchrotron phase in degrees
%Y = @(phi_s) sqrt(abs(cosd(phi_s)-((pi-2*phi_s*pi/180)/2)*sind(phi_s)));
%%for phi_s synchrotron phase in degrees - for height, not required

A_b = @(V, phi_s) 16*sqrt((beta^2*E*V*1e6)/(2*pi*omega_0^2*h*abs(eta)))*a_b(phi_s); %for V in MV, E in eV, gives result in eVs

%Choose phi_s=30 degrees (arbitrary, can be changed)
A_b = @(V) A_b(V,30); %output in eVs, for V in MV

%Plot of bucket area at chosen synchronous phase
figure
fplot(A_b, [0 1])
xlabel('V_{rf} [MV]');
ylabel('A_{B} [eVs]');

%Plot of bucket area at chosen synchronous phase
figure
fplot(A_b, [0 0.01])
xlabel('V_{rf} [MV]');
ylabel('A_{B} [eVs]');

%%
% Longitudinal emittance (2 sigma) at 26GeV = 0.35eVs, at 1.3TeV = 0.85eVs.
% Expect to use voltage >~1MV/m for time to accelerate beam to top energy.
% Easily above lower bound constraint from longitudinal emittance (sub 1MV).
% Therefore, stronger constraint on rf voltage is that required for acceleration in cycle time.

%% Bucket area evolution over acceleration
%scan bucket area from minimum to maximum energy at fixed rf voltage (first
%input to change only)
V = 0.1; %MV/m
c=2.998e8; %m/s
e=1.6e-19; %C
KE = linspace(26e9,1.3e12,100); %eV
m = 0.938e9; %eV
E=KE+m; %eV
gamma = E./m;
beta = sqrt(1-1./gamma.^2);
circumference = 6.9e3; %m
R_0 = circumference/(2*pi); %radius of SPS in m
omega_0 = beta.*c./R_0; %revolution frequency
h = 11052; %harmonic number based on python cavity calulations (rf freq = 480MHz)
gamma_tr = 22.8; %from https://accelconf.web.cern.ch/AccelConf/IPAC2011/papers/mops012.pdf

eta = 1/gamma_tr^2 - 1./gamma.^2; %slippage factor at injection

a_b = @(phi_s) (1-sind(phi_s))/(1+sind(phi_s)); %for phi_s synchrotron phase in degrees
A_b = @(V, phi_s) 16.*sqrt((beta.^2.*E.*V.*1e6)./(2.*pi.*omega_0.^2.*h.*abs(eta))).*a_b(phi_s); %for V in MV, E in eV, gives result in eVs

%Choose phi_s=30 degrees (arbitrary, can be changed)
A_b = A_b(V,30); %output in eVs, for V in MV

%Plot of bucket area with kinetic energy at chosen rf voltage
plot(KE*1e-9,A_b)
xlabel('KE [GeV]');
ylabel('A_{B} [eVs]');

%%
% Shows that stronger bucket area constraint comes from injection energy rather than extraction. Can use this script to check bucket area evolution when rf
% voltage is chosen
