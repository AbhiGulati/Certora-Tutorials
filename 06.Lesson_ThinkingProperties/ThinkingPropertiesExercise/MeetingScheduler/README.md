
- ❓ Is there a way to check that a Meeting always starts as UNITIALIZED?
- Unit test that confirms that the start and end times provided when creating a meeting are properly saved onto the meeting
- Check that only the owner can cancel the meeting
    - ❓ In my test for this (`onlyOwnerCanCancel`), I do a `scheduleMeeting` so that I have a handle on the meeting owner, and then check that `cancelMeeting` can only be called by the owner. But I'm limiting myself to cases where they are called back-to-back, so this test is not as generic as I would like. Would it be better to "harness" a getter for the owner, so that I can have the meeting start in a more arbitrary state.
    - ❓ My test for this is failing, can you tell why?
- Meeting can be started by anyone after startTime and beforeEnd time (check this with `lastReverted` etc)
- A meeting can be joined if it is STARTED (can be joined even if we have passed the endTime, so long as no one has ENDed the meeting)
    - ❓ My test for this is failing, can you tell why?
- The owner of a meeting cannot change
    - Don't think I can test this without access to the `organizer`

# Categories

## Valid states
- I generally don't understand this category
- ❓ Is it fair to say that these will usually be proved by `invariant`s rather than `rule`s?
- If a meeting is UNINITIALIZED or PENDING or CANCELLED, its number of participants will be 0


## Variable transitions
- If `numParticipants` changed, it was due to a call to `joinMeeting`
- If `numParticipants` changed, then meeting status did not change. Also vice versa.
- Meeting start and end times can only be changed by `scheduleMeeting`

## State transitions
- ❓ What separates this from variable transitions?
- If meeting state changes to ENDED, it must have previously been STARTED and the call was to `endMeeting`

## High level properties
- Don't see any examples of this

## Risk analysis
- Don't know how to reason about this. There's no funds involved etc.