methods {
    balanceOf(address user) returns (uint) envfree;
    ethBalance(address user) returns (uint) envfree;
}

ghost mathint totalFeesEarnedPerShareGhost {
    init_state axiom totalFeesEarnedPerShareGhost == 0;
}

ghost mathint sumOfAllBalances {
    init_state axiom sumOfAllBalances == 0;
}

ghost mapping(uint => uint) feesCollectedPerShare;

ghost mapping(uint => uint) rewards;

ghost mapping(uint => uint) balances;

ghost mathint sumOfAllAssets {
    init_state axiom sumOfAllAssets == 0;
}
    // function assetsOf(address user) public view returns(uint) {
    //     return accounts[user].Rewards + balances[user] * (totalFeesEarnedPerShare - accounts[user].feesCollectedPerShare);
    // }

hook Sstore accounts[KEY address u].Rewards uint newReward (uint oldReward) STORAGE {
    rewards[u] = newReward;
    sumOfAllAssets = sumOfAllAssets + newReward - oldReward;
}

hook Sstore totalFeesEarnedPerShare uint newTotalFeesEarnedPerShare (uint oldTotalFeesEarnedPerShare) STORAGE {
    totalFeesEarnedPerShareGhost = newTotalFeesEarnedPerShare;
    sumOfAllAssets = sumOfAllAssets + sumOfAllBalances * (newTotalFeesEarnedPerShare - oldTotalFeesEarnedPerShare);
}

hook Sstore accounts[KEY address u].feesCollectedPerShare uint newFeesCollectedPerShare (uint oldFeesCollectedPerShare) STORAGE {
    feesCollectedPerShare[u] = newFeesCollectedPerShare;
    sumOfAllAssets = sumOfAllAssets - balances[u] * (newFeesCollectedPerShare - oldFeesCollectedPerShare);
}

hook Sstore balances[KEY address u] uint newBalance (uint oldBalance) STORAGE {
    sumOfAllAssets = sumOfAllAssets + (newBalance - oldBalance) * (totalFeesEarnedPerShareGhost - feesCollectedPerShare[u]);
    sumOfAllBalances = sumOfAllBalances + newBalance - oldBalance;
    balances[u] = newBalance;
}

// Note: This rule is expected to be bogus, I'm just using it to poke around
rule sumOfAllAssetsDoesntChange(method f)
filtered {
    f -> f.selector != collectFees().selector  && 
        f.selector != withdraw(uint256).selector && 
        f.selector != deposit().selector && 
        f.selector != OwnerDoItsJobAndEarnsFeesToItsClients().selector && 
        !f.isView
}
{
    env e;
    calldataarg args;

    mathint sumOfAllAssetsBefore = sumOfAllAssets;

    f(e, args);

    mathint sumOfAllAssetsAfter = sumOfAllAssets;

    assert sumOfAllAssetsBefore == sumOfAllAssetsAfter;
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


rule rewardIncreasesOnlyDepositOrWithdraw(method f)
filtered {
    f -> !f.isView
}
{
    env e;
    calldataarg args;
    address u;

    uint rewardBefore = rewards[u];

    f(e, args);

    uint rewardAfter = rewards[u];

    require(rewardAfter > rewardBefore);

    assert f.selector == deposit().selector || f.selector == withdraw(uint256).selector;
}



rule consecutiveCollectFeesDoesNothing() {
    env e;
    address u;

    uint ethBalanceBefore = ethBalance(u);

    collectFees(e);

    uint ethBalanceAfter1 = ethBalance(u);

    assert ethBalanceAfter1 != ethBalanceBefore => u == e.msg.sender;

    collectFees(e);

    uint ethBalanceAfter2 = ethBalance(u);

    assert ethBalanceAfter1 == ethBalanceAfter2;
}