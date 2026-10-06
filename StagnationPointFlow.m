function StagnationPointFlow()
% Hiemenz stagnation-point boundary layer
% f''' + f*f'' - (f')^2 + 1 = 0
% f(0)=0, f'(0)=0, f'(infinity)=1
% Numerical method: Bisection shooting + classical RK4

eta_max = 6.0;
N = 1000;
h = eta_max/N;
eta = 0:h:eta_max;

tol = 1e-6;
s_low = 0.0;
s_high = 2.0;
max_iter = 100;

history = zeros(max_iter,3);

for iter = 1:max_iter
    s_guess = (s_low + s_high)/2;
    f_prime_inf = shoot(s_guess,h,N);
    history(iter,:) = [iter,s_guess,f_prime_inf];

    fprintf('Iteration %2d: f''''(0)=%.10f, f''''(6)=%.10f\n', ...
        iter,s_guess,f_prime_inf);

    if abs(f_prime_inf - 1.0) < tol
        break;
    end

    if f_prime_inf < 1.0
        s_low = s_guess;
    else
        s_high = s_guess;
    end
end

s_correct = s_guess;

Y = zeros(3,N+1);
Y(:,1) = [0;0;s_correct];

for i = 1:N
    Y(:,i+1) = rk4_step(Y(:,i),h);
end

fprintf('\nConvergence achieved.\n');
fprintf('f''''(0) = %.10f\n',s_correct);
fprintf('f''''(6) = %.10f\n',Y(2,end));

figure('Color','w');
plot(eta,Y(1,:),'LineWidth',2); hold on;
plot(eta,Y(2,:),'LineWidth',2);
plot(eta,Y(3,:),'--','LineWidth',2);
grid on;
xlabel('\\eta'); ylabel('Function values');
title('Stagnation-Point Flow: Complete Profiles');
legend('f(\\eta)','f''(\\eta)','f''''(\\eta)','Location','NorthWest');

figure('Color','w');
plot(Y(2,:),eta,'LineWidth',2);
grid on;
xlabel('f''(\\eta)'); ylabel('\\eta');
title('Velocity Profile');

figure('Color','w');
plot(history(1:iter,1),history(1:iter,2),'o-','LineWidth',1.5);
yline(s_correct,'--');
grid on;
xlabel('Bisection iteration'); ylabel('Trial f''''(0)');
title('Bisection Shooting Convergence');

figure('Color','w');
semilogy(history(1:iter,1),abs(history(1:iter,3)-1),'o-','LineWidth',1.5);
yline(tol,'--');
grid on;
xlabel('Bisection iteration');
ylabel('|f''(\\eta_{max})-1|');
title('Residual Convergence');
end

function Y_next = rk4_step(Y,h)
k1 = system_deriv(Y);
k2 = system_deriv(Y + 0.5*h*k1);
k3 = system_deriv(Y + 0.5*h*k2);
k4 = system_deriv(Y + h*k3);
Y_next = Y + h*(k1 + 2*k2 + 2*k3 + k4)/6;
end

function dY = system_deriv(Y)
f = Y(1); fp = Y(2); fpp = Y(3);
dY = [fp; fpp; -f*fpp + fp^2 - 1];
end

function f_prime_inf = shoot(s,h,N)
Y = [0;0;s];
for i = 1:N
    Y = rk4_step(Y,h);
    if any(~isfinite(Y))
        f_prime_inf = 999;
        return;
    end
end
f_prime_inf = Y(2);
end
