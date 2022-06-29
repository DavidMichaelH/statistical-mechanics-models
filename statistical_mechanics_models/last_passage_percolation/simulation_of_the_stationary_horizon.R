###############################################
# This function is the ququeing mapping D 
# from the paper "Global structure of 
# competition interfaces and semi-infinite geodesics in 
# Brownian last-passage percolation"
# Z1 and Z2 are vectors of BMS with drift
# drift of Z2 must be bigger than drift of Z1
# N_points is the length of the vectors
###############################################
D_queue <- function(Z2,Z1)
{
  N_points <- length(Z1)
  
  max_from_zero <- max(Z1 - Z2)
  
  max_from_t <- rep(NA,N_points)
  
  max_from_t[1] <- max_from_zero
  
  # getting a function for the max after time t
  for(i in 2:N_points)
  {
    if(Z1[i - 1] - Z2[i - 1] == max_from_t[i - 1])
    {
      max_from_t[i] <- max(Z1[i:N_points] - Z2[i:N_points])
    }
    else
    {
      max_from_t[i] <- max_from_t[i - 1]
    }
  }
  
  return(Z1 + max_from_zero - max_from_t)
  
}


#################################################################
# This is the mapping D^n that maps n functions to a single one. It works recursively
# Z is a matrix. The number of rows is the number of inputs to the function
# the columns are the disctretized versions of the input functions
#################################################################
general_D_queue <- function(Z)
{
  N_functions <- nrow(Z)
  
  # set the base for the recursion
  if(N_functions == 1)
  {
    return(as.vector(Z))
  }
  
  my_matrix <- matrix(Z[2:N_functions,],nrow = N_functions - 1,ncol = ncol(Z))
  
  return(D_queue(general_D_queue(my_matrix),Z[1,]))
}






###########################################################
# now simulating the stationary horizon (SH). 
# The default is the parameterization from the paper 
# "The stationary horizon and semi-infinite geodesics in the directed landscape"
# where each BM has diffusivity \sqrt 2 and drift 2\xi. The parameters can be changed
#######################################################
xi_vector <- c(-10,-5,-3,-2,-1,0,1,2,3,5,10)

N_functions <- length(xi_vector)

# parameters for the SH
diffusivity <- sqrt(2)

drift_factor <- 2

# end is where we will stop simulating. 
# We will want to make this big enough so that the max is unlikeley to occur after that time
end <- 2
step_size <- 0.0001

vertical_step_size <- sqrt(step_size)

N_points <- end/step_size

## each row will be a discretized, independent Brownian motion with appropriate drift
BM_drifts <- matrix(0,nrow = N_functions,ncol = N_points)

## each row will be the discretized Busemann function
Buse_functions <- matrix(0,nrow = N_functions,ncol = N_points)

# simulate the independent Brownian motions
for(i in 1:N_functions)
{
  for(j in 2:N_points)
  {
    BM_drifts[i,j] <- BM_drifts[i,j - 1] + diffusivity*rnorm(1,drift_factor/diffusivity*xi_vector[i]*step_size,vertical_step_size)
  }
}

# Now, we send these through the queueing mappings
# the output is a N_functions-dimensional vector of the stationary horizon with the specified drifts  
for(i in 1:N_functions)
{
  modified_matrix <- matrix(BM_drifts[1:i,],nrow = i,ncol = N_points)
  output_vector <- general_D_queue(modified_matrix)
  ## We center in the middle, then reverse time and make everything negative.
  Buse_functions[i,] <- -rev(output_vector - output_vector[N_points/2])
  
}


# we use a division factor to truncate the range we are looking at. 
# We are trying to simulate the sup of a BM with drift in an infinite time interval
# our simulation is therefore less valid near the boundary of the range we use. 
division_factor <- 4
x_vals <- seq(-end/division_factor,end/division_factor,length.out = N_points/division_factor*2 + 1)

# plot the functions on the same graph. Modify this for a different number of functions simulated 
plot(x_vals,Buse_functions[11,(N_points/division_factor):(3*N_points/division_factor)],type = "l",col = "brown",xlab = "x",ylab = expression(G[{xi}])) 
lines(x_vals,Buse_functions[1,(N_points/division_factor):(3*N_points/division_factor)],type = "l",col = "black")
lines(x_vals,Buse_functions[10,(N_points/division_factor):(3*N_points/division_factor) ],type = "l",col = "mediumblue")
lines(x_vals,Buse_functions[2,(N_points/division_factor):(3*N_points/division_factor)],type = "l",col = "turquoise")
lines(x_vals,Buse_functions[9,(N_points/division_factor):(3*N_points/division_factor) ],type = "l",col = "orange")
lines(x_vals,Buse_functions[3,(N_points/division_factor):(3*N_points/division_factor) ],type = "l",col = "deeppink")
lines(x_vals,Buse_functions[8,(N_points/division_factor):(3*N_points/division_factor) ],type = "l",col = "gold4")
lines(x_vals,Buse_functions[4,(N_points/division_factor):(3*N_points/division_factor)],type = "l",col = "green")
lines(x_vals,Buse_functions[7,(N_points/division_factor):(3*N_points/division_factor)],type = "l",col = "red")
lines(x_vals,Buse_functions[5,(N_points/division_factor):(3*N_points/division_factor) ],type = "l",col = "violet")
lines(x_vals,Buse_functions[6,(N_points/division_factor):(3*N_points/division_factor)],type = "l",col = "blue")

title(main = expression(paste("The stationary horizon ", G[xi](x), " for various parameters ",xi)))
