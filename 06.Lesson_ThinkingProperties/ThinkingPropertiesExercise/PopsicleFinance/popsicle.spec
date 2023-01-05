methods {
    balanceOf(address user) returns (uint) envfree;
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

    uint rewardBefore = accounts(e.msg.sender);

    withdraw(e, amount);

    assert(balanceOf(e.msg.sender) < balanceBefore);
}

// rule immediateWithdrawGivesNoRewards