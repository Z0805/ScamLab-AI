import re

from ml_model import predict_scam


SCAM_PATTERNS = {

    "Prize / Lottery Scam": [
        "you won",
        "you have won",
        "congratulations",
        "winner",
        "lucky winner",
        "lottery",
        "jackpot",
        "prize",
        "cash prize",
        "grand prize",
        "reward",
        "free gift",
        "free iphone",
        "free phone",
        "free mobile",
        "claim your prize",
        "claim your reward",
        "claim your gift",
        "claim now",
        "giveaway",
        "selected as winner",
        "selected for a reward",
    ],

    "Bank / KYC Scam": [
        "bank account",
        "account blocked",
        "account suspended",
        "account will be blocked",
        "account will be closed",
        "kyc",
        "kyc update",
        "kyc expired",
        "complete kyc",
        "verify your account",
        "verify bank account",
        "bank verification",
        "update your bank details",
        "bank details",
        "net banking",
        "internet banking",
    ],

    "OTP / Credential Scam": [
        "otp",
        "one time password",
        "verification code",
        "security code",
        "login code",
        "password",
        "passcode",
        "pin",
        "cvv",
        "card number",
        "credit card",
        "debit card",
        "aadhaar",
        "aadhar",
        "pan card",
        "pan number",
        "account number",
        "username",
        "login details",
        "verify identity",
    ],

    "UPI / Payment Scam": [
        "upi id",
        "make payment",
        "send money",
        "transfer money",
        "pay now",
        "pay immediately",
        "payment pending",
        "payment failed",
        "refund",
        "refund pending",
        "receive payment",
        "collect request",
        "payment link",
        "transaction failed",
        "transaction pending",
    ],

    "Delivery / Courier Scam": [
        "package",
        "parcel",
        "delivery",
        "courier",
        "shipment",
        "delivery failed",
        "delivery attempt failed",
        "delivery address",
        "update delivery address",
        "customs fee",
        "delivery fee",
        "shipping fee",
        "package held",
        "parcel held",
        "package will be returned",
        "parcel will be returned",
    ],

    "Job / Employment Scam": [
        "work from home",
        "work-from-home",
        "part time job",
        "part-time job",
        "easy money",
        "earn money",
        "earn daily",
        "earn per day",
        "make money",
        "job opportunity",
        "job offer",
        "vacancy",
        "hiring",
        "selected for the job",
        "registration fee",
        "training fee",
        "joining fee",
        "processing fee",
        "job deposit",
    ],

    "Investment Scam": [
        "investment",
        "invest now",
        "guaranteed returns",
        "guaranteed profit",
        "guaranteed income",
        "double your money",
        "triple your money",
        "high returns",
        "high profit",
        "quick profit",
        "quick returns",
        "risk free investment",
        "zero risk",
        "crypto",
        "cryptocurrency",
        "bitcoin",
        "trading opportunity",
        "stock tips",
        "forex",
    ],

    "Loan Scam": [
        "instant loan",
        "instant personal loan",
        "pre approved loan",
        "pre-approved loan",
        "loan approved",
        "loan offer",
        "easy loan",
        "quick loan",
        "low interest loan",
        "loan application",
        "loan processing fee",
        "loan approval fee",
        "loan verification fee",
    ],

    "SIM / Mobile Scam": [
        "sim blocked",
        "sim card blocked",
        "mobile number blocked",
        "number will be blocked",
        "sim will be deactivated",
        "mobile will be disconnected",
        "recharge required",
        "sim verification",
        "sim kyc",
        "update sim details",
    ],

    "Government / Authority Impersonation": [
        "government",
        "income tax",
        "tax department",
        "police department",
        "cyber crime",
        "cybercrime",
        "court notice",
        "legal notice",
        "government notice",
        "official notice",
        "case registered",
        "fir",
        "fine",
        "penalty",
        "arrest warrant",
        "warrant",
    ],

    "Tech Support Scam": [
        "virus detected",
        "your computer is infected",
        "your device is infected",
        "security alert",
        "security warning",
        "technical support",
        "tech support",
        "call support",
        "contact support",
        "remote access",
        "remote desktop",
        "computer problem",
        "device problem",
    ],

    "Scholarship / Education Scam": [
        "scholarship",
        "scholarship approved",
        "scholarship amount",
        "student reward",
        "education grant",
        "education fund",
        "admission offer",
        "college admission",
        "registration fee",
        "application fee",
    ],

    "Travel / Visa Scam": [
        "visa approved",
        "visa offer",
        "visa processing",
        "visa fee",
        "passport",
        "flight ticket",
        "travel offer",
        "holiday package",
        "free trip",
        "hotel booking",
        "travel reward",
    ],

    "Social / Romance Scam": [
        "send me money",
        "help me financially",
        "emergency money",
        "i need money",
        "send a gift card",
        "gift card",
        "online relationship",
        "investment opportunity",
    ],
}


