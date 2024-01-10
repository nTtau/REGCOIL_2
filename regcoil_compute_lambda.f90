subroutine regcoil_compute_lambda()

  use regcoil_variables, only: nlambda, lambda_min, lambda_max, lambda, general_option, verbose
  use stel_kinds

  implicit none

  integer :: j

  if (allocated(lambda)) deallocate(lambda)
  allocate(lambda(nlambda))
  
  lambda(1) = 0
  do j = 1,nlambda-1
     lambda(j+1) = lambda_min * exp((log(lambda_max/lambda_min)*(j-1))/(nlambda-2))
  end do

  if (general_option==1 .and. verbose) then
     print *,"We will use the following values of the regularization weight lambda:"
     print "(*(es10.3))",lambda
  end if

end subroutine regcoil_compute_lambda
