from django.db import models

class Register(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    password = models.CharField(max_length=220)
    is_blocked = models.BooleanField(default=False)

    def __str__(self):
        return self.name
        
class Card(models.Model):

    customer = models.ForeignKey(
        Register,
        on_delete=models.CASCADE
    )

    last_four = models.CharField(max_length=4)

    card_type = models.CharField(
        max_length=10,
        choices=[
            ('CREDIT', 'Credit Card'),
            ('DEBIT', 'Debit Card')
        ],
        default='CREDIT'
    )

    credit_limit = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=50000
    )

    expiry_date = models.DateField()

    failed_pin_attempts = models.PositiveIntegerField(default=0)

    status = models.CharField(
        max_length=10,
        choices=[
            ('ACTIVE', 'Active'),
            ('BLOCKED', 'Blocked'),
            ('EXPIRED', 'Expired')
        ],
        default='ACTIVE'
    )

    def __str__(self):
        return f"****{self.last_four}"


# TRANSACTION MODEL

class Transaction(models.Model):

    card = models.ForeignKey(
        Card,
        on_delete=models.PROTECT
    )

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    merchant = models.CharField(max_length=150)

    location = models.CharField(max_length=150, blank=True)

    status = models.CharField(
        max_length=10,
        choices=[
            ('PENDING', 'Pending'),
            ('APPROVED', 'Approved'),
            ('FLAGGED', 'Flagged'),
            ('DECLINED', 'Declined')
        ],
        default='PENDING'
    )

    risk_score = models.FloatField(default=0)

    txn_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Transaction {self.id}"


# FRAUD ALERT MODEL

class FraudAlert(models.Model):

    transaction = models.OneToOneField(
        Transaction,
        on_delete=models.CASCADE
    )

    rule_hit = models.CharField(max_length=255, blank=True)

    risk_score = models.FloatField(default=0)

    alert_status = models.CharField(
        max_length=10,
        choices=[
            ('NEW', 'New'),
            ('REVIEWED', 'Reviewed'),
            ('RESOLVED', 'Resolved')
        ],
        default='NEW'
    )

    alert_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Fraud Alert {self.id}"


