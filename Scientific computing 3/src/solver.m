n = 500;
mu = linspace(0,0.5,n);
sol1 = zeros(1,n);
sol2 = zeros(1,n);
sol3 = zeros(1,n);
aur = zeros(1,n);
plan = zeros(1,n);
syms x;

for i = 1:n
    eqn1 = x - ((1-mu(i))/(x+mu(i))^2) - mu(i)/(x-(1-mu(i)))^2 == 0;
    eqn2 = x - ((1-mu(i))/(x+mu(i))^2) + mu(i)/(x-(1-mu(i)))^2 == 0;
    eqn3 = x + ((1-mu(i))/(x+mu(i))^2) + mu(i)/(x-(1-mu(i)))^2 == 0;
    sol1(i) = solve(eqn1,x,'Real',true);
    sol2(i) = solve(eqn2,x,'Real',true);
    sol3(i) = solve(eqn3,x,'Real',true);
    aur(i) = -mu(i);
    plan(i) = 1-mu(i);
    i
end

figure
plot(mu,sol1,mu,plan,mu,sol2,mu,aur,mu,sol3,'LineWidth',2)
legend('1-µ<x , L2','Planet','-µ<x<1-µ , L1','Sun','x<-µ , L3')
xlabel('µ')
ylabel('x')

muj = 1./1047;
eqn1 = x - ((1-muj)/(x+muj)^2) - muj/(x-(1-muj))^2 == 0;
eqn2 = x - ((1-muj)/(x+muj)^2) + muj/(x-(1-muj))^2 == 0;
eqn3 = x + ((1-muj)/(x+muj)^2) + muj/(x-(1-muj))^2 == 0;
sol11 = solve(eqn1,x,'Real',true)
sol22 = solve(eqn2,x,'Real',true)
sol33 = solve(eqn3,x,'Real',true)