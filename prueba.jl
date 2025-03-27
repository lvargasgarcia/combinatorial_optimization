using Combinatorics
using Random


function compose(pi::Vector{Int}, sigma::Vector{Int})
    n = length(pi)
    result = Vector{Int}(undef, n)
    for i in 1:n
        result[i] = pi[sigma[i]]
    end
    return result
end

function inverse(sigma::Vector{Int})
    n = length(sigma)
    result = Vector{Int}(undef, n)
    for i in 1:n
        result[sigma[i]] = i
    end
    return result
end

function partition_crossover(sigma_1::Vector{Int}, sigma_2::Vector{Int})
    child = sigma_1
    moves = []
    pi = compose(inverse(sigma_1), sigma_2)
    i = 1
    n = length(sigma_1)
    while i <= n
        h = [i for i in 1:n]
        l = i 
        h[l] = pi[l]
        j = h[l]
        while l < j 
            l = l + 1
            h[l] = pi[l]
            j = max(j, h[l])
        end
        append!(moves, h)
        child = compose(child, h)
        i = l + 1
    end
    return child, moves
end



#Test function with random pairs of Sn
function test()
    n = 5000
    maximum = 0

    for i in 1:100000
        sigma1 = randperm(n)
        sigma2 = randperm(n)
        child, moves = partition_crossover(sigma1, sigma2)
        if child != sigma2
            println("Child is not equal to sigma2")
            println("Sigma1", sigma1)
            println("Sigma2", sigma2)
            println("Child", child)
            break
        else
            println("Child is equal to sigma2")
            println(length(moves))
        end

        if length(moves) > maximum
            maximum = length(moves)
        end

        if length(moves) == 10
            partition_crossover(sigma1, sigma2)
        end

    end

    println("Max number of moves: ", maximum)

end

test()