URGENCY_PATTERNS = [
    "urgent",
    "urgently",
    "immediately",
    "act now",
    "act immediately",
    "do it now",
    "respond now",
    "reply now",
    "within 24 hours",
    "within 48 hours",
    "today only",
    "expires today",
    "last chance",
    "limited time",
    "hurry",
    "final warning",
    "final notice",
    "important notice",
    "action required",
    "immediate action required",
]


THREAT_PATTERNS = [
    "account will be blocked",
    "account will be closed",
    "account suspended",
    "legal action",
    "police action",
    "police case",
    "arrest",
    "arrest warrant",
    "court case",
    "court notice",
    "fine",
    "penalty",
    "you will be arrested",
    "your number will be blocked",
    "your sim will be blocked",
    "your service will be disconnected",
]


LINK_PATTERNS = [
    "click here",
    "click this link",
    "click the link",
    "follow this link",
    "open this link",
    "tap this link",
    "visit this link",
    "link below",
    "click below",
    "verify here",
    "login here",
    "download here",
]


def detect_legitimate_transaction(text_lower):
    """
    Detect common legitimate bank transaction alerts.

    A legitimate transaction normally contains:
    - debited/credited language
    - a transaction amount
    - and a transaction reference, masked account,
      merchant or UPI reference

    This helps prevent ordinary bank alerts from being
    incorrectly classified as scams.
    """

    debit_credit = any(
        phrase in text_lower
        for phrase in [
            "debited",
            "credited",
            "has been debited",
            "has been credited",
        ]
    )

    amount_pattern = re.search(
        r"(rs\.?|inr|₹)\s?\d+(?:,\d{3})*(?:\.\d{1,2})?",
        text_lower
    )

    transaction_reference = any(
        phrase in text_lower
        for phrase in [
            "upi:",
            "txn",
            "transaction id",
            "reference number",
            "ref no",
            "utr",
        ]
    )

    masked_account = bool(
        re.search(r"\bxx+\d{2,6}\b", text_lower)
    )

    merchant_context = any(
        phrase in text_lower
        for phrase in [
            "merchant",
            "purchase",
            "transaction",
            "upi:",
            "credited",
        ]
    )

    return (
        debit_credit
        and amount_pattern is not None
        and (
            transaction_reference
            or masked_account
            or merchant_context
        )
    )


