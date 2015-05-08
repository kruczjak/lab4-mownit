graphics_toolkit('gnuplot')

global counter = 0
global T0 = 0
global maxVal = 1
global energy;

function ret = F(x1, y1, x2, y2)
	ret = sqrt( pow2(y1-y2) + pow2(x1 - x2) );
end

function ret = temp(n)
	global T0;
	ret = T0/n;
end

function dist = calculate_F(arr, n)
	dist = 0.0;
	for i = 1:n-1
		dist += F(arr(i,1), arr(i,2), arr(i+1,1), arr(i+1,2));
	end
	dist += F(arr(n,1), arr(n,2), arr(1,1), arr(1,2));
end

function new = swap(arr, n)
	new = arr;
	a = randi(n,1);
	b = randi(n,1);
	while(a==0)
		a = randi(n,1);
	end
	while(b==a || b == 0)
		b = randi(n,1);
	end
	tmp = new(a, :);
	new(a, :) = new(b, :);
	new(b, :) = tmp;
end

function arr = genFour(arr, n)
	sigma = 300
	mu = 500
	arr = randn(n,2)
	arr = arr + mu
	arr = arr * sigma
end

function arr = genGroups(arr, n)
	dx = n/9;
	dy = n/9;
	bx = 0;
	by = 0;
	for i = 1:n
		%arr(i,0) = normal(i+dx*bx, (i+dx*bx)+2);
		%arr(i,1) = normal(i+dy*by, (i+dy*by)+2);
		if i % 9 == 0 and i!=0
			bx+=1;
		end
		if bx == 3
			bx=0;
			by+=1;
		end
	end

end

function path = annealing(arr, n, T, k)
	global energy;
	%arr = genGroups(arr,n);
	arr = genFour(arr,n);
	val = calculate_F(arr,n);
	path = arr;
	for i = 1:k
		neigh = swap(path, n);
		val2 = calculate_F(neigh, n);
		if val2 < val
			path = neigh;
			val = val2;
		elseif exp((val-val2) / T) > 0.8
			path = neigh;
			val = val2;
		end
		T = temp(i);

		energy(i) = val;
	end
end

n = input("Podaj n:");
T0 = input("Podaj T:");
k = input("Podaj liczbę kroków:");
energy = double(zeros(k,1));
maxVal = input("Podaj max random:");
arr = randi(maxVal,n,2)

solve = annealing(arr, n, T0, k);
solve(n+1, :) = solve(1,:);
energy
figure(1);
plot(solve(:,1), solve(:,2));
figure(2);
plot(1:k, energy);
