% For nominal particle, what is rate of frequency tune required
clear

V = 1e6; %MV/m
c=2.998e8; %m/s
e=1.6e-19; %C
KE_init = 26e9; %eV
KE_final = 150e9;%1.3e12; %eV
n_turns = (KE_final - KE_init)/V; 
%t_final = 34; %s
KE = linspace(KE_init,KE_final,n_turns); %eV
%time = linspace(0,t_final,n_turns);
m = 0.938e9; %eV
E=KE+m; %eV
gamma = E./m;
beta = sqrt(1-1./gamma.^2);
circumference = 6.9e3; %m
R_0 = circumference/(2*pi); %radius of SPS in m
freq_rev = beta.*c./circumference; %revolution frequency
h = 4600; %harmonic number based on python cavity calulations (rf freq = 480MHz)

shift = diff(freq_rev); %difference from step to step in revolution frequency
rf_shift = h*shift; %difference from step to step in rf
period = 1./freq_rev; %for each turn
time = cumsum(period); %cumulative time at each step
rate = rf_shift./period(2:end); %Hz per second

plot(time(2:end),rate);