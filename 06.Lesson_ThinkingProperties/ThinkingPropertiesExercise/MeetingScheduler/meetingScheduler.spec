

methods {
    getStateById(uint meetingId) envfree;
    getStartTimeById(uint meetingId) returns (uint) envfree;
    getEndTimeById(uint meetingId) returns (uint) envfree;
    getNumOfParticipents(uint meetingId) returns (uint) envfree;
}

rule meetingCanBeStartedByAnyone() {
    env e;
    uint meetingId = 0;

    scheduleMeeting(e, meetingId, 100, 200);

    env e2;
    require e2.block.timestamp > 100 && e2.block.timestamp < 200;

    uint meetingStatus = getStateById(meetingId);
    bool meetingIsPending = meetingStatus == 1;
    bool isAfterStart = e2.block.timestamp > getStartTimeById(meetingId);
    bool isBeforeEnd = e2.block.timestamp < getEndTimeById(meetingId);
    assert meetingIsPending && isAfterStart && isBeforeEnd;
    startMeeting@withrevert(e2, meetingId);

    assert !lastReverted;
    assert getStateById(meetingId) == 2;
}

rule meetingStartTimeBeforeEndTime() {
    env e;
    uint meetingId = 0;
    uint startTime;
    uint endTime;

    scheduleMeeting(e, meetingId, startTime, endTime);

    assert startTime < endTime;

    assert getStartTimeById(meetingId) == startTime;
    assert getEndTimeById(meetingId) == endTime;
}

rule onlyOwnerCanCancel() {
    env e;
    uint meetingId = 0;
    uint startTime;
    uint endTime;

    scheduleMeeting(e, meetingId, startTime, endTime);

    env e2;

    cancelMeeting(e2, meetingId);

    assert e.msg.sender == e2.msg.sender;
}

rule meetingCanBeJoinedIfStarted() {
    uint meetingId = 0;

    require getStateById(meetingId) == 2;
    uint numParticipants = getNumOfParticipents(meetingId);

    env e;
    joinMeeting@withrevert(e, meetingId);

    assert !lastReverted;
    assert getNumOfParticipents(meetingId) == numParticipants + 1;
}

rule validTransitionToMeetingEnded() {
    env e;
    method f;
    calldataarg args;
    uint meetingId;

    uint stateBefore = getStateById(meetingId);
    require stateBefore != 3;

    f(e, args);

    require getStateById(meetingId) == 3;

    assert stateBefore == 2;
    assert f.selector == endMeeting(uint256).selector;
}