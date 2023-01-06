methods {
    balanceOf(address user) returns (uint) envfree;
    ethBalance(address user) returns (uint) envfree;
}

rule depositIncreasesTokenBalance() {
    env e;
    require(e.msg.value > 0);

    uint balanceBefore = balanceOf(e.msg.sender);

    deposit(e);

    uint balanceAfter = balanceOf(e.msg.sender);

    assert(balanceAfter > balanceBefore);
}

rule withdrawDecreasesBalance() {
    env e;
    uint amount;
    require(amount > 0);

    uint balanceBefore = balanceOf(e.msg.sender);
    require(balanceBefore >= amount);

    withdraw(e, amount);

    assert(balanceOf(e.msg.sender) < balanceBefore);
}

rule tokenBalanceIncreasesOnlyFromDeposit(method f) 
filtered {
    f -> f.selector != transfer(address, uint256).selector  && 
        f.selector != transferFrom(address, address, uint256).selector && !f.isView
}
{
    env e;
    calldataarg args;

    uint balanceBefore = balanceOf(e.msg.sender);

    f(e, args);

    require balanceOf(e.msg.sender) > balanceBefore;

    assert(f.selector == deposit().selector);
}

rule tokenBalanceDecreasesOnlyFromWithdraw(method f) 
filtered {
    f -> f.selector != transfer(address, uint256).selector  && 
        f.selector != transferFrom(address, address, uint256).selector && !f.isView
}
{
    env e;
    calldataarg args;

    uint balanceBefore = balanceOf(e.msg.sender);

    f(e, args);

    require balanceOf(e.msg.sender) < balanceBefore;

    assert(f.selector == withdraw(uint).selector);
}

rule callersETHBalancesIncreasesOnlyFromCollectFees(method f)
filtered {
    f -> !f.isView
}
{
    env e;
    calldataarg args;

    uint balanceBefore = ethBalance(e.msg.sender);

    f(e, args);

    uint balanceAfter = ethBalance(e.msg.sender);

    require(balanceAfter > balanceBefore);

    assert f.selector == collectFees().selector;
}

ghost mathint sumAllFunds {
    // for the constructor - assuming that on the constructor the value of the ghost is 0
	init_state axiom sumAllFunds == 0;
}

hook Sstore accounts[KEY address u].feesCollectedPerShare uint newFeesCollectedPerShare STORAGE {
    sumAllFunds = 1;
}
