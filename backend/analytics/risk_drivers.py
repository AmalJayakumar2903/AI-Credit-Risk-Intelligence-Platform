MIN_OBSERVATIONS = 30


def top_risk_grade(segmentation):

    eligible = {
        grade: rate
        for grade, rate in
        segmentation["grade_default_rate"].items()
        if segmentation["grade_distribution"].get(
            grade,
            0
        ) >= MIN_OBSERVATIONS
    }

    top_grade = max(
        eligible,
        key=eligible.get
    )

    return {
        "grade": top_grade,
        "default_rate": eligible[top_grade],
        "loan_count":
            segmentation["grade_distribution"][
                top_grade
            ]
    }

def top_risk_purpose(segmentation):

    eligible = {
        purpose: rate
        for purpose, rate in
        segmentation["purpose_default_rate"].items()
        if segmentation["purpose_distribution"].get(
            purpose,
            0
        ) >= MIN_OBSERVATIONS
    }

    top_purpose = max(
        eligible,
        key=eligible.get
    )

    return {
        "purpose": top_purpose,
        "default_rate":
            eligible[top_purpose],

        "loan_count":
            segmentation["purpose_distribution"][
                top_purpose
            ]
    }

def top_risk_state(segmentation):

    eligible = {
        state: rate
        for state, rate in
        segmentation["state_default_rate"].items()
        if segmentation["state_distribution"].get(
            state,
            0
        ) >= MIN_OBSERVATIONS
    }

    top_state = max(
        eligible,
        key=eligible.get
    )

    return {
        "state": top_state,
        "default_rate":
            eligible[top_state],

        "loan_count":
            segmentation["state_distribution"][
                top_state
            ]
    }