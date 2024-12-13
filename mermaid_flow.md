```
stateDiagram-v2
    [*] --> ClaimSubmission: New Claim
    
    state ClaimSubmission {
        [*] --> Pending: Initial Status
    }
    
    state "Initial Status Check" as StatusCheck {
        state "Check Current Status" as check
        [*] --> check
        check --> Excluded: Status is Approved/Denied
        check --> ManualReview: Status is Appeal
        check --> CenturionCheck: Status is Pending
    }
    
    Pending --> StatusCheck
    
    state "Centurion Eligibility Check" as CenturionCheck {
        state "Evaluate Parameters" as eval
        [*] --> eval
        eval --> CenturionProcess: Meets Parameters
        eval --> ManualReview: Outside Parameters
    }
    
    state "Centurion Processing" as CenturionProcess {
        state "Automated Analysis" as analysis
        [*] --> analysis
        analysis --> PreApproved: High Confidence Approve\n(>70% probability)
        analysis --> PreDenied: High Confidence Deny\n(<30% probability)
        analysis --> Flagged: Medium Confidence\n(30-70% probability)
        analysis --> Flagged: Detected Historical\nImage Reuse
    }
    
    state "Manual Review" as ManualReview {
        state "Claims Engineer Analysis" as engineerReview
        [*] --> engineerReview
        engineerReview --> PreApproved: Approved
        engineerReview --> PreDenied: Denied
    }
    
    Flagged --> ManualReview
    
    state "Final Processing" as FinalProcess {
        [*] --> NotifyTeam: Update Status
        NotifyTeam --> GenerateReport: Send Email
        GenerateReport --> [*]: Process Complete
    }
    
    PreApproved --> FinalProcess
    PreDenied --> FinalProcess
    Excluded --> [*]
    
    note right of ClaimSubmission
        All new claims start with
        Pending status
    end note
    
    note right of CenturionCheck
        Checks claim size and
        other parameters against
        predefined thresholds
    end note
    
    note right of CenturionProcess
        Automated analysis includes:
        - Probability scoring
        - Fraud detection
        - Historical image matching
    end note
    
    note right of ManualReview
        Claims Engineers review:
        - Flagged claims
        - Appeals
        - Claims outside
          Centurion parameters
    end note
```