def analyze_message(text):

    text_lower = text.lower()

    score = 0
    indicators = []
    detected_categories = []

    # -----------------------------------------
    # LEGITIMATE TRANSACTION DETECTION
    # -----------------------------------------

    legitimate_transaction = detect_legitimate_transaction(
        text_lower
    )

    # -----------------------------------------
    # RULE-BASED SCAM DETECTION
    # -----------------------------------------

    for category, patterns in SCAM_PATTERNS.items():

        matches = [
            pattern
            for pattern in patterns
            if pattern in text_lower
        ]

        # Generic transaction-related words should not
        # create a scam score for a verified-looking
        # debit/credit bank notification.
        if (
            legitimate_transaction
            and category == "UPI / Payment Scam"
        ):
            matches = [
                pattern
                for pattern in matches
                if pattern not in [
                    "payment",
                    "upi",
                    "transaction",
                ]
            ]

        if matches:

            detected_categories.append(category)

            if len(matches) == 1:
                score += 20

            elif len(matches) == 2:
                score += 30

            else:
                score += 40

            indicators.append(
                f"{category}: suspicious language detected"
            )

    # -----------------------------------------
    # URGENCY DETECTION
    # -----------------------------------------

    urgency_matches = [
        pattern
        for pattern in URGENCY_PATTERNS
        if pattern in text_lower
    ]

    if urgency_matches:

        score += 20

        indicators.append(
            "Uses urgency or pressure to force quick action"
        )

    # -----------------------------------------
    # THREAT DETECTION
    # -----------------------------------------

    threat_matches = [
        pattern
        for pattern in THREAT_PATTERNS
        if pattern in text_lower
    ]

    if threat_matches:

        score += 25

        indicators.append(
            "Uses threats, fear, or consequences to pressure the user"
        )

    # -----------------------------------------
    # LINK DETECTION
    # -----------------------------------------

    actual_urls = re.findall(
        r"(https?://\S+|www\.\S+)",
        text_lower
    )

    link_language = any(
        phrase in text_lower
        for phrase in LINK_PATTERNS
    )

    if actual_urls or link_language:

        score += 30

        indicators.append(
            "Contains or encourages the user to follow a link"
        )

    # -----------------------------------------
    # SENSITIVE INFORMATION DETECTION
    # -----------------------------------------

    sensitive_terms = [
        "otp",
        "password",
        "pin",
        "cvv",
        "verification code",
        "security code",
        "card number",
        "account number",
        "aadhaar",
        "aadhar",
        "pan number",
        "bank details",
        "login details",
    ]

    sensitive_found = [
        term
        for term in sensitive_terms
        if term in text_lower
    ]

    if sensitive_found:

        score += 30

        indicators.append(
            "Requests sensitive personal, banking, or login information"
        )

    # -----------------------------------------
    # MONEY REQUEST DETECTION
    # -----------------------------------------

    money_terms = [
        "send money",
        "transfer money",
        "pay now",
        "payment",
        "fee",
        "deposit",
        "processing fee",
        "registration fee",
        "verification fee",
    ]

    money_found = [
        term
        for term in money_terms
        if term in text_lower
    ]

    # A legitimate transaction notification can mention
    # payment-related terminology without requesting money.
    if legitimate_transaction:

        money_found = [
            term
            for term in money_found
            if term not in [
                "payment",
            ]
        ]

    if money_found:

        score += 25

        indicators.append(
            "Requests money, payment, transfer, or a fee"
        )

    # -----------------------------------------
    # UNKNOWN SENDER DETECTION
    # -----------------------------------------

    unknown_sender_terms = [
        "unknown number",
        "unknown sender",
        "unknown contact",
        "private number",
        "unsaved number",
    ]

    if any(
        term in text_lower
        for term in unknown_sender_terms
    ):

        score += 15

        indicators.append(
            "Appears to originate from an unknown or unverified sender"
        )

    # -----------------------------------------
    # REWARD + LINK DETECTION
    # -----------------------------------------

    reward_terms = [
        "free",
        "prize",
        "reward",
        "winner",
        "cashback",
        "gift",
        "lottery",
        "bonus",
    ]

    reward_found = any(
        term in text_lower
        for term in reward_terms
    )

    if reward_found and (
        actual_urls or link_language
    ):

        score += 20

        indicators.append(
            "Combines a reward/free offer with a link"
        )

    # -----------------------------------------
    # EXCESSIVE EXCLAMATION DETECTION
    # -----------------------------------------

    if text.count("!") >= 3:

        score += 5

        indicators.append(
            "Uses excessive exclamation or attention-grabbing language"
        )

    # -----------------------------------------
    # LEGITIMATE TRANSACTION SAFETY ADJUSTMENT
    # -----------------------------------------

    if legitimate_transaction:

        # Remove residual generic transaction risk.
        score = max(0, score - 20)

        # If there are no strong scam indicators,
        # keep the transaction alert at zero.
        strong_scam_indicators = (
            urgency_matches
            or threat_matches
            or actual_urls
            or link_language
            or sensitive_found
            or money_found
            or unknown_sender_terms
        )

        if not strong_scam_indicators:
            score = 0

    # -----------------------------------------
    # LIMIT RULE SCORE
    # -----------------------------------------

    score = min(score, 100)

    # -----------------------------------------
    # ML MODEL PREDICTION
    # -----------------------------------------

    ml_result = predict_scam(text)

    ml_prediction = ml_result["label"]
    ml_probability = ml_result["scam_probability"]

    # -----------------------------------------
    # RISK LEVEL
    # -----------------------------------------

    if score >= 70:

        risk_level = "HIGH RISK"

    elif score >= 40:

        risk_level = "SUSPICIOUS"

    elif score >= 20:

        risk_level = "POTENTIALLY SUSPICIOUS"

    else:

        risk_level = "LOW RISK"

    # -----------------------------------------
    # CATEGORY
    # -----------------------------------------

    if legitimate_transaction and score < 40:

        category = "Legitimate Transaction Alert"

    elif detected_categories:

        category = detected_categories[0]

    elif actual_urls or link_language:

        category = "Suspicious Link"

    elif sensitive_found:

        category = "Credential Theft"

    elif money_found:

        category = "Financial Scam"

    elif ml_prediction == "SCAM":

        category = "ML-Detected Scam"

    else:

        category = "General Message"

    # -----------------------------------------
    # RECOMMENDATION
    # -----------------------------------------

    if legitimate_transaction and score < 40:

        recommendation = (
            "This appears to be a normal transaction notification. "
            "No major scam indicators were detected. "
            "For disputes or unexpected transactions, contact your "
            "bank through its official channels."
        )

    elif score >= 70:

        recommendation = (
            "Do not click links, download files, share OTPs, "
            "passwords or banking information, or send money. "
            "Verify the sender through an official website or "
            "trusted contact."
        )

    elif score >= 40:

        recommendation = (
            "Treat this message with caution. Do not provide "
            "personal information or make payments until the "
            "sender and request have been independently verified."
        )

    elif score >= 20:

        recommendation = (
            "Some suspicious characteristics were detected. "
            "Verify the message before taking any action."
        )

    else:

        recommendation = (
            "No major scam indicators were detected. However, "
            "unexpected messages should still be verified."
        )

    # -----------------------------------------
    # FINAL RESULT
    # -----------------------------------------

    return {
        "score": score,
        "risk_level": risk_level,
        "category": category,
        "indicators": indicators,
        "recommendation": recommendation,
        "ml_prediction": ml_prediction,
        "ml_probability": ml_probability,
    }