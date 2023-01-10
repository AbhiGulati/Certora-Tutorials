(Did not have as much time to work on and organize this one)

# Categories

## Unit tests
- ❌ Unit test for `deposit` - check that rewards and balances are updated
    - ❓ Is there any way to check things about properties of `accounts` without making it public or using a harness? Would this be a good use of a `ghost`?
- ✅ `deposit` increases balance
- ✅ `withdraw` decreases balance
- ✅ If user’s token balance increased, then `deposit` was called
- ✅ If decreased, then `withdraw` was called
- ❌ If someone deposits and then immediately collects fees, they won't earn any fees
    - ❓ How can I test this one (assuming it's worth testing)? Their ETH balance will decrease by gas costs, so I can't check that their balance is unchanged. Checking that it's nonincreasing feels like it would miss the case when the fees earned are smaller than the gas costs.

## Variable transitions
- ❌ If `reward` increased, it was from a call to `deposit` or `withdraw`
    - Need to set up a ghost to access `reward`
- ❌ If caller's ETH balance increased, it was from a call to `collectFees()`
    - ❓ This one is failing. It seems to think that a call to `withdraw` triggers an ETH transfer. See anything wrong with my spec `callersETHBalancesIncreasesOnlyFromCollectFees`?
- Create a ghost for the sum of all assets of users in the system. Confirm that only certain functions can change this amount.

## High level properties
- Someone who never deposited should not be able to collect any fees
- If someone withdraws half their shares and then collects fees later, they will get less fees than if they didn’t withdraw half their shares
- When `OwnerDoItsJobAndEarnsFeesToItsClients` is called, people get more fees out. This is the only way that fees increase.
- After someone collects fees, the second call to collect fees will return nothing
