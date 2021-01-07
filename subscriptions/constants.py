class UserTypes:
    INDIVIDUAL = 'individual'
    BUSINESS = 'business'

    Choices = (
        (INDIVIDUAL, 'individual'),
        (BUSINESS, 'business'),
    )


class BillingType:
    MONTHLY = 'monthly'
    YEARLY = 'yearly'

    Choices = (
        (MONTHLY, 'monthly'),
        (YEARLY, 'yearly'),
    )

class SpecialOffers:
    STUDENT = 'student'
    CLASSROOM_ASSISTANT = 'classroom_assistant'
    OPEN_SOURCE = 'open_source'

    Choices = (
        (STUDENT, 'student'),
        (CLASSROOM_ASSISTANT, 'classroom assistant'),
        (OPEN_SOURCE, 'open source'),

    )