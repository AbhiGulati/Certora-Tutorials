(Did not have as much time to work on and organize this one)

# Categories

## Unit tests
- ❌ Unit test for `deposit` - check that rewards and balances are updated
    - ❓ Is there any way to check things about properties of `accounts` without making it public or using a harness? Would this be a good use of a `ghost`?
- ✅ `deposit` increases balance
- ✅ `withdraw` decreases balance
- ✅ If user’s token balance increased, then `deposit` was called
- ✅ If decreased, then `withdraw` was called
- ✅ If someone deposits and then immediately collects fees, they won't earn any fees
    - I had to add some helpers to expose things in order to `require` that the Rewards start out 0.

## Variable transitions
- ✅ If `reward` increased, it was from a call to `deposit` or `withdraw`
    - Need to set up a ghost to access `reward`
- ✅ If caller's ETH balance increased, it was from a call to `collectFees()` or `withdraw()`
- ✅ Create a ghost for the sum of all assets of users in the system. Confirm that only certain functions can change this amount.
    - ❓I had to write a lot of ghosts for this one. The rule is `sumOfAllAssetsDoesntChange`, and it failed for `transfer` and `transferFrom` which I believe is expected because there's a bug in the Popsicle code. Would love a sanity check of my approach.

## High level properties
- ❌ Someone who never deposited should not be able to collect any fees
    - ❓There is not a way to check something like "never deposited", right? And if I tried to use an invariant, I wouldn't be able to check something like "cannot collect fees" since the body of an invariant shouldn't involve state changes.
- If someone withdraws half their shares and then collects fees later, they will get less fees than if they didn’t withdraw half their shares
- When `OwnerDoItsJobAndEarnsFeesToItsClients` is called, people get more fees out. This is the only way that fees increase.
- ❌ After someone collects fees, the second call to collect fees will return nothing
    - ❓This rule (`consecutiveCollectFeesDoesNothing`) is failing. I believe it's because the `.call(..)` is resulting in a HAVOC to the balance of a user who was not involved in the transaction. How do I tell the prover to treat this as a simple ETH transfer? Or is it a bad idea to do that